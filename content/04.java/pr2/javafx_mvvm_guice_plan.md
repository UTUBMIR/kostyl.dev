# Модуль "JavaFX MVVM + Google Guice" для `04.java/pr2`

## Мета

Створити цикл із **глибоких, академічних статей** у директорії `content/04.java/pr2/`, що проведе читача від базових концепцій JavaFX через патерн MVVM до повноцінної інтеграції з Google Guice для побудови масштабованих desktop-додатків. Наскрізний приклад — **платформа аудіокниг** (продовження проєкту з бази даних).

> [!IMPORTANT]  
> **Вимоги до стилю та обсягу:**
> - **Академічний, книжковий стиль** — формальний, але живий; текст-перше, код-ілюстрація.
> - Кожна стаття ~ **1000–1200 рядків** Markdown.
> - **Писати частинами по ~100 рядків**, а не всю статтю одразу. Після кожного блоку — перевірка, корекція, продовження.
> - Суворе дотримання `prompt.md` (Why Before How, Scaffolding, Text First, Code Anatomy, No Silent Code).
> - Активне використання Docus-компонентів із `DOCUS_COMPONENTS.md`.
> - Інтеграція з попередніми матеріалами: Repository, Unit of Work, Dependency Injection (Guice).

---

## Навігаційний файл

Оновлення `.navigation.yml` у `content/04.java/pr2/`:

```yaml
title: Проектування баз даних та JavaFX MVVM
```

---

## Нумерація статей

Продовження існуючої нумерації:

- **25.javafx-fundamentals.md** — JavaFX: Основи побудови графічних інтерфейсів
- **26.javafx-properties-bindings.md** — Properties та Bindings: Реактивність у JavaFX
- **27.ui-architecture-patterns.md** — MVC vs MVP vs MVVM: Еволюція архітектурних патернів UI
- **28.mvvm-viewmodel-implementation.md** — MVVM на практиці: Побудова ViewModel
- **29.mvvm-view-controller.md** — View та Controller: Зв'язування з ViewModel через FXML
- **30.mvvm-guice-integration.md** — Інтеграція MVVM з Guice: Автоматична ін'єкція залежностей
- **31.mvvm-validation-error-handling.md** — Валідація та обробка помилок у MVVM
- **32.mvvm-navigation-screen-management.md** — Навігація та управління екранами у JavaFX MVVM
- **33.mvvm-testing.md** — Тестування JavaFX MVVM-додатків
- **34.javafx-styling-themes.md** — Стилізація та теми у JavaFX: CSS та User Experience
- **35.full-project-audiobook-platform.md** — Повний проєкт: Audiobook Platform з MVVM + Guice
- **36.reactive-programming-rxjavafx.md** (опціонально) — Реактивне програмування у JavaFX: RxJavaFX
- **37.internationalization-localization.md** (опціонально) — Інтернаціоналізація (i18n) та локалізація

---

## Зв'язок з попередніми матеріалами

### Інтеграційні точки

1. **Стаття 24 (Guice)** → **Стаття 30 (MVVM + Guice)**
   - Стаття 24 вже ввела Guice та показала базову інтеграцію з JavaFX через ControllerFactory.
   - Стаття 30 розширює це, показуючи повну інтеграцію з MVVM-архітектурою.

2. **Статті 12-20 (Repository, Unit of Work, Specification)** → **Стаття 35 (Повний проєкт)**
   - Всі патерни доступу до даних використовуються у фінальному проєкті.
   - ViewModel викликає Service → Service використовує Repository + Unit of Work.

3. **Стаття 22-23 (Тестування)** → **Стаття 33 (Тестування MVVM)**
   - Інтеграційні тести з H2 та Testcontainers застосовуються для тестування ViewModel + Repository.

### Наскрізний приклад

**Платформа аудіокниг** (Audiobook Platform) — єдиний проєкт, що проходить через всі статті:

- **Статті 01-08**: Проектування бази даних (authors, audiobooks, genres, users, collections, listening_progress).
- **Статті 09-24**: Реалізація Data Access Layer (Repository, Unit of Work, Guice).
- **Статті 25-35**: Побудова Presentation Layer (JavaFX UI, MVVM, навігація, стилізація).

---

## Verification Plan

### Під час написання

- Після кожного блоку (~100 рядків) — перевірка цілісності тексту, відповідності `prompt.md`.
- Перевірка всіх Docus-компонентів: `::mermaid`, `::plant-uml`, `::tabs`, `::steps`, `::code-group`, `::card-group`.
- Перевірка Java-прикладів на компіляцію (хоча б синтаксично).
- Перевірка FXML-прикладів на валідність XML.

### Після завершення модуля

- Запуск dev-сервера (`npm run dev`) та перевірка рендерингу кожної статті.
- Перевірка PlantUML-діаграм через PlantUML сервер.
- Перевірка Mermaid-діаграм у браузері.
- Наскрізне читання: чи є логічний перехід від статті 25 до статті 35.
- Перевірка посилань між статтями (внутрішні посилання на попередні матеріали).

---

## Технічні вимоги

### Залежності для прикладів коду

```xml
<!-- pom.xml -->
<dependencies>
    <!-- JavaFX -->
    <dependency>
        <groupId>org.openjfx</groupId>
        <artifactId>javafx-controls</artifactId>
        <version>21</version>
    </dependency>
    <dependency>
        <groupId>org.openjfx</groupId>
        <artifactId>javafx-fxml</artifactId>
        <version>21</version>
    </dependency>
    
    <!-- Dependency Injection -->
    <dependency>
        <groupId>com.google.inject</groupId>
        <artifactId>guice</artifactId>
        <version>7.0.0</version>
    </dependency>
    
    <!-- Database -->
    <dependency>
        <groupId>com.h2database</groupId>
        <artifactId>h2</artifactId>
        <version>2.2.224</version>
    </dependency>
    <dependency>
        <groupId>com.zaxxer</groupId>
        <artifactId>HikariCP</artifactId>
        <version>5.1.0</version>
    </dependency>
    <dependency>
        <groupId>org.flywaydb</groupId>
        <artifactId>flyway-core</artifactId>
        <version>10.10.0</version>
    </dependency>
    
    <!-- Testing -->
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>5.10.2</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.mockito</groupId>
        <artifactId>mockito-core</artifactId>
        <version>5.11.0</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testfx</groupId>
        <artifactId>testfx-junit5</artifactId>
        <version>4.0.18</version>
        <scope>test</scope>
    </dependency>
    
    <!-- Optional: RxJava -->
    <dependency>
        <groupId>io.reactivex.rxjava3</groupId>
        <artifactId>rxjava</artifactId>
        <version>3.1.8</version>
    </dependency>
    <dependency>
        <groupId>io.reactivex.rxjava3</groupId>
        <artifactId>rxjavafx</artifactId>
        <version>3.0.2</version>
    </dependency>
</dependencies>
```

### Структура проєкту-прикладу

```
audiobook-platform/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── dev/kostyl/audiobook/
│   │   │       ├── domain/           # Domain Model (Audiobook, Author, Genre)
│   │   │       ├── repository/       # Repository interfaces + JDBC implementations
│   │   │       ├── service/          # Business Logic (AudiobookService, CollectionService)
│   │   │       ├── viewmodel/        # ViewModels (AudiobookListViewModel, AudiobookFormViewModel)
│   │   │       ├── controller/       # FXML Controllers (мінімальні)
│   │   │       ├── infrastructure/   # Guice Modules, Navigator, ScreenRegistry
│   │   │       └── AudiobookApp.java # Application Entry Point
│   │   └── resources/
│   │       ├── fxml/                 # FXML files
│   │       ├── css/                  # Stylesheets (light-theme.css, dark-theme.css)
│   │       ├── db/migration/         # Flyway migrations (V1__Create_authors.sql, ...)
│   │       └── messages*.properties  # i18n bundles
│   └── test/
│       └── java/
│           └── dev/kostyl/audiobook/
│               ├── viewmodel/        # ViewModel unit tests
│               ├── repository/       # Repository integration tests
│               └── ui/               # TestFX UI tests
└── pom.xml
```

---

## Стилістичні рекомендації

### Код

- **Java Code Style**: Google Java Style Guide (4 пробіли, camelCase).
- **SQL**: snake_case для таблиць та колонок, UPPERCASE для ключових слів.
- **FXML**: kebab-case для fx:id (`audiobook-table`, `add-button`).
- **CSS**: kebab-case для класів (`.primary-button`, `.table-row-cell`).

### Діаграми

- **Mermaid**: для швидких блок-схем, sequence diagrams, ER-діаграм (до 5 сутностей).
- **PlantUML**: для детальних UML-діаграм класів, складних sequence diagrams, компонентних діаграм.
- Візуалізація концепцій.

### Компоненти Docus

- `::note` — додаткова інформація, історичний контекст.
- `::tip` — best practices, корисні поради.
- `::warning` — застереження, типові помилки.
- `::caution` — критичні застереження, небезпечні операції.
- `::steps` — покрокові інструкції, алгоритми.
- `::tabs` — порівняння підходів, різні реалізації.
- `::code-group` — код для різних платформ/мов/підходів.
- `::card-group` — групування концепцій, порівняльні таблиці.
- `::code-collapse` — довгий код, що не є критичним для розуміння.

---

## Рішення (затверджено)

- ✅ **Нумерація:** Продовження існуючої (25-37).
- ✅ **Наскрізний приклад:** Audiobook Platform (продовження з попередніх статей).
- ✅ **Обсяг:** 11 основних статей (~1000-1500 рядків кожна) + 2 опціональні (~800-1000 рядків).
- ✅ **Стиль:** Академічний, книжковий, текст-перше, код-ілюстрація.
- ✅ **Інтеграція:** Тісний зв'язок зі статтями 01-24 (база даних, Repository, Guice).
- ✅ **Практичність:** Кожна стаття містить практичні завдання 3 рівнів складності.

---

## Часова оцінка написання

При написанні **частинами по ~100 рядків** з перевіркою після кожного блоку:

- **Стаття 25-34** (по 1000-1200 рядків): ~10-12 блоків × 11 статей = **110-132 блоки**.
- **Стаття 35** (1200-1500 рядків): ~12-15 блоків.
- **Статті 36-37** (опціонально, по 800-1000 рядків): ~8-10 блоків × 2 = **16-20 блоків**.

**Загальна оцінка:** ~140-170 блоків по 100 рядків = **14,000-17,000 рядків Markdown**.

При темпі **1 блок (100 рядків) за 15-20 хвилин** (з перевіркою):
- **Основні статті (25-35):** ~40-50 годин чистого написання.
- **Опціональні статті (36-37):** ~5-7 годин.

**Рекомендація:** Писати по 2-3 блоки за сесію (30-60 хвилин), з перервами для перевірки та корекції.

---

## Наступні кроки

1. ✅ **План створено** — цей документ.
2. ⏳ **Написання статей** — починаючи зі статті 25, частинами по ~100 рядків.
3. ⏳ **Перевірка після кожної статті** — рендеринг, діаграми, посилання.
4. ⏳ **Фінальна перевірка модуля** — наскрізне читання, узгодженість з попередніми матеріалами.
5. ⏳ **Створення GitHub-репозиторію** з повним кодом проєкту Audiobook Platform (для статті 35).


### Стаття 36. Реактивне програмування у JavaFX: RxJavaFX

**Файл:** `content/04.java/pr2/36.reactive-programming-rxjavafx.md`  
**Обсяг:** ~800–1000 рядків (опціонально)

#### Зміст

1. **Вступ: Від Properties до Observables** (~80 рядків)
   - JavaFX Properties — це реактивність, але обмежена.
   - RxJava — потужніша парадигма для роботи з асинхронними потоками даних.
   - RxJavaFX — міст між JavaFX та RxJava.

2. **Основи RxJava: Observable, Observer, Operators** (~150 рядків)
   - `Observable.just()`, `Observable.fromIterable()`, `Observable.interval()`.
   - Оператори: `map()`, `filter()`, `flatMap()`, `debounce()`, `throttle()`.
   - Підписка: `subscribe(onNext, onError, onComplete)`.

3. **RxJavaFX: Інтеграція з JavaFX Properties** (~150 рядків)
   - `JavaFxObservable.valuesOf(property)` — перетворення Property у Observable.
   - Приклад: пошук з debouncing:
     ```java
     JavaFxObservable.valuesOf(searchField.textProperty())
         .debounce(300, TimeUnit.MILLISECONDS)
         .distinctUntilChanged()
         .observeOn(JavaFxScheduler.platform())
         .subscribe(query -> viewModel.search(query));
     ```

4. **Асинхронні операції через RxJava** (~120 рядків)
   - Заміна Task на Observable:
     ```java
     public Observable<List<Audiobook>> loadAudiobooks() {
         return Observable.fromCallable(() -> repository.findAll())
             .subscribeOn(Schedulers.io())
             .observeOn(JavaFxScheduler.platform());
     }
     ```

5. **Практичні завдання** (~50 рядків)

---

### Стаття 37. Інтернаціоналізація (i18n) та локалізація

**Файл:** `content/04.java/pr2/37.internationalization-localization.md`  
**Обсяг:** ~800–1000 рядків (опціонально)

#### Зміст

1. **Вступ: Багатомовність додатку** (~80 рядків)
   - Чому i18n важлива: глобальна аудиторія, доступність.
   - ResourceBundle — стандартний механізм Java.

2. **ResourceBundle: Файли локалізації** (~120 рядків)
   - Створення `messages_en.properties`, `messages_uk.properties`:
     ```properties
     # messages_en.properties
     app.title=Audiobook Platform
     button.add=Add Audiobook
     button.delete=Delete
     
     # messages_uk.properties
     app.title=Платформа аудіокниг
     button.add=Додати аудіокнигу
     button.delete=Видалити
     ```

3. **Використання у FXML** (~100 рядків)
   - Атрибут `%key`: `<Button text="%button.add" />`.
   - Завантаження ResourceBundle у FXMLLoader:
     ```java
     ResourceBundle bundle = ResourceBundle.getBundle("messages", new Locale("uk"));
     loader.setResources(bundle);
     ```

4. **Динамічна зміна мови** (~120 рядків)
   - Перезавантаження View при зміні локалі.
   - Збереження вибраної мови у Preferences.

5. **Практичні завдання** (~50 рядків)

---


**Файл:** `content/04.java/pr2/35.full-project-audiobook-platform.md`  
**Обсяг:** ~1200–1500 рядків (фінальна, найбільша стаття)

#### Зміст

1. **Вступ: Від теорії до production-ready додатку** (~100 рядків)
   - Hook: "Ми пройшли шлях від проектування бази даних до MVVM. Настав час з'єднати все разом у повноцінний додаток."
   - Мета статті: покрокова побудова Audiobook Platform з усіма вивченими патернами.
   - Функціональність: управління аудіокнигами, авторами, жанрами, колекціями, прогресом прослуховування.

2. **Архітектура проєкту: Огляд шарів** (~150 рядків)
   - **Presentation Layer**: Views (FXML), Controllers, ViewModels.
   - **Business Logic Layer**: Services (AudiobookService, CollectionService).
   - **Data Access Layer**: Repositories (AudiobookRepository, AuthorRepository), Unit of Work.
   - **Infrastructure Layer**: Database (Flyway migrations), Guice Modules, Navigator.
   - `::mermaid` — layered architecture diagram з усіма компонентами.
   - `::code-tree` — повна структура директорій проєкту.

3. **Domain Model: Сутності та Value Objects** (~150 рядків)
   - Класи: `Audiobook`, `Author`, `Genre`, `User`, `Collection`, `ListeningProgress`.
   - Value Objects: `Duration`, `Email`, `AudiobookTitle`.
   - Приклад:
     ```java
     public class Audiobook {
         private final UUID id;
         private final AudiobookTitle title;
         private final Author author;
         private final Genre genre;
         private final Duration duration;
         private final Year releaseYear;
         private final String description;
         private final String coverImagePath;
         
         // Constructor, getters
     }
     ```
   - `::note` — "Value Objects інкапсулюють валідацію: `new Duration(-10)` викине виняток."

4. **Data Access Layer: Repositories з JDBC** (~200 рядків)
   - Реалізація `JdbcAudiobookRepository`:
     ```java
     public class JdbcAudiobookRepository implements AudiobookRepository {
         private final DataSource dataSource;
         private final AudiobookMapper mapper;
         
         @Inject
         public JdbcAudiobookRepository(DataSource dataSource, AudiobookMapper mapper) {
             this.dataSource = dataSource;
             this.mapper = mapper;
         }
         
         @Override
         public List<Audiobook> findAll() {
             String sql = """
                 SELECT a.*, au.first_name, au.last_name, g.name as genre_name
                 FROM audiobooks a
                 JOIN authors au ON a.author_id = au.id
                 JOIN genres g ON a.genre_id = g.id
                 """;
             try (Connection conn = dataSource.getConnection();
                  Statement stmt = conn.createStatement();
                  ResultSet rs = stmt.executeQuery(sql)) {
                 
                 List<Audiobook> audiobooks = new ArrayList<>();
                 while (rs.next()) {
                     audiobooks.add(mapper.map(rs));
                 }
                 return audiobooks;
             }
         }
     }
     ```
   - Використання Connection Pool (HikariCP).
   - `::code-collapse` — повна реалізація Repository з CRUD-операціями.

5. **Service Layer: Бізнес-логіка** (~150 рядків)
   - `AudiobookService` з транзакціями через Unit of Work:
     ```java
     public class AudiobookService {
         private final AudiobookRepository audiobookRepository;
         private final UnitOfWork unitOfWork;
         
         @Inject
         public AudiobookService(AudiobookRepository repo, UnitOfWork uow) {
             this.audiobookRepository = repo;
             this.unitOfWork = uow;
         }
         
         public void addAudiobook(Audiobook audiobook) {
             unitOfWork.begin();
             try {
                 audiobookRepository.save(audiobook);
                 unitOfWork.commit();
             } catch (Exception e) {
                 unitOfWork.rollback();
                 throw new ServiceException("Failed to add audiobook", e);
             }
         }
     }
     ```
   - Валідація на рівні Service: перевірка унікальності, бізнес-правила.

6. **Presentation Layer: ViewModels** (~200 рядків)
   - `AudiobookListViewModel`:
     ```java
     public class AudiobookListViewModel {
         private final ObservableList<AudiobookViewModel> audiobooks = FXCollections.observableArrayList();
         private final ObjectProperty<AudiobookViewModel> selectedAudiobook = new SimpleObjectProperty<>();
         private final StringProperty searchQuery = new SimpleStringProperty("");
         private final BooleanProperty isLoading = new SimpleBooleanProperty(false);
         
         private final AudiobookService audiobookService;
         private final Navigator navigator;
         
         @Inject
         public AudiobookListViewModel(AudiobookService service, Navigator navigator) {
             this.audiobookService = service;
             this.navigator = navigator;
             setupSearchFilter();
         }
         
         public void loadAudiobooks() {
             isLoading.set(true);
             Task<List<Audiobook>> task = new Task<>() {
                 @Override
                 protected List<Audiobook> call() {
                     return audiobookService.getAllAudiobooks();
                 }
             };
             task.setOnSucceeded(e -> {
                 audiobooks.setAll(task.getValue().stream()
                     .map(AudiobookViewModel::new)
                     .collect(Collectors.toList()));
                 isLoading.set(false);
             });
             executor.submit(task);
         }
     }
     ```
   - `AudiobookFormViewModel` для додавання/редагування.
   - `CollectionViewModel` для управління колекціями.

7. **Views та Controllers** (~150 рядків)
   - `audiobook-list-view.fxml`:
     ```xml
     <BorderPane xmlns:fx="http://javafx.com/fxml">
         <top>
             <HBox spacing="10" padding="10">
                 <TextField fx:id="searchField" promptText="Search audiobooks..." />
                 <Button fx:id="addButton" text="Add Audiobook" onAction="#onAddClicked" />
             </HBox>
         </top>
         <center>
             <TableView fx:id="audiobookTable">
                 <columns>
                     <TableColumn text="Title" fx:id="titleColumn" />
                     <TableColumn text="Author" fx:id="authorColumn" />
                     <TableColumn text="Duration" fx:id="durationColumn" />
                 </columns>
             </TableView>
         </center>
     </BorderPane>
     ```
   - `AudiobookListController` з мінімальною логікою (лише bindings).

8. **Guice Configuration: Модулі та Bindings** (~150 rядків)
   - `AudiobookModule`:
     ```java
     public class AudiobookModule extends AbstractModule {
         @Override
         protected void configure() {
             // Data Access
             bind(DataSource.class).toProvider(HikariDataSourceProvider.class).in(Singleton.class);
             bind(AudiobookRepository.class).to(JdbcAudiobookRepository.class);
             bind(AuthorRepository.class).to(JdbcAuthorRepository.class);
             bind(GenreRepository.class).to(JdbcGenreRepository.class);
             
             // Services
             bind(AudiobookService.class).in(Singleton.class);
             bind(CollectionService.class).in(Singleton.class);
             
             // Infrastructure
             bind(Navigator.class).to(FxmlNavigator.class).in(Singleton.class);
             bind(ScreenRegistry.class).in(Singleton.class);
             
             // ViewModels
             bind(AudiobookListViewModel.class).in(Singleton.class);
         }
     }
     ```
   - `HikariDataSourceProvider` для конфігурації Connection Pool.

9. **Application Entry Point** (~100 рядків)
   - `AudiobookApp`:
     ```java
     public class AudiobookApp extends Application {
         private Injector injector;
         
         @Override
         public void init() {
             injector = Guice.createInjector(new AudiobookModule());
             
             // Flyway migrations
             Flyway flyway = Flyway.configure()
                 .dataSource(injector.getInstance(DataSource.class))
                 .load();
             flyway.migrate();
         }
         
         @Override
         public void start(Stage primaryStage) {
             Navigator navigator = injector.getInstance(Navigator.class);
             ((FxmlNavigator) navigator).setPrimaryStage(primaryStage);
             
             navigator.navigateTo("audiobook-list");
             
             primaryStage.setTitle("Audiobook Platform");
             primaryStage.setWidth(1200);
             primaryStage.setHeight(800);
             primaryStage.show();
         }
         
         @Override
         public void stop() {
             injector.getInstance(DataSource.class).close();
         }
     }
     ```

10. **Функціональність: Основні Use Cases** (~200 рядків)
    - **UC1: Перегляд списку аудіокниг** — завантаження, пошук, сортування.
    - **UC2: Додавання нової аудіокниги** — форма з валідацією, збереження через Service.
    - **UC3: Редагування аудіокниги** — завантаження даних у форму, оновлення.
    - **UC4: Видалення аудіокниги** — підтвердження через діалог, каскадне видалення.
    - **UC5: Управління колекціями** — створення, додавання аудіокниг, видалення.
    - **UC6: Відстеження прогресу** — оновлення позиції прослуховування.
    - `::steps` — покрокова реалізація кожного Use Case.

11. **Deployment: Збірка та запуск** (~100 рядків)
    - Maven/Gradle конфігурація з усіма залежностями.
    - Створення executable JAR через `maven-shade-plugin` або `jlink`.
    - Приклад `pom.xml`:
      ```xml
      <dependencies>
          <dependency>
              <groupId>org.openjfx</groupId>
              <artifactId>javafx-controls</artifactId>
              <version>21</version>
          </dependency>
          <dependency>
              <groupId>com.google.inject</groupId>
              <artifactId>guice</artifactId>
              <version>7.0.0</version>
          </dependency>
          <dependency>
              <groupId>com.h2database</groupId>
              <artifactId>h2</artifactId>
              <version>2.2.224</version>
          </dependency>
      </dependencies>
      ```

12. **Практичні завдання** (~80 рядків)
    - Рівень 1: Додати функціональність фільтрації за жанром.
    - Рівень 2: Реалізувати експорт списку аудіокниг у CSV.
    - Рівень 3: Додати систему рейтингів та відгуків користувачів.

13. **Підсумок та подальші кроки** (~50 рядків)
    - Що ми побудували: повноцінний MVVM-додаток з DI, тестами, стилізацією.
    - Можливі покращення: міграція на PostgreSQL, додавання REST API, інтеграція з хмарним сховищем.
    - Посилання на GitHub-репозиторій з повним кодом проєкту.

---


**Файл:** `content/04.java/pr2/34.javafx-styling-themes.md`  
**Обсяг:** ~1000–1200 рядків

#### Зміст

1. **Вступ: Від функціональності до естетики** (~80 рядків)
   - Hook: "Ваш додаток працює ідеально: MVVM, Guice, тести. Але він виглядає як Windows 95. Користувачі оцінюють не лише функціональність, а й зовнішній вигляд."
   - Чому стилізація важлива: перше враження, usability, brand identity.
   - JavaFX CSS: адаптація веб-стандарту для desktop.

2. **JavaFX CSS: Основи синтаксису** (~150 рядків)
   - Схожість з веб-CSS: селектори, властивості, значення.
   - Відмінності: префікс `-fx-`, специфічні властивості (`-fx-background-color`, `-fx-text-fill`).
   - Приклад:
     ```css
     .button {
         -fx-background-color: #3498db;
         -fx-text-fill: white;
         -fx-font-size: 14px;
         -fx-padding: 10px 20px;
         -fx-background-radius: 5px;
     }
     
     .button:hover {
         -fx-background-color: #2980b9;
     }
     ```
   - Підключення CSS до Scene: `scene.getStylesheets().add("styles.css")`.
   - `::code-group` — приклади стилізації Button, Label, TextField.

3. **Селектори та псевдокласи** (~120 рядків)
   - **Type selector**: `.button`, `.label`, `.text-field`.
   - **ID selector**: `#saveButton` (встановлюється через `button.setId("saveButton")`).
   - **Class selector**: `.primary-button` (встановлюється через `button.getStyleClass().add("primary-button")`).
   - **Псевдокласи**: `:hover`, `:pressed`, `:focused`, `:disabled`.
   - Приклад: кнопка з різними станами (normal, hover, pressed, disabled).

4. **Теми: Light та Dark Mode** (~200 рядків)
   - Створення двох CSS-файлів: `light-theme.css` та `dark-theme.css`.
   - Приклад light-theme.css:
     ```css
     .root {
         -fx-base: #ffffff;
         -fx-background: #f5f5f5;
         -fx-control-inner-background: #ffffff;
         -fx-accent: #3498db;
         -fx-default-button: #3498db;
         -fx-focus-color: #3498db;
     }
     ```
   - Приклад dark-theme.css:
     ```css
     .root {
         -fx-base: #2c3e50;
         -fx-background: #1a252f;
         -fx-control-inner-background: #34495e;
         -fx-accent: #3498db;
         -fx-text-base-color: #ecf0f1;
     }
     ```
   - Перемикання теми у runtime:
     ```java
     public void switchTheme(String themeName) {
         scene.getStylesheets().clear();
         scene.getStylesheets().add(getClass().getResource(themeName + "-theme.css").toExternalForm());
     }
     ```
   - `::tabs` — Light Theme vs Dark Theme

5. **CSS Variables у JavaFX** (~120 рядків)
   - Визначення змінних через `-fx-base`, `-fx-accent`:
     ```css
     .root {
         -primary-color: #3498db;
         -secondary-color: #2ecc71;
         -danger-color: #e74c3c;
     }
     
     .primary-button {
         -fx-background-color: -primary-color;
     }
     
     .danger-button {
         -fx-background-color: -danger-color;
     }
     ```
   - Переваги: централізована зміна кольорів, легке створення варіацій теми.

6. **Стилізація складних компонентів: TableView** (~150 рядків)
   - Анатомія TableView: `.table-view`, `.column-header`, `.table-cell`, `.table-row-cell`.
   - Приклад: зебра-стилізація (чергування кольорів рядків):
     ```css
     .table-row-cell:odd {
         -fx-background-color: #f9f9f9;
     }
     
     .table-row-cell:selected {
         -fx-background-color: #3498db;
         -fx-text-fill: white;
     }
     
     .table-row-cell:hover {
         -fx-background-color: #ecf0f1;
     }
     ```
   - Стилізація заголовків колонок, сортування, скролбарів.

7. **Inline стилі vs CSS-класи** (~100 рядків)
   - Inline: `button.setStyle("-fx-background-color: red;")` — швидко, але не масштабується.
   - CSS-класи: `button.getStyleClass().add("danger-button")` — рекомендований підхід.
   - Коли використовувати inline: динамічна зміна одного параметра (наприклад, прогрес-бар).
   - `::warning` — "Уникайте inline-стилів для статичного дизайну — використовуйте CSS."

8. **Іконки та шрифти** (~120 рядків)
   - Підключення Font Awesome або Material Icons:
     ```java
     @font-face {
         font-family: 'FontAwesome';
         src: url('fonts/fontawesome-webfont.ttf');
     }
     
     .icon-button {
         -fx-font-family: 'FontAwesome';
         -fx-font-size: 18px;
     }
     ```
   - Використання у коді: `label.setText("\uf067");` (Unicode для іконки).
   - Альтернатива: бібліотека FontAwesomeFX.

9. **Responsive Design: адаптація під розмір вікна** (~100 рядків)
   - Media queries у JavaFX (обмежена підтримка).
   - Альтернатива: динамічна зміна стилів через Bindings:
     ```java
     scene.widthProperty().addListener((obs, old, newWidth) -> {
         if (newWidth.doubleValue() < 800) {
             root.getStyleClass().add("compact-mode");
         } else {
             root.getStyleClass().remove("compact-mode");
         }
     });
     ```

