import json
import os
import subprocess

questions = [
    {
        "Question Text": "Що відбувається в пам'яті при виконанні коду `a = [1, 2, 3]` та `b = a`, а потім `b.append(4)`?",
        "Question Type": "Multiple Choice",
        "Option 1": "Створюється копія списку `a`, тому `a` залишається `[1, 2, 3]`, а `b` стає `[1, 2, 3, 4]`.",
        "Option 2": "Обидві змінні `a` та `b` посилаються на один і той самий об'єкт у купі (heap). Метод `append(4)` змінює цей об'єкт, тому обидві змінні покажуть `[1, 2, 3, 4]`.",
        "Option 3": "Виникне помилка `AttributeError`, оскільки змінні в Python є незмінними (immutable) за замовчуванням.",
        "Option 4": "Створюється глибока копія (deep copy) об'єкта, оскільки оператор `=` виконує копіювання за значенням.",
        "Option 5": "",
        "Correct Answer": "2",
        "Time in seconds": "30",
        "Image Link": "",
        "Answer explanation": "У Python змінні є посиланнями на об'єкти в пам'яті. При присвоєнні `b = a` нова змінна `b` починає посилатися на той самий список у пам'яті, що й `a`. Оскільки списки є змінними (mutable) об'єктами, модифікація списку через `b` призводить до зміни спільного об'єкта, що відображається і через `a`."
    },
    {
        "Question Text": "Дано кортеж `t = (1, 2, [3, 4])`. Що станеться при спробі виконати команду `t[2].append(5)`?",
        "Question Type": "Multiple Choice",
        "Option 1": "Виникне помилка `TypeError: 'tuple' object does not support item assignment`, тому що кортежі є незмінними.",
        "Option 2": "Операція виконається успішно, і кортеж стане `(1, 2, [3, 4, 5])`.",
        "Option 3": "Елемент `5` додасться до списку, але сам список буде скопійовано у нове місце в пам'яті.",
        "Option 4": "Кортеж буде автоматично перетворено на список (list) для виконання операції.",
        "Option 5": "",
        "Correct Answer": "2",
        "Time in seconds": "45",
        "Image Link": "",
        "Answer explanation": "Кортеж є незмінним (immutable) контейнером, тобто не можна змінити самі посилання на його елементи (наприклад, виконати `t[2] = 9`). Проте, якщо елементом кортежу є змінний об'єкт (наприклад, список), ми можемо змінювати сам цей об'єкт (наприклад, викликати `append`). Посилання у кортежі на цей список при цьому залишається незмінним."
    },
    {
        "Question Text": "Який результат виведе наступний код при послідовному виконанні?\n\n```python\ndef add_item(item, box=[]):\n    box.append(item)\n    return box\n\nprint(add_item(1))\nprint(add_item(2))\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "`[1]` та `[2]` на окремих рядках.",
        "Option 2": "`[1]` та `[1, 2]` на окремих рядках.",
        "Option 3": "`[1]` та `Error: box is not defined`.",
        "Option 4": "`[1]` та `[]` на окремих рядках.",
        "Option 5": "",
        "Correct Answer": "2",
        "Time in seconds": "45",
        "Image Link": "",
        "Answer explanation": "У Python значення за замовчуванням для аргументів функцій обчислюються один раз під час визначення (дефініції) функції, а не при кожному її виклику. Оскільки списки є змінними (mutable), спільний список `box` зберігається між викликами та накопичує елементи. Щоб уникнути цього, використовують `box=None` та ініціалізацію всередині функції: `if box is None: box = []`."
    },
    {
        "Question Text": "Що виведе наступний фрагмент коду?\n\n```python\nx = 10\ndef outer():\n    x = 20\n    def inner():\n        global x\n        x = 30\n    inner()\n    print(x)\n\nouter()\nprint(x)\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "`20` та `30` на окремих рядках.",
        "Option 2": "`30` та `30` на окремих рядках.",
        "Option 3": "`20` та `10` на окремих рядках.",
        "Option 4": "`30` та `10` на окремих рядках.",
        "Option 5": "",
        "Correct Answer": "1",
        "Time in seconds": "45",
        "Image Link": "",
        "Answer explanation": "Завдяки ключовому слову `global x` у функції `inner`, зміна `x = 30` стосується саме глобальної змінної `x` (яка спочатку дорівнювала `10` і стає `30`). У функції `outer` змінна `x = 20` є локальною для `outer` (enclosing для `inner`). Оскільки в `outer` немає декларації `global` чи `nonlocal`, її локальний `x` залишається рівним `20`. Тому `print(x)` всередині `outer` виведе `20`, а глобальний `print(x)` в кінці програми виведе `30`."
    },
    {
        "Question Text": "Які з наведених об'єктів можуть бути використані як ключі в словнику Python? (Виберіть усі правильні варіанти)",
        "Question Type": "Checkbox",
        "Option 1": "`(1, 2, 'hello')`",
        "Option 2": "`[1, 2, 3]`",
        "Option 3": "`{'key': 'value'}`",
        "Option 4": "`frozenset([1, 2, 3])`",
        "Option 5": "`(1, 2, [3, 4])`",
        "Correct Answer": "1,4",
        "Time in seconds": "45",
        "Image Link": "",
        "Answer explanation": "Ключами словника в Python можуть бути лише хешовані (hashable) об'єкти. Хешованими є незмінні типи даних (числа, рядки, кортежі, що містять лише хешовані елементи, frozenset). Змінні типи (списки, словники, звичайні множини set, а також кортежі, що містять списки чи інші змінні об'єкти) не є хешованими і викликають помилку `TypeError: unhashable type` при спробі використати їх як ключі."
    },
    {
        "Question Text": "Який словник буде створено в результаті виконання наступного коду?\n\n```python\nkeys = ['a', 'b', 'c']\nvalues = [1, 2]\nmy_dict = {k: v for k, v in zip(keys, values)}\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "`{'a': 1, 'b': 2, 'c': None}`",
        "Option 2": "`{'a': 1, 'b': 2}`",
        "Option 3": "Виникне помилка `ValueError: not enough values to unpack`, оскільки довжини списків різні.",
        "Option 4": "`{'a': 1, 'b': 2, 'c': 2}`",
        "Option 5": "",
        "Correct Answer": "2",
        "Time in seconds": "30",
        "Image Link": "",
        "Answer explanation": "Функція `zip()` об'єднує елементи ітерованих об'єктів у кортежі. Якщо вхідні послідовності мають різну довжину, `zip()` зупиняє роботу, коли завершується найкоротша послідовність (в Python 3). Тому елемент `'c'` буде проігнорований, і генератор словника створить `{'a': 1, 'b': 2}`."
    },
    {
        "Question Text": "Які з наведених тверджень описують обмеження анонімних (лямбда) функцій в Python? (Виберіть усі правильні варіанти)",
        "Question Type": "Checkbox",
        "Option 1": "Лямбда-функції можуть містити лише один вираз (expression), результат якого автоматично повертається.",
        "Option 2": "У тілі лямбда-функцій не можна використовувати багаторядкові інструкції, такі як `if-elif-else` (дозволено лише тернарний оператор) або цикли `for`/`while`.",
        "Option 3": "Лямбда-функції не підтримують передачу аргументів за замовчуванням.",
        "Option 4": "У лямбда-функціях неможливо використовувати анотації типів (type hinting) для аргументів та результату.",
        "Option 5": "Лямбда-функції не можуть бути передані як аргументи в інші функції (наприклад, в `map` чи `filter`).",
        "Correct Answer": "1,2,4",
        "Time in seconds": "60",
        "Image Link": "",
        "Answer explanation": "Лямбда-функції в Python обмежені синтаксично: вони можуть містити лише один вираз, не підтримують присвоєння змінних (`=`), інструкції розгалуження та циклів (крім тернарного оператора), а також не підтримують анотації типів. Проте вони підтримують аргументи за замовчуванням (наприклад, `lambda x=1: x`), і їх зазвичай передають як аргументи в інші функції (наприклад, як ключ сортування `key=lambda x: x[1]`)."
    },
    {
        "Question Text": "У чому полягає ключова різниця між `x = [i**2 for i in range(10**6)]` та `y = (i**2 for i in range(10**6))`?",
        "Question Type": "Multiple Choice",
        "Option 1": "`x` створює генератор, який обчислює значення ліниво, а `y` створює кортеж у пам'яті.",
        "Option 2": "`x` є списком, який повністю створюється та завантажується в оперативну пам'ять, тоді як `y` є генератором, що повертає елементи по одному за запитом (ліниві обчислення) та майже не займає пам'яті.",
        "Option 3": "Немає жодної різниці в споживанні пам'яті чи швидкості, це просто альтернативні синтаксиси для створення списків.",
        "Option 4": "`y` виконується набагато повільніше при першому зверненні, оскільки автоматично компілюється в C-код.",
        "Option 5": "",
        "Correct Answer": "2",
        "Time in seconds": "45",
        "Image Link": "",
        "Answer explanation": "Квадратні дужки `[...]` створюють генератор списку (list comprehension), який відразу обчислює всі елементи та зберігає їх у пам'яті. Круглі дужки `(...)` створюють генераторний вираз (generator expression), який повертає об'єкт-генератор. Він не обчислює значення наперед, а генерує їх 'ліниво' (lazy evaluation) за допомогою протоколу ітерації, що суттєво економить пам'ять при роботі з великими послідовностями."
    },
    {
        "Question Text": "Що виведе наступний код?\n\n```python\ndef my_gen():\n    yield 1\n    print(\"Step A\")\n    yield 2\n    print(\"Step B\")\n\ng = my_gen()\nprint(next(g))\nprint(next(g))\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "`1` та `Step A` та `2` на окремих рядках.",
        "Option 2": "`1` та `Step A` та `2` та `Step B` на окремих рядках.",
        "Option 3": "`Step A` та `1` та `Step B` та `2` на окремих рядках.",
        "Option 4": "`1` та `2` та `Step A` на окремих рядках.",
        "Option 5": "",
        "Correct Answer": "1",
        "Time in seconds": "45",
        "Image Link": "",
        "Answer explanation": "Перший виклик `next(g)` запускає генератор, який виконується до першого `yield 1` і повертає `1`, призупиняючи свій стан. Другий виклик `next(g)` відновлює роботу генератора з місця зупинки: виконується `print(\"Step A\")`, потім генератор доходить до `yield 2`, повертає `2` і знову призупиняється. Інструкція `print(\"Step B\")` виконається лише при наступному виклику `next(g)`, який також викине виняток `StopIteration`."
    },
    {
        "Question Text": "Яке ключове слово використовується в Python для оголошення того, що змінна у внутрішній функції відноситься до області видимості найближчої зовнішньої (але не глобальної) функції?",
        "Question Type": "Fill-in-the-Blank",
        "Option 1": "nonlocal",
        "Option 2": "",
        "Option 3": "",
        "Option 4": "",
        "Option 5": "",
        "Correct Answer": "",
        "Time in seconds": "30",
        "Image Link": "",
        "Answer explanation": "Ключове слово `nonlocal` використовується для вказівки інтерпретатору, що змінна належить до області видимості найближчої зовнішньої функції (enclosing scope), яка не є глобальною. Це дозволяє модифікувати таку змінну всередині вкладеної функції (наприклад, для реалізації замикань)."
    },
    {
        "Question Text": "Що виведе цей код?\n\n```python\ndef counter(start):\n    count = start\n    def increment():\n        nonlocal count\n        count += 1\n        return count\n    return increment\n\nc1 = counter(5)\nc2 = counter(10)\nprint(c1())\nprint(c2())\nprint(c1())\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "`6`, `11` та `7` на окремих рядках.",
        "Option 2": "`6`, `11` та `12` на окремих рядках.",
        "Option 3": "`6`, `7` та `8` на окремих рядках.",
        "Option 4": "`6`, `11` та `6` на окремих рядках.",
        "Option 5": "",
        "Correct Answer": "1",
        "Time in seconds": "45",
        "Image Link": "",
        "Answer explanation": "Замикання (closure) — це внутрішня функция, яка зберігає посилання на змінні зі своєї лексичної області видимості (enclosing scope) навіть після того, як зовнішня функція завершила роботу. Кожен виклик `counter` створює нову незалежну область видимості. Тому `c1` та `c2` мають свої власні екземпляри змінної `count`. Перший виклик `c1()` збільшує його `count` з 5 до 6, виклик `c2()` збільшує його `count` з 10 до 11, а наступний виклик `c1()` збільшує перший `count` з 6 до 7."
    },
    {
        "Question Text": "Що виведе наступний код і чому?\n\n```python\nfuncs = []\nfor i in range(3):\n    funcs.append(lambda: i)\n\nprint([f() for f in funcs])\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "`[0, 1, 2]`",
        "Option 2": "`[2, 2, 2]`",
        "Option 3": "`[0, 0, 0]`",
        "Option 4": "Виникне помилка `NameError: free variable 'i' is referenced before assignment`.",
        "Option 5": "",
        "Correct Answer": "2",
        "Time in seconds": "45",
        "Image Link": "",
        "Answer explanation": "Це класична проблема пізнього зв'язування (late binding) в замиканнях. Змінні, що використовуються в замиканнях, шукаються в момент виклику функції, а не в момент її створення. На момент виклику `f()` цикл вже заверсився, і змінна `i` дорівнює `2`. Оскільки всі лямбда-функції замикаються на одну й ту саму змінну `i`, вони всі повертають `2`. Щоб виправити це, можна передавати `i` як аргумент за замовчуванням: `lambda val=i: val`."
    },
    {
        "Question Text": "Яким буде вивід наступного коду?\n\n```python\ndef display(a, b, *args, **kwargs):\n    print(a, b, args, kwargs)\n\ndisplay(1, 2, 3, 4, x=5, y=6)\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "`1 2 (3, 4) {'x': 5, 'y': 6}`",
        "Option 2": "`1 2 [3, 4] {'x': 5, 'y': 6}`",
        "Option 3": "`1 2 (3, 4) [('x', 5), ('y', 6)]`",
        "Option 4": "Помилка `TypeError: display() takes 2 positional arguments but 4 were given`.",
        "Option 5": "",
        "Correct Answer": "1",
        "Time in seconds": "30",
        "Image Link": "",
        "Answer explanation": "Параметри `1` та `2` присвоюються позиційним аргументам `a` та `b`. Всі наступні позиційні аргументи (`3, 4`) збираються оператором `*args` у кортеж (tuple). Всі іменовані аргументи (`x=5, y=6`) збираються оператором `**kwargs` у словник (dict)."
    },
    {
        "Question Text": "Що виведе наступний код?\n\n```python\ndef echo_gen():\n    val = yield \"Start\"\n    yield f\"Received: {val}\"\n\ng = echo_gen()\nprint(next(g))\nprint(g.send(\"Hello\"))\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "`Start` та `Received: Hello` на окремих рядках.",
        "Option 2": "`Hello` та `Received: Start` на окремих рядках.",
        "Option 3": "`Start` та `Received: None` на окремих рядках.",
        "Option 4": "Виникне помилка `TypeError: can't send non-None value to a just-started generator`.",
        "Option 5": "",
        "Correct Answer": "1",
        "Time in seconds": "60",
        "Image Link": "",
        "Answer explanation": "Перший виклик `next(g)` (або `g.send(None)`) запускає генератор і доходить до першого `yield \"Start\"`, повертаючи рядок `\"Start\"`. Наступний виклик `g.send(\"Hello\")` відновлює виконання генератора та присвоює надіслане значення `\"Hello\"` змінній `val`. Потім виконання продовжується до другого `yield f\"Received: {val}\"`, який повертає `\"Received: Hello\"`."
    },
    {
        "Question Text": "Що відбудеться у словнику `d = {}` при виконанні наступного коду, якщо відомо, що `hash(1) == hash(1.0)` та `1 == 1.0`?\n\n```python\nd[1] = \"integer\"\nd[1.0] = \"float\"\nprint(d)\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "`{1: 'integer', 1.0: 'float'}` — словник міститиме два окремі ключі, оскільки типи даних різні.",
        "Option 2": "`{1: 'float'}` — оскільки хеш-код та значення ключів рівні, ключ `1` буде перезаписаний новим значенням, а сам ключ збереже свій початковий тип (int).",
        "Option 3": "`{1.0: 'float'}` — ключ `1` буде повністю замінений ключем `1.0`.",
        "Option 4": "Виникне помилка `KeyError: duplicate key hash`.",
        "Option 5": "",
        "Correct Answer": "2",
        "Time in seconds": "45",
        "Image Link": "",
        "Answer explanation": "В Python два об'єкти вважаються однаковими ключами в словнику, якщо вони рівні (`==`) та мають однакове значення хешу (`hash()`). Оскільки `1 == 1.0` є істиною, і їхні хеш-коди збігаються, словник розглядає їх як один і той самий ключ. При виконанні `d[1.0] = \"float\"` значення перезаписується, але оскільки ключ вже існував (тип int `1`), тип самого ключа в структурі не змінюється. Тому виведеться `{1: 'float'}`."
    },
    {
        "Question Text": "Опишіть, як працює автоматичне закриття генератора при виході з циклу `for` за допомогою винятку `GeneratorExit`. Що станеться, якщо всередині генератора перехопити цей виняток у блоці `try...except GeneratorExit` та спробувати виконати ще один `yield`?",
        "Question Type": "Open-Ended",
        "Option 1": "",
        "Option 2": "",
        "Option 3": "",
        "Option 4": "",
        "Option 5": "",
        "Correct Answer": "",
        "Time in seconds": "120",
        "Image Link": "",
        "Answer explanation": "Коли генератор збирається сміттям (garbage collected) або закривається примусово через метод `close()` (що також відбувається під капотом при виході з циклу `for` раніше завершення ітерації), в нього кидається виняток `GeneratorExit`.    Генератор може перехопити його, наприклад, для очищення ресурсів (закриття відкритих файлів чи мережевих з'єднань). Проте, якщо після перехоплення `GeneratorExit` генератор спробує виконати ще одну інструкцію `yield`, інтерпретатор Python викине виняток `RuntimeError: generator ignored GeneratorExit`. Генератор має або просто вийти (виконати return), або прокинути цей виняток далі."
    }
]

out_dir = "tests/05.python"
os.makedirs(out_dir, exist_ok=True)
json_path = "tmp_questions.json"
xlsx_path = os.path.join(out_dir, "01.basics-functions-generators-closures.xlsx")

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

subprocess.run(["python3", "wayground_exporter.py", json_path, "-o", xlsx_path])
os.remove(json_path)
print(f"Created {xlsx_path} successfully.")
