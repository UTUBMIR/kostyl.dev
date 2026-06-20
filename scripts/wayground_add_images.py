#!/usr/bin/env python3
"""
wayground_add_images.py — Додає зображення до варіантів відповідей у тесті Wayground.

Флоу:
  1. Логін через email/пароль -> отримання _sid cookie
  2. GET quiz -> витягуємо version_id та повну структуру питань
  3. Читаємо JSON-маппінг: яке питання, який варіант, який файл зображення
  4. Завантажуємо кожне зображення на AWS S3 через Wayground media API
  5. PATCH quiz question -> замінюємо варіант відповіді на image-варіант

Використання:
  python3 wayground_add_images.py --quiz-id <QUIZ_ID> --mapping <mapping.json>
  python3 wayground_add_images.py --quiz-id <QUIZ_ID> --mapping <mapping.json> --dry-run

Credentials:
  Зберігати у .env поряд зі скриптом або передавати через змінні середовища:
    WAYGROUND_EMAIL=...
    WAYGROUND_PASSWORD=...

Формат mapping.json:
  [
    {
      "question_index": 0,          // індекс питання в тесті (0-based)
      "option_index": 1,             // індекс варіанта відповіді (0-based)
      "image_path": "images/q1_opt2.png"  // шлях до файлу відносно mapping.json
    },
    ...
  ]
"""

import os
import sys
import json
import uuid
import struct
import argparse
import requests
from pathlib import Path


# ---------------------------------------------------------------------------
# Авторизація
# ---------------------------------------------------------------------------

def login(email: str, password: str) -> requests.Session:
    """
    Логінимось на Wayground, повертаємо авторизований Session з _sid cookie.
    """
    print(f"[~] Авторизація як {email}...")

    resp = requests.post(
        "https://wayground.com/_authserver/public/public/v1/auth/login/local",
        json={
            "username": email,
            "password": password,
            "requestId": str(uuid.uuid4()),
        },
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Origin": "https://wayground.com",
            "Referer": "https://wayground.com/login",
        },
        timeout=30,
    )

    if resp.status_code != 200:
        raise RuntimeError(f"Помилка авторизації. HTTP {resp.status_code}: {resp.text[:300]}")

    body = resp.json()
    if not body.get("success"):
        raise RuntimeError(f"Авторизація не вдалась: {body}")

    sid = resp.cookies.get("_sid")
    quizizz_uid = resp.cookies.get("quizizz_uid")

    if not sid:
        raise RuntimeError("_sid cookie не знайдено у відповіді login!")

    session = requests.Session()
    session.cookies.set("_sid", sid, domain="wayground.com")
    if quizizz_uid:
        session.cookies.set("quizizz_uid", quizizz_uid, domain="wayground.com")
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Origin": "https://wayground.com",
        "Content-Type": "application/json",
    })

    user = body.get("data", {}).get("user", {})
    name = f"{user.get('firstName', '')} {user.get('lastName', '')}".strip()
    print(f"[✓] Авторизовано: {name} (id={user.get('id')})")

    return session


# ---------------------------------------------------------------------------
# Отримання даних тесту
# ---------------------------------------------------------------------------

def get_quiz(session: requests.Session, quiz_id: str) -> tuple[str, list[dict]]:
    """
    Повертає (version_id, questions) з draft-версії тесту.
    """
    print(f"[~] Завантажуємо тест {quiz_id}...")

    url = f"https://wayground.com/_quizserver/main/v2/quiz/{quiz_id}"
    resp = session.get(url, headers={"Referer": f"https://wayground.com/admin/quiz/{quiz_id}/edit"}, timeout=30)

    if resp.status_code != 200:
        raise RuntimeError(f"Не вдалось отримати тест. HTTP {resp.status_code}: {resp.text[:300]}")

    body = resp.json()
    if not body.get("success"):
        raise RuntimeError(f"API повернув помилку: {body}")

    data = body["data"]
    quiz = data["quiz"]

    # Після публікації draft може бути None — беремо published version
    version_source = data.get("draft") or None
    if version_source is None:
        published_id: str = quiz.get("publishedVersion") or quiz.get("draftVersion")
        if not published_id:
            raise RuntimeError("Тест не має ні draft, ні published версії")
        version_id = published_id
    else:
        version_id = version_source["_id"]

    # Завантажуємо питання через окремий endpoint (працює для обох версій)
    q_url = (
        f"https://wayground.com/_quizserver/main/v3/quiz/"
        f"{quiz_id}/version/{version_id}/questions"
    )
    q_resp = session.get(q_url, headers={"Referer": f"https://wayground.com/admin/quiz/{quiz_id}/edit"}, timeout=30)
    if q_resp.status_code != 200 or not q_resp.json().get("success"):
        raise RuntimeError(f"Не вдалось завантажити питання. HTTP {q_resp.status_code}: {q_resp.text[:200]}")
    questions: list[dict] = q_resp.json()["data"]["questions"]

    print(f"[✓] Тест завантажено. version_id={version_id}, питань={len(questions)}")
    return version_id, questions


