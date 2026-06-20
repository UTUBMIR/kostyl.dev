import os
import requests

# ==================== НАЛАШТУВАННЯ АВТОРИЗАЦІЇ ====================
# Твої актуальні дані, які ми витягли з дампа
COOKIES = {
    "_sid": "J7mFQu_Knc8p1ttpvGZjjkaayQcZi_fwJKNgdisfiRs-9wB4hYSFoFpF6oQnSYVF_ec8uSYKLGQhgra_626TJgJfi5q1Ws4ZyYwQzzVCh44LClGqTfW98SE.oXSk1Wbuh9qqkOrBeB0ocw.flcj-LBSoDwwkszZ",
    "quizizz_uid": "9c053f05-93a8-4d97-970c-c0123c7c6684"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "X-CSRF-Token": "HqCM_HO9MW_3-eddKxYXYHXLVEk",
    "Origin": "https://wayground.com",
    "Referer": "https://wayground.com/admin/quiz/6a2d172938dbd449b9f0041c/edit"
}
# ==================================================================

def upload_image_to_quizizz(image_source):
    """
    Завантажує будь-яку картинку на сервери Quizizz.
    :param image_source: Шлях до локального файлу (наприклад, 'photo.jpg') або URL картинки з інтернету
    :return: final_url, який треба вставляти в питання
    """
    session = requests.Session()
    session.headers.update(HEADERS)
    for name, value in COOKIES.items():
        session.cookies.set(name, value, domain="wayground.com")

    # 1. Отримуємо бінарні дані картинки
    if image_source.startswith(('http://', 'https://')):
        print(f"[~] Завантажуємо картинку з інтернету: {image_source}")
        img_resp = requests.get(image_source)
        if img_resp.status_code != 200:
            raise Exception(f"Не вдалося скачати картинку за посиланням. Статус: {img_resp.status_code}")
        image_data = img_resp.content
    else:
        if not os.path.exists(image_source):
            raise FileNotFoundError(f"Файл не знайдено за шляхом: {image_source}")
        print(f"[~] Читаємо локальний файл: {image_source}")
        with open(image_source, "rb") as f:
            image_data = f.read()

    # 2. Запитуємо Pre-signed URL у Quizizz
    print("[~] Запитуємо підписане посилання у Quizizz...")
    init_url = "https://media.quizizz.com/_mdserver/main/getUploadURL?destination=quizzes&enableAcceleration=true"
    response = session.post(init_url)
    
    if response.status_code != 200 or not response.json().get("success"):
        print("[X] Помилка авторизації або запиту токена!")
        print("Текст відповіді:", response.text)
        return None

    res_json = response.json()
    signed_url = res_json["data"]["signedUrl"]
    final_url = res_json["data"]["finalUrl"]

    # 3. Відправляємо байти на AWS S3
    print("[~] Відправляємо файл у сховище AWS S3...")
    s3_headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    s3_response = requests.put(signed_url, headers=s3_headers, data=image_data)

    if s3_response.status_code == 200:
        print("[✓] Успішно завантажено в хмару!")
        return final_url
    else:
        print(f"[X] Помилка завантаження на AWS S3. Статус: {s3_response.status_code}")
        print(s3_response.text)
        return None


def save_question_changes(quiz_id, version_id, question_payload):
    """
    Зберігає оновлену структуру питання на сервері через PATCH запит.
    """
    session = requests.Session()
    session.headers.update(HEADERS)
    for name, value in COOKIES.items():
        session.cookies.set(name, value, domain="wayground.com")

    patch_url = f"https://wayground.com/_quizserver/main/v3/quiz/{quiz_id}/version/{version_id}/questions"
    
    print("[~] Надсилаємо PATCH запит для збереження питання...")
    response = session.patch(patch_url, json=question_payload)
    
    if response.status_code == 200 and response.json().get("success"):
        print("[✓] Зміни успішно збережено в системі Quizizz/Wayground!")
        return response.json()
    else:
        print(f"[X] Не вдалося зберегти питання. Статус коду: {response.status_code}")
        print("Відповідь сервера:", response.text)
        return None