10. **Практичні завдання** (~80 рядків)
    - Рівень 1: Створити CSS-файл з стилізацією кнопок (primary, secondary, danger).
    - Рівень 2: Реалізувати перемикання між Light та Dark темою.
    - Рівень 3: Стилізувати TableView з custom заголовками та hover-ефектами.

11. **Підсумок** (~30 рядків)

---


**Файл:** `content/04.java/pr2/33.mvvm-testing.md`  
**Обсяг:** ~1000–1200 рядків

#### Зміст

1. **Вступ: Переваги MVVM для тестування** (~80 рядків)
   - Hook: "Як протестувати JavaFX-додаток? Запускати UI та клікати мишкою? Ні — MVVM дозволяє тестувати логіку без UI."
   - Три рівні тестування: Unit (ViewModel), Integration (ViewModel + Repository), UI (TestFX).
   - Чому MVVM полегшує тестування: ViewModel — це POJO, не залежить від JavaFX Application Thread.

2. **Unit-тестування ViewModel** (~200 рядків)
   - Тестування без JavaFX: ViewModel як звичайний Java-клас.
   - Приклад тесту:
     ```java
     @ExtendWith(MockitoExtension.class)
     class AudiobookListViewModelTest {
         @Mock
         private AudiobookRepository repository;
         
         private AudiobookListViewModel viewModel;
         
         @BeforeEach
         void setUp() {
             viewModel = new AudiobookListViewModel(repository);
         }
         
         @Test
         void shouldLoadAudiobooks() {
             // Given
             List<Audiobook> audiobooks = List.of(
                 new Audiobook("Title 1", author1, genre1, 3600),
                 new Audiobook("Title 2", author2, genre2, 7200)
             );
             when(repository.findAll()).thenReturn(audiobooks);
             
             // When
             viewModel.loadAudiobooks();
             
             // Then
             assertEquals(2, viewModel.getAudiobooks().size());
             assertEquals("Title 1", viewModel.getAudiobooks().get(0).getTitle());
         }
     }
     ```
   - Тестування Properties: `assertEquals("Expected", viewModel.titleProperty().get())`.
   - `::code-group` — кілька unit-тестів для різних сценаріїв.

3. **Тестування асинхронних операцій** (~150 рядків)
   - Проблема: `loadAudiobooks()` використовує Task → асинхронне виконання.
   - Рішення 1: Синхронне виконання у тестах (без Task).
   - Рішення 2: `CountDownLatch` або `CompletableFuture` для очікування завершення.
   - Приклад:
     ```java
     @Test
     void shouldLoadAudiobooksAsync() throws InterruptedException {
         // Given
         CountDownLatch latch = new CountDownLatch(1);
         when(repository.findAll()).thenReturn(audiobooks);
         
         // When
         viewModel.getAudiobooks().addListener((ListChangeListener<AudiobookViewModel>) c -> {
             latch.countDown();
         });
         viewModel.loadAudiobooks();
         
         // Then
         assertTrue(latch.await(5, TimeUnit.SECONDS));
         assertEquals(2, viewModel.getAudiobooks().size());
     }
     ```
   - `::warning` — "Асинхронні тести складніші та повільніші — розгляньте синхронний режим для unit-тестів."

4. **Тестування валідації** (~120 рядків)
   - Перевірка валідаційної логіки:
     ```java
     @Test
     void shouldSetErrorWhenTitleIsEmpty() {
         // When
         viewModel.titleProperty().set("");
         
         // Then
         assertNotNull(viewModel.titleErrorProperty().get());
         assertTrue(viewModel.titleErrorProperty().get().contains("required"));
     }
     
     @Test
     void shouldClearErrorWhenTitleIsValid() {
         // Given
         viewModel.titleProperty().set("");
         
         // When
         viewModel.titleProperty().set("Valid Title");
         
         // Then
         assertNull(viewModel.titleErrorProperty().get());
     }
     ```
   - Тестування `isValidProperty`: `assertFalse(viewModel.isValidProperty().get())`.

5. **Тестування Commands** (~100 рядків)
   - Перевірка, що Command викликає правильний метод:
     ```java
     @Test
     void shouldDeleteSelectedAudiobook() {
         // Given
         AudiobookViewModel selected = new AudiobookViewModel(audiobook1);
         viewModel.setSelectedAudiobook(selected);
         
         // When
         viewModel.deleteSelected();
         
         // Then
         verify(repository).delete(audiobook1.getId());
         assertFalse(viewModel.getAudiobooks().contains(selected));
     }
     ```
   - Тестування `canExecute`: `assertFalse(viewModel.getDeleteCommand().canExecute())` коли нічого не обрано.

6. **Інтеграційне тестування: ViewModel + Repository** (~150 рядків)
   - Тестування з реальною базою даних (H2 in-memory):
     ```java
     @ExtendWith(GuiceExtension.class)
     @GuiceModules(TestModule.class)
     class AudiobookListViewModelIntegrationTest {
         @Inject
         private AudiobookRepository repository;
         
         @Inject
         private AudiobookListViewModel viewModel;
         
         @Test
         void shouldLoadAudiobooksFromDatabase() {
             // Given
             repository.save(audiobook1);
             repository.save(audiobook2);
             
             // When
             viewModel.loadAudiobooks();
             
             // Then
             assertEquals(2, viewModel.getAudiobooks().size());
         }
     }
     ```
   - Використання Testcontainers для PostgreSQL (якщо потрібно).
   - `::note` — "Інтеграційні тести повільніші, але перевіряють реальну взаємодію компонентів."

7. **UI-тестування з TestFX** (~200 рядків)
   - Що таке TestFX: фреймворк для автоматизованого тестування JavaFX UI.
   - Приклад тесту:
     ```java
     @ExtendWith(ApplicationExtension.class)
     class AudiobookListViewTest extends ApplicationTest {
         @Override
         public void start(Stage stage) {
             // Завантаження FXML та ініціалізація
             FXMLLoader loader = new FXMLLoader(getClass().getResource("audiobook-list-view.fxml"));
             Parent root = loader.load();
             stage.setScene(new Scene(root));
             stage.show();
         }
         
         @Test
         void shouldDisplayAudiobooksInTable(FxRobot robot) {
             // Given: дані вже завантажені у ViewModel
             
             // Then
             TableView<AudiobookViewModel> table = robot.lookup("#audiobookTable").query();
             assertEquals(2, table.getItems().size());
         }
         
         @Test
         void shouldOpenFormWhenAddButtonClicked(FxRobot robot) {
             // When
             robot.clickOn("#addButton");
             
             // Then
             robot.lookup(".dialog-pane").query(); // Діалог відкрився
         }
     }
     ```
   - Селектори: `#id`, `.css-class`, `"Button Text"`.
   - `::warning` — "UI-тести найповільніші та найкрихкіші — використовуйте їх для критичних user flows."

8. **Test Doubles: Mock, Stub, Fake** (~120 рядків)
   - **Mock**: перевірка взаємодії (`verify(repository).save(any())`).
   - **Stub**: повернення заздалегідь визначених даних (`when(repo.findAll()).thenReturn(list)`).
   - **Fake**: спрощена реалізація (InMemoryRepository для тестів).
   - Коли що використовувати: Mock для unit, Fake для integration.
   - `::tabs` — приклади Mock vs Stub vs Fake.

9. **Практичні завдання** (~80 рядків)
   - Рівень 1: Написати unit-тест для ViewModel з валідацією.
   - Рівень 2: Створити інтеграційний тест з H2 in-memory database.
   - Рівень 3: Реалізувати TestFX-тест для форми додавання аудіокниги.

10. **Підсумок** (~30 рядків)

---


**Файл:** `content/04.java/pr2/32.mvvm-navigation-screen-management.md`  
**Обсяг:** ~1000–1200 рядків

#### Зміст

1. **Вступ: Проблема переходів між екранами** (~80 рядків)
   - Hook: "Користувач натискає 'Add Audiobook' → відкривається форма → після збереження повертається до списку. Хто керує цим процесом? Controller? ViewModel?"
   - Проблема: навігація — це UI-логіка, але ViewModel не повинен знати про Stage та Scene.
   - Рішення: Navigator/ScreenManager — окремий компонент для управління екранами.

2. **Патерни навігації у desktop-додатках** (~120 рядків)
   - **Single Window Navigation**: заміна вмісту одного вікна (BorderPane.setCenter()).
   - **Multiple Windows**: відкриття нових Stage (діалоги, модальні вікна).
   - **Wizard Pattern**: покрокова навігація (Next/Previous).
   - `::card-group` — три патерни з прикладами використання.

3. **Navigator Pattern: Централізоване управління навігацією** (~200 рядків)
   - Інтерфейс `Navigator`:
     ```java
     public interface Navigator {
         void navigateTo(String screenId);
         void navigateTo(String screenId, Map<String, Object> params);
         void openDialog(String screenId);
         void closeCurrentDialog();
         void goBack();
     }
     ```
   - Реалізація `FxmlNavigator`:
     ```java
     public class FxmlNavigator implements Navigator {
         private final Injector injector;
         private final Stage primaryStage;
         private final Map<String, String> screenRegistry;
         private final Stack<Parent> navigationStack;
         
         @Override
         public void navigateTo(String screenId) {
             String fxmlPath = screenRegistry.get(screenId);
             Parent root = loadFxml(fxmlPath);
             navigationStack.push(root);
             primaryStage.getScene().setRoot(root);
         }
         
         private Parent loadFxml(String path) {
             FXMLLoader loader = new FXMLLoader(getClass().getResource(path));
             loader.setControllerFactory(injector::getInstance);
             return loader.load();
         }
     }
     ```
   - `::steps` — покрокова реалізація Navigator.