# ---------------------------------------------------------------------------
# Завантаження зображення на AWS S3 через Wayground media API
# ---------------------------------------------------------------------------

def get_image_dimensions(data: bytes) -> tuple[int, int]:
    """
    Визначає ширину та висоту зображення з бінарних даних (PNG / JPEG).
    Без зовнішніх залежностей.
    """
    # PNG: 8-байтова сигнатура, потім IHDR chunk з розмірами на байтах 16-24
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", data[16:24])
        return w, h
    # JPEG: шукаємо SOF-маркер (0xFF 0xC0/C1/C2)
    if data[:2] == b"\xff\xd8":
        i = 2
        while i + 4 < len(data):
            if data[i] != 0xFF:
                break
            marker = data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2):
                h, w = struct.unpack(">HH", data[i + 5 : i + 9])
                return w, h
            seg_len = struct.unpack(">H", data[i + 2 : i + 4])[0]
            i += 2 + seg_len
    # fallback для інших форматів
    return 800, 600


def upload_image(session: requests.Session, image_path: Path) -> str:
    """
    Завантажує локальний файл на сервери Wayground/S3.
    Повертає finalUrl для вставки в структуру питання.
    """
    if not image_path.exists():
        raise FileNotFoundError(f"Файл не знайдено: {image_path}")

    print(f"  [~] Завантажуємо {image_path.name}...")
    image_data = image_path.read_bytes()
    width, height = get_image_dimensions(image_data)
    print(f"       розміри: {width}×{height}px")

    # 1. Отримуємо pre-signed S3 URL
    init_resp = session.post(
        "https://media.quizizz.com/_mdserver/main/getUploadURL"
        "?destination=quizzes&enableAcceleration=true",
        timeout=30,
    )
    if init_resp.status_code != 200 or not init_resp.json().get("success"):
        raise RuntimeError(f"Не вдалось отримати upload URL: {init_resp.text[:300]}")

    res = init_resp.json()["data"]
    signed_url: str = res["signedUrl"]
    final_url: str = res["finalUrl"]

    # 2. PUT бінарні дані на S3.
    # S3 pre-signed URL підписаний з Content-Type: application/x-www-form-urlencoded —
    # саме цей тип вказано в підписі, тому будь-який інший дасть 403 SignatureDoesNotMatch.
    s3_resp = requests.put(
        signed_url,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=image_data,
        timeout=60,
    )
    if s3_resp.status_code != 200:
        raise RuntimeError(f"Помилка S3 upload. HTTP {s3_resp.status_code}: {s3_resp.text[:200]}")

    print(f"  [✓] Завантажено: {final_url}")
    return final_url, width, height


# ---------------------------------------------------------------------------
# Вивід списку питань
# ---------------------------------------------------------------------------

def list_questions(questions: list[dict]) -> None:
    """
    Виводить нумерований список питань з варіантами відповідей.
    Допомагає скласти mapping.json.
    """
    import re
    # Видаляємо HTML-теги для читабельного виводу
    def strip_html(text: str) -> str:
        return re.sub(r"<[^>]+>", "", text or "").strip()

    print(f"\nВсього питань: {len(questions)}\n")
    print("=" * 60)

    for q_idx, q in enumerate(questions):
        struct = q.get("structure", {})
        query_text = strip_html(struct.get("query", {}).get("text", ""))
        q_type = struct.get("kind", q.get("type", "?"))
        correct_answer = struct.get("answer")  # int (1-based) для MCQ

        # Скорочуємо довгий текст
        if len(query_text) > 80:
            query_text = query_text[:77] + "..."

        print(f"[{q_idx}] ({q_type}) {query_text}")

        options = struct.get("options", [])
        for opt_idx, opt in enumerate(options):
            opt_text = strip_html(opt.get("text", ""))
            opt_type = opt.get("type", "text")
            is_image = opt_type == "image"
            is_correct = (correct_answer == opt_idx + 1)

            marker = "✓" if is_correct else " "
            img_tag = " [IMAGE]" if is_image else ""
            opt_label = f"  [{marker}] opt {opt_idx}: {opt_text[:60]}{img_tag}"
            print(opt_label)

        print()

    print("=" * 60)
    print("Використовуй question_index та option_index у mapping.json")