# ==================== ПРИКЛАД ВИКОРИСТАННЯ ====================
if __name__ == "__main__":
    
    # ID вашого тесту та його поточної версії з дампа
    QUIZ_ID = "6a2d172938dbd449b9f0041c"
    VERSION_ID = "6a2d356e448089203f3698f2"
    
    local_img = "2.jpg" 
    
    # Створимо пустий файл для тесту, якщо у тебе немає під рукою реального 2.jpg
    if not os.path.exists(local_img):
        with open(local_img, "wb") as f:
            f.write(b"fake image bytes") 

    # Крок 1 та 2: Завантажуємо картинку на сервери Amazon S3
    new_image_url = upload_image_to_quizizz(local_img)
    
    if new_image_url:
        print(f"\n[✓] Новий URL картинки: {new_image_url}")
        print("[~] Формуємо структуру питання для збереження...")
        
        # Крок 3: Готуємо payload запиту (адаптований JSON з вашого дампа під Python-dict)
        payload = {
            "updates": [
                {
                    "structure": {
                        "settings": {
                            "hasCorrectAnswer": True,
                            "fibDataType": "string",
                            "canSubmitCustomResponse": False,
                            "doesOptionHaveMultipleTargets": False,
                            "showAdvancedRTE": False
                        },
                        "hasMath": False,
                        "query": {
                            "type": "text",
                            "hasMath": False,
                            "math": {"latex": [], "template": None},
                            "answerTime": -1,
                            "text": "Який спосіб передачі структури у funktion є рекомендованим за замовчуванням, якщо функція має лише читати дані без модифікації оригіналу?",
                            "media": []
                        },
                        "options": [
                            {
                                "type": "image",
                                "hasMath": False,
                                "math": {"latex": [], "template": None},
                                "answerTime": 0,
                                "id": "6a2d1738ecbfcf4864b0a191",
                                "text": "<p></p>",
                                # Сюди динамічно підставляється отримане посилання
                                "media": [
                                    {
                                        "type": "image",
                                        "url": new_image_url, 
                                        "meta": {
                                            "width": 850,
                                            "height": 1377,
                                            "layout": "contain",
                                            "googleSearch": False,
                                            "altText": None,
                                            "text": "<p></p>"
                                        }
                                    }
                                ],
                                "_id": "6a2d1738ecbfcf4864b0a191"
                            },
                            {
                                "type": "text",
                                "hasMath": False,
                                "math": {"latex": [], "template": None},
                                "answerTime": 0,
                                "id": "6a2d1738ecbfcf4864b0a192",
                                "text": "За константним посиланням (`const T&amp;`)",
                                "media": [],
                                "_id": "6a2d1738ecbfcf4864b0a192"
                            },
                            {
                                "type": "text",
                                "hasMath": False,
                                "math": {"latex": [], "template": None},
                                "answerTime": 0,
                                "id": "6a2d1738ecbfcf4864b0a193",
                                "text": "За неконстантним посиланням (`T&amp;`)",
                                "media": [],
                                "_id": "6a2d1738ecbfcf4864b0a193"
                            },
                            {
                                "type": "text",
                                "hasMath": False,
                                "math": {"latex": [], "template": None},
                                "answerTime": 0,
                                "id": "6a2d1738ecbfcf4864b0a194",
                                "text": "<p>За вказівником на константу (`const T*`)</p>",
                                "media": [],
                                "_id": "6a2d1738ecbfcf4864b0a194"
                            }
                        ],
                        "explain": {
                            "type": "",
                            "text": "Передача за константним посиланням (`const T&amp;`) не створює копію об&#39;єкта (передається лише його адреса), а ключове слово `const` гарантує незмінність оригіналу на рівні компілятора.",
                            "media": [],
                            "hasMath": False,
                            "math": {"template": None, "latex": []},
                            "answerTime": 0
                        },
                        "hints": [],
                        "kind": "MCQ",
                        "theme": {
                            "fontFamily": "Quicksand",
                            "titleFontFamily": "Quicksand",
                            "fontColor": {"text": "#5D2057"},
                            "background": {"color": "#FFFFFF", "image": "", "video": ""},
                            "shape": {"largeShapeColor": "#E9E0F3", "smallShapeColor": "#9A4292"}
                        },
                        "marks": {"correct": 1, "incorrect": 0},
                        "answer": 1
                    },
                    "standards": [],
                    "topics": [],
                    "isSuperParent": False,
                    "standardIds": [],
                    "unifiedStandardIds": [],
                    "aiGenerated": False,
                    "__v": 1,
                    "ver": 2,
                    "parent": "6a2d173925ffde610cefb904",
                    "_id": "6a2d35867abeac3bf4e9ca37",
                    "time": 30000,
                    "published": False,
                    "aiCreateMeta": {},
                    "type": "MCQ",
                    "aiMeta": {}
                }
            ]
        }
        
        # Фінальний крок: Зберігаємо все на сервері
        save_question_changes(QUIZ_ID, VERSION_ID, payload)
    else:
        print("[X] Не вдалося завершити процес через помилку завантаження файлу.")