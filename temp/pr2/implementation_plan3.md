# Серія статей: Патерни доступу до даних з JDBC та H2

## Мета

Створити цикл із **11 статей** (`09`–`19`) у `content/04.java/pr2/`. Еволюція від наївного JDBC до рефлексійного `GenericRepository`. Схема — аудіоплатформа з `ddl_h2.sql`. Стиль — як у `01.data-mapper-part1/part2.md`.

> [!IMPORTANT]
> - Статті 01–06 вже існують (концептуальне/логічне моделювання, нормалізація, фізична схема, класифікація таблиць, міграції Flyway)
> - Статті 07–08 з попереднього плану **не написані** — 07 (Impedance Mismatch) буде написана з нуля як стаття 09
> - Рефлексія — **ТІЛЬКИ** в останній статті (19)

---

## Структура (11 статей, 09–19)

| № | Файл | Тема | Ключовий патерн |
|---|---|---|---|
| 09 | `09.impedance-mismatch.md` | Object-Relational Impedance Mismatch | — (теоретична) |
| 10 | `10.jdbc-fundamentals.md` | JDBC: наївний підхід, проблеми | — |
| 11 | `11.connection-pool.md` | Connection Pool: реалізація з нуля | Object Pool (GoF) |
| 12 | `12.row-data-gateway.md` | Row Data Gateway | Row Data Gateway (Fowler) |
| 13 | `13.table-data-gateway.md` | Table Data Gateway + доменна модель | Table Data Gateway (Fowler) |
| 14 | `14.repository-data-mapper.md` | Repository + Data Mapper з JDBC | Repository, Data Mapper (Fowler) |
| 15 | `15.identity-map.md` | Identity Map: кешування сутностей | Identity Map (Fowler) |
| 16 | `16.unit-of-work.md` | Unit of Work: транзакції та відстеження | Unit of Work (Fowler) |
| 17 | `17.strategy-sql.md` | Strategy: винесення SQL | Strategy (GoF) |
| 18 | `18.proxy-lazy-loading.md` | Proxy: Lazy Loading для One-To-Many | Proxy (GoF) |
| 19 | `19.generic-repository-reflection.md` | GenericRepository через рефлексію | Reflection + Annotations |

---

## Детальний зміст кожної статті

### 09. Impedance Mismatch (з нуля)

**Мета:** Пояснити фундаментальну невідповідність між OOP і реляційною моделлю.

1. **Вступ** — "У БД аудіокнига — рядок з `author_id`. У Java — об'єкт з полем `Author author`"
2. **5 ключових розбіжностей:**
   - Гранулярність (Value Object `Name` = 2 стовпці)
   - Успадкування (Java ієрархії vs плоскі таблиці)
   - Ідентичність (`==` vs `.equals()` vs PK)
   - Зв'язки (посилання на об'єкт vs FK)
   - Навігація (крапкова нотація vs JOIN)
3. **Ручний маппінг** — `ResultSet` → Java Object, параметр за параметром
4. **Патерни подолання** — Active Record, Data Mapper, ORM (огляд)
5. **Зв'язок з наступними статтями** — дорожня карта серії

### 10. JDBC Fundamentals

**Мета:** Перший робочий CRUD через JDBC, виявлення проблем.

1. **Архітектура JDBC** — `DriverManager` → `Connection` → `PreparedStatement` → `ResultSet`
2. **Перший CRUD: AuthorNaiveDao** — весь SQL в методах, Connection в кожному методі
3. **Проблеми:** SQL-ін'єкції, витік ресурсів, дублювання маппінгу, відсутність транзакцій
4. **Виправлення:** `PreparedStatement`, try-with-resources, `ConnectionManager`
5. **Завдання:** написати `GenreNaiveDao`, `UserDao`

### 11. Connection Pool (реалізація з нуля)

**Мета:** Реалізувати власний Connection Pool як патерн Object Pool.

