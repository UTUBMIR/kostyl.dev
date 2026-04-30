# Серія статей: Патерни доступу до даних з JDBC та H2

## Мета

Створити цикл із **7 глибоких, академічних статей** (`09`–`15`) у `content/04.java/pr2/`, що проведе читача від наївного JDBC-коду до рефлексійного `GenericRepository`. Наскрізний приклад — **платформа аудіокниг** (та ж схема з `ddl_h2.sql`). Стиль — як у `01.data-mapper-part1.md` / `02.data-mapper-part2.md`, але сховище — H2/JDBC замість JSON/GSON.

> [!IMPORTANT]
> - Академічний, книжковий стиль згідно з `prompt.md`
> - Кожна стаття ~1000–1200 рядків Markdown
> - Суворе дотримання Docus-компонентів із `DOCUS_COMPONENTS.md`
> - **Рефлексія з'являється ТІЛЬКИ в останній статті (15)**
> - Еволюційний підхід: кожна стаття показує проблему попереднього рішення → нове рішення

---

## Структура модуля (7 статей)

### Стаття 09. JDBC Fundamentals: Наївний підхід до персистентності

**Файл:** `content/04.java/pr2/09.jdbc-fundamentals.md`

#### Зміст

1. **Вступ: Від SQL до Java** (~100 рядків)
   - Hook: "Ми спроектували схему, написали DDL, запустили міграції. Тепер потрібно зв'язати Java-об'єкти з таблицями. Найпростіший спосіб — JDBC."
   - Що таке JDBC (Java Database Connectivity) — стандарт JDK для роботи з БД
   - Чому JDBC — фундамент, на якому побудовано Hibernate, MyBatis, jOOQ

2. **Архітектура JDBC** (~150 рядків)
   - `DriverManager` → `Connection` → `Statement`/`PreparedStatement` → `ResultSet`
   - `::mermaid` — послідовна діаграма JDBC workflow
   - `DataSource` як альтернатива `DriverManager` (Connection Pool)
   - H2: підключення через `jdbc:h2:./data/audiobook_db;MODE=PostgreSQL`

3. **Перший CRUD: Наївний підхід** (~300 рядків)
   - Клас `AuthorNaiveDao` — весь SQL прямо в методах, створення Connection в кожному методі
   - `findById()`, `findAll()`, `save()`, `update()`, `delete()`
   - Маппінг `ResultSet` → `Author` вручну
   - Повний приклад із `main()` та демонстрацією роботи
   - `::terminal-preview` — результат виконання

4. **Проблеми наївного підходу** (~200 рядків)
   - SQL-ін'єкції через `Statement` → перехід до `PreparedStatement`
   - Витік ресурсів: `Connection`, `Statement`, `ResultSet` не закриваються → try-with-resources
   - Дублювання коду маппінгу
   - Відсутність транзакцій
   - `::warning` — "Кожна з цих проблем — це реальний баг у production"

5. **Виправлений варіант** (~200 рядків)
   - `PreparedStatement` замість `Statement`
   - try-with-resources
   - `ConnectionManager` — централізоване управління з'єднаннями
   - `::tabs` — "До" vs "Після" для кожного виправлення

6. **Підсумки та завдання** (~80 рядків)
   - Рівень 1: Написати `GenreNaiveDao`
   - Рівень 2: Додати пошук за ім'ям автора
   - Рівень 3: Реалізувати `UserDao` з обробкою nullable полів

---

### Стаття 10. Row Data Gateway: Інкапсуляція рядка таблиці

**Файл:** `content/04.java/pr2/10.row-data-gateway.md`

#### Зміст

1. **Вступ: Проблема розсипаного маппінгу** (~100 рядків)
   - Hook: "У наївному підході код маппінгу `ResultSet → Object` повторюється в кожному методі. А що, якщо об'єкт сам знатиме, як себе зберегти?"
   - Martin Fowler, P of EAA: Row Data Gateway

