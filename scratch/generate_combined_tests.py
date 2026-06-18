import json
import os
import subprocess

questions = [
    {
        "Question Text": "Дано сирий HTTP/1.1 запит:\n```http\nGET /api/v1/users HTTP/1.1\nAccept: application/json\n\n```\nЧому сучасний вебсервер поверне помилку `400 Bad Request` на цей запит?",
        "Question Type": "Multiple Choice",
        "Option 1": "Браузер не надіслав заголовок `Host`, який є обов'язковим у протоколі HTTP/1.1 для роботи віртуального хостингу.",
        "Option 2": "HTTP/1.1 не підтримує метод `GET` без тіла запиту.",
        "Option 3": "Відсутній заголовок `Content-Length`, обов'язаний для будь-якого HTTP-запиту.",
        "Option 4": "Шлях `/api/v1/users` має обов'язково починатися з протоколу `https://`.",
        "Option 5": "",
        "Correct Answer": "1",
        "Time in seconds": "30",
        "Image Link": "",
        "Answer explanation": "У протоколі HTTP/1.1 заголовок `Host` є обов'язковим. Він дозволяє вебсерверу визначити, до якого саме віртуального хоста (доменного імені) адресовано запит, оскільки на одній IP-адресі може працювати багато сайтів. Якщо заголовок `Host` відсутній, сервер повертає `400 Bad Request`."
    },
    {
        "Question Text": "Проаналізуйте сиру відповідь сервера:\n```http\nHTTP/1.1 200 OK\nTransfer-Encoding: chunked\nContent-Type: text/html\n\n5\nHello\n7\n World!\n0\n\n```\nЯким буде фінальний текст, який отримає клієнт у тілі відповіді після її розкодування?",
        "Question Type": "Multiple Choice",
        "Option 1": "Hello World!",
        "Option 2": "Hello\\n World!",
        "Option 3": "5Hello7 World!0",
        "Option 4": "Hello World!0",
        "Option 5": "",
        "Correct Answer": "1",
        "Time in seconds": "30",
        "Image Link": "",
        "Answer explanation": "У `Transfer-Encoding: chunked` тіло повідомлення розбивається на шматки (chunks). Перед кожним шматком передається його розмір у шістнадцятковій системі числення (hex), за яким іде CRLF, а потім сам шматок даних. Рядок `5` означає 5 байт (`Hello`), `7` означає 7 байт (` World!`), а `0` позначає завершення передачі. Фінальне зшите тіло буде `Hello World!`."
    },
    {
        "Question Text": "Сервер надіслав таку відповідь:\n```http\nHTTP/1.1 200 OK\nSet-Cookie: session=xyz987; Domain=api.example.com; Path=/; Secure; HttpOnly; SameSite=Lax\n\n```\nУ якому з наступних випадків браузер надішле цей cookie назад на сервер?",
        "Question Type": "Multiple Choice",
        "Option 1": "При запиті до `http://api.example.com/` (по протоколу HTTP).",
        "Option 2": "При запиті до `https://example.com/` (батьківський домен).",
        "Option 3": "При запиті до `https://api.example.com/users` (по протоколу HTTPS).",
        "Option 4": "При запиті до `https://evil.example.com/` (інший піддомен).",
        "Option 5": "",
        "Correct Answer": "3",
        "Time in seconds": "30",
        "Image Link": "",
        "Answer explanation": "Атрибут `Secure` дозволяє надсилати cookie лише через захищене з'єднання (HTTPS), тому варіант з HTTP відпадає. Атрибут `Domain=api.example.com` обмежує cookie цим конкретним піддоменом та його піддоменами, тому на батьківський домен `example.com` або інший піддомен `evil.example.com` браузер цей cookie не надішле. Отже, правильний шлях — `https://api.example.com/users`."
    },
    {
        "Question Text": "Користувач авторизований на сайті `shop.com`. Cookie для кошика встановлено так:\n```http\nSet-Cookie: cart=items_list; SameSite=Lax\n\n```\nКористувач перебуває на сторонньому сайті `badsite.com`. Яка дія на `badsite.com` призведе до того, що браузер автоматично надішле цей cookie на `shop.com`?",
        "Question Type": "Multiple Choice",
        "Option 1": "JavaScript-скрипт на `badsite.com` робить фоновий AJAX-запит: `fetch('https://shop.com/api/cart')`.",
        "Option 2": "Користувач клікає по звичайному HTML-посиланню `<a href=\"https://shop.com/cart\">Переглянути кошик</a>` на сторінці `badsite.com`.",
        "Option 3": "На сторінці `badsite.com` завантажується зображення `<img src=\"https://shop.com/logo.png\" />`.",
        "Option 4": "Зловмисна сторінка на `badsite.com` робить POST-відправку прихованої HTML-форми на `https://shop.com/checkout`.",
        "Option 5": "",
        "Correct Answer": "2",
        "Time in seconds": "30",
        "Image Link": "",
        "Answer explanation": "`SameSite=Lax` забезпечує баланс безпеки. Він блокує надсилання cookies при крос-доменних субзапитах (зображення, фрейми) та методах модифікації стану (POST/PUT через форми або AJAX fetch). Проте він дозволяє передавати cookies при безпечній top-level навігації (наприклад, GET-запит при звичайному переході за посиланням `<a>`)."
    },
    {
        "Question Text": "Чому сучасний браузер відхилить (не запише у своє сховище) наступний cookie, надісланий сервером з домену `https://example.com`?\n```http\nSet-Cookie: __Host-id=val123; Domain=example.com; Path=/; Secure; HttpOnly\n\n```\n(Виберіть усі правильні варіанти)",
        "Question Type": "Checkbox",
        "Option 1": "Атрибут `Domain` встановлено в `example.com`, хоча префікс `__Host-` забороняє вказувати цей атрибут (cookie має прив'язуватися суворо до поточного хоста).",
        "Option 2": "Забуто атрибут `SameSite=Strict`, який є обов'язковим для префікса `__Host-`.",
        "Option 3": "Префікс `__Host-` вимагає, щоб атрибут `Path` дорівнював `/` (тут це виконано, але наявність `Domain` ламає все).",
        "Option 4": "Cookie передається без атрибуту `Expires` або `Max-Age`.",
        "Option 5": "",
        "Correct Answer": "1",
        "Time in seconds": "30",
        "Image Link": "",
        "Answer explanation": "Префікс `__Host-` накладає жорсткі вимоги безпеки на браузер: 1) cookie повинен мати атрибут `Secure` (доставка по HTTPS), 2) `Path` має бути встановлений в `/`, 3) **атрибут `Domain` не повинен бути присутній** (cookie не може бути поширений на піддомени). Якщо ці вимоги порушено (зокрема, додано `Domain`), браузер відхиляє cookie."
    },
    {
        "Question Text": "Браузер отримав відповідь із двома cookies:\n```http\nHTTP/1.1 200 OK\nSet-Cookie: theme=dark; Path=/\nSet-Cookie: user=Oleg; Path=/; Max-Age=3600\n\n```\nЯка різниця в часі життя (lifecycle) цих двох cookies?",
        "Question Type": "Multiple Choice",
        "Option 1": "`theme` буде видалено відразу при першому оновленні сторінки, а `user` існуватиме 1 годину.",
        "Option 2": "`theme` є сесійним cookie і буде видалено після закриття вкладки або браузера користувачем, тоді як `user` збережеться в базі даних браузера рівно на 3600 секунд (1 годину).",
        "Option 3": "Обидва cookies є сесійними та будуть видалені при закритті браузера, бо `Max-Age` ігнорується без атрибуту `Expires`.",
        "Option 4": "`theme` зберігається назавжди, оскільки час життя не обмежено, а `user` видалиться через годину.",
        "Option 5": "",
        "Correct Answer": "2",
        "Time in seconds": "30",
        "Image Link": "",
        "Answer explanation": "Якщо в `Set-Cookie` не вказано атрибути `Max-Age` або `Expires`, cookie вважається сесійним (Session Cookie). Браузер видаляє його, коли сесія користувача завершується (зазвичай при закритті браузера). Cookie `user` має явний `Max-Age=3600` (1 година), тому він є персистентним і зберігається браузером на вказаний час навіть після перезапуску програми."
    },
    {
        "Question Text": "Клієнт надіслав наступний запит:\n```http\nGET /api/data HTTP/1.1\nHost: example.com\nIf-Modified-Since: Tue, 16 Jun 2026 15:00:00 GMT\n\n```\nДані на сервері не змінювалися з вказаного часу. Яку відповідь повинен повернути сервер за специфікацією HTTP?",
        "Question Type": "Multiple Choice",
        "Option 1": "`204 No Content` без заголовків та без тіла.",
        "Option 2": "`200 OK` з повним тілом даних, ігноруючи дату.",
        "Option 3": "`304 Not Modified` без тіла (payload), але з метаданими (заголовками).",
        "Option 4": "`412 Precondition Failed` з описом помилки в форматі JSON.",
        "Option 5": "",
        "Correct Answer": "3",
        "Time in seconds": "30",
        "Image Link": "",
        "Answer explanation": "Заголовок `If-Modified-Since` реалізує механізм умовного запиту (Conditional GET). Якщо ресурс на сервері не змінювався з часу, вказаного клієнтом, сервер зобов'язаний повернути статус `304 Not Modified` з порожнім тілом. Клієнт бере дані зі свого кешу, що суттєво заощаджує мережевий трафік."
    },
    {
        "Question Text": "У чому полягає фундаментальна різниця між директивами `no-cache` та `no-store` у заголовку `Cache-Control` відповіді сервера?",
        "Question Type": "Multiple Choice",
        "Option 1": "`no-cache` забороняє кешування на проксі-серверах (CDN), а `no-store` забороняє кешування в браузері.",
        "Option 2": "`no-cache` дозволяє зберігати відповідь у кеші, але вимагає від клієнта обов'язково перевірити її актуальність на сервері (Conditional GET) перед кожним використанням, тоді як `no-store` повністю забороняє записувати відповідь у будь-яке сховище.",
        "Option 3": "`no-store` дозволяє кешувати відповідь на 10 хвилин, а `no-cache` забороняє кешування взагалі.",
        "Option 4": "`no-cache` використовується лише для POST-запитів, а `no-store` — виключно для GET-запитів.",
        "Option 5": "",
        "Correct Answer": "2",
        "Time in seconds": "30",
        "Image Link": "",
        "Answer explanation": "Директива `no-store` створена для конфіденційних даних (паролі, банківські виписки) і наказує ніколи не зберігати відповідь на диску чи в пам'яті. Директива `no-cache` дозволяє кешувати ресурс, але забороняє віддавати його без попередньої перевірки на сервері (через умовні заголовки `If-None-Match`/`If-Modified-Since`). Якщо сервер каже 304, кешована копія використовується."
    },
    {
        "Question Text": "Сервер повернув заголовок:\n```http\nCache-Control: public, max-age=60, stale-while-revalidate=30\n```\nКористувач робить повторний запит до ресурсу через 75 секунд після першого завантаження. Як поведе себе браузер?",
        "Question Type": "Multiple Choice",
        "Option 1": "Браузер вважатиме кеш застарілим, заблокує рендеринг сторінки та чекатиме повної відповіді від сервера.",
        "Option 2": "Браузер миттєво поверне користувачу застарілу версію з кешу (stale), а у фоновому режимі (асинхронно) надішле запит до сервера для оновлення кешу на майбутнє.",
        "Option 3": "Браузер автоматично видалить цей ресурс із кешу і поверне помилку `504 Gateway Timeout`.",
        "Option 4": "Браузер надішле запит на сервер, і якщо сервер відповість помилкою, покаже порожню сторінку.",
        "Option 5": "",
        "Correct Answer": "2",
        "Time in seconds": "30",
        "Image Link": "",
        "Answer explanation": "Директива `stale-while-revalidate=30` визначає вікно часу (тут 60 + 30 = 90 секунд), протягом якого застарілий кеш може бути використаний негайно, поки браузер робить фоновий запит для його оновлення. Оскільки 75 секунд потрапляє в інтервал між 60 та 90 секундами, користувач отримає відповідь миттєво з кешу, а в фоні відбудеться оновлення."
    },
    {
        "Question Text": "Для чого сервер додає заголовок `Vary: Accept-Encoding, Accept-Language` у відповідь?\n```http\nHTTP/1.1 200 OK\nContent-Type: application/json\nCache-Control: public, max-age=3600\nVary: Accept-Encoding, Accept-Language\n\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "Щоб браузер знав, які методи стиснення підтримує сервер для наступних запитів.",
        "Option 2": "Щоб проміжні кеші (CDN, проксі) та браузер зберігали окремі копії ресурсу для кожної комбінації заголовків `Accept-Encoding` та `Accept-Language` запиту.",
        "Option 3": "Щоб змусити клієнта завжди надсилати ці заголовки, інакше сервер поверне помилку `406 Not Acceptable`.",
        "Option 4": "Цей заголовок використовується для автентифікації користувача на основі мови його системи.",
        "Option 5": "",
        "Correct Answer": "2",
        "Time in seconds": "30",
        "Image Link": "",
        "Answer explanation": "Заголовок `Vary` визначає, які заголовки запиту впливають на вміст відповіді. Якщо сервер віддає різний контент для різних мов (`Accept-Language`) або стискає його різними методами (`Accept-Encoding`), проксі-сервер чи CDN повинні знати про це. `Vary` запобігає ситуації, коли користувач з англійським інтерфейсом отримає з кешу раніше збережену українську версію сайту."
    },
    {
        "Question Text": "Розглянемо SMTP-сесію:\n```http\nS: 220 mail.example.com ESMTP Postfix\nC: EHLO app.local\nS: 250-mail.example.com Hello\nS: 250-STARTTLS\nS: 250-SIZE 10485760\nC: STARTTLS\nS: 220 2.0.0 Ready to start TLS\n[Клієнт і сервер виконують TLS Handshake]\n```\nЯку дію повинен зробити SMTP-клієнт відразу після успішного завершення TLS Handshake?",
        "Question Type": "Multiple Choice",
        "Option 1": "Надіслати команду `AUTH PLAIN` для передачі логіна та пароля.",
        "Option 2": "Надіслати команду `EHLO app.local` ще раз, щоб повторно привітатися всередині шифрованого тунелю.",
        "Option 3": "Одразу розпочати надсилання конверту листа за допомогою `MAIL FROM`.",
        "Option 4": "Закрити з'єднання командою `QUIT`, оскільки TLS Handshake є фінальною фазою.",
        "Option 5": "",
        "Correct Answer": "2",
        "Time in seconds": "30",
        "Image Link": "",
        "Answer explanation": "Після виконання команди `STARTTLS` та завершення TLS Handshake з'єднання переходить у зашифрований режим. Специфікація ESMTP вимагає, щоб клієнт надіслав команду `EHLO` знову. Це необхідно тому, що набір розширень, які підтримує сервер, може змінитися після встановлення шифрування (наприклад, сервер з міркувань безпеки не показує підтримку `AUTH` до того, як канал буде зашифровано)."
    },
    {
        "Question Text": "Дано запис SMTP-діалогу:\n```http\nC: MAIL FROM:<bounce-handler@sender.com>\nC: RCPT TO:<bob@recipient.com>\nC: DATA\nS: 354 Start mail input\nC: From: Alice <alice@brand.com>\nC: To: Bob <bob@recipient.com>\nC: Subject: Welcome!\nC:\nC: Hello Bob!\nC: .\n```\nКуди поштовий сервер надішле сповіщення про помилку доставки (bounce message), якщо поштова скринька Боба переповнена?",
        "Question Type": "Multiple Choice",
        "Option 1": "На адресу `alice@brand.com` (Header Sender, вказаний в `From:` тіла листа).",
        "Option 2": "На адресу `bounce-handler@sender.com` (Envelope Sender / Return-Path, вказаний у `MAIL FROM`).",
        "Option 3": "Сервер не буде нікуди надсилати помилку, а просто проігнорує лист.",
        "Option 4": "На обидві адреси одночасно: `bounce-handler@sender.com` та `alice@brand.com`.",
        "Option 5": "",
        "Correct Answer": "2",
        "Time in seconds": "30",
        "Image Link": "",
        "Answer explanation": "У пошті є два відправники: 1) Envelope Sender (задається командою `MAIL FROM:<...>` на рівні SMTP транспорту). Саме туди повертаються всі технічні помилки доставки (bounces). 2) Header Sender (заголовок `From:` усередині блоку `DATA`). Цю адресу бачить кінцевий користувач у своєму Outlook/Gmail. Вона використовується для звичайних відповідей користувача (Reply). У цьому випадку помилка доставки піде на `bounce-handler@sender.com`."
    },
    {
        "Question Text": "У ході SMTP-діалогу на команду клієнта сервер повернув відповідь:\n```http\nC: RCPT TO:<john.doe@company.com>\nS: 550 5.1.1 User Unknown\n```\nЯкі висновки має зробити програма-відправник на основі цього коду?",
        "Question Type": "Multiple Choice",
        "Option 1": "Це тимчасова помилка (код класу 4xx), слід зачекати кілька хвилин та спробувати відправити цей лист ще раз.",
        "Option 2": "Це постійна помилка (код класу 5xx), що вказує на відсутність такого адресата. Слід припинити спроби доставки на цю адресу та зафіксувати помилку.",
        "Option 3": "Помилка виникла на стороні мережевого з'єднання, необхідно терміново виконати перепідключення до SMTP-сервера.",
        "Option 4": "Сервер просить клієнта пройти автентифікацію `AUTH` перед тим, як надсилати пошту.",
        "Option 5": "",
        "Correct Answer": "2",
        "Time in seconds": "30",
        "Image Link": "",
        "Answer explanation": "Коди SMTP, що починаються на `5` (клас 5xx), позначають постійні помилки (Permanent Failures). Это означає, що повторна спроба за тих самих умов дасть такий самий негативний результат. Код `550 User Unknown` свідчить про те, що такої скриньки на сервері одержувача не існує, тому повторювати запит безглуздо."
    },
    {
        "Question Text": "Розробник створює поштове повідомлення, яке містить:\n1. Гарно відформатований HTML-текст.\n2. Простий текстовий варіант (Plain text) для старих поштових клієнтів.\n3. Прикріплений файл-звіт `report.pdf`.\n\nЯкою має бути правильна ієрархія MIME-типів (`multipart/mixed` та `multipart/alternative`) для цього листа?",
        "Question Type": "Multiple Choice",
        "Option 1": "multipart/alternative як зовнішній контейнер, що містить `multipart/mixed` (в якому лежить HTML та plain text) та PDF-файл.",
        "Option 2": "multipart/mixed як зовнішній контейнер, що містить `multipart/alternative` (в якому об'єднано plain text та HTML версії) та окрему частину для PDF-файлу з типом `application/pdf`.",
        "Option 3": "Лист має складатися виключно з одного рівня `multipart/mixed`, в якому всі три елементи (Plain text, HTML, PDF) лежать на одному рівні паралельно.",
        "Option 4": "Використовувати `multipart/related` як зовнішній контейнер для PDF-файлу, а `multipart/alternative` для тексту.",
        "Option 5": "",
        "Correct Answer": "2",
        "Time in seconds": "45",
        "Image Link": "",
        "Answer explanation": "Зовнішній контейнер має об'єднувати логічно різні сутності: сам вміст листа та окреме вкладення (для цього слугує `multipart/mixed`). Всередині нього вміст листа представляється двома взаємозамінними варіантами (HTML або Plain text), які об'єднуються в `multipart/alternative`, щоб поштовий клієнт вибрав найкращий для відображення формат."
    },
    {
        "Question Text": "Розробник намагається відправити лист у .NET за допомогою `System.Net.Mail.SmtpClient`. У конфігурації вказано порт `465` (Implicit TLS) та `EnableSsl = true`.\nЧому цей код завершується помилкою таймауту або збою підключення?",
        "Question Type": "Multiple Choice",
        "Option 1": "Для роботи порту 465 необхідно додатково встановити пакет `System.Net.Security.Tls`.",
        "Option 2": "Клас `SmtpClient` у .NET підтримує шифрування лише через механізм `STARTTLS` (який починається як plaintext-з'єднання і потім підвищується до TLS, зазвичай на порту 587). Він не підтримує Implicit TLS (де TLS-з'єднання встановлюється відразу при підключенні на порту 465).",
        "Option 3": "При використанні порту 465 властивість `EnableSsl` має бути встановлена в `false`.",
        "Option 4": "Порт 465 зарезервований виключно для отримання пошти через IMAP, а не для SMTP.",
        "Option 5": "",
        "Correct Answer": "2",
        "Time in seconds": "45",
        "Image Link": "",
        "Answer explanation": "Історично `System.Net.Mail.SmtpClient` у .NET реалізує лише схему `Explicit SSL/TLS` (STARTTLS). При `EnableSsl = true` клієнт спочатку підключається по звичайному TCP, а потім надсилає команду `STARTTLS` для початку шифрування. На порту `465` сервер очікує негайного TLS Handshake при підключенні (Implicit TLS). Оскільки `SmtpClient` намагається слати plaintext команду, виникає збій. Для роботи з Implicit TLS (465) у .NET рекомендується використовувати сторонню бібліотеку `MailKit`."
    },
    {
        "Question Text": "Чому протокол HTTP/3 повністю відмовився від використання TCP на користь QUIC (поверх UDP)?",
        "Question Type": "Multiple Choice",
        "Option 1": "TCP не підтримує шифрування трафіку, тоді як UDP є шифрованим за замовчуванням.",
        "Option 2": "Для усунення проблеми блокування початку черги (Head-of-Line Blocking) на транспортному рівні TCP: при втраті одного пакету в TCP зупиняється передача всіх паралельних потоків даних HTTP, тоді як у QUIC втрата пакету в одному потоці не блокує інші.",
        "Option 3": "UDP дозволяє передавати файли необмеженого розміру без поділу на сегменти.",
        "Option 4": "TCP є застарілим протоколом, який не підтримує передачу текстових заголовків HTTP.",
        "Option 5": "",
        "Correct Answer": "2",
        "Time in seconds": "45",
        "Image Link": "",
        "Answer explanation": "В HTTP/2 кілька запитів передаються паралельно (мультиплексуються) через одне TCP-з'єднання. Проте на рівні TCP всі вони є єдиним потоком байтів. Якщо один TCP-пакет губиться в мережі, TCP зупиняє приймання всіх наступних байтів до перевідправки втраченого пакету. Це блокує всі паралельні HTTP-потоки (HOL blocking). HTTP/3 використовує QUIC поверх UDP, де кожен HTTP-потік є незалежним на транспортному рівні, і втрата пакету в одному потоці не впливає на інші."
    }
]

# --- Export to Excel ---

out_dir = "tests/01.csharp/13.network-programming"
os.makedirs(out_dir, exist_ok=True)
json_path = "tmp_questions.json"
xlsx_path = os.path.join(out_dir, "08.web-protocols-combined.xlsx")

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print("Running wayground_exporter.py...")
subprocess.run(["python3", "wayground_exporter.py", json_path, "-o", xlsx_path])
os.remove(json_path)

print(f"✅ Created {xlsx_path} successfully. Total questions: {len(questions)}")