4. **Screen Registry: Реєстрація екранів** (~120 рядків)
   - Проблема: жорстке кодування шляхів до FXML у кожному місці.
   - Рішення: централізований реєстр екранів:
     ```java
     public class ScreenRegistry {
         private final Map<String, String> screens = new HashMap<>();
         
         public ScreenRegistry() {
             screens.put("audiobook-list", "/fxml/audiobook-list-view.fxml");
             screens.put("audiobook-form", "/fxml/audiobook-form-view.fxml");
             screens.put("author-list", "/fxml/author-list-view.fxml");
         }
         
         public String getFxmlPath(String screenId) {
             return screens.get(screenId);
         }
     }
     ```
   - Конфігурація у Guice Module: `bind(ScreenRegistry.class).in(Singleton.class)`.

5. **Передача параметрів між екранами** (~150 рядків)
   - Проблема: як передати `Audiobook` з списку у форму редагування?
   - **Підхід 1**: Через ViewModel (Singleton ViewModel зберігає selectedItem).
   - **Підхід 2**: Через параметри Navigator:
     ```java
     navigator.navigateTo("audiobook-form", Map.of("audiobook", selectedAudiobook));
     ```
   - **Підхід 3**: Через AssistedInject (фабрика створює ViewModel з параметром).
   - Порівняння підходів: простота vs гнучкість vs type-safety.
   - `::tabs` — три підходи з прикладами коду.

6. **Модальні діалоги: openDialog() та результат** (~150 рядків)
   - Відкриття модального вікна:
     ```java
     public <T> Optional<T> openDialog(String screenId) {
         Stage dialog = new Stage();
         dialog.initModality(Modality.APPLICATION_MODAL);
         
         Parent root = loadFxml(screenRegistry.getFxmlPath(screenId));
         dialog.setScene(new Scene(root));
         dialog.showAndWait();
         
         // Отримання результату з ViewModel
         Object controller = loader.getController();
         if (controller instanceof DialogController) {
             return ((DialogController<T>) controller).getResult();
         }
         return Optional.empty();
     }
     ```
   - Приклад: діалог "Select Author" → повернення обраного Author у головний екран.
   - `::note` — "`showAndWait()` блокує виконання до закриття діалогу."

7. **Navigation Stack: історія переходів та goBack()** (~120 рядків)
   - Збереження історії навігації у Stack:
     ```java
     private final Stack<Parent> navigationStack = new Stack<>();
     
     @Override
     public void goBack() {
         if (navigationStack.size() > 1) {
             navigationStack.pop(); // Видалити поточний
             Parent previous = navigationStack.peek();
             primaryStage.getScene().setRoot(previous);
         }
     }
     ```
   - Кнопка "Back" у UI → виклик `navigator.goBack()`.
   - `::warning` — "Stack може зростати необмежено — розгляньте обмеження розміру або очищення при певних умовах."

8. **Інтеграція Navigator з ViewModel** (~120 рядків)
   - ViewModel не повинен знати про Navigator безпосередньо (порушення MVVM).
   - Рішення: Events або Callbacks:
     ```java
     public class AudiobookListViewModel {
         private final ObjectProperty<NavigationRequest> navigationRequest = new SimpleObjectProperty<>();
         
         public void onAddClicked() {
             navigationRequest.set(new NavigationRequest("audiobook-form"));
         }
         
         public ObjectProperty<NavigationRequest> navigationRequestProperty() {
             return navigationRequest;
         }
     }
     ```
   - Controller слухає navigationRequest та викликає Navigator:
     ```java
     viewModel.navigationRequestProperty().addListener((obs, old, request) -> {
         if (request != null) {
             navigator.navigateTo(request.getScreenId(), request.getParams());
             viewModel.navigationRequestProperty().set(null); // Reset
         }
     });
     ```

9. **Повний приклад: Додаток з навігацією** (~150 рядків)
   - Структура: MainView (BorderPane з меню) → центральна частина змінюється при навігації.
   - Меню: "Audiobooks", "Authors", "Genres" → кожна кнопка викликає `navigator.navigateTo()`.
   - Повний код Navigator, ScreenRegistry, інтеграція з Guice.
   - `::code-tree` — структура проєкту з навігацією.

10. **Практичні завдання** (~80 рядків)
    - Рівень 1: Реалізувати простий Navigator з переходом між двома екранами.
    - Рівень 2: Додати модальний діалог з поверненням результату.
    - Рівень 3: Реалізувати Wizard Pattern (покрокова форма з Next/Previous/Finish).

11. **Підсумок** (~30 рядків)

---


**Файл:** `content/04.java/pr2/31.mvvm-validation-error-handling.md`  
**Обсяг:** ~1000–1200 рядків

#### Зміст