2. **Концепція Row Data Gateway** (~120 рядків)
   - Визначення: об'єкт-обгортка над одним рядком таблиці, що містить getter/setter + методи збереження
   - `::mermaid` — класова діаграма: `AuthorGateway` з полями + `insert()`, `update()`, `delete()`, `static findById()`
   - Відмінність від Active Record: Gateway не містить бізнес-логіки
   - Цитата Фаулера

3. **Реалізація для Author** (~250 рядків)
   - `AuthorGateway` — поля, конструктори, `insert()`, `update()`, `delete()`
   - Статичні Finder-методи: `findById()`, `findAll()`
   - Код Anatomy для кожного методу

4. **Реалізація для Genre** (~150 рядків)
   - `GenreGateway` — аналогічно, але з `UNIQUE` constraint

5. **Проблеми Row Data Gateway** (~100 рядків)
   - Доменний об'єкт = Gateway → порушення SRP
   - Не масштабується для складних зв'язків (Audiobook з Author + Genre)
   - Тісне зв'язування з SQL
   - `::warning` — "Row Data Gateway підходить для простих CRUD, але для складних доменів потрібен інший підхід"

6. **Підсумки та завдання** (~80 рядків)

---

### Стаття 11. Table Data Gateway: Виділення окремого шару доступу

**Файл:** `content/04.java/pr2/11.table-data-gateway.md`

#### Зміст

1. **Вступ: Від Row до Table** (~100 рядків)
   - Hook: "Row Data Gateway змішує дані та SQL в одному об'єкті. Що, якщо виділити SQL в окремий клас — по одному на таблицю?"
   - Martin Fowler: Table Data Gateway

2. **Концепція Table Data Gateway** (~120 рядків)
   - Визначення: один клас = один фасад до однієї таблиці
   - `::mermaid` — порівняння: Row Data Gateway vs Table Data Gateway
   - Доменна модель окремо від Gateway

3. **Доменна модель (Entity classes)** (~150 рядків)
   - `Author`, `Genre`, `User` — чисті POJO/Record без SQL-залежностей
   - Два конструктори: для створення нових + для відновлення зі сховища
   - `equals()`/`hashCode()` за `id`

4. **Реалізація AuthorTableGateway** (~200 рядків)
   - `findById()`, `findAll()`, `save()`, `update()`, `deleteById()`
   - Приватний метод `mapRow(ResultSet rs)` — маппінг в одному місці
   - Використання `ConnectionManager`

5. **Реалізація AudiobookTableGateway** (~200 рядків)
   - Демонстрація проблеми зв'язків: `author_id` → як отримати `Author`?
   - Варіант 1: повертати `Audiobook` з `authorId` (UUID) — без об'єкта
   - Варіант 2: робити JOIN і маппити Author всередині — зв'язування Gateway'їв
   - `::tabs` — порівняння двох варіантів

6. **Проблеми Table Data Gateway** (~100 рядків)
   - Дублювання SQL у кожному Gateway
   - Проблема зв'язків залишається
   - Немає абстракції — клієнт залежить від конкретного Gateway

7. **Підсумки та завдання** (~80 рядків)

---

### Стаття 12. Repository + Data Mapper: Правильна архітектура з JDBC

**Файл:** `content/04.java/pr2/12.repository-data-mapper-jdbc.md`

#### Зміст

1. **Вступ: Еволюція до правильної архітектури** (~100 рядків)
   - Hook: "Ми пройшли від наївного JDBC через Row і Table Data Gateway. Кожен підхід мав свої обмеження. Тепер ми готові до патерну, який став індустріальним стандартом."
   - Посилання на `01.data-mapper-part1.md` — "Ми вже знаємо цей патерн із JSON. Тепер застосуємо його до JDBC."

2. **Архітектура рішення** (~120 рядків)
   - `::mermaid` — шарова архітектура: Domain → Repository Interface → JDBC Repository Implementation
   - Інтерфейс `Repository<T, ID>` (той самий, що в частині 1)
   - Специфічні інтерфейси: `AuthorRepository`, `GenreRepository`, `AudiobookRepository`

