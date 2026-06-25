#!/usr/bin/env python3
"""Insert git-workflow and mypy/Pyright sections."""

FILE = "content/05.python/00.modules-packages-venv.md"

with open(FILE, "rb") as f:
    raw = f.read()

content = raw.decode("utf-8", errors="replace")

# ─── 1. Git workflow section ─────────────────────────────────────────────────
# Insert before "### Порівняльна таблиця:"

GIT_SECTION = """\
### Робота з `git`: що робити після `git clone`?

Один із найпоширеніших питань початківців: *«Я склонував репозиторій. Що далі?»*. Відповідь залежить від того, яким менеджером пакетів користується проект.

#### Як розпізнати менеджер пакетів проекту

Першим ділом — подивіться на файли у корені репозиторію:

::field-group

::field{name="uv.lock + pyproject.toml" type="Проект на uv"}
Є обидва файли — це `uv`-проект. Команда для старту: `uv sync`.
```
my-project/
├── pyproject.toml   ← залежності та метадані
├── uv.lock          ← детермінований lockfile
├── .python-version  ← зафіксована версія Python
└── src/
```
::

::field{name="poetry.lock + pyproject.toml" type="Проект на Poetry"}
Є `poetry.lock` — це Poetry-проект. Команда для старту: `poetry install`.
```
my-project/
├── pyproject.toml   ← залежності та метадані
├── poetry.lock      ← детермінований lockfile
└── src/
```
::

::field{name="requirements.txt" type="Класичний pip-проект"}
Тільки `requirements.txt` — класичний підхід. Команда для старту: `pip install -r requirements.txt`.
```
my-project/
├── requirements.txt ← список залежностей
└── app.py
```
::

::

#### Флоу після `git clone` — `uv`-проект

::steps

### Клонувати та перейти у директорію

```bash
git clone https://github.com/org/my-project.git
cd my-project
```

### Перевірити версію Python (опційно)

`uv` прочитає `.python-version` автоматично. Якщо потрібна версія відсутня — `uv` завантажить її сам:

```bash
cat .python-version  # наприклад: 3.12
uv python list       # перевірити що встановлено
```

### Синхронізувати середовище

Одна команда — і все готово. `uv` сам створить `.venv/` і встановить точні версії з `uv.lock`:

```bash
uv sync
```

::terminal-preview{title="uv sync після git clone"}

<div class="line"><span class="opacity-40">$</span> <strong>uv sync</strong></div>
<div class="line">Using CPython 3.12.8 interpreter at: /Users/user/.local/share/uv/python/...</div>
<div class="line">Creating virtual environment at: .venv</div>
<div class="line">Resolved <span class="text-blue-400">42</span> packages in <span class="text-green-400">183ms</span></div>
<div class="line">Installed <span class="text-blue-400">42</span> packages in <span class="text-green-400">1.2s</span></div>
<div class="line"> + fastapi==0.115.6</div>
<div class="line"> + sqlalchemy==2.0.36</div>
<div class="line"> + ... та інші</div>
<div class="line"><span class="text-green-400">All dependencies are satisfied.</span></div>

::

### Запустити проект

```bash
uv run python main.py          # скрипт
uv run uvicorn app:app --reload  # FastAPI
uv run pytest                  # тести
```

::

::note
Ніякого `source .venv/bin/activate` — `uv run` все робить сам. Але якщо хочете активувати середовище явно для IDE або оболонки: `source .venv/bin/activate`.
::

#### Флоу після `git clone` — Poetry-проект

::steps

### Клонувати та перейти у директорію

```bash
git clone https://github.com/org/my-project.git
cd my-project
```

### Перевірити налаштування Poetry (один раз)

```bash
# Рекомендовано: зберігати venv всередині проекту
poetry config virtualenvs.in-project true
```

### Встановити залежності

Poetry прочитає `poetry.lock` і встановить точні версії:

```bash
poetry install
```

::terminal-preview{title="poetry install після git clone"}

<div class="line"><span class="opacity-40">$</span> <strong>poetry install</strong></div>
<div class="line">Installing dependencies from lock file</div>
<div class="line"></div>
<div class="line">Package operations: <span class="text-blue-400">38</span> installs, <span class="text-yellow-400">0</span> updates, <span class="text-rose-400">0</span> removals</div>
<div class="line">  • Installing annotated-types (0.7.0)</div>
<div class="line">  • <span class="text-green-400">Installing fastapi (0.115.6)</span></div>
<div class="line">  • Installing pydantic (2.10.3)</div>
<div class="line">  • Installing sqlalchemy (2.0.36)</div>
<div class="line">  • ...</div>
<div class="line"></div>
<div class="line">Installing the current project: <span class="text-green-400">my-project (0.1.0)</span></div>

::

### Запустити проект

```bash
poetry run python main.py
poetry run uvicorn app:app --reload
poetry run pytest
```

::

#### Що комітити у `git`? Таблиця

Правило просте: **lockfile завжди комітити**, `.venv` — **ніколи**.

| Файл | Комітити? | Причина |
|---|---|---|
| `pyproject.toml` | ✅ Так | Метадані та прямі залежності проекту |
| `uv.lock` | ✅ Так | Детермінований lockfile для відтворення |
| `poetry.lock` | ✅ Так | Детермінований lockfile для відтворення |
| `requirements.txt` | ✅ Так | Якщо проект класичний pip |
| `.python-version` | ✅ Так | Фіксує версію Python для команди |
| `.venv/` | ❌ Ні | Велика, специфічна для ОС — у `.gitignore` |
| `__pycache__/` | ❌ Ні | Кеш байткоду — у `.gitignore` |
| `*.pyc` | ❌ Ні | Компільований байткод — у `.gitignore` |
| `.env` | ❌ Ні | Секрети та конфіги — у `.gitignore` |

#### Стандартний `.gitignore` для Python-проекту

```gitignore
# Віртуальні середовища
.venv/
venv/
env/

# Байткод та кеш
__pycache__/
*.py[cod]
*$py.class
*.pyo

# Артефакти збірки
dist/
build/
*.egg-info/
*.egg

# Тести та покриття
.pytest_cache/
.coverage
htmlcov/

# Типи та лінтери
.mypy_cache/
.ruff_cache/

# Середовище та секрети
.env
.env.local
*.env

# IDE
.idea/
.vscode/
*.swp
```

---

"""

# ─── 2. mypy / Pyright section ──────────────────────────────────────────────
# Insert before "### Порівняльна таблиця:"

MYPY_SECTION = """\
### Статичний аналіз типів: `mypy` та `Pyright`

Python — мова з **динамічною** типізацією: типи перевіряються під час виконання. Але з Python 3.5+ з'явилися **анотації типів** (`def foo(x: int) -> str:`), і на цій основі побудовані **статичні аналізатори** — інструменти, що знаходять помилки типів *до* запуску програми.

::card-group

::card{title="mypy" icon="i-heroicons-check-badge"}
Офіційний статичний аналізатор від команди Python. Написаний на Python. Стандарт для більшості проектів, широко підтримується в CI/CD та IDE.
::

::card{title="Pyright" icon="i-heroicons-bolt"}
Написаний на TypeScript (!) від Microsoft. Значно швидший за mypy. Є основою для type-checking у Pylance (VSCode). Також доступний як CLI — `pyright`.
::

::

#### Навіщо потрібен статичний аналіз типів?

```python
# Без анотацій — помилка знайдеться лише під час виконання
def get_user_age(user):
    return user["age"] + 1  # KeyError? TypeError? Дізнаємось пізно

# З анотаціями — mypy/Pyright знаходять помилки відразу
from typing import TypedDict

class User(TypedDict):
    name: str
    age: int

def get_user_age(user: User) -> int:
    return user["age"] + 1  # mypy: OK
    # return user["nme"] + 1  # mypy: ERROR — key "nme" не існує у User
```

#### `mypy` — встановлення та базове використання

```bash
# Встановлення
uv add --dev mypy
# або
pip install mypy

# Запуск для файлу
mypy main.py

# Запуск для всього проекту
mypy .

# Перевірка конкретного пакету
mypy my_package/
```

::terminal-preview{title="mypy — знаходження помилок типів"}

<div class="line"><span class="opacity-40">$</span> <strong>mypy main.py</strong></div>
<div class="line">main.py:<span class="text-yellow-400">12</span>: error: Argument 1 to "add" has incompatible type <span class="text-rose-400">"str"</span>; expected <span class="text-green-400">"int"</span>  [arg-type]</div>
<div class="line">main.py:<span class="text-yellow-400">18</span>: error: Item <span class="text-rose-400">"None"</span> of "Optional[str]" has no attribute "upper"  [union-attr]</div>
<div class="line">main.py:<span class="text-yellow-400">25</span>: error: Return type declared as <span class="text-green-400">"int"</span>, actual return type <span class="text-rose-400">"str"</span>  [return-value]</div>
<div class="line">Found <span class="text-rose-400">3 errors</span> in 1 file (checked 1 source file)</div>

::

#### Конфігурація `mypy` у `pyproject.toml`

```toml
[tool.mypy]
python_version = "3.12"
strict = true              # найсуворіший режим — рекомендовано для нових проектів

# Що перевіряти
check_untyped_defs = true  # перевіряти навіть нетиповані функції
disallow_untyped_defs = true  # вимагати анотацій для всіх функцій
disallow_any_generics = true  # заборонити голі Generic (list замість list[str])
warn_return_any = true     # попереджати про return Any

# Що ігнорувати
ignore_missing_imports = true  # якщо бібліотека не має стабів

# Виключення конкретних модулів
[[tool.mypy.overrides]]
module = ["tests.*"]
disallow_untyped_defs = false  # у тестах дозволяємо без анотацій
```

#### Практичний приклад: типовані структури даних

```python
from typing import Optional, Union
from collections.abc import Sequence

# TypedDict — словник зі строгою структурою
from typing import TypedDict

class Address(TypedDict):
    street: str
    city: str
    postal_code: str

class UserProfile(TypedDict, total=False):  # total=False — всі поля необов'язкові
    bio: str
    avatar_url: str

class User(TypedDict):
    id: int
    name: str
    email: str
    address: Address
    profile: UserProfile  # вкладений TypedDict

# Функція з повними анотаціями
def find_users_by_city(
    users: Sequence[User],
    city: str,
    limit: Optional[int] = None,
) -> list[User]:
    """Знаходить користувачів із зазначеного міста."""
    result = [u for u in users if u["address"]["city"] == city]
    if limit is not None:
        result = result[:limit]
    return result

# mypy перевірить:
# - що users є Sequence[User]
# - що city є str
# - що limit є Optional[int] (може бути None)
# - що функція повертає list[User]
```

#### `Pyright` — швидший альтернативний аналізатор

```bash
# Встановлення через uv
uv add --dev pyright
# або глобально
uvx pyright --version

# Запуск
pyright .
pyright main.py --pythonversion 3.12
```

::terminal-preview{title="pyright — аналіз типів"}

<div class="line"><span class="opacity-40">$</span> <strong>pyright .</strong></div>
<div class="line">Loading configuration file at /Users/user/my-project/pyrightconfig.json</div>
<div class="line">pyright 1.1.391</div>
<div class="line"></div>
<div class="line">/<span class="text-blue-400">my_project/service.py</span></div>
<div class="line">  /<span class="text-blue-400">my_project/service.py</span>:<span class="text-yellow-400">34</span>:<span class="text-yellow-400">16</span> - error: Expression of type <span class="text-rose-400">"str | None"</span> cannot be assigned to declared type <span class="text-green-400">"str"</span> (reportAssignmentType)</div>
<div class="line">  /<span class="text-blue-400">my_project/service.py</span>:<span class="text-yellow-400">51</span>:<span class="text-yellow-400">9</span> - error: Argument of type <span class="text-rose-400">"int"</span> cannot be assigned to parameter <span class="text-green-400">"name"</span> of type <span class="text-rose-400">"str"</span> (reportArgumentType)</div>
<div class="line"></div>
<div class="line"><span class="text-blue-400">2 errors</span>, 0 warnings, 0 informations</div>
<div class="line">Completed in <span class="text-green-400">0.43s</span></div>

::

#### Конфігурація Pyright — `pyrightconfig.json`

```json
{
  "pythonVersion": "3.12",
  "venvPath": ".",
  "venv": ".venv",
  "typeCheckingMode": "strict",
  "include": ["src", "tests"],
  "exclude": ["**/__pycache__"],
  "reportMissingImports": true,
  "reportMissingTypeStubs": false,
  "reportUnknownVariableType": false
}
```

Або у `pyproject.toml`:

```toml
[tool.pyright]
pythonVersion = "3.12"
venvPath = "."
venv = ".venv"
typeCheckingMode = "strict"
include = ["src"]
exclude = ["**/__pycache__"]
```

#### Порівняння mypy vs Pyright

| Характеристика | mypy | Pyright |
|---|---|---|
| **Мова реалізації** | Python | TypeScript |
| **Швидкість** | ⚠️ Повільніший на великих проектах | ⚡ Значно швидший, інкрементальний |
| **Строгість** | ✅ Налаштовувана | ✅ Налаштовувана |
| **IDE-інтеграція** | PyCharm, VSCode (mypy extension) | VSCode (Pylance базується на Pyright) |
| **Підтримка стандартів** | ✅ PEP 484, 526, 544... | ✅ PEP 484, 526, 544... |
| **Plugins** | ✅ Є (Django, SQLAlchemy) | ⚠️ Менше plugins |
| **CI/CD** | ✅ Стандарт де-факто | ✅ Зростає |
| **Рекомендація** | Зрілі проекти, Django, MLops | FastAPI, нові проекти, VSCode-workflow |

::tip
**FastAPI** офіційно рекомендує Pyright (через Pylance у VSCode). **Django** та більшість MLops-інструментів — mypy з відповідними plugin-ами (`django-stubs`, `sqlalchemy-stubs`).
::

#### Інтеграція у workflow з `uv`

```bash
# Додавання аналізаторів у dev-залежності
uv add --dev mypy pyright

# Запуск у CI/CD або pre-commit
uv run mypy .
uv run pyright .

# Часто використовують разом з ruff (лінтер)
uv add --dev ruff
uv run ruff check .
uv run ruff format .
```

#### `pyproject.toml` — повна конфігурація типового проекту

```toml
[project]
name = "my-service"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["fastapi>=0.115", "sqlalchemy>=2.0"]

[dependency-groups]
dev = ["mypy>=1.13", "pyright>=1.1", "ruff>=0.8", "pytest>=8.0"]

[tool.mypy]
python_version = "3.12"
strict = true
ignore_missing_imports = true

[tool.pyright]
pythonVersion = "3.12"
typeCheckingMode = "basic"
venvPath = "."
venv = ".venv"

[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]
```

---

"""

# ─── Insert git section before "### Порівняльна таблиця:" ────────────────────

GIT_ANCHOR = "\n### Порівняльна таблиця: `venv`+`pip` vs `uv` vs `Poetry`"
if GIT_ANCHOR in content:
    content = content.replace(GIT_ANCHOR, "\n" + GIT_SECTION + GIT_ANCHOR[1:], 1)
    print("Git workflow section inserted")
else:
    print("ERROR: Git anchor not found")

# ─── Insert mypy section right before the comparison table ───────────────────

MYPY_ANCHOR = "\n### Порівняльна таблиця: `venv`+`pip` vs `uv` vs `Poetry`"
if MYPY_ANCHOR in content:
    content = content.replace(MYPY_ANCHOR, "\n" + MYPY_SECTION + MYPY_ANCHOR[1:], 1)
    print("mypy/Pyright section inserted")
else:
    print("ERROR: mypy anchor not found")

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print("File saved OK")
