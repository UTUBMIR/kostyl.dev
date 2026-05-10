# Робота з зображеннями та діаграмами

## 1. Команди та Workflow
Використовуйте два скрипти для автоматизації: `fetch_images.py` (пошук/завантаження) та `insert_images.py` (вставка у файл).

```bash
# 1. Пошук та завантаження (ліміт -l, інтерактивно -i)
python scripts/fetch_images.py "query description" --md content/path/article.md -l 1 -i

# 2. Вставка у markdown замість маркерів <!-- IMAGE: desc -->
python scripts/insert_images.py content/path/article.md
```

## 2. Ключові Правила
- **Авто-шлях**: Папка для зображень визначається за шляхом до `.md` файлу (без числових префіксів). 
  - `content/07.tools/02.kubernetes/01.why.md` → `public/images/tools/kubernetes/why/`
- **Нумерація**: Файли іменуються `01.png`, `02.svg`, ... відповідно до порядку маркерів.
- **Якість**: Пріоритет форматам: **SVG** > **PNG** > WebP. Мінімальна ширина: 800px.
- **Джерела**: Пріоритет офіційним докам (k8s.io, docker.com) та тех-блогам (medium, digitalocean).

## 3. КРИТИЧНЕ ПРАВИЛО: Image + PlantUML
Кожна технічна ілюстрація (архітектура, схема, потоки даних) **ОБОВ'ЯЗКОВО** супроводжується PlantUML-діаграмою безпосередньо під зображенням для забезпечення редагованості та доступності.

- **Світлий фон**: Усі PlantUML-діаграми обов'язково повинні мати білий/світлий задній фон (`skinparam backgroundColor #ffffff`) для забезпечення високої контрастності та зручності читання незалежно від поточної теми сайту (світлої чи темної).

```markdown
![alt text](/images/path/01.png){.diagram-img}

::plant-uml
@startuml
skinparam style plain
skinparam backgroundColor #ffffff
...
@enduml
::
```

## 4. Підготовка контенту
Додавайте маркери `<!-- IMAGE: опис зображення -->` у місця вставки. Текст після `IMAGE:` стане `alt`-текстом зображення.

## 5. Залежності
`pip install ddgs requests pillow`.