3. **Базовий абстрактний JdbcRepository** (~250 рядків)
   - `AbstractJdbcRepository<T, ID>` — спільна логіка JDBC
   - Абстрактні методи: `mapRow(ResultSet)`, `getTableName()`, `getInsertSql()`, `getUpdateSql()`, `setInsertParams()`, `setUpdateParams()`
   - Реалізація `findById()`, `findAll()`, `deleteById()`, `count()`, `existsById()`
   - ConnectionManager як залежність

4. **Конкретна реалізація JdbcAuthorRepository** (~200 рядків)
   - Реалізація абстрактних методів
   - Специфічні методи: `findByLastName()`, `findByFullName()`
   - Повний Code Anatomy

5. **Конкретна реалізація JdbcGenreRepository** (~150 рядків)
   - `findByName()` з UNIQUE constraint

6. **JdbcAudiobookRepository зі зв'язками** (~200 рядків)
   - JOIN-запити для завантаження Author та Genre
   - Маппінг складних об'єктів: `Audiobook` з вкладеними `Author` та `Genre`
   - N+1 проблема: чому не завантажувати все відразу?

7. **Підсумки та завдання** (~80 рядків)

---

### Стаття 13. Strategy Pattern: Винесення SQL у стратегії

**Файл:** `content/04.java/pr2/13.strategy-sql-queries.md`

#### Зміст

1. **Вступ: Проблема жорстко закодованого SQL** (~100 рядків)
   - Hook: "Наш `AbstractJdbcRepository` працює. Але SQL-запити жорстко прописані у кожній реалізації. А якщо ми хочемо підтримувати H2 і PostgreSQL одночасно? Або динамічно формувати WHERE-частину?"
   - GoF: Strategy Pattern — "визначає сімейство алгоритмів, інкапсулює кожен з них і робить їх взаємозамінними"

2. **Концепція: SQL як стратегія** (~120 рядків)
   - `::mermaid` — UML діаграма Strategy для SQL
   - Інтерфейс `SqlDialect<T>` з методами: `insertSql()`, `updateSql()`, `selectByIdSql()`, `selectAllSql()`, `deleteSql()`
   - Альтернатива: `QueryBuilder` як окрема стратегія формування WHERE

3. **Реалізація SqlDialect** (~200 рядків)
   - `AuthorSqlDialect` для H2
   - `AuthorPostgresSqlDialect` — відмінності (наприклад, ENUM, синтаксис)
   - `::tabs` — H2 vs PostgreSQL для одного й того ж запиту

4. **Інтеграція Strategy у Repository** (~200 рядків)
   - Модифікований `AbstractJdbcRepository` приймає `SqlDialect` через конструктор
   - `JdbcAuthorRepository` більше не містить SQL-рядків
   - `::code-group` — До (SQL в Repository) vs Після (SQL в Strategy)

5. **QueryStrategy для динамічних запитів** (~200 рядків)
   - Інтерфейс `QueryStrategy<T>` з `buildQuery()` та `setParams(PreparedStatement)`
   - `AuthorByLastNameQuery`, `AudiobookByGenreAndYearQuery`
   - Комбінування стратегій: `CompositeQueryStrategy`
   - Порівняння зі Specification Pattern із частини 2 (JSON)

6. **Підсумки та завдання** (~80 рядків)

---

### Стаття 14. Proxy Pattern: Lazy Loading для One-To-Many

**Файл:** `content/04.java/pr2/14.proxy-lazy-loading.md`

#### Зміст

1. **Вступ: Проблема жадібного завантаження** (~100 рядків)
   - Hook: "Audiobook має список `AudiobookFile`. При завантаженні 100 аудіокниг, чи потрібно одразу завантажувати 500 файлів? А якщо 95% запитів не звертаються до файлів?"
   - Eager vs Lazy Loading — фундаментальна дилема ORM
   - GoF: Proxy Pattern