1. **Проблема** — створення `Connection` дороге (~50-100ms), а наївний підхід створює нове на кожен запит
2. **Object Pool Pattern (GoF)** — визначення, діаграма
3. **Реалізація `SimpleConnectionPool`** — `BlockingQueue<Connection>`, `getConnection()`, `releaseConnection()`, `close()`
4. **Proxy для автоповернення** — `PooledConnection implements Connection` (делегат, що при `close()` повертає з'єднання в пул)
5. **Конфігурація** — min/max connections, timeout, validation query
6. **Порівняння з HikariCP** — що наша реалізація не робить (leak detection, metrics, statement caching)
7. **Завдання:** додати health check, timeout на очікування

### 12. Row Data Gateway

**Мета:** Перший Fowler-патерн — об'єкт = рядок таблиці.

1. **Концепція** — цитата Fowler, діаграма
2. **`AuthorGateway`** — поля + `insert()`, `update()`, `delete()`, `static findById()`
3. **`GenreGateway`** — аналогічно
4. **Проблеми** — порушення SRP, не масштабується для зв'язків
5. **Завдання**

### 13. Table Data Gateway

**Мета:** Виділення SQL в окремий клас, доменна модель окремо.

1. **Концепція** — порівняння з Row Data Gateway
2. **Доменна модель** — `Author`, `Genre`, `Audiobook` як чисті POJO
3. **`AuthorTableGateway`** — CRUD + `mapRow(ResultSet)`
4. **`AudiobookTableGateway`** — проблема зв'язків: `authorId` vs JOIN
5. **Проблеми** — дублювання SQL, немає абстракції
6. **Завдання**

### 14. Repository + Data Mapper з JDBC

**Мета:** Правильна шарова архітектура — інтерфейс Repository + JDBC-реалізація.

1. **Архітектура** — Domain → Repository Interface → JDBC Implementation
2. **`Repository<T, ID>`** інтерфейс (з data-mapper-part1)
3. **`AbstractJdbcRepository<T, ID>`** — Template Method: абстрактні `mapRow()`, `getTableName()`, `getInsertSql()` тощо
4. **`JdbcAuthorRepository`**, **`JdbcGenreRepository`** — конкретні реалізації
5. **`JdbcAudiobookRepository`** — JOIN для Author + Genre, маппінг складних об'єктів
6. **Завдання**

### 15. Identity Map

**Мета:** Кешування завантажених сутностей у рамках сесії.

1. **Проблема** — два `findById("123")` створюють два різні об'єкти; зміна одного не видна іншому
2. **Концепція** — Fowler, діаграма "є в кеші? → повернути / завантажити + кешувати"
3. **Реалізація `IdentityMap<ID, T>`** — `Map<ID, T>`, `get()`, `put()`, `remove()`, `clear()`
4. **Інтеграція з Repository** — `CachedJdbcRepository` з Identity Map
5. **Область видимості** — per-request, per-transaction, per-session
6. **Проблеми** — стале кешування, пам'ять, конкурентність
7. **Завдання**

### 16. Unit of Work (детально, з JDBC-транзакціями)

**Мета:** Відстеження змін та координація запису — з реальними JDBC-транзакціями.

1. **Проблема** — кожен `save()` = окремий `INSERT`/`UPDATE`. 10 змін = 10 транзакцій
2. **Концепція** — Fowler, стани: New → Dirty → Deleted → commit/rollback
3. **Реалізація `UnitOfWork<T, ID>`** — `registerNew()`, `registerDirty()`, `registerDeleted()`, `commit()`, `rollback()`
4. **Інтеграція з JDBC-транзакціями** — `Connection.setAutoCommit(false)`, `commit()`, `rollback()` в `catch`
5. **Координація з Identity Map** — UoW оновлює IM після commit
6. **Change Tracking** — автоматичне виявлення "брудних" об'єктів (snapshot-based)
7. **Завдання**

### 17. Strategy: SQL у стратегіях

**Мета:** Витягнути SQL із репозиторіїв у замінювані стратегії.

1. **Проблема** — SQL жорстко в кожній реалізації; H2 vs PostgreSQL мають різний синтаксис
2. **`SqlDialect<T>`** — інтерфейс зі всіма SQL-запитами для сутності
3. **`AuthorH2Dialect`**, **`AuthorPostgresDialect`** — конкретні реалізації
4. **Інтеграція** — Repository приймає `SqlDialect` через конструктор
5. **`QueryStrategy`** — динамічні WHERE: `AuthorByLastNameQuery`, `AudiobookByGenreQuery`
6. **Порівняння зі Specification** (з data-mapper-part2)
7. **Завдання**

### 18. Proxy: Lazy Loading

**Мета:** Lazy Loading для One-To-Many через Proxy-патерн.

1. **Проблема** — 100 аудіокниг × 5 файлів = 500 непотрібних записів
2. **`LazyList<T> implements List<T>`** — делегує до справжнього списку, ініціалізує при першому доступі
3. **Інтеграція** — `audiobook.setFiles(new LazyList<>(() -> fileRepo.findByAudiobookId(id)))`
4. **`LazyReference<T>`** — для Many-To-One (Author в Audiobook)
5. **N+1 Problem** — пояснення, візуалізація, рішення (batch loading)
6. **Завдання**

### 19. GenericRepository через рефлексію

**Мета:** Фінальна еволюція — метапрограмування замість ручного маппінгу.

1. **Проблема дублювання** — 3 репозиторії поруч → видно однаковий паттерн
2. **Reflection API** — `Class<T>`, `Field`, `getDeclaredFields()`, `setAccessible()`
3. **Анотації** — `@Table("authors")`, `@Column("first_name")`, `@Id`
4. **`ReflectiveRowMapper`** — створює об'єкт з `ResultSet` через рефлексію
5. **`GenericJdbcRepository<T, ID>`** — автогенерація INSERT/SELECT/UPDATE/DELETE
6. **Обмеження** — складні JOIN, оптимізація, Lazy Loading
7. **Тизер** — "Ви реалізували мініатюрний ORM. Hibernate робить те саме, але на порядки складніше"
8. **Завдання**

---

## Verification Plan

- Перевірка SQL на відповідність `ddl_h2.sql`
- Перевірка Docus-компонентів (`::mermaid`, `::tabs`, `::steps`, `::code-group`)
- `npm run dev` — рендеринг кожної статті
- Наскрізне читання 09→19: логічні переходи між статтями
