#!/usr/bin/env python3
import os
import re
import sys
import argparse
import requests
from urllib.parse import urlparse

# Спробуємо імпортувати duckduckgo_search. Якщо його немає, дамо інструкцію зі встановлення.
try:
    from duckduckgo_search import DDGS
except ImportError:
    print("Помилка: Бібліотека 'duckduckgo_search' не встановлена.", file=sys.stderr)
    print("Будь ласка, встановіть її за допомогою команди:", file=sys.stderr)
    print("pip install duckduckgo_search requests", file=sys.stderr)
    sys.exit(1)


def sanitize_filename(name):
    """Очищує ім'я файлу від заборонених символів."""
    return "".join(c for c in name if c.isalnum() or c in (" ", "_", "-")).rstrip()


def get_image_dir_from_md_path(md_path):
    """
    Аналізує шлях до markdown файлу за правилами prompt.md та повертає шлях
    до папки із зображеннями відносно кореня проекту (public/images/...).
    Наприклад:
      content/12.html-css/05.html-forms.md -> public/images/html-css/html-forms
    """
    normalized_path = os.path.normpath(md_path)
    parts = normalized_path.split(os.sep)

    if "content" in parts:
        content_idx = parts.index("content")
        rel_parts = parts[content_idx + 1 :]
    else:
        # Якщо папка content не знайдена в шляху, використовуємо останні частини шляху
        rel_parts = parts[-3:] if len(parts) >= 3 else parts

    cleaned_parts = []
    for part in rel_parts:
        if part.endswith(".md"):
            part = part[:-3]  # видаляємо розширення
        # Видаляємо числові префікси, наприклад "12.html-css" -> "html-css"
        cleaned_part = re.sub(r"^\d+\.", "", part)
        cleaned_parts.append(cleaned_part)

    return os.path.join("public", "images", *cleaned_parts)


def download_image(url, folder, filename):
    """Завантажує зображення за URL та зберігає у вказану папку."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        parsed_url = urlparse(url)
        ext = os.path.splitext(parsed_url.path)[1]
        if not ext or len(ext) > 5:
            content_type = response.headers.get("content-type", "")
            if "image/jpeg" in content_type:
                ext = ".jpg"
            elif "image/png" in content_type:
                ext = ".png"
            elif "image/svg+xml" in content_type:
                ext = ".svg"
            elif "image/gif" in content_type:
                ext = ".gif"
            elif "image/webp" in content_type:
                ext = ".webp"
            else:
                ext = ".jpg"

        full_filename = f"{filename}{ext}"
        filepath = os.path.join(folder, full_filename)

        # Запобігаємо перезапису файлів з однаковими назвами
        counter = 1
        while os.path.exists(filepath):
            filepath = os.path.join(folder, f"{filename}_{counter}{ext}")
            counter += 1

        with open(filepath, "wb") as f:
            f.write(response.content)

        # Повертаємо назву збереженого файлу відносно папки public
        # щоб легко сформувати посилання для markdown
        return filepath
    except Exception as e:
        print(f" Не вдалося завантажити {url}: {e}", file=sys.stderr)
        return None


def fetch_and_download(query, limit=1, output_dir=None, md_path=None):
    """Шукає картинки через DuckDuckGo та завантажує їх."""
    # Визначаємо папку завантаження
    if md_path:
        target_dir = get_image_dir_from_md_path(md_path)
        print(f" Шлях визначено автоматично за md-файлом: {target_dir}")
    elif output_dir:
        target_dir = output_dir
    else:
        target_dir = "downloads"

    os.makedirs(target_dir, exist_ok=True)
    print(f"Шукаємо зображення за запитом: '{query}' (ліміт: {limit})...")

    downloaded_paths = []
    try:
        with DDGS() as ddgs:
            results = ddgs.images(
                keywords=query,
                region="wt-wt",
                safesearch="moderate",
                max_results=limit,
            )

            if not results:
                print("Зображень за таким запитом не знайдено.")
                return

            base_filename = sanitize_filename(query).replace(" ", "_").lower()

            for idx, item in enumerate(results):
                img_url = item.get("image")
                print(f"[{idx+1}/{limit}] Завантаження з {img_url}...")
                saved_path = download_image(img_url, target_dir, f"{base_filename}_{idx+1}")
                if saved_path:
                    downloaded_paths.append(saved_path)
                    print(f"   Збережено: {saved_path}")

            # Виводимо готові посилання у форматі markdown
            if downloaded_paths:
                print("\n" + "=" * 50)
                print("ГОТОВІ ВСТАВКИ ДЛЯ MARKDOWN:")
                print("=" * 50)
                for path in downloaded_paths:
                    # Отримуємо шлях відносно папки 'public', наприклад: /images/html-css/...
                    parts = path.split(os.sep)
                    if "public" in parts:
                        pub_idx = parts.index("public")
                        md_img_path = "/" + "/".join(parts[pub_idx + 1 :])
                    else:
                        md_img_path = "/" + path.replace(os.sep, "/")

                    print(f"![{query}]({md_img_path}){{.diagram-img}}")
                print("=" * 50 + "\n")

    except Exception as e:
        print(f"Помилка під час пошуку: {e}", file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скрипт для пошуку та завантаження зображень.")
    parser.add_argument("query", type=str, help="Пошуковий запит (наприклад, 'docker container logo')")
    parser.add_argument("-l", "--limit", type=int, default=1, help="Кількість зображень для завантаження (типово 1)")
    parser.add_argument("-o", "--output", type=str, default=None, help="Папка для збереження (використовується якщо немає --md)")
    parser.add_argument("--md", type=str, default=None, help="Шлях до md-файлу, щоб автоматично побудувати структуру папок")

    args = parser.parse_args()
    fetch_and_download(args.query, args.limit, args.output, args.md)