# ---------------------------------------------------------------------------
# Побудова image-варіанту відповіді
# ---------------------------------------------------------------------------

def build_image_option(original_option: dict, image_url: str, width: int, height: int) -> dict:
    """
    Бере оригінальну структуру варіанта відповіді і перетворює її на image-тип.
    Зберігає _id та id незмінними (щоб правильна відповідь залишилась правильною).
    """
    return {
        **original_option,
        "type": "image",
        "text": "<p></p>",
        "media": [
            {
                "type": "image",
                "url": image_url,
                "meta": {
                    "width": width,
                    "height": height,
                    "layout": "contain",
                    "googleSearch": False,
                    "altText": None,
                    "text": "<p></p>",
                },
            }
        ],
    }


# ---------------------------------------------------------------------------
# PATCH питання на сервері
# ---------------------------------------------------------------------------

def patch_question(
    session: requests.Session,
    quiz_id: str,
    version_id: str,
    question: dict,
) -> bool:
    """
    Надсилає оновлену структуру одного питання через PATCH.
    """
    url = (
        f"https://wayground.com/_quizserver/main/v3/quiz/"
        f"{quiz_id}/version/{version_id}/questions"
    )
    resp = session.patch(
        url,
        json={"updates": [question]},
        headers={"Referer": f"https://wayground.com/admin/quiz/{quiz_id}/edit"},
        timeout=30,
    )
    if resp.status_code == 200 and resp.json().get("success"):
        return True
    print(f"  [X] PATCH помилка. HTTP {resp.status_code}: {resp.text[:300]}")
    return False


# ---------------------------------------------------------------------------
# Головна логіка
# ---------------------------------------------------------------------------

def process_mapping(
    session: requests.Session,
    quiz_id: str,
    mapping: list[dict],
    mapping_dir: Path,
    dry_run: bool = False,
) -> None:
    """
    Основний цикл: для кожного запису в маппінгу завантажує зображення
    і оновлює відповідний варіант відповіді.
    """
    version_id, questions = get_quiz(session, quiz_id)

    print(f"\n[~] Обробляємо {len(mapping)} записів маппінгу...\n")

    success_count = 0
    error_count = 0

    for i, entry in enumerate(mapping):
        q_idx: int = entry["question_index"]
        opt_idx: int = entry["option_index"]
        img_rel: str = entry["image_path"]

        # Шлях до зображення: URL або локальний файл
        if img_rel.startswith("http://") or img_rel.startswith("https://"):
            final_url = img_rel
            width, height = 0, 0
            print(f"[{i+1}/{len(mapping)}] Питання #{q_idx+1}, варіант #{opt_idx+1} <- {img_rel[:60]}...")

            if dry_run:
                print(f"  [DRY-RUN] URL-зображення, пропускаємо")
                success_count += 1
                continue
        else:
            image_path = (mapping_dir / img_rel).resolve()
            print(f"[{i+1}/{len(mapping)}] Питання #{q_idx+1}, варіант #{opt_idx+1} <- {img_rel}")

        # Валідація індексів
        if q_idx >= len(questions):
            print(f"  [X] question_index={q_idx} виходить за межі (всього {len(questions)} питань)")
            error_count += 1
            continue

        question = questions[q_idx]
        options: list[dict] = question["structure"]["options"]

        if opt_idx >= len(options):
            print(f"  [X] option_index={opt_idx} виходить за межі (всього {len(options)} варіантів)")
            error_count += 1
            continue

        if dry_run:
            print(f"  [DRY-RUN] Пропускаємо реальний upload/patch")
            print(f"             question._id={question['_id']}, option._id={options[opt_idx]['_id']}")
            success_count += 1
            continue

        # Завантажуємо зображення (лише для локальних файлів)
        if not (img_rel.startswith("http://") or img_rel.startswith("https://")):
            try:
                final_url, width, height = upload_image(session, image_path)
            except (FileNotFoundError, RuntimeError) as e:
                print(f"  [X] {e}")
                error_count += 1
                continue

        # Підміняємо варіант відповіді
        updated_option = build_image_option(options[opt_idx], final_url, width, height)
        question["structure"]["options"][opt_idx] = updated_option

        # Зберігаємо на сервері
        if patch_question(session, quiz_id, version_id, question):
            print(f"  [✓] Збережено!")
            success_count += 1
            # Оновлюємо локальну копію питань щоб наступні PATCH містили актуальний стан
            questions[q_idx] = question
        else:
            error_count += 1

    print(f"\n{'='*50}")
    print(f"Готово! Успішно: {success_count}, Помилок: {error_count}")
    if error_count == 0:
        print(f"Відкрий тест для перевірки: https://wayground.com/admin/quiz/{quiz_id}/edit")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def load_credentials() -> tuple[str, str]:
    """
    Читає WAYGROUND_EMAIL / WAYGROUND_PASSWORD з .env файлу або змінних середовища.
    .env шукається в директорії скрипту і в поточній директорії.
    """
    # Спробуємо завантажити .env вручну (без python-dotenv)
    for env_dir in [Path(__file__).parent, Path.cwd()]:
        env_file = env_dir / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, val = line.partition("=")
                    # Не перезаписуємо вже встановлені змінні середовища
                    os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))
            break

    email = os.environ.get("WAYGROUND_EMAIL", "")
    password = os.environ.get("WAYGROUND_PASSWORD", "")
    return email, password