1. **Вступ: Валідація — частина презентаційної логіки** (~80 рядків)
   - Hook: "Користувач вводить тривалість аудіокниги: '-10'. Де перевірити, що це неправильно? У Repository? У Service? Ні — у ViewModel."
   - Валідація у MVVM: перевірка даних перед передачею у Model.
   - Два рівні валідації: UI-рівень (формат, обов'язковість) та бізнес-рівень (унікальність, бізнес-правила).

2. **Валідація на рівні Properties** (~150 рядків)
   - **Reactive Validation**: валідація при кожній зміні Property.
   - Приклад: `titleProperty` → перевірка на порожність → `titleErrorProperty`.
   - Реалізація:
     ```java
     private final StringProperty title = new SimpleStringProperty();
     private final StringProperty titleError = new SimpleStringProperty();
     
     public AudiobookFormViewModel() {
         title.addListener((obs, old, newVal) -> {
             if (newVal == null || newVal.trim().isEmpty()) {
                 titleError.set("Title is required");
             } else if (newVal.length() > 255) {
                 titleError.set("Title is too long (max 255 characters)");
             } else {
                 titleError.set(null);
             }
         });
     }
     ```
   - Binding у View: `errorLabel.textProperty().bind(viewModel.titleErrorProperty())`.

3. **Validator Pattern: Централізована валідація** (~150 рядків)
   - Проблема: валідація розкидана по всьому ViewModel → дублювання.
   - Рішення: окремий клас `Validator<T>`:
     ```java
     public interface Validator<T> {
         ValidationResult validate(T value);
     }
     
     public class ValidationResult {
         private final boolean valid;
         private final String errorMessage;
         
         public static ValidationResult success() {
             return new ValidationResult(true, null);
         }
         
         public static ValidationResult error(String message) {
             return new ValidationResult(false, message);
         }
     }
     ```
   - Приклад: `TitleValidator`, `DurationValidator`, `EmailValidator`.
   - `::code-group` — кілька Validators з прикладами.

4. **Композиція валідаторів: CompositeValidator** (~120 рядків)
   - Об'єднання кількох валідаторів для одного поля:
     ```java
     public class CompositeValidator<T> implements Validator<T> {
         private final List<Validator<T>> validators;
         
         @Override
         public ValidationResult validate(T value) {
             for (Validator<T> validator : validators) {
                 ValidationResult result = validator.validate(value);
                 if (!result.isValid()) {
                     return result;
                 }
             }
             return ValidationResult.success();
         }
     }
     ```
   - Використання: `new CompositeValidator<>(notEmptyValidator, maxLengthValidator, noSpecialCharsValidator)`.

5. **Валідація форми: isValidProperty** (~150 рядків)
   - Агрегація валідності всіх полів у одну BooleanProperty:
     ```java
     private final BooleanProperty isValid = new SimpleBooleanProperty();
     
     public AudiobookFormViewModel() {
         BooleanBinding titleValid = titleError.isNull();
         BooleanBinding durationValid = durationError.isNull();
         BooleanBinding authorValid = selectedAuthor.isNotNull();
         
         isValid.bind(titleValid.and(durationValid).and(authorValid));
     }
     ```
   - Binding кнопки "Save": `saveButton.disableProperty().bind(viewModel.isValidProperty().not())`.
   - `::mermaid` — flowchart: Properties → Validators → Error Properties → isValid → Button.disable.

6. **Асинхронна валідація: перевірка унікальності** (~150 рядків)
   - Проблема: перевірка унікальності username потребує запиту до БД.
   - Рішення: асинхронна валідація через Task:
     ```java
     public void validateUsernameUniqueness(String username) {
         Task<Boolean> task = new Task<>() {
             @Override
             protected Boolean call() {
                 return userRepository.existsByUsername(username);
             }
         };
         task.setOnSucceeded(e -> {
             if (task.getValue()) {
                 usernameError.set("Username already exists");
             } else {
                 usernameError.set(null);
             }
         });
         executor.submit(task);
     }
     ```
   - Debouncing: не перевіряти при кожному натисканні клавіші, а з затримкою.
   - `::warning` — "Асинхронна валідація може призвести до race conditions — використовуйте debouncing."

7. **Обробка помилок Repository та Service** (~150 рядків)
   - Виняток у Repository → перехоплення у ViewModel → відображення у View.
   - Приклад:
     ```java
     public void saveAudiobook() {
         try {
             Audiobook audiobook = mapToModel();
             audiobookRepository.save(audiobook);
             successMessage.set("Audiobook saved successfully");
         } catch (DataAccessException e) {
             errorMessage.set("Failed to save audiobook: " + e.getMessage());
             logger.error("Error saving audiobook", e);
         }
     }
     ```
   - Типи помилок: валідаційні (показуємо біля поля), системні (показуємо Alert), критичні (логуємо + повідомляємо адміністратора).

8. **Відображення помилок у View** (~120 рядків)
   - **Inline errors**: Label біля TextField з червоним текстом.
   - **Toast notifications**: тимчасове повідомлення у куті екрану.
   - **Alert dialogs**: модальне вікно для критичних помилок.
   - Приклад Toast через ControlsFX:
     ```java
     Notifications.create()
         .title("Error")
         .text(viewModel.getErrorMessage())
         .showError();
     ```
   - `::tabs` — три способи відображення помилок з прикладами.

9. **Практичні завдання** (~80 рядків)
   - Рівень 1: Створити Validator для email-адреси з regex-перевіркою.
   - Рівень 2: Реалізувати форму з валідацією всіх полів та isValidProperty.
   - Рівень 3: Додати асинхронну валідацію унікальності з debouncing.

10. **Підсумок** (~30 рядків)

---


**Файл:** `content/04.java/pr2/30.mvvm-guice-integration.md`  
**Обсяг:** ~1200–1400 рядків

#### Зміст

1. **Вступ: Проблема ручного створення ViewModel** (~100 рядків)
   - Hook: "Ви побудували ViewModel, Controller, Repository. Але хто створює ці об'єкти? Хто передає Repository у ViewModel? Хто передає ViewModel у Controller?"
   - Наївний підхід: ручне створення у `Application.start()` → граф залежностей стає некерованим.
   - Рішення: Guice автоматично створює та впроваджує всі залежності.

2. **Архітектура інтеграції: Guice + JavaFX** (~120 рядків)
   - **Guice Injector**: центральний контейнер, що створює об'єкти.
   - **Module**: конфігурація bindings (Repository → JdbcRepository, DataSource → HikariCP).
   - **ControllerFactory**: міст між FXMLLoader та Guice — створює Controllers через Injector.
   - `::mermaid` — component diagram: Application → Injector → Module → ControllerFactory → FXMLLoader → Controller → ViewModel → Repository.

3. **Guice Module для JavaFX-додатку** (~150 рядків)
   - Створення `AudiobookModule`:
     ```java
     public class AudiobookModule extends AbstractModule {
         @Override
         protected void configure() {
             bind(DataSource.class).toProvider(HikariDataSourceProvider.class).in(Singleton.class);
             bind(AudiobookRepository.class).to(JdbcAudiobookRepository.class);
             bind(AuthorRepository.class).to(JdbcAuthorRepository.class);
             bind(GenreRepository.class).to(JdbcGenreRepository.class);
         }
         
         @Provides
         @Singleton
         AudiobookListViewModel provideAudiobookListViewModel(AudiobookRepository repo) {
             return new AudiobookListViewModel(repo);
         }
     }
     ```
   - `::note` — "Singleton scope для Repository — одна інстанція на весь додаток."

4. **Custom ControllerFactory: Ін'єкція Controllers через Guice** (~200 рядків)
   - Проблема: FXMLLoader створює Controllers через `Class.newInstance()` — без Guice.
   - Рішення: `FXMLLoader.setControllerFactory(injector::getInstance)`.
   - Приклад:
     ```java
     public class GuiceControllerFactory implements Callback<Class<?>, Object> {
         private final Injector injector;
         
         public GuiceControllerFactory(Injector injector) {
             this.injector = injector;
         }
         
         @Override
         public Object call(Class<?> type) {
             return injector.getInstance(type);
         }
     }
     ```
   - Використання:
     ```java
     FXMLLoader loader = new FXMLLoader(getClass().getResource("AudiobookListView.fxml"));
     loader.setControllerFactory(new GuiceControllerFactory(injector));
     Parent root = loader.load();
     ```
   - `::code-group` — без Guice vs з Guice (порівняння коду).

5. **Ін'єкція ViewModel у Controller через конструктор** (~150 рядків)
   - Controller з `@Inject`:
     ```java
     public class AudiobookListController {
         @FXML private TableView<AudiobookViewModel> audiobookTable;
         
         private final AudiobookListViewModel viewModel;
         
         @Inject
         public AudiobookListController(AudiobookListViewModel viewModel) {
             this.viewModel = viewModel;
         }
         
         @FXML
         public void initialize() {
             audiobookTable.setItems(viewModel.getAudiobooks());
             viewModel.loadAudiobooks();
         }
     }
     ```
   - Guice автоматично створює ViewModel та впроваджує у Controller.
   - `::tip` — "Конструкторна ін'єкція — найбезпечніший спосіб: всі залежності гарантовано присутні."

6. **Scopes у JavaFX: Singleton vs Prototype** (~150 рядків)
   - **Singleton**: один екземпляр на весь додаток (Repository, DataSource, Service).
   - **Prototype** (без scope): новий екземпляр при кожному запиті (ViewModel для діалогів).
   - Проблема: якщо ViewModel — Singleton, то при відкритті двох вікон буде конфлікт стану.
   - Рішення: ViewModel для головних екранів — Singleton, для діалогів — Prototype.
   - `::warning` — "Будьте обережні з Singleton ViewModel — переконайтеся, що стан не конфліктує між екранами."

7. **Lifecycle Management: Ініціалізація та Shutdown** (~120 рядків)
   - Ініціалізація Guice у `Application.start()`:
     ```java
     public class AudiobookApp extends Application {
         private Injector injector;
         
         @Override
         public void start(Stage primaryStage) {
             injector = Guice.createInjector(new AudiobookModule());
             
             FXMLLoader loader = new FXMLLoader(getClass().getResource("main-view.fxml"));
             loader.setControllerFactory(injector::getInstance);
             Parent root = loader.load();
             
             primaryStage.setScene(new Scene(root));
             primaryStage.show();
         }
         
         @Override
         public void stop() {
             // Закриття ресурсів (DataSource, тощо)
             injector.getInstance(DataSource.class).close();
         }
     }
     ```
   - `::note` — "`stop()` викликається при закритті додатку — ідеальне місце для cleanup."

8. **Assisted Injection: Параметризовані ViewModel** (~150 рядків)
   - Проблема: ViewModel потребує параметр (наприклад, `AudiobookDetailViewModel(Audiobook audiobook)`).
   - Рішення: Guice AssistedInject — фабрика для створення ViewModel з параметрами.
   - Приклад:
     ```java
     public interface AudiobookDetailViewModelFactory {
         AudiobookDetailViewModel create(Audiobook audiobook);
     }
     
     public class AudiobookDetailViewModel {
         @Inject
         public AudiobookDetailViewModel(@Assisted Audiobook audiobook, AudiobookRepository repo) {
             // ...
         }
     }
     ```
   - Конфігурація у Module: `install(new FactoryModuleBuilder().build(AudiobookDetailViewModelFactory.class))`.

9. **Повний приклад: Додаток з Guice + MVVM** (~150 рядків)
   - Структура проєкту: Module, Application, Controllers, ViewModels, Repositories.
   - Повний код `AudiobookApp` з ініціалізацією Guice та завантаженням головного екрану.
   - `::code-tree` — структура директорій проєкту.

10. **Практичні завдання** (~80 рядків)
    - Рівень 1: Налаштувати Guice Module для простого додатку з одним Repository.
    - Рівень 2: Реалізувати ControllerFactory та інтегрувати з FXMLLoader.
    - Рівень 3: Створити додаток з кількома екранами, кожен з власним ViewModel, всі через Guice.

11. **Підсумок** (~30 рядків)

---


**Файл:** `content/04.java/pr2/29.mvvm-view-controller.md`  
**Обсяг:** ~1000–1200 рядків

#### Зміст

1. **Вступ: Роль Controller у MVVM** (~80 рядків)
   - Hook: "У MVP Controller — це мозок додатку. У MVVM — це лише 'клей' між FXML та ViewModel. Чому?"
   - Controller у MVVM: мінімальний, лише ініціалізація bindings та передача подій до ViewModel.
   - Принцип: вся логіка у ViewModel, Controller — лише технічний адаптер.

2. **FXML: Декларативний опис UI** (~150 рядків)
   - Структура FXML-файлу: `<?xml version>`, `<BorderPane>`, `fx:controller`.
   - Приклад: `audiobook-list-view.fxml` з TableView, кнопками "Add", "Delete", "Refresh".
   - Атрибут `fx:id` — зв'язок з полями Controller.
   - `::code-tree` — структура проєкту: `resources/fxml/audiobook-list-view.fxml`, `controller/AudiobookListController.java`.

3. **Controller: Ін'єкція FXML-компонентів** (~120 рядків)
   - Анотація `@FXML` для полів: `@FXML private TableView<AudiobookViewModel> audiobookTable;`.
   - Метод `initialize()`: викликається після завантаження FXML.
   - Приклад:
     ```java
     public class AudiobookListController {
         @FXML private TableView<AudiobookViewModel> audiobookTable;
         @FXML private Button deleteButton;
         
         private AudiobookListViewModel viewModel;
         
         @FXML
         public void initialize() {
             // Ініціалізація bindings
         }
     }
     ```
   - `::note` — "`initialize()` — це конструктор для FXML-контролерів."

4. **Bindings: Зв'язування View з ViewModel** (~200 рядків)
   - **TableView ↔ ObservableList**: `audiobookTable.setItems(viewModel.getAudiobooks())`.
   - **TableColumn ↔ Property**: `titleColumn.setCellValueFactory(cellData -> cellData.getValue().titleProperty())`.
   - **Button.disable ↔ BooleanProperty**: `deleteButton.disableProperty().bind(viewModel.selectedAudiobookProperty().isNull())`.
   - **TextField ↔ StringProperty**: `searchField.textProperty().bindBidirectional(viewModel.searchQueryProperty())`.
   - Повний приклад ініціалізації bindings у `initialize()`.
   - `::code-group` — FXML + Controller з bindings.

5. **Event Handlers: Делегування до ViewModel** (~120 рядків)
   - Кнопка "Refresh": `@FXML private void onRefreshClicked() { viewModel.loadAudiobooks(); }`.
   - Кнопка "Delete": `@FXML private void onDeleteClicked() { viewModel.deleteSelected(); }`.
   - Selection change: `audiobookTable.getSelectionModel().selectedItemProperty().addListener((obs, old, selected) -> viewModel.setSelectedAudiobook(selected));`.
   - `::warning` — "Controller НЕ містить бізнес-логіки — лише виклики методів ViewModel."

6. **FXMLLoader та ін'єкція ViewModel** (~150 рядків)
   - Проблема: як передати ViewModel у Controller?
   - Рішення 1: Setter-ін'єкція після завантаження FXML.
   - Рішення 2: Custom ControllerFactory (підготовка до Guice).
   - Приклад:
     ```java
     FXMLLoader loader = new FXMLLoader(getClass().getResource("AudiobookListView.fxml"));
     Parent root = loader.load();
     AudiobookListController controller = loader.getController();
     controller.setViewModel(viewModel);
     ```
   - `::steps` — покрокове завантаження FXML з ін'єкцією ViewModel.

7. **Діалоги та навігація між екранами** (~120 рядків)
   - Відкриття нового вікна: `Stage dialog = new Stage(); dialog.setScene(new Scene(root));`.
   - Модальні діалоги: `dialog.initModality(Modality.APPLICATION_MODAL)`.
   - Передача даних між екранами: через ViewModel або через параметри конструктора.
   - Приклад: діалог "Add Audiobook" → повернення результату у головний екран.

8. **Обробка помилок у View** (~100 рядків)
   - `errorMessageProperty` у ViewModel → Label у View.
   - Binding: `errorLabel.textProperty().bind(viewModel.errorMessageProperty())`.
   - Відображення Alert при критичних помилках:
     ```java
     viewModel.errorMessageProperty().addListener((obs, old, error) -> {
         if (error != null && !error.isEmpty()) {
             Alert alert = new Alert(Alert.AlertType.ERROR, error);
             alert.showAndWait();
         }
     });
     ```

9. **Практичні завдання** (~80 рядків)
   - Рівень 1: Створити FXML з ListView та кнопкою, зв'язати з ViewModel через Controller.
   - Рівень 2: Реалізувати форму редагування автора з bidirectional bindings.
   - Рівень 3: Побудувати master-detail інтерфейс з навігацією між екранами.

10. **Підсумок** (~30 рядків)

---


**Файл:** `content/04.java/pr2/28.mvvm-viewmodel-implementation.md`  
**Обсяг:** ~1200–1400 рядків

#### Зміст

1. **Вступ: Від теорії до коду** (~80 рядків)
   - Hook: "Ми знаємо, що MVVM — це правильно. Але як саме виглядає ViewModel? Які методи? Які Properties? Як він взаємодіє з Repository?"
   - Мета статті: покрокова побудова `AudiobookListViewModel` для екрану списку аудіокниг.

2. **Анатомія ViewModel: Структура та відповідальності** (~150 рядків)
   - **Презентаційна логіка**: форматування дат, обчислення тривалості у годинах/хвилинах.
   - **Стан UI**: обраний елемент, режим редагування, повідомлення про помилки.
   - **Commands**: методи для дій користувача (`loadAudiobooks()`, `deleteSelected()`, `addToCollection()`).
   - **Properties**: `ObservableList<AudiobookViewModel>`, `selectedAudiobookProperty`, `isLoadingProperty`, `errorMessageProperty`.
   - `::note` — "ViewModel — це адаптер між Domain Model (Audiobook) та View (TableView)."

3. **Wrapper Pattern: AudiobookViewModel як обгортка** (~150 рядків)
   - Чому не використовувати `Audiobook` безпосередньо у View: Domain-об'єкт не має Properties.
   - `AudiobookViewModel` обгортає `Audiobook` та експонує Properties:
     ```java
     public class AudiobookViewModel {
         private final Audiobook audiobook;
         private final StringProperty title;
         private final StringProperty authorName;
         private final StringProperty formattedDuration;
         
         public AudiobookViewModel(Audiobook audiobook) {
             this.audiobook = audiobook;
             this.title = new SimpleStringProperty(audiobook.getTitle());
             this.authorName = new SimpleStringProperty(audiobook.getAuthor().getFullName());
             this.formattedDuration = new SimpleStringProperty(formatDuration(audiobook.getDuration()));
         }
     }
     ```
   - Двостороння синхронізація: зміна у Property → оновлення Domain-об'єкта.
   - `::code-group` — Domain Model vs ViewModel (порівняння структури).

4. **Побудова AudiobookListViewModel: Крок за кроком** (~250 рядків)
   - **Крок 1**: Оголошення залежностей (Repository через конструктор).
   - **Крок 2**: Ініціалізація Properties (`audiobooks = FXCollections.observableArrayList()`).
   - **Крок 3**: Метод `loadAudiobooks()` — виклик Repository, маппінг у ViewModel, оновлення ObservableList.
   - **Крок 4**: Обробка помилок — `errorMessageProperty` для відображення у View.
   - **Крок 5**: Метод `deleteSelected()` — видалення через Repository, оновлення списку.
   - Повний код `AudiobookListViewModel` з коментарями.
   - `::steps` — покрокова побудова ViewModel.

5. **Lifecycle ViewModel: Ініціалізація та очищення** (~100 рядків)
   - Метод `initialize()`: завантаження даних при створенні ViewModel.
   - Метод `dispose()`: відписка від listeners, закриття ресурсів.
   - Чому це важливо: уникнення memory leaks.
   - `::warning` — "Завжди викликайте dispose() при закритті View, інакше ViewModel залишиться в пам'яті."

6. **Commands у MVVM: Інкапсуляція дій** (~150 рядків)
   - Проблема: кнопка "Delete" має бути неактивною, якщо нічого не обрано.
   - Рішення: Command Pattern — об'єкт, що інкапсулює дію та її доступність.
   - Приклад: `RelayCommand` (простий Command для JavaFX):
     ```java
     public class RelayCommand {
         private final Runnable action;
         private final BooleanProperty canExecute;
         
         public void execute() {
             if (canExecute.get()) action.run();
         }
     }
     ```
   - Binding: `deleteButton.disableProperty().bind(deleteCommand.canExecuteProperty().not())`.
   - `::code-collapse` — повна реалізація RelayCommand.

7. **Асинхронність у ViewModel: Task та Platform.runLater()** (~150 рядків)
   - Проблема: `loadAudiobooks()` виконує JDBC-запит → блокує UI-потік.
   - Рішення: `javafx.concurrent.Task` — фонове виконання з автоматичним поверненням у UI-потік.
   - Приклад:
     ```java
     public void loadAudiobooks() {
         Task<List<Audiobook>> task = new Task<>() {
             @Override
             protected List<Audiobook> call() {
                 return audiobookRepository.findAll();
             }
         };
         task.setOnSucceeded(e -> {
             List<Audiobook> result = task.getValue();
             audiobooks.setAll(result.stream()
                 .map(AudiobookViewModel::new)
                 .collect(Collectors.toList()));
         });
         new Thread(task).start();
     }
     ```
   - `::tip` — "Task автоматично повертається у JavaFX Application Thread при setOnSucceeded()."

8. **Тестування ViewModel без UI** (~120 рядків)
   - Переваги MVVM: ViewModel тестується як звичайний Java-клас.
   - Приклад unit-тесту:
     ```java
     @Test
     void shouldLoadAudiobooks() {
         // Given
         when(repository.findAll()).thenReturn(List.of(audiobook1, audiobook2));
         
         // When
         viewModel.loadAudiobooks();
         
         // Then
         assertEquals(2, viewModel.getAudiobooks().size());
     }
     ```
   - `::note` — "Для тестування Properties використовуйте JUnit + Mockito, без запуску JavaFX."

9. **Практичні завдання** (~80 рядків)
   - Рівень 1: Створити `GenreViewModel` з Properties для назви та опису.
   - Рівень 2: Реалізувати `AuthorListViewModel` з методами `loadAuthors()` та `deleteSelected()`.
   - Рівень 3: Додати до `AudiobookListViewModel` фільтрацію за жанром (FilteredList + Predicate).

10. **Підсумок** (~30 рядків)

---


**Файл:** `content/04.java/pr2/27.ui-architecture-patterns.md`  
**Обсяг:** ~1000–1200 рядків

#### Зміст

1. **Вступ: Чому "все в одному класі" — це проблема** (~100 рядків)
   - Hook: "Ви створили контролер JavaFX. У ньому 500 рядків: JDBC-запити, валідація, обробка кліків, форматування дат. Як це тестувати? Як повторно використати логіку?"
   - Проблема God Object: контролер знає все і робить все.
   - Необхідність розділення відповідальностей: UI ↔ Логіка ↔ Дані.

2. **Model-View-Controller (MVC): Класичний підхід** (~150 рядків)
   - Історія: Trygve Reenskaug, Smalltalk-80 (1979).
   - **Model**: дані та бізнес-логіка.
   - **View**: відображення даних.
   - **Controller**: обробка введення користувача, оновлення Model.
   - Потік даних: User → Controller → Model → View.
   - Проблема в desktop-додатках: View часто безпосередньо спостерігає за Model (Observer pattern) → складність.
   - `::mermaid` — sequence diagram: User clicks → Controller updates Model → Model notifies View → View re-renders.

3. **Model-View-Presenter (MVP): Пасивний View** (~150 рядків)
   - Еволюція MVC для desktop (Taligent, 1990-ті).
   - **Presenter**: посередник між View та Model. View стає "дурним" — не знає про Model.
   - View реалізує інтерфейс (наприклад, `ITrackListView`), Presenter викликає методи цього інтерфейсу.
   - Переваги: View легко замінити (навіть на mock у тестах), Presenter тестується без UI.
   - Недолік: багато boilerplate-коду (для кожної взаємодії потрібен метод в інтерфейсі View).
   - `::plant-uml` — class diagram: Presenter → IView (interface) ← TrackListView (implementation).

4. **Model-View-ViewModel (MVVM): Реактивність через Bindings** (~200 рядків)
   - Історія: Microsoft, WPF (2005), John Gossman.
   - **ViewModel**: проміжний шар між View та Model, що містить **презентаційну логіку** та **стан UI**.
   - Ключова відмінність: View **автоматично синхронізується** з ViewModel через **Data Binding** (Properties у JavaFX).
   - ViewModel не знає про View (на відміну від Presenter у MVP).
- Приклад: `ViewModel.titleProperty()` ← `TextField.textProperty()` (bidirectional binding).

5. **Порівняльна таблиця: MVC vs MVP vs MVVM** (~120 рядків)
   - `::card-group` — три картки з характеристиками кожного патерну.
   - Таблиця: View знає про Model? Testability? Boilerplate? Підходить для JavaFX?
   - `::note` — "MVVM — природний вибір для JavaFX завдяки вбудованій системі Properties та Bindings."

6. **Чому MVVM для JavaFX: Технічне обґрунтування** (~150 рядків)
   - JavaFX Properties — це готова інфраструктура для MVVM.
   - FXML + ViewModel: розділення UI-розмітки та логіки.
   - Тестування: ViewModel тестується без запуску JavaFX Application Thread.
   - Приклад: `TrackListViewModel` з `ObservableList<TrackViewModel>` → `TableView` автоматично відображає зміни.

7. **Анатомія MVVM у JavaFX: Компоненти** (~120 рядків)
   - **Model**: Domain-об'єкти (`Audiobook`, `Author`) + Repository.
   - **ViewModel**: `AudiobookListViewModel` з Properties (`titleProperty`, `selectedAudiobookProperty`), Commands (методи для дій).
   - **View**: FXML + Controller (мінімальний, лише ініціалізація bindings).
   - `::mermaid` — component diagram: View → ViewModel → Service → Repository → Database.

8. **Практичні завдання** (~80 рядків)
   - Рівень 1: Визначити, який патерн використовується у заданому коді (MVC/MVP/MVVM).
   - Рівень 2: Рефакторити God Object контролер на MVVM (виділити ViewModel).
   - Рівень 3: Спроектувати MVVM-архітектуру для екрану "User Profile" (список колекцій, статистика прослуховування).

9. **Підсумок** (~30 рядків)

---


**Файл:** `content/04.java/pr2/26.javafx-properties-bindings.md`  
**Обсяг:** ~1000–1200 рядків

#### Зміст

1. **Вступ: Проблема синхронізації стану** (~100 рядків)
   - Hook: "Користувач вводить назву аудіокниги у TextField. Як автоматично оновити Label з попереднім переглядом? Як зробити кнопку 'Save' активною лише коли всі поля заповнені?"
   - Наївний підхід: слухачі подій + ручне оновлення → спагетті-код.
   - Реактивний підхід: Properties та Bindings — автоматична синхронізація.

2. **JavaFX Properties: Обгортки над значеннями** (~150 рядків)
   - Що таке Property: `StringProperty`, `IntegerProperty`, `BooleanProperty`, `ObjectProperty<T>`.
   - Відмінність від звичайних полів: можливість підписки на зміни.
   - `SimpleStringProperty`, `ReadOnlyStringProperty` — immutable властивості.
   - Приклад: `StringProperty title = new SimpleStringProperty("Unknown")`.
   - `::code-group` — порівняння: звичайне поле vs Property.

3. **Change Listeners: Реакція на зміни** (~120 рядків)
   - `addListener(ChangeListener)` — callback при зміні значення.
   - Приклад: відстеження введення у TextField → валідація у реальному часі.
   - `::warning` — "Listener спрацьовує при кожній зміні — уникайте важких операцій всередині."

4. **Bindings: Декларативна синхронізація** (~200 рядків)
   - **Unidirectional Binding**: `label.textProperty().bind(textField.textProperty())`.
   - **Bidirectional Binding**: `textField.textProperty().bindBidirectional(model.titleProperty())`.
   - **Computed Bindings**: `Bindings.concat()`, `Bindings.when()`, `Bindings.createStringBinding()`.
   - Приклад: кнопка "Save" активна лише коли `title.isNotEmpty() AND duration > 0`.
   - `::mermaid` — flowchart: TextField → Property → Binding → Label (автоматичне оновлення).

5. **Fluent API для складних виразів** (~120 рядків)
   - `titleProperty().isEmpty()` → `BooleanBinding`.
   - `durationProperty().greaterThan(0)` → `BooleanBinding`.
   - Комбінування: `titleEmpty.or(durationInvalid)`.
   - Приклад: `saveButton.disableProperty().bind(titleEmpty.or(durationInvalid))`.

6. **ObservableList та ObservableMap** (~150 рядків)
   - `ObservableList<Audiobook>` — колекція, що повідомляє про зміни.
   - Інтеграція з `ListView` та `TableView`: автоматичне оновлення UI при додаванні/видаленні елементів.
   - Приклад: `tableView.setItems(observableAudiobooks)` → додавання елемента → UI оновлюється автоматично.
   - `::note` — "ObservableList — це міст між вашою моделлю даних та UI."

7. **Практичний приклад: Форма з валідацією** (~150 рядків)
   - Форма додавання аудіокниги: Title (TextField), Duration (Spinner), Author (ComboBox).
   - Валідація: Title не порожній, Duration > 0, Author обраний.
   - Кнопка "Save" активна лише при валідних даних.
   - Повний код з Properties та Bindings.
   - `::code-collapse` — повний приклад форми.

8. **Практичні завдання** (~80 рядків)
   - Рівень 1: Створити TextField та Label, зв'язані через binding (введення → автоматичне відображення).
   - Рівень 2: Реалізувати форму з двома полями, де кнопка активна лише при заповненні обох.
   - Рівень 3: Побудувати калькулятор загальної тривалості аудіокниг у колекції (ObservableList → computed binding).

9. **Підсумок** (~30 рядків)

---


Студенти вже пройшли:
- **Проектування БД** (статті 01-08): Концептуальне/логічне/фізичне моделювання, нормалізація, міграції
- **JDBC та патерни доступу до даних** (статті 09-20): Row/Table Data Gateway, Repository, Data Mapper, Identity Map, Unit of Work, Specification
- **Асинхронність та тестування** (статті 21-23): Асинхронний JDBC, інтеграційні тести з H2 та Testcontainers
- **Dependency Injection** (стаття 24): Google Guice — основи, модулі, скопи, інтеграція з JavaFX

Тепер настав час **з'єднати все разом** у повноцінному JavaFX-додатку з архітектурою MVVM.

---

## Структура модуля (8-10 статей)

### Стаття 25. JavaFX: Основи побудови графічних інтерфейсів

**Файл:** `content/04.java/pr2/25.javafx-fundamentals.md`  
**Обсяг:** ~1000–1200 рядків

#### Зміст

1. **Вступ: Від консолі до вікон** (~100 рядків)
   - Hook: "Ви побудували репозиторії, Unit of Work, Guice-модулі. Але користувач не бачить жодного рядка вашого коду — він бачить лише вікно з кнопками. Як з'єднати ці два світи?"
   - Чому JavaFX, а не Swing: сучасна архітектура, CSS-стилізація, FXML, інтеграція з Java 11+.
   - Історія: JavaFX 2.0 (2011) → JavaFX 8 (2014) → OpenJFX (2018, модульна система).
   - `::note` — JavaFX як частина OpenJDK з Java 11, окремий модуль `javafx.controls`, `javafx.fxml`.

2. **Архітектура JavaFX: Scene Graph та Application Lifecycle** (~150 рядків)
   - **Scene Graph**: ієрархічне дерево вузлів (Node → Parent → Region → Control).
   - **Stage** (вікно) → **Scene** (контейнер) → **Root Node** (кореневий layout).
   - Життєвий цикл `Application`: `init()` → `start(Stage)` → `stop()`.
   - `::mermaid` — діаграма Scene Graph: Stage → Scene → VBox → Button, Label.
   - Візуалізація ієрархії: Stage → Scene → Root (у JavaFX).

3. **Перший JavaFX-додаток: Hello Audiobook Platform** (~120 рядків)
   - Мінімальний приклад: вікно з написом "Audiobook Platform" та кнопкою "Load Tracks".
   - Розбір коду: `Application.launch()`, `Stage.setTitle()`, `Scene`, `VBox`, `Button`.
   - `::code-group` — Java-код + XAML приклад.
   - `::tip` — "JavaFX Application Thread: всі UI-операції мають виконуватись у цьому потоці."

4. **Layout-контейнери: Організація простору** (~150 рядків)
   - **VBox/HBox**: вертикальне/горизонтальне розташування.
   - **BorderPane**: top, bottom, left, right, center — класичний layout для додатків.
   - **GridPane**: табличне розташування (форми).
   - **StackPane**: накладання елементів один на одного.
   - Приклад: BorderPane з меню зверху (HBox), списком треків зліва (ListView), деталями справа (VBox).
   - `::tabs` — кожен layout з прикладом коду та візуалізацією.

5. **Controls: Основні компоненти UI** (~120 рядків)
   - **Button**, **Label**, **TextField**, **TextArea**.
   - **ListView**, **TableView** — відображення колекцій.
   - **ComboBox**, **CheckBox**, **RadioButton**.
   - Приклад: TableView для списку аудіокниг (колонки: Title, Author, Duration).
   - `::field-group` — документація властивостей TableView (items, columns, selectionModel).

6. **Event Handling: Реакція на дії користувача** (~120 рядків)
   - `setOnAction()` для Button.
   - `EventHandler<ActionEvent>` vs лямбда-вирази.
   - Приклад: кнопка "Add to Collection" → виклик методу сервісу.
   - `::warning` — "Не виконуйте тривалі операції (JDBC-запити) у UI-потоці — додаток зависне."

7. **FXML: Декларативний опис інтерфейсу** (~150 рядків)
   - Що таке FXML: XML-розмітка для UI (аналог HTML для веб).
   - Чому FXML: розділення UI та логіки, можливість використання Scene Builder.
   - Приклад: `TrackListView.fxml` з TableView та кнопками.
   - Завантаження FXML: `FXMLLoader.load()`.
   - `::code-group` — FXML + Java-контролер.

8. **Практичні завдання** (~80 рядків)
   - Рівень 1: Створити вікно з формою додавання автора (TextField для імені, Button "Save").
   - Рівень 2: Побудувати TableView для відображення жанрів з можливістю видалення.
   - Рівень 3: Реалізувати master-detail інтерфейс: список аудіокниг зліва, деталі справа.

9. **Підсумок** (~30 рядків)

---