2. **Концепція Lazy Loading через Proxy** (~150 рядків)
   - `::mermaid` — sequence diagram: перший доступ до `getFiles()` → SQL-запит → кешування
   - Virtual Proxy: об'єкт-заглушка, що "прикидається" справжнім списком
   - Три підходи: Lazy Initialization, Virtual Proxy, Ghost Object
   - `::card-group` — порівняння трьох підходів

3. **LazyList — розумний список** (~200 рядків)
   - Реалізація `LazyList<T> implements List<T>` — делегує до справжнього списку, але ініціалізує його при першому доступі
   - `Supplier<List<T>>` як фабрика завантаження
   - Метод `isLoaded()` для діагностики
   - `::warning` — "LazyList не є потокобезпечним. Для багатопоточності потрібен synchronized або DCL"

4. **Інтеграція у доменну модель** (~200 рядків)
   - `Audiobook` отримує поле `List<AudiobookFile> files`
   - При завантаженні з БД: `audiobook.setFiles(new LazyList<>(() -> fileRepo.findByAudiobookId(id)))`
   - `AudiobookFile` як окрема сутність з `JdbcAudiobookFileRepository`
   - `Collection` з `LazyList<Audiobook>` через junction-таблицю `audiobook_collection`

5. **Proxy для Many-To-One** (~150 рядків)
   - `Author` в `Audiobook` — замість JOIN можна завантажувати лениво
   - `LazyReference<T>` — обгортка для одиночного об'єкта
   - Коли Lazy, а коли Eager: правила вибору
   - `::tabs` — Eager vs Lazy для різних сценаріїв

6. **N+1 Problem та батчеві завантаження** (~100 рядків)
   - Що таке N+1: завантаження 100 книг → 1 SELECT + 100 SELECT для авторів
   - `::mermaid` — візуалізація N+1
   - Рішення: batch loading, JOIN fetch, subselect fetch
   - `::note` — "Саме для вирішення N+1 ORM-фреймворки (Hibernate) використовують складні стратегії завантаження"

7. **Підсумки та завдання** (~80 рядків)

---

### Стаття 15. Reflection-Based GenericRepository: Метапрограмування

**Файл:** `content/04.java/pr2/15.generic-repository-reflection.md`

#### Зміст

1. **Вступ: Дублювання як симптом** (~100 рядків)
   - Hook: "Подивіться на `JdbcAuthorRepository`, `JdbcGenreRepository`, `JdbcAudiobookRepository`. Вони відрізняються лише: назвою таблиці, списком стовпців, маппінгом полів. А що, якщо Java може дізнатися це все сама — через рефлексію?"
   - `::code-group` — три репозиторії поруч → видно паттерн дублювання

2. **Java Reflection API: Основи** (~200 рядків)
   - `Class<T>`, `Field`, `Method`, `Constructor`
   - `getDeclaredFields()`, `field.setAccessible(true)`, `field.get(obj)`, `field.set(obj, value)`
   - Анотації: `@Retention`, `@Target` — як створювати власні
   - `::warning` — "Рефлексія — потужний, але небезпечний інструмент. Вона обходить інкапсуляцію і уповільнює виконання."

3. **Власні анотації для маппінгу** (~150 рядків)
   - `@Table(name = "authors")` — ім'я таблиці
   - `@Column(name = "first_name")` — ім'я стовпця
   - `@Id` — позначення первинного ключа
   - `@ManyToOne` / `@OneToMany` — маркери зв'язків (опціонально)
   - Анотовані доменні класи: `Author`, `Genre`, `User`

4. **ReflectiveRowMapper** (~200 рядків)
   - Клас, що через рефлексію створює об'єкт з `ResultSet`
   - `mapRow(ResultSet rs, Class<T> clazz)` → створення через конструктор → заповнення через `Field.set()`
   - Обробка типів: `UUID`, `String`, `int`, `LocalDateTime`, `Enum`
   - Кешування метаданих: `Map<Class<?>, List<FieldMapping>>`