def main():
    parser = argparse.ArgumentParser(
        description="Додає зображення до варіантів відповідей у тесті Wayground.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Приклади:
  # Переглянути питання тесту (щоб скласти mapping.json)
  python3 wayground_add_images.py --quiz-id <ID> --list

  # Запустити з маппінгом
  python3 wayground_add_images.py --quiz-id <ID> --mapping mapping.json

  # Перевірити маппінг без реальних змін
  python3 wayground_add_images.py --quiz-id <ID> --mapping mapping.json --dry-run

Credentials (один з варіантів):
  1. Файл .env поряд зі скриптом:   WAYGROUND_EMAIL=... / WAYGROUND_PASSWORD=...
  2. Змінні середовища:              export WAYGROUND_EMAIL=...
  3. Аргументи CLI:                  --email ... --password ...
        """,
    )
    parser.add_argument("--quiz-id", required=True, help="ID тесту з URL (наприклад: 6a2d172938dbd449b9f0041c)")
    parser.add_argument("--list", action="store_true", help="Вивести список питань і варіантів відповідей")
    parser.add_argument("--mapping", help="Шлях до JSON-файлу з маппінгом зображень")
    parser.add_argument("--email", help="Email для Wayground (або WAYGROUND_EMAIL у .env)")
    parser.add_argument("--password", help="Пароль для Wayground (або WAYGROUND_PASSWORD у .env)")
    parser.add_argument("--dry-run", action="store_true", help="Перевірити маппінг без реальних змін")

    args = parser.parse_args()

    # Валідація аргументів
    if not args.list and not args.mapping:
        parser.error("Треба вказати --list або --mapping")

    # Credentials
    env_email, env_password = load_credentials()
    email = args.email or env_email
    password = args.password or env_password

    if not email or not password:
        print("[X] Credentials не знайдено.")
        print("    Створи .env файл або передай --email / --password")
        sys.exit(1)

    # Авторизація
    try:
        session = login(email, password)
    except RuntimeError as e:
        print(f"[X] {e}")
        sys.exit(1)

    # --list: показати питання і вийти
    if args.list:
        try:
            _, questions = get_quiz(session, args.quiz_id)
        except RuntimeError as e:
            print(f"[X] {e}")
            sys.exit(1)
        list_questions(questions)
        return

    # --mapping: основна обробка
    mapping_path = Path(args.mapping).resolve()
    if not mapping_path.exists():
        print(f"[X] Файл маппінгу не знайдено: {mapping_path}")
        sys.exit(1)

    mapping: list[dict] = json.loads(mapping_path.read_text(encoding="utf-8"))
    if not isinstance(mapping, list) or not mapping:
        print("[X] mapping.json має бути непорожнім масивом об'єктів")
        sys.exit(1)

    mapping_dir = mapping_path.parent

    print(f"[~] Quiz ID:  {args.quiz_id}")
    print(f"[~] Маппінг: {mapping_path} ({len(mapping)} записів)")
    if args.dry_run:
        print("[~] Режим DRY-RUN — реальних змін не буде\n")

    try:
        process_mapping(session, args.quiz_id, mapping, mapping_dir, dry_run=args.dry_run)
    except RuntimeError as e:
        print(f"[X] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
