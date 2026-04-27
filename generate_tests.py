import json
import os
import subprocess

questions = [
    {
        "Question Text": "Який стан отримує контейнер після виконання команди `docker create` і в чому його особливість?",
        "Question Type": "Multiple Choice",
        "Option 1": "Стан 'Running'. Контейнер створено і він автоматично виконує процес з PID 1.",
        "Option 2": "Стан 'Created'. Контейнер має виділені ресурси (namespace, файлову систему), але головний процес ще не запущено.",
        "Option 3": "Стан 'Paused'. Контейнер підготовлено, але його процеси заморожені до виконання `docker unpause`.",
        "Option 4": "Стан 'Exited'. Контейнер успішно підготовлено і очікує підключення.",
        "Option 5": "",
        "Correct Answer": "2",
        "Time in seconds": "45",
        "Image Link": "",
        "Answer explanation": "Стан Created означає, що Docker підготував усю конфігурацію, файлову систему і мережу для контейнера, проте головний процес (PID 1) ще не почав виконуватися."
    },
    {
        "Question Text": "У чому полягає ключова відмінність між станом 'Paused' та зупинкою контейнера ('Exited')?",
        "Question Type": "Multiple Choice",
        "Option 1": "'Paused' завершує процеси з graceful shutdown, а 'Exited' — ні.",
        "Option 2": "У стані 'Paused' процеси миттєво заморожуються на рівні ядра (cgroup freezer) і залишаються в пам'яті, тоді як зупинка відправляє SIGTERM і завершує процеси.",
        "Option 3": "'Paused' використовується лише для тимчасового звільнення місця на диску, а 'Exited' — для звільнення оперативної пам'яті.",
        "Option 4": "Між ними немає різниці, це різні команди для однієї дії.",
        "Option 5": "",
        "Correct Answer": "2",
        "Time in seconds": "60",
        "Image Link": "",
        "Answer explanation": "Команда pause заморожує процеси за допомогою cgroup freezer: процеси не виконуються, але їх стан залишається в оперативній пам'яті. При docker stop процесам надсилається SIGTERM і вони коректно завершуються (graceful shutdown)."
    },
    {
        "Question Text": "Які з наведених тверджень про процес PID 1 всередині контейнера є правильними?",
        "Question Type": "Checkbox",
        "Option 1": "Завершення процесу з PID 1 призводить до зупинки всього контейнера.",
        "Option 2": "PID 1 у контейнері завжди збігається з PID цього ж процесу на хост-системі.",
        "Option 3": "PID 1 отримує сигнали від Docker (наприклад, SIGTERM при виконанні docker stop).",
        "Option 4": "PID 1 відповідає за reaping zombie-процесів усередині контейнера.",
        "Option 5": "Контейнер може працювати без процесу PID 1, якщо запущено інші фонові процеси.",
        "Correct Answer": "1,3,4",
        "Time in seconds": "60",
        "Image Link": "",
        "Answer explanation": "Процес PID 1 є головним у namespace контейнера: його життя дорівнює жи життю контейнера. Він також обробляє системні сигнали від Docker і відповідає за 'збір' (reaping) дочірніх процесів, запобігаючи виникненню zombie-процесів. На хост-системі цей процес має інший, унікальний PID."
    },
    {
        "Question Text": "Чому використання shell form (`CMD nginx -g \"daemon off;\"`) в Dockerfile вважається поганою практикою?",
        "Question Type": "Multiple Choice",
        "Option 1": "Shell form вимагає більше оперативної пам'яті для роботи.",
        "Option 2": "Процесом PID 1 стає `/bin/sh`, який може не передавати сигнали (наприклад, SIGTERM) головному процесу, призводячи до некоректного завершення.",
        "Option 3": "Shell form не дозволяє передавати змінні оточення в контейнер.",
        "Option 4": "Контейнери, створені з shell form, неможливо підключити до мережі.",
        "Option 5": "",
        "Correct Answer": "2",
        "Time in seconds": "60",
        "Image Link": "",
        "Answer explanation": "При використанні shell form Docker запускає команду через `/bin/sh -c`. Таким чином PID 1 отримує shell. Shell може не передавати сигнали (SIGTERM) дочірнім процесам, що часто призводить до їх примусового вбивства через SIGKILL та створення zombie-процесів."
    },
    {
        "Question Text": "Який системний сигнал відправляє Docker процесу PID 1 при виконанні команди `docker stop` за замовчуванням?",
        "Question Type": "Fill-in-the-Blank",
        "Option 1": "SIGTERM",
        "Option 2": "",
        "Option 3": "",
        "Option 4": "",
        "Option 5": "",
        "Correct Answer": "",
        "Time in seconds": "30",
        "Image Link": "",
        "Answer explanation": "За замовчуванням `docker stop` відправляє сигнал SIGTERM (signal 15) для ініціювання graceful shutdown (коректного завершення роботи). Якщо процес не завершується протягом таймауту (10 секунд), тоді відправляється SIGKILL."
    },
    {
        "Question Text": "Яку команду слід використати для того, щоб відкрити інтерактивний shell (`bash`) всередині вже працюючого контейнера з іменем `web`?",
        "Question Type": "Fill-in-the-Blank",
        "Option 1": "docker exec -it web bash",
        "Option 2": "",
        "Option 3": "",
        "Option 4": "",
        "Option 5": "",
        "Correct Answer": "",
        "Time in seconds": "30",
        "Image Link": "",
        "Answer explanation": "Команда `docker exec` використовується для виконання команд всередині працюючого контейнера. Прапорці `-it` забезпечують інтерактивний режим і TTY для роботи з shell (`bash`)."
    },
    {
        "Question Text": "Ви виконали команду `docker exec web apt update && apt install curl`, щоб встановити `curl` у працюючий контейнер. Що станеться з цією утилітою, якщо ви видалите контейнер і створите новий з того ж образу?",
        "Question Type": "Multiple Choice",
        "Option 1": "Утиліта збережеться, оскільки `docker exec` модифікує базовий образ.",
        "Option 2": "Утиліта залишиться доступною завдяки автоматичному бекапу Docker.",
        "Option 3": "Утиліта зникне, оскільки всі зміни були зроблені лише в тимчасовому (writable) шарі видаленого контейнера.",
        "Option 4": "Docker видасть помилку при створенні нового контейнера, повідомивши про змінений шар.",
        "Option 5": "",
        "Correct Answer": "3",
        "Time in seconds": "45",
        "Image Link": "",
        "Answer explanation": "Будь-які зміни, зроблені через `docker exec` (встановлення пакетів, зміна файлів), зберігаються лише у writable layer (шарі для запису) конкретного контейнера. Після видалення контейнера ці зміни безповоротно втрачаються. Для постійних змін необхідно оновлювати Dockerfile."
    },
    {
        "Question Text": "Яка команда дозволяє відфільтрувати вивід `docker inspect` і отримати лише IP-адресу контейнера `web`? (Введіть команду з використанням --format)",
        "Question Type": "Fill-in-the-Blank",
        "Option 1": "docker inspect --format='{{.NetworkSettings.IPAddress}}' web",
        "Option 2": "",
        "Option 3": "",
        "Option 4": "",
        "Option 5": "",
        "Correct Answer": "",
        "Time in seconds": "60",
        "Image Link": "",
        "Answer explanation": "Форматування `--format` з використанням синтаксису Go templates (`{{.NetworkSettings.IPAddress}}`) є найшвидшим способом отримати конкретне значення, таке як IP-адреса, з великого JSON-об'єкта, який повертає `docker inspect`."
    },
    {
        "Question Text": "За замовчуванням Docker зберігає логи контейнерів у:",
        "Question Type": "Multiple Choice",
        "Option 1": "Системному журналі `syslog` або `journald`",
        "Option 2": "Базі даних SQLite, прихованій в системних файлах Docker",
        "Option 3": "JSON-файлах на хост-системі",
        "Option 4": "Безпосередньо в оперативній пам'яті (in-memory) для швидкого доступу",
        "Option 5": "",
        "Correct Answer": "3",
        "Time in seconds": "30",
        "Image Link": "",
        "Answer explanation": "За замовчуванням використовується log driver `json-file`, який зберігає весь STDOUT та STDERR вивід процесу в окремих JSON-файлах у директорії `/var/lib/docker/containers/<id>/`."
    },
    {
        "Question Text": "Ви встановили ліміт на використання пам'яті контейнером: `docker run -d --memory=\"512m\" ...`. Що станеться, якщо процеси всередині контейнера спробують виділити більше пам'яті, ніж дозволено (за умови відсутності swap)?",
        "Question Type": "Multiple Choice",
        "Option 1": "Docker автоматично тимчасово збільшить ліміт пам'яті, повідомивши про це адміністратора.",
        "Option 2": "Процеси просто зависнуть в очікуванні звільнення пам'яті іншими контейнерами.",
        "Option 3": "Ядро Linux активує OOM Killer, який почне вбивати процеси всередині контейнера.",
        "Option 4": "Контейнер миттєво перейде в стан 'Paused'.",
        "Option 5": "",
        "Correct Answer": "3",
        "Time in seconds": "45",
        "Image Link": "",
        "Answer explanation": "Коли контейнер досягає жорсткого ліміту пам'яті і не може використовувати swap, ядро системи викликає механізм OOM Killer (Out Of Memory Killer), який примусово завершує процеси для звільнення пам'яті. Це може призвести навіть до зупинки контейнера (статус OOMKilled), якщо буде вбито PID 1."
    },
    {
        "Question Text": "Яка різниця між виводом команди `docker top web` та команди `docker exec web ps aux`?",
        "Question Type": "Checkbox",
        "Option 1": "`docker top` показує PID процесів з точки зору хост-системи.",
        "Option 2": "`docker top` може показати процеси лише зупинених контейнерів.",
        "Option 3": "`docker exec ps aux` показує PID процесів всередині ізольованого PID namespace контейнера.",
        "Option 4": "Різниці немає, ці команди виконують одне й те саме під капотом.",
        "Option 5": "",
        "Correct Answer": "1,3",
        "Time in seconds": "60",
        "Image Link": "",
        "Answer explanation": "Команда `docker top` показує процеси з точки зору системи-хоста (де вони мають реальні системні PID), тоді як виконання `ps aux` всередині контейнера через `exec` показує процеси в ізольованому PID namespace (де головний процес завжди має PID 1)."
    },
    {
        "Question Text": "Що означає опція `--cpu-shares` порівняно з `--cpus` при обмеженні ресурсів?",
        "Question Type": "Checkbox",
        "Option 1": "`--cpus` встановлює жорсткий ліміт (hard limit) на кількість процесорного часу.",
        "Option 2": "`--cpu-shares` визначає відносний пріоритет: впливає на виділення CPU тільки тоді, коли система завантажена.",
        "Option 3": "`--cpus` дозволяє вказати конкретні номери ядер процесора для контейнера.",
        "Option 4": "Коли система не завантажена, контейнер з `--cpu-shares=512` може використовувати всі доступні ресурси CPU.",
        "Option 5": "",
        "Correct Answer": "1,2,4",
        "Time in seconds": "60",
        "Image Link": "",
        "Answer explanation": "`--cpus` є жорстким обмеженням — контейнер ніколи не споживатиме більше відведеної частки. Натомість `--cpu-shares` лише встановлює 'вагу' (пріоритет) для планувальника: якщо є вільні ресурси, контейнер може взяти 100% CPU, але при конкуренції між контейнерами час розподілятиметься пропорційно їхнім shares."
    },
    {
        "Question Text": "Які з перелічених тверджень є дійсними обмеженнями команди `docker cp`?",
        "Question Type": "Checkbox",
        "Option 1": "Не зберігає права доступу до файлів.",
        "Option 2": "Не ефективна для постійного (persistent) зберігання даних контейнера у порівнянні з томами.",
        "Option 3": "Не підтримує копіювання файлів з контейнера на хост-систему.",
        "Option 4": "Не працює зі зупиненими контейнерами.",
        "Option 5": "",
        "Correct Answer": "1,2",
        "Time in seconds": "60",
        "Image Link": "",
        "Answer explanation": "Команда `docker cp` копіює файли з правами за замовчуванням (не зберігає оригінальні права доступу) і не замінює томи (volumes) для постійного зберігання даних. Проте вона чудово працює зі зупиненими контейнерами і дозволяє двостороннє копіювання."
    },
    {
        "Question Text": "Поясніть, чому стан `Paused` рідко використовується у повсякденній роботі, але є важливим для оркестраторів та сценаріїв live migration.",
        "Question Type": "Open-Ended",
        "Option 1": "",
        "Option 2": "",
        "Option 3": "",
        "Option 4": "",
        "Option 5": "",
        "Correct Answer": "",
        "Time in seconds": "120",
        "Image Link": "",
        "Answer explanation": "Стан Paused миттєво заморожує процеси за допомогою cgroup freezer без втрати їхнього стану в пам'яті. Це важливо для оркестраторів (напр. Kubernetes, Swarm), щоб перенести контейнер на інший хост (live migration) без зупинки та перезапуску застосунку, зберігаючи його поточний оперативний стан."
    }
]

out_dir = "tests/07.tools/01.docker"
os.makedirs(out_dir, exist_ok=True)
json_path = "tmp_questions.json"
xlsx_path = os.path.join(out_dir, "06.container-lifecycle.xlsx")

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

subprocess.run(["python3", "wayground_exporter.py", json_path, "-o", xlsx_path])
os.remove(json_path)
print(f"Created {xlsx_path} successfully.")