5. **ReflectiveGenericRepository** (~250 рядків)
   - `GenericJdbcRepository<T, ID>` — повна реалізація
   - Автоматична генерація SQL: `INSERT INTO authors (id, first_name, ...) VALUES (?, ?, ...)`
   - `findById()`, `findAll()`, `save()`, `update()`, `deleteById()` — все через рефлексію
   - `::mermaid` — архітектурна діаграма: Annotation → Reflection → SQL Generation → JDBC

6. **Використання GenericRepository** (~150 рядків)
   - `GenericJdbcRepository<Author, UUID> authorRepo = new GenericJdbcRepository<>(Author.class, connectionManager);`
   - Порівняння обсягу коду: ручний репозиторій (~100 рядків) vs рефлексійний (~0 рядків специфічного коду)
   - `::tabs` — "Ручний" vs "Рефлексійний" для `AuthorRepository`

7. **Обмеження та шлях до ORM** (~100 рядків)
   - Що не може рефлексійний GenericRepository: складні JOIN, оптимізація запитів, кешування, Lazy Loading
   - `::note` — "Вітаємо: ви щойно реалізували мініатюрний ORM. Саме так влаштований Hibernate під капотом — тільки на порядки складніший."
   - Тизер: JPA, Hibernate, Spring Data

8. **Підсумки та завдання** (~80 рядків)
   - Рівень 3: Додати підтримку `@ManyToOne` — автоматичний JOIN через рефлексію

---

## Додаткові патерни — пропозиції

> [!IMPORTANT]
> Нижче — патерни, які я пропоную додати або інтегрувати. Потрібна ваша думка.

### Вже інтегровано у план:
1. **Strategy** (стаття 13) — винесення SQL у стратегії
2. **Proxy / Lazy Loading** (стаття 14) — для One-To-Many
3. **Template Method** — природно виникає в `AbstractJdbcRepository` (стаття 12)
4. **Data Mapper** — JDBC-версія (стаття 12)

### Додаткові пропозиції (можна додати як окремі статті або інтегрувати):

| Патерн | Де інтегрувати | Опис |
|---|---|---|
| **Connection Pool** | Стаття 09 або 12 | `HikariCP` замість ручного `DriverManager`. Критично для production |
| **DAO Factory / Abstract Factory** | Стаття 11 або 12 | Фабрика, що створює правильний DAO залежно від типу БД |
| **Unit of Work** | Стаття 12 (інтеграція) | Вже є з JSON-версії, адаптувати для JDBC-транзакцій |
| **Identity Map** | Стаття 12 (інтеграція) | Кешування завантажених сутностей у рамках транзакції |
| **Query Object** | Стаття 13 (інтеграція) | Об'єктне представлення SQL-запиту (типобезпечний builder) |

---

## Open Questions

> [!WARNING]
> 1. **Чи потрібна окрема стаття про Impedance Mismatch?** Стаття 07 (`07.impedance-mismatch.md`) вже існує в плані. Чи достатньо посилання на неї, чи варто повторити ключові ідеї у статті 09?
> 2. **ConnectionPool (HikariCP):** Додавати в одну зі статей чи ні? Це production-необхідна річ, але ускладнює навчальний матеріал.
> 3. **Unit of Work + Identity Map для JDBC:** Інтегрувати в статтю 12 чи створити окрему статтю (це додасть 8-му статтю)?
> 4. **Чи влаштовує нумерація 09–15?** Або краще починати з іншого номера?

---

## Verification Plan

### Під час написання
- Після кожного блоку (~100 рядків) — перевірка цілісності тексту
- Перевірка SQL-прикладів на відповідність реальній схемі `ddl_h2.sql`
- Перевірка Docus-компонентів: `::mermaid`, `::plant-uml`, `::tabs`, `::steps`, `::code-group`

### Після завершення
- Запуск dev-сервера (`npm run dev`) та перевірка рендерингу
- Наскрізне читання: логічний перехід від статті 09 до 15
- Перевірка зв'язності з існуючими статтями 01–08
