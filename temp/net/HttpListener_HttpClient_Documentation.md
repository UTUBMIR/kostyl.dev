# 📖 HttpListener та HttpClient: Детальна документація

## Зміст

### HttpListener
1. [Огляд HttpListener](#огляд-httplistener)
2. [Архітектура та життєвий цикл](#архітектура-та-життєвий-цикл-httplistener)
3. [Конфігурація та налаштування](#конфігурація-httplistener)
4. [HttpListenerContext та його компоненти](#httplistenercontext)
5. [HttpListenerRequest - деталі](#httplistenerrequest)
6. [HttpListenerResponse - деталі](#httplistenerresponse)
7. [Робота з префіксами (Prefixes)](#префікси-httplistener)
8. [Автентифікація та безпека](#автентифікація-httplistener)
9. [Обмеження та особливості](#обмеження-httplistener)

### HttpClient
10. [Огляд HttpClient](#огляд-httpclient)
11. [Життєвий цикл HttpClient](#життєвий-цикл-httpclient)
12. [HttpClientHandler та конфігурація](#httpclienthandler)
13. [Методи відправки запитів](#методи-httpclient)
14. [HttpRequestMessage та HttpResponseMessage](#httprequestmessage-та-httpresponsemessage)
15. [Обробка відповідей та контенту](#обробка-контенту)
16. [Таймаути та скасування](#таймаути-та-скасування)
17. [Повторні спроби та resilience](#повторні-спроби)
18. [HttpClient Best Practices](#httpclient-best-practices)
19. [Порівняння підходів](#порівняння-підходів)

---

## Огляд HttpListener

### Що таке HttpListener?

**HttpListener** — це клас у .NET Framework/Core, який надає простий HTTP сервер, керований програмно. Він є оболонкою навколо Windows HTTP Server API (HTTP.sys) на Windows або власної реалізації на інших платформах.

### Основне призначення

- **Створення HTTP серверів** без потреби у повноцінному веб-сервері (IIS, Apache)
- **Легкі HTTP сервіси** для внутрішніх потреб
- **Тестові HTTP endpoints**
- **Webhook receivers**
- **Локальні API для десктопних додатків**
- **Development tools** (локальні сервери для розробки)

### Ключові характеристики

| Характеристика | Опис |
|----------------|------|
| **Простота** | Мінімальна конфігурація для базового HTTP сервера |
| **Низький рівень** | Прямий доступ до HTTP запитів/відповідей |
| **Кросплатформність** | .NET Core/5+ підтримує Windows, Linux, macOS |
| **Продуктивність** | HTTP.sys на Windows забезпечує високу продуктивність |
| **Обмеження** | Немає вбудованої маршрутизації, middleware, DI |

### Namespace та збірка

```
Namespace: System.Net
Assembly: System.dll (.NET Framework)
          System.Net.HttpListener.dll (.NET Core/5+)
```

### Підтримка платформ

- **Windows**: Повна підтримка через HTTP.sys
- **Linux/macOS**: Підтримка через managed implementation (.NET Core 2.0+)
- **.NET Framework**: Windows only
- **.NET Core/5+**: Cross-platform

### Коли використовувати HttpListener

**✅ Використовуйте, коли:**
- Потрібен простий HTTP endpoint без ASP.NET
- Розробляєте desktop додаток з HTTP API
- Потрібен легкий тестовий сервер
- Webhook receiver з мінімальними залежностями
- Прототипування та експерименти

**❌ НЕ використовуйте, коли:**
- Потрібен production веб-сервер зі складною логікою
- Необхідна маршрутизація, middleware, dependency injection
- Потрібні вбудовані features (authentication, CORS, compression)
- Розробляєте повноцінний веб-додаток (використовуйте ASP.NET Core)

---

## Архітектура та життєвий цикл HttpListener

### Архітектура компонентів

```
┌─────────────────────────────────────┐
│         Application Code            │
└──────────────┬──────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│         HttpListener                 │
│  ┌────────────────────────────────┐  │
│  │    Prefixes Collection         │  │
│  │  - http://localhost:8080/      │  │
│  │  - https://example.com/api/    │  │
│  └────────────────────────────────┘  │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│      Platform HTTP Server            │
│  Windows: HTTP.sys (kernel mode)    │
│  Linux/macOS: Managed implementation │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│          Network Layer               │
│          TCP/IP Stack                │
└──────────────────────────────────────┘
```

### Життєвий цикл запиту

#### 1. Ініціалізація

```
HttpListener listener = new HttpListener();
```

**Що відбувається:**
- Створюється екземпляр HttpListener
- Ініціалізуються внутрішні структури даних
- НЕ відбувається прив'язка до портів (ще не активний)

#### 2. Конфігурація

```
listener.Prefixes.Add("http://localhost:8080/");
listener.AuthenticationSchemes = AuthenticationSchemes.Anonymous;
listener.TimeoutManager.IdleConnection = TimeSpan.FromMinutes(5);
```

**Конфігуровані параметри:**
- **Prefixes** - список URL префіксів для прослуховування
- **AuthenticationSchemes** - схеми аутентифікації
- **TimeoutManager** - налаштування таймаутів
- **IgnoreWriteExceptions** - ігнорувати помилки запису
- **Realm** - realm для базової аутентифікації

#### 3. Запуск

```
listener.Start();
```

**Що відбувається:**
- Реєструються всі префікси в HTTP.sys (Windows) або managed listener
- Відкриваються необхідні порти
- Сервер готовий приймати з'єднання
- Виникає **HttpListenerException**, якщо порт зайнятий або недостатньо прав

**Права доступу:**
- На Windows для не-адміністратора потрібна резервація URL через `netsh`
- На Linux/macOS потрібні права для біндингу на порт < 1024

#### 4. Прийом запитів

**Синхронний режим:**
```
HttpListenerContext context = listener.GetContext();
```

**Асинхронний режим:**
```
HttpListenerContext context = await listener.GetContextAsync();
```

**Що відбувається:**
- Метод блокується до надходження запиту
- При отриманні запиту створюється **HttpListenerContext**
- Context містить Request, Response та User (якщо authenticated)
- Кожен виклик обробляє ОДИН запит

#### 5. Обробка запиту

```
HttpListenerRequest request = context.Request;
HttpListenerResponse response = context.Response;

// Читання request
string method = request.HttpMethod;
string url = request.Url.ToString();
byte[] body = ReadInputStream(request.InputStream);

// Формування response
response.StatusCode = 200;
response.ContentType = "application/json";
byte[] responseBytes = Encoding.UTF8.GetBytes(json);
response.ContentLength64 = responseBytes.Length;
await response.OutputStream.WriteAsync(responseBytes, 0, responseBytes.Length);
```

**Важливо:**
- Request доступний тільки для читання
- Response потрібно налаштувати перед відправкою
- OutputStream потрібно закрити після запису
- Context автоматично очищається після закриття Response

#### 6. Завершення обробки

```
response.Close();
```

**Що відбувається:**
- Відправляються всі буферизовані дані
- Закривається TCP з'єднання (або повертається в pool для keep-alive)
- Звільняються ресурси Context
- Listener готовий до наступного запиту

#### 7. Зупинка

```
listener.Stop();
```

**Що відбувається:**
- Припиняється прийом нових з'єднань
- Активні запити завершуються (graceful shutdown)
- Звільняються всі ресурси
- Префікси дереєструються

#### 8. Очищення

```
listener.Close(); // або listener.Dispose()
```

**Різниця між Stop() і Close():**
- **Stop()** - припиняє прийом запитів, але listener можна перезапустити через Start()
- **Close()/Dispose()** - повністю звільняє ресурси, listener більше не можна використовувати

### Паралельна обробка запитів

HttpListener приймає тільки один запит за раз. Для паралельної обробки:

```csharp
while (true)
{
    HttpListenerContext context = await listener.GetContextAsync();
    
    // Запускаємо обробку в окремій задачі
    _ = Task.Run(() => HandleRequest(context));
    
    // Одразу повертаємось до прийому наступного запиту
}
```

**Що відбувається:**
- Основний цикл швидко приймає запити
- Кожен запит обробляється в окремому Task
- Можливо N паралельних обробок
- Потрібен контроль за кількістю паралельних задач (throttling)

---

## Конфігурація HttpListener

### Властивості HttpListener

#### Prefixes (HttpListenerPrefixCollection)

**Призначення:** Колекція URL префіксів, на яких listener приймає запити.

**Формат префіксу:**
```
scheme://hostname:port/path/
```

**Правила:**
- ПОВИНЕН закінчуватись на `/`
- Scheme: тільки `http` або `https`
- Hostname: може бути IP, домен, `localhost`, `*`, `+`
- Port: обов'язковий
- Path: опціональний, підтримує wildcards

**Приклади валідних префіксів:**
```csharp
// Локальний хост, конкретний порт
listener.Prefixes.Add("http://localhost:8080/");

// Всі інтерфейси, strong wildcard
listener.Prefixes.Add("http://*:8080/");

// Всі інтерфейси, weak wildcard (Windows)
listener.Prefixes.Add("http://+:8080/");

// Конкретний домен
listener.Prefixes.Add("http://example.com:80/");

// З підшляхом
listener.Prefixes.Add("http://localhost:8080/api/");
listener.Prefixes.Add("http://localhost:8080/webhooks/");

// HTTPS (потрібен сертифікат)
listener.Prefixes.Add("https://localhost:8443/");

// IP адреса
listener.Prefixes.Add("http://192.168.1.100:8080/");
```

**Wildcard символи:**
- `*` (strong wildcard) - всі hostname, які не matched іншими префіксами
- `+` (weak wildcard) - всі hostname для цього порту (Windows only)

**Пріоритет matching:**
1. Точний hostname з найдовшим path
2. Точний hostname з коротшим path
3. Wildcard hostname з найдовшим path
4. Wildcard hostname з коротшим path

**Приклад:**
```csharp
listener.Prefixes.Add("http://localhost:8080/api/users/");
listener.Prefixes.Add("http://localhost:8080/api/");
listener.Prefixes.Add("http://localhost:8080/");

// Запит до /api/users/123 → перший префікс (найточніший)
// Запит до /api/products → другий префікс
// Запит до /other → третій префікс
```

#### AuthenticationSchemes

**Призначення:** Вказує схеми аутентифікації, які підтримує сервер.

**Доступні значення:**
- `AuthenticationSchemes.Anonymous` - без аутентифікації (за замовчуванням)
- `AuthenticationSchemes.Basic` - HTTP Basic Authentication
- `AuthenticationSchemes.Digest` - HTTP Digest Authentication (Windows only)
- `AuthenticationSchemes.Negotiate` - Windows Negotiate (NTLM/Kerberos)
- `AuthenticationSchemes.Ntlm` - NTLM authentication

**Комбінування схем:**
```csharp
listener.AuthenticationSchemes = 
    AuthenticationSchemes.Basic | 
    AuthenticationSchemes.Anonymous;
```

**Динамічний вибір схеми:**
```csharp
listener.AuthenticationSchemeSelectorDelegate = (request) =>
{
    // Вибираємо схему на основі запиту
    if (request.Url.AbsolutePath.StartsWith("/admin"))
        return AuthenticationSchemes.Basic;
    return AuthenticationSchemes.Anonymous;
};
```

**Доступ до authenticated користувача:**
```csharp
HttpListenerContext context = await listener.GetContextAsync();
IPrincipal user = context.User;

if (user != null && user.Identity.IsAuthenticated)
{
    string username = user.Identity.Name;
    string authType = user.Identity.AuthenticationType;
}
```

#### Realm

**Призначення:** Вказує realm для Basic/Digest authentication.

```csharp
listener.Realm = "MySecureAPI";
```

Відображається в браузері при запиті credentials:
```
The site says: "MySecureAPI"
```

#### TimeoutManager (Windows only)

**Призначення:** Налаштування різних таймаутів для HTTP з'єднань.

```csharp
TimeoutManager timeouts = listener.TimeoutManager;

// Таймаут неактивного з'єднання
timeouts.IdleConnection = TimeSpan.FromMinutes(2);

// Таймаут для читання entity body
timeouts.EntityBody = TimeSpan.FromSeconds(120);

// Таймаут для drain entity body
timeouts.DrainEntityBody = TimeSpan.FromSeconds(60);

// Таймаут для headers
timeouts.HeaderWait = TimeSpan.FromSeconds(120);

// Мінімальний send rate (байт/сек)
timeouts.MinSendBytesPerSecond = 150;

// Таймаут для отримання request
timeouts.RequestQueue = TimeSpan.FromMinutes(2);
```

**Коли використовувати:**
- Захист від повільних клієнтів (Slowloris attacks)
- Обмеження часу обробки запиту
- Контроль ресурсів сервера

#### IgnoreWriteExceptions

**Призначення:** Визначає, чи ігнорувати винятки при записі у response stream.

```csharp
listener.IgnoreWriteExceptions = true;
```

**Використання:**
- `true` - винятки не викидаються, але можна перевірити через `response.OutputStream.CanWrite`
- `false` (за замовчуванням) - винятки викидаються при помилках запису

**Типові сценарії:**
- Клієнт розірвав з'єднання до завершення відповіді
- Network timeout
- Клієнт не читає response достатньо швидко

#### UnsafeConnectionNtlmAuthentication

**Призначення:** Дозволяє NTLM аутентифікацію через небезпечні з'єднання (Windows only).

```csharp
listener.UnsafeConnectionNtlmAuthentication = true;
```

**Небезпека:** NTLM credentials можуть бути reused для інших запитів на тому ж з'єднанні.

### ExtendedProtectionPolicy

**Призначення:** Додатковий захист для Windows Integrated Authentication.

```csharp
listener.ExtendedProtectionPolicy = new ExtendedProtectionPolicy(
    PolicyEnforcement.Always,
    ProtectionScenario.TransportSelected,
    new ServiceNameCollection(new[] { "HTTP/myserver" })
);
```

**Захист від:**
- Credential forwarding attacks
- Man-in-the-middle attacks

---

## HttpListenerContext

### Структура HttpListenerContext

**HttpListenerContext** — це об'єкт, який інкапсулює один HTTP запит та відповідь.

**Властивості:**

#### Request (HttpListenerRequest)

Об'єкт запиту - доступний тільки для читання, містить всю інформацію про вхідний HTTP запит.

```csharp
HttpListenerRequest request = context.Request;
```

**Детальніше:** [HttpListenerRequest](#httplistenerrequest)

#### Response (HttpListenerResponse)

Об'єкт відповіді - використовується для формування HTTP відповіді клієнту.

```csharp
HttpListenerResponse response = context.Response;
```

**Детальніше:** [HttpListenerResponse](#httplistenerresponse)

#### User (IPrincipal)

Інформація про аутентифікованого користувача (якщо є).

```csharp
IPrincipal user = context.User;

if (user != null && user.Identity.IsAuthenticated)
{
    string username = user.Identity.Name;
    string authType = user.Identity.AuthenticationType;
    
    // Перевірка ролей (якщо WindowsPrincipal)
    if (user is WindowsPrincipal windowsUser)
    {
        bool isAdmin = windowsUser.IsInRole(WindowsBuiltInRole.Administrator);
    }
}
```

**Null, якщо:**
- `AuthenticationSchemes = Anonymous`
- Клієнт не надав credentials
- Аутентифікація не вдалась

### Життєвий цикл Context

1. **Створення** - при виклику `GetContextAsync()`
2. **Активний** - доступні Request та Response
3. **Обробка** - читання Request, формування Response
4. **Закриття** - після `Response.Close()`
5. **Очищення** - автоматичне звільнення ресурсів

**Важливо:**
- Context НЕ можна reuse
- Response ПОТРІБНО закрити
- Після закриття Request/Response більше не доступні
- Не потрібно explicitly dispose Context

---

## HttpListenerRequest

### Огляд

**HttpListenerRequest** надає повний доступ до всіх деталей HTTP запиту.

### Основні властивості

#### Метод та URL

```csharp
// HTTP метод
string method = request.HttpMethod; // "GET", "POST", "PUT", etc.

// Повний URL
Uri url = request.Url;
// url.Scheme: "http" або "https"
// url.Host: "localhost"
// url.Port: 8080
// url.AbsolutePath: "/api/users/123"
// url.Query: "?sort=name&order=asc"

// Тільки path та query
string pathAndQuery = request.RawUrl; // "/api/users/123?sort=name&order=asc"

// Розпарсений query string
NameValueCollection query = request.QueryString;
string sort = query["sort"]; // "name"
string order = query["order"]; // "asc"
```

#### HTTP версія

```csharp
Version version = request.ProtocolVersion;
// version.Major: 1 або 2
// version.Minor: 0 або 1

// Перевірка версії
if (request.ProtocolVersion.Major == 2)
{
    // HTTP/2 запит
}
```

#### Заголовки

```csharp
// Всі заголовки
WebHeaderCollection headers = request.Headers;

// Кількість заголовків
int count = headers.Count;

// Читання конкретного заголовка
string contentType = headers["Content-Type"];
string userAgent = headers["User-Agent"];
string authorization = headers["Authorization"];

// Ітерація по всіх заголовках
foreach (string key in headers.AllKeys)
{
    string value = headers[key];
    Console.WriteLine($"{key}: {value}");
}

// Перевірка існування
bool hasAuth = headers["Authorization"] != null;
```

**Типові властивості (shortcuts):**

```csharp
// Content-Type
string contentType = request.ContentType; // shortcut для headers["Content-Type"]

// Content-Length
long contentLength = request.ContentLength64;

// User-Agent
string userAgent = request.UserAgent;

// Accept
string[] acceptTypes = request.AcceptTypes; // розпарсений Accept header

// Referer
Uri referer = request.UrlReferrer;

// Host
string host = request.UserHostName;

// Keep-Alive
bool keepAlive = request.KeepAlive;

// Transfer-Encoding
string transferEncoding = request.TransportContext?.ToString();
```

#### Cookies

```csharp
// Колекція cookies
CookieCollection cookies = request.Cookies;

// Кількість cookies
int count = cookies.Count;

// Читання конкретного cookie
Cookie sessionCookie = cookies["sessionId"];
if (sessionCookie != null)
{
    string value = sessionCookie.Value;
    string domain = sessionCookie.Domain;
    string path = sessionCookie.Path;
    DateTime expires = sessionCookie.Expires;
    bool httpOnly = sessionCookie.HttpOnly;
    bool secure = sessionCookie.Secure;
}

// Ітерація
foreach (Cookie cookie in cookies)
{
    Console.WriteLine($"{cookie.Name} = {cookie.Value}");
}
```

#### Клієнтська інформація

```csharp
// IP адреса клієнта
IPEndPoint remoteEndPoint = request.RemoteEndPoint;
string clientIp = remoteEndPoint.Address.ToString();
int clientPort = remoteEndPoint.Port;

// Локальна адреса (на якій прийнято запит)
IPEndPoint localEndPoint = request.LocalEndPoint;

// Hostname клієнта (якщо доступний)
string hostname = request.UserHostName;

// User-Agent
string userAgent = request.UserAgent;

// Supported languages
string[] languages = request.UserLanguages; // з Accept-Language header
```

#### Тіло запиту (Body)

```csharp
// Чи є тіло запиту
bool hasBody = request.HasEntityBody;

// Content-Length (розмір тіла)
long contentLength = request.ContentLength64;

// Encoding тіла
Encoding encoding = request.ContentEncoding; // з Content-Type header

// Stream для читання тіла
Stream inputStream = request.InputStream;

// Синхронне читання
byte[] buffer = new byte[request.ContentLength64];
int bytesRead = inputStream.Read(buffer, 0, buffer.Length);
string bodyText = request.ContentEncoding.GetString(buffer);

// Асинхронне читання
using (StreamReader reader = new StreamReader(inputStream, encoding))
{
    string bodyText = await reader.ReadToEndAsync();
}
```

**Важливо:**
- InputStream можна прочитати тільки ОДИН раз
- Після читання stream не можна перемотати назад
- Для повторного читання потрібно буферизувати дані

#### HTTPS та сертифікати

```csharp
// Чи з'єднання безпечне (HTTPS)
bool isSecure = request.IsSecureConnection;

// Інформація про TLS (якщо HTTPS)
if (isSecure)
{
    // Transport context
    TransportContext transportContext = request.TransportContext;
    
    // Клієнтський сертифікат (якщо є)
    X509Certificate2 clientCert = request.GetClientCertificate();
    
    if (clientCert != null)
    {
        string subject = clientCert.Subject;
        string issuer = clientCert.Issuer;
        DateTime validFrom = clientCert.NotBefore;
        DateTime validTo = clientCert.NotAfter;
    }
    
    // Асинхронне отримання сертифіката
    X509Certificate2 cert = await request.GetClientCertificateAsync();
}
```

#### Аутентифікація

```csharp
// Чи клієнт аутентифікований
bool isAuthenticated = request.IsAuthenticated;

// Чи запит локальний
bool isLocal = request.IsLocal; // true, якщо з localhost

// Чи використовується WebSockets (upgrade)
bool isWebSocketRequest = request.IsWebSocketRequest;
```

#### Додаткові властивості

```csharp
// Service name (для Kerberos/Negotiate auth)
string serviceName = request.ServiceName;

// Request trace identifier (для логування)
Guid requestId = request.RequestTraceIdentifier;
```

### Методи HttpListenerRequest

#### GetClientCertificate()

Синхронно отримує клієнтський SSL/TLS сертифікат.

```csharp
X509Certificate2 cert = request.GetClientCertificate();
```

**Повертає:** `null`, якщо сертифікат відсутній або з'єднання не HTTPS.

#### GetClientCertificateAsync()

Асинхронно отримує клієнтський SSL/TLS сертифікат.

```csharp
X509Certificate2 cert = await request.GetClientCertificateAsync();
```

#### BeginGetClientCertificate() / EndGetClientCertificate()

Асинхронні методи у стилі APM (застарілий паттерн).

### Обробка різних типів контенту

#### application/json

```csharp
if (request.ContentType?.Contains("application/json") == true)
{
    using (StreamReader reader = new StreamReader(request.InputStream, request.ContentEncoding))
    {
        string json = await reader.ReadToEndAsync();
        var data = JsonSerializer.Deserialize<MyClass>(json);
    }
}
```

#### application/x-www-form-urlencoded

```csharp
if (request.ContentType?.Contains("application/x-www-form-urlencoded") == true)
{
    using (StreamReader reader = new StreamReader(request.InputStream, request.ContentEncoding))
    {
        string formData = await reader.ReadToEndAsync();
        NameValueCollection form = HttpUtility.ParseQueryString(formData);
        string username = form["username"];
        string password = form["password"];
    }
}
```

#### multipart/form-data

```csharp
if (request.ContentType?.Contains("multipart/form-data") == true)
{
    // Потрібна бібліотека для парсингу multipart
    // або ручний парсинг boundary
    string boundary = GetBoundary(request.ContentType);
    var parts = ParseMultipart(request.InputStream, boundary);
}
```

**Примітка:** HttpListener НЕ має вбудованого парсера для multipart/form-data. Потрібно використовувати сторонні бібліотеки або писати власний parser.

---

## HttpListenerResponse

### Огляд

**HttpListenerResponse** використовується для формування та відправки HTTP відповіді клієнту.

### Основні властивості

#### Статус відповіді

```csharp
// Статус код (число)
response.StatusCode = 200; // 200, 404, 500, etc.

// Статус опис (текст)
response.StatusDescription = "OK"; // "OK", "Not Found", "Internal Server Error"

// Зазвичай достатньо встановити тільки StatusCode
// StatusDescription буде встановлено автоматично
```

**Стандартні статус коди:**
- 200 OK
- 201 Created
- 204 No Content
- 301 Moved Permanently
- 302 Found
- 304 Not Modified
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 500 Internal Server Error
- 503 Service Unavailable

#### Заголовки відповіді

```csharp
// Колекція заголовків
WebHeaderCollection headers = response.Headers;

// Додавання заголовків
response.Headers.Add("X-Custom-Header", "CustomValue");
response.Headers.Add("X-Request-ID", Guid.NewGuid().ToString());

// Видалення заголовка
response.Headers.Remove("X-Custom-Header");

// Очищення всіх заголовків
response.Headers.Clear();

// ВАЖЛИВО: Деякі заголовки мають спеціальні властивості і не можна
// встановлювати через Headers.Add()
```

**Спеціальні властивості для заголовків:**

```csharp
// Content-Type
response.ContentType = "application/json; charset=utf-8";

// Content-Length
response.ContentLength64 = 1234; // розмір у байтах

// Keep-Alive
response.KeepAlive = true; // Connection: keep-alive

// Transfer-Encoding: chunked
response.SendChunked = true;

// Location (для 3xx redirects)
response.RedirectLocation = "https://example.com/new-location";
```

#### Content-Type та Encoding

```csharp
// MIME type з charset
response.ContentType = "application/json; charset=utf-8";

// Encoding (використовується для текстових даних)
response.ContentEncoding = Encoding.UTF8;
```

**Типові Content-Type значення:**
- `text/html; charset=utf-8` - HTML
- `application/json; charset=utf-8` - JSON
- `application/xml; charset=utf-8` - XML
- `text/plain; charset=utf-8` - Текст
- `application/octet-stream` - Бінарні дані
- `image/jpeg` - JPEG зображення
- `image/png` - PNG зображення
- `application/pdf` - PDF документ

#### Content-Length

```csharp
// Розмір тіла відповіді в байтах
response.ContentLength64 = bodyBytes.Length;
```

**Автоматичне встановлення:**
- Якщо НЕ встановлено вручну
- І НЕ використовується chunked encoding
- .NET спробує визначити автоматично

**Рекомендація:** Завжди встановлюйте явно для кращої продуктивності.

#### Cookies

```csharp
// Додавання cookie
Cookie cookie = new Cookie("sessionId", "abc123xyz")
{
    Domain = "example.com",
    Path = "/",
    Expires = DateTime.Now.AddHours(1),
    HttpOnly = true,
    Secure = true,
    SameSite = CookieOptions.SameSiteMode.Strict
};
response.Cookies.Add(cookie);

// Або через AppendCookie (рекомендовано)
response.AppendCookie(cookie);

// Видалення cookie (встановити Expires у минулому)
Cookie deleteCookie = new Cookie("sessionId", "")
{
    Expires = DateTime.Now.AddDays(-1)
};
response.AppendCookie(deleteCookie);
```

#### Redirects

```csharp
// 302 Found (temporary redirect)
response.Redirect("https://example.com/new-location");

// Еквівалентно:
response.StatusCode = 302;
response.RedirectLocation = "https://example.com/new-location";

// 301 Moved Permanently
response.StatusCode = 301;
response.RedirectLocation = "https://example.com/new-location";
```

#### Chunked Transfer Encoding

```csharp
// Активувати chunked encoding
response.SendChunked = true;

// Тепер Content-Length НЕ потрібен
// Дані відправляються частинами (chunks)

// Запис даних
await response.OutputStream.WriteAsync(chunk1, 0, chunk1.Length);
await response.OutputStream.FlushAsync();

await response.OutputStream.WriteAsync(chunk2, 0, chunk2.Length);
await response.OutputStream.FlushAsync();

// Закриття завершує передачу
response.Close();
```

**Коли використовувати:**
- Невідомий розмір відповіді заздалегідь
- Streaming великих даних
- Server-Sent Events
- Генерація контенту on-the-fly

#### Keep-Alive

```csharp
// Підтримувати з'єднання відкритим для наступних запитів
response.KeepAlive = true; // за замовчуванням

// Закрити з'єднання після відповіді
response.KeepAlive = false;
```

**HTTP/1.1:** Keep-Alive увімкнено за замовчуванням  
**HTTP/1.0:** Keep-Alive вимкнено за замовчуванням

#### ProtocolVersion

```csharp
// HTTP версія відповіді (зазвичай встановлюється автоматично)
response.ProtocolVersion = new Version(1, 1); // HTTP/1.1
```

### Методи HttpListenerResponse

#### OutputStream

**Властивість:** Stream для запису тіла відповіді.

```csharp
Stream output = response.OutputStream;

// Запис байтів
byte[] data = Encoding.UTF8.GetBytes("Hello, World!");
await output.WriteAsync(data, 0, data.Length);

// Після запису ОБОВ'ЯЗКОВО закрити
output.Close(); // або response.Close()
```

#### Close()

Завершує відповідь та відправляє всі буферизовані дані.

```csharp
// Закрити без тіла
response.Close();

// Закрити з тілом (shortcut)
byte[] responseBytes = Encoding.UTF8.GetBytes("Hello!");
response.Close(responseBytes, willBlock: true);
```

**Параметр willBlock:**
- `true` - метод блокується до повної відправки
- `false` - метод повертається одразу, дані відправляються асинхронно

#### Abort()

Негайно закриває з'єднання без відправки даних.

```csharp
response.Abort();
```

**Використання:**
- При критичних помилках
- Коли неможливо сформувати коректну відповідь
- Для примусового розриву з'єднання

**Увага:** Клієнт отримає connection reset або incomplete response.

#### CopyFrom()

Копіює властивості з іншого HttpListenerResponse.

```csharp
response.CopyFrom(templateResponse);
```

**Копіюються:**
- StatusCode, StatusDescription
- ProtocolVersion
- KeepAlive
- SendChunked
- Усі заголовки

**НЕ копіюються:**
- OutputStream (унікальний для кожної відповіді)

#### AddHeader()

Додає заголовок (застарілий метод, краще використовувати `Headers.Add()`).

```csharp
response.AddHeader("X-Custom", "Value");
```

#### AppendHeader()

Додає заголовок або додає значення до існуючого.

```csharp
response.AppendHeader("X-Custom", "Value1");
response.AppendHeader("X-Custom", "Value2");
// Результат: X-Custom: Value1, Value2
```

#### AppendCookie()

Додає cookie до відповіді (рекомендовано замість `Cookies.Add()`).

```csharp
Cookie cookie = new Cookie("name", "value");
response.AppendCookie(cookie);
```

#### SetCookie()

Встановлює cookie (замінює існуючий з таким же ім'ям).

```csharp
Cookie cookie = new Cookie("name", "newValue");
response.SetCookie(cookie);
```

#### Redirect()

Відправляє 302 redirect.

```csharp
response.Redirect("https://example.com/new-page");
```

### Послідовність відправки відповіді

**Правильна послідовність:**

```csharp
// 1. Встановити статус код
response.StatusCode = 200;

// 2. Встановити заголовки
response.ContentType = "application/json; charset=utf-8";
response.Headers.Add("X-Request-ID", requestId);
response.Headers.Add("Cache-Control", "no-cache");

// 3. Додати cookies (якщо потрібно)
response.AppendCookie(sessionCookie);

// 4. Встановити Content-Length (якщо відомий)
response.ContentLength64 = responseBytes.Length;

// 5. Записати тіло
await response.OutputStream.WriteAsync(responseBytes, 0, responseBytes.Length);

// 6. Закрити
response.Close();
```

**Важливо:**
- Заголовки ПОТРІБНО встановити ДО запису у OutputStream
- Після початку запису заголовки змінити НЕМОЖЛИВО
- Close() ОБОВ'ЯЗКОВИЙ для завершення відповіді

### Обробка помилок

```csharp
try
{
    // Формування відповіді
    await response.OutputStream.WriteAsync(data, 0, data.Length);
    response.Close();
}
catch (HttpListenerException ex)
{
    // Клієнт розірвав з'єднання
    Console.WriteLine($"Client disconnected: {ex.Message}");
    response.Abort(); // Закрити з'єднання
}
catch (ObjectDisposedException)
{
    // Response вже закритий
}
```

**Типові винятки:**
- `HttpListenerException` - проблеми з мережею/клієнтом
- `ObjectDisposedException` - спроба використання закритого response
- `InvalidOperationException` - некоректна операція (наприклад, зміна заголовків після запису)

---

## Префікси HttpListener

### Синтаксис префіксів

**Загальний формат:**
```
scheme://hostname:port/path/
```

### Компоненти префіксу

#### Scheme (протокол)

**Доступні значення:**
- `http://` - HTTP (незашифровано)
- `https://` - HTTPS (з TLS/SSL)

**Обмеження:**
- Тільки `http` або `https`
- Інші протоколи (ws, ftp, тощо) НЕ підтримуються

#### Hostname

**Варіанти:**

**1. Конкретний hostname:**
```csharp
listener.Prefixes.Add("http://localhost:8080/");
listener.Prefixes.Add("http://example.com:8080/");
```

**2. IP адреса:**
```csharp
listener.Prefixes.Add("http://127.0.0.1:8080/");
listener.Prefixes.Add("http://192.168.1.100:8080/");
listener.Prefixes.Add("http://[::1]:8080/"); // IPv6
```

**3. Strong wildcard (*):**
```csharp
listener.Prefixes.Add("http://*:8080/");
```
- Приймає запити на ВСІ hostname/IP для цього порту
- Найнижчий пріоритет matching

**4. Weak wildcard (+) (Windows only):**
```csharp
listener.Prefixes.Add("http://+:8080/");
```
- Приймає запити на всі hostname, які не matched іншими listeners
- Дозволяє sharing port між різними процесами

**Різниця між * та +:**
- `*` - exclusive, блокує порт для інших процесів
- `+` - shared, дозволяє multiple listeners на одному порту

#### Port

**Правила:**
- Обов'язковий параметр
- Діапазон: 1-65535
- Стандартні порти: 80 (HTTP), 443 (HTTPS)
- Порти < 1024 вимагають підвищених прав (Linux/macOS)

**Приклади:**
```csharp
listener.Prefixes.Add("http://localhost:80/");   // HTTP standard
listener.Prefixes.Add("https://localhost:443/"); // HTTPS standard
listener.Prefixes.Add("http://localhost:8080/"); // Custom port
```

#### Path

**Правила:**
- Опціональний параметр
- ПОВИНЕН закінчуватись на `/`
- Case-sensitive на Linux/macOS
- Case-insensitive на Windows

**Приклади:**
```csharp
// Root path
listener.Prefixes.Add("http://localhost:8080/");

// Specific paths
listener.Prefixes.Add("http://localhost:8080/api/");
listener.Prefixes.Add("http://localhost:8080/webhooks/");
listener.Prefixes.Add("http://localhost:8080/admin/dashboard/");

// НЕВАЛІДНИЙ (не закінчується на /)
// listener.Prefixes.Add("http://localhost:8080/api"); // ПОМИЛКА
```

### Matching запитів до префіксів

**Пріоритет matching (від вищого до нижчого):**

1. **Exact hostname + longest path**
2. **Exact hostname + shorter path**
3. **Wildcard hostname + longest path**
4. **Wildcard hostname + shorter path**

**Приклад:**
```csharp
listener.Prefixes.Add("http://localhost:8080/api/users/");      // Пріоритет 1
listener.Prefixes.Add("http://localhost:8080/api/");            // Пріоритет 2
listener.Prefixes.Add("http://*:8080/api/products/");           // Пріоритет 3
listener.Prefixes.Add("http://*:8080/");                        // Пріоритет 4

// Запити:
// http://localhost:8080/api/users/123       → Префікс 1
// http://localhost:8080/api/products        → Префікс 2
// http://192.168.1.1:8080/api/products/456  → Префікс 3
// http://example.com:8080/other             → Префікс 4
```

### Права доступу

#### Windows

**Без підвищених прав:**
```
Помилка: Access Denied (HttpListenerException)
```

**Рішення 1: Запустити як адміністратор**

**Рішення 2: Зарезервувати URL для користувача**
```powershell
# PowerShell з правами адміністратора
netsh http add urlacl url=http://+:8080/ user=DOMAIN\Username

# Для локального користувача
netsh http add urlacl url=http://+:8080/ user=Everyone

# Переглянути існуючі резервації
netsh http show urlacl

# Видалити резервацію
netsh http delete urlacl url=http://+:8080/
```

#### Linux/macOS

**Порти < 1024:**
- Вимагають root прав
- Рекомендація: використовувати порти >= 1024

**Рішення 1: Запустити з sudo**
```bash
sudo dotnet run
```

**Рішення 2: Дозволити біндинг для конкретного порту**
```bash
# Linux (використовувати capabilities)
sudo setcap CAP_NET_BIND_SERVICE=+eip /path/to/dotnet

# Або використовувати authbind
```

**Рішення 3: Використовувати reverse proxy**
- Nginx/Apache на порту 80/443
- Проксіювати на додаток на порту 8080+

### HTTPS префікси

**Вимоги для HTTPS:**

1. **SSL/TLS сертифікат**
2. **Прив'язка сертифіката до порту**

**Windows - прив'язка сертифіката:**
```powershell
# 1. Створити self-signed сертифікат (для розробки)
$cert = New-SelfSignedCertificate -DnsName "localhost" -CertStoreLocation "cert:\LocalMachine\My"

# 2. Отримати thumbprint
$cert.Thumbprint

# 3. Прив'язати сертифікат до порту
$guid = [guid]::NewGuid().ToString("B")
netsh http add sslcert ipport=0.0.0.0:8443 certhash=$($cert.Thumbprint) appid="$guid"

# 4. Тепер можна використовувати HTTPS
```

**Linux/macOS:**
- Потрібен PEM сертифікат та ключ
- Налаштування залежить від платформи
- Рекомендація: використовувати Kestrel в ASP.NET Core для кращої підтримки

**Використання:**
```csharp
listener.Prefixes.Add("https://localhost:8443/");
```

### Множинні префікси

**Один listener може слухати багато префіксів:**

```csharp
HttpListener listener = new HttpListener();

// HTTP та HTTPS
listener.Prefixes.Add("http://localhost:8080/");
listener.Prefixes.Add("https://localhost:8443/");

// Різні paths
listener.Prefixes.Add("http://localhost:8080/api/");
listener.Prefixes.Add("http://localhost:8080/webhooks/");

// Різні hostnames
listener.Prefixes.Add("http://localhost:8080/");
listener.Prefixes.Add("http://127.0.0.1:8080/");
listener.Prefixes.Add("http://example.com:8080/");

listener.Start();
```

**Використання:**
- Підтримка HTTP та HTTPS одночасно
- Різні paths для різної логіки
- Multiple domains на одному порту

### Помилки та виключення

**HttpListenerException - типові сценарії:**

1. **Port already in use:**
```
The process cannot access the file because it is being used by another process
```

2. **Access Denied:**
```
Access is denied
```

3. **Invalid prefix format:**
```
Prefix must end with '/'
```

**Перевірка чи префікс валідний:**
```csharp
try
{
    listener.Prefixes.Add("http://localhost:8080/");
    listener.Start();
}
catch (HttpListenerException ex)
{
    if (ex.ErrorCode == 5) // Access Denied
    {
        Console.WriteLine("Потрібні права адміністратора або URL reservation");
    }
    else if (ex.ErrorCode == 32) // Port in use
    {
        Console.WriteLine("Порт вже використовується іншим процесом");
    }
}
```

---

## Автентифікація HttpListener

### Підтримувані схеми аутентифікації

HttpListener підтримує наступні HTTP authentication schemes:

#### 1. Anonymous (без аутентифікації)

**За замовчуванням**, жодної аутентифікації не вимагається.

```csharp
listener.AuthenticationSchemes = AuthenticationSchemes.Anonymous;
```

**Використання:**
- Публічні endpoints
- Відкриті API
- Локальні development servers

#### 2. Basic Authentication

**HTTP Basic Authentication** - передача username:password в Base64.

```csharp
listener.AuthenticationSchemes = AuthenticationSchemes.Basic;
listener.Realm = "My Secure API";

// Обробка
HttpListenerContext context = await listener.GetContextAsync();

if (context.User != null && context.User.Identity.IsAuthenticated)
{
    HttpListenerBasicIdentity identity = (HttpListenerBasicIdentity)context.User.Identity;
    string username = identity.Name;
    string password = identity.Password; // ⚠️ Plain text!
    
    // Власна валідація
    if (ValidateCredentials(username, password))
    {
        // Дозволити доступ
    }
    else
    {
        response.StatusCode = 401;
        response.Close();
    }
}
else
{
    // Запит credentials
    response.StatusCode = 401;
    response.Close();
}
```

**Безпека:**
- ⚠️ Credentials передаються в Base64 (НЕ шифрування!)
- **ОБОВ'ЯЗКОВО використовувати HTTPS**
- Без HTTPS credentials видимі в plain text

**Заголовок Authorization:**
```
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
```
Де `dXNlcm5hbWU6cGFzc3dvcmQ=` це Base64("username:password")

#### 3. Digest Authentication (Windows only)

**HTTP Digest Authentication** - більш безпечна, ніж Basic.

```csharp
listener.AuthenticationSchemes = AuthenticationSchemes.Digest;
listener.Realm = "My Secure API";
```

**Особливості:**
- Credentials НЕ передаються напряму
- Використовується challenge-response механізм
- Краще, ніж Basic, але рідко використовується
- Windows only в .NET

#### 4. Windows Authentication (NTLM/Negotiate)

**Інтегрована Windows аутентифікація.**

```csharp
listener.AuthenticationSchemes = AuthenticationSchemes.Negotiate;
// або
listener.AuthenticationSchemes = AuthenticationSchemes.Ntlm;
```

**Використання:**
- Intranet додатки в Windows середовищі
- Active Directory інтеграція
- Single Sign-On для Windows користувачів

**Доступ до Windows User:**
```csharp
HttpListenerContext context = await listener.GetContextAsync();

if (context.User is WindowsPrincipal windowsUser)
{
    WindowsIdentity identity = (WindowsIdentity)windowsUser.Identity;
    string username = identity.Name; // DOMAIN\Username
    string authType = identity.AuthenticationType; // "NTLM" або "Negotiate"
    
    // Перевірка ролей
    bool isAdmin = windowsUser.IsInRole(WindowsBuiltInRole.Administrator);
    bool isUser = windowsUser.IsInRole(WindowsBuiltInRole.User);
}
```

### Комбінування схем

Можна дозволити множинні схеми аутентифікації:

```csharp
listener.AuthenticationSchemes = 
    AuthenticationSchemes.Basic | 
    AuthenticationSchemes.Negotiate |
    AuthenticationSchemes.Anonymous;
```

**Як працює:**
- Сервер повідомляє клієнту всі доступні схеми
- Клієнт вибирає одну з них
- Обробка залежить від обраної схеми

### Динамічний вибір схеми аутентифікації

**AuthenticationSchemeSelectorDelegate** дозволяє вибирати схему на основі запиту:

```csharp
listener.AuthenticationSchemeSelectorDelegate = (request) =>
{
    // Адмін панель - тільки Windows auth
    if (request.Url.AbsolutePath.StartsWith("/admin"))
        return AuthenticationSchemes.Negotiate;
    
    // API - Basic auth
    if (request.Url.AbsolutePath.StartsWith("/api"))
        return AuthenticationSchemes.Basic;
    
    // Публічні ресурси - без auth
    return AuthenticationSchemes.Anonymous;
};
```

### Власна валідація credentials

Для Basic Authentication часто потрібна власна валідація:

```csharp
listener.AuthenticationSchemes = AuthenticationSchemes.Basic;
listener.Realm = "API";

while (true)
{
    HttpListenerContext context = await listener.GetContextAsync();
    
    bool isAuthenticated = false;
    
    if (context.User?.Identity is HttpListenerBasicIdentity basicIdentity)
    {
        string username = basicIdentity.Name;
        string password = basicIdentity.Password;
        
        // Валідація проти бази даних
        isAuthenticated = await ValidateUser(username, password);
    }
    
    if (!isAuthenticated)
    {
        context.Response.StatusCode = 401;
        context.Response.AddHeader("WWW-Authenticate", $"Basic realm=\"{listener.Realm}\"");
        context.Response.Close();
        continue;
    }
    
    // Обробка аутентифікованого запиту
    await HandleRequest(context);
}
```

### WWW-Authenticate header

При 401 відповіді потрібно відправити **WWW-Authenticate** header:

```csharp
response.StatusCode = 401;
response.AddHeader("WWW-Authenticate", "Basic realm=\"My API\"");
response.Close();
```

**Формати для різних схем:**

```
Basic:     WWW-Authenticate: Basic realm="API"
Digest:    WWW-Authenticate: Digest realm="API", qop="auth", nonce="..."
Negotiate: WWW-Authenticate: Negotiate
NTLM:      WWW-Authenticate: NTLM
```

### Bearer Token Authentication

HttpListener НЕ має вбудованої підтримки Bearer tokens (OAuth/JWT), але можна реалізувати вручну:

```csharp
listener.AuthenticationSchemes = AuthenticationSchemes.Anonymous;

HttpListenerContext context = await listener.GetContextAsync();

// Читаємо Authorization header
string authHeader = context.Request.Headers["Authorization"];

if (!string.IsNullOrEmpty(authHeader) && authHeader.StartsWith("Bearer "))
{
    string token = authHeader.Substring("Bearer ".Length);
    
    // Валідація JWT token
    if (ValidateJwtToken(token))
    {
        // Токен валідний
        await HandleRequest(context);
    }
    else
    {
        context.Response.StatusCode = 401;
        context.Response.Close();
    }
}
else
{
    context.Response.StatusCode = 401;
    context.Response.AddHeader("WWW-Authenticate", "Bearer realm=\"API\"");
    context.Response.Close();
}
```

### Extended Protection

Додатковий захист для Windows Authentication:

```csharp
listener.ExtendedProtectionPolicy = new ExtendedProtectionPolicy(
    PolicyEnforcement.Always,
    ProtectionScenario.TransportSelected,
    new ServiceNameCollection(new[] { "HTTP/myserver.example.com" })
);
```

**Захист від:**
- Credential relay attacks
- Man-in-the-middle attacks

**Вимоги:**
- Windows OS
- HTTPS (для TransportSelected)
- Negotiate або NTLM authentication

---

## Обмеження HttpListener

### Функціональні обмеження

#### 1. Відсутність вбудованої маршрутизації

HttpListener НЕ має системи маршрутизації - потрібно реалізовувати вручну:

```csharp
// Ручна маршрутизація
string path = context.Request.Url.AbsolutePath;
string method = context.Request.HttpMethod;

if (method == "GET" && path == "/api/users")
{
    await HandleGetUsers(context);
}
else if (method == "POST" && path == "/api/users")
{
    await HandleCreateUser(context);
}
else if (method == "GET" && Regex.IsMatch(path, @"^/api/users/\d+$"))
{
    int id = int.Parse(path.Split('/').Last());
    await HandleGetUser(context, id);
}
else
{
    context.Response.StatusCode = 404;
    context.Response.Close();
}
```

**Для складних додатків:** Використовуйте ASP.NET Core з вбудованою маршрутизацією.

#### 2. Відсутність middleware pipeline

Немає концепції middleware як в ASP.NET Core - потрібно реалізовувати вручну:

```csharp
async Task ProcessRequest(HttpListenerContext context)
{
    // Middleware 1: Logging
    LogRequest(context.Request);
    
    // Middleware 2: Authentication
    if (!await AuthenticateRequest(context))
    {
        context.Response.StatusCode = 401;
        context.Response.Close();
        return;
    }
    
    // Middleware 3: Rate Limiting
    if (!await CheckRateLimit(context))
    {
        context.Response.StatusCode = 429;
        context.Response.Close();
        return;
    }
    
    // Actual request handling
    await HandleRequest(context);
}
```

#### 3. Відсутність dependency injection

Немає вбудованого DI контейнера - потрібно використовувати сторонню бібліотеку або ручне управління залежностями.

#### 4. Відсутність Model Binding

Немає автоматичного перетворення JSON/форм у об'єкти - потрібно парсити вручну:

```csharp
// Ручний парсинг JSON
using (StreamReader reader = new StreamReader(request.InputStream))
{
    string json = await reader.ReadToEndAsync();
    var model = JsonSerializer.Deserialize<MyModel>(json);
}
```

#### 5. Відсутність вбудованого multipart/form-data парсера

Для обробки файлів потрібна стороння бібліотека або власна реалізація.

### Платформні обмеження

#### Windows

**Переваги:**
- Використовує HTTP.sys (kernel-mode driver)
- Висока продуктивність
- Повна підтримка всіх features

**Обмеження:**
- Потрібні права адміністратора або URL reservation
- Port sharing через weak wildcard (+)

#### Linux/macOS (.NET Core/5+)

**Реалізація:**
- Managed implementation (не HTTP.sys)
- Менша продуктивність порівняно з Windows

**Обмеження:**
- Weak wildcard (+) НЕ підтримується
- Digest authentication НЕ підтримується
- Windows Integrated Auth НЕ підтримується
- TimeoutManager НЕ підтримується
- ExtendedProtectionPolicy НЕ підтримується

**Рекомендація для production на Linux:** Використовуйте Kestrel (ASP.NET Core).

### Обмеження продуктивності

#### 1. Один запит за раз в GetContextAsync()

```csharp
// Це блокується на кожному запиті
HttpListenerContext context = await listener.GetContextAsync();
```

**Рішення:** Обробляти запити паралельно:
```csharp
while (true)
{
    var context = await listener.GetContextAsync();
    _ = Task.Run(() => HandleRequest(context));
}
```

#### 2. Відсутність connection pooling

Кожне з'єднання може обробляти тільки обмежену кількість запитів.

#### 3. Відсутність HTTP/2 підтримки

HttpListener підтримує тільки HTTP/1.1 та HTTP/1.0.

**Для HTTP/2:** Використовуйте Kestrel в ASP.NET Core.

### Обмеження безпеки

#### 1. Відсутність автоматичного HTTPS redirect

Потрібно реалізовувати вручну:
```csharp
if (!context.Request.IsSecureConnection)
{
    string httpsUrl = $"https://{context.Request.Url.Host}:8443{context.Request.Url.PathAndQuery}";
    context.Response.Redirect(httpsUrl);
    context.Response.Close();
    return;
}
```

#### 2. Відсутність вбудованого CORS

Потрібно додавати CORS headers вручну:
```csharp
response.Headers.Add("Access-Control-Allow-Origin", "*");
response.Headers.Add("Access-Control-Allow-Methods", "GET, POST");
```

#### 3. Відсутність автоматичного request validation

Немає захисту від:
- SQL Injection (потрібна власна валідація)
- XSS attacks (потрібна власна sanitization)
- CSRF (потрібні власні tokens)

### Коли НЕ використовувати HttpListener

**❌ НЕ використовуйте для:**
- Production веб-додатків зі складною логікою
- High-traffic публічних API
- Додатків з великою кількістю endpoints
- Коли потрібні сучасні features (HTTP/2, WebSockets, тощо)
- Коли потрібна кросплатформність з однаковою продуктивністю

**✅ Використовуйте натомість:**
- **ASP.NET Core** (Kestrel) - для повноцінних веб-додатків
- **Nancy** - легкий framework для простих API
- **ServiceStack** - high-performance framework

---

## Огляд HttpClient

### Що таке HttpClient?

**HttpClient** — це клас у .NET для виконання HTTP запитів. Він є основним інструментом для взаємодії з HTTP API, веб-сервісами та веб-сайтами з C# коду.

### Основне призначення

- **Виклик REST API**
- **Взаємодія з веб-сервісами**
- **Завантаження даних з інтернету**
- **Відправка даних на сервери**
- **Integration testing HTTP endpoints**

### Ключові характеристики

| Характеристика | Опис |
|----------------|------|
| **Асинхронність** | Повна підтримка async/await |
| **Переви використання** | Thread-safe, можна reuse між запитами |
| **Connection pooling** | Автоматичне управління з'єднаннями |
| **Compression** | Автоматична обробка gzip/deflate |
| **Redirects** | Автоматичне слідування redirects |
| **Cookies** | Підтримка cookie containers |
| **Timeouts** | Налаштовувані таймаути |
| **Cancellation** | Підтримка CancellationToken |

### Namespace та збірка

```
Namespace: System.Net.Http
Assembly: System.Net.Http.dll
```

**Доступно в:**
- .NET Framework 4.5+
- .NET Core 1.0+
- .NET 5.0+
- .NET Standard 2.0+

### Базовий приклад

```csharp
using System.Net.Http;
using System.Threading.Tasks;

// ⚠️ ВАЖЛИВО: HttpClient повинен бути static або singleton!
private static readonly HttpClient _httpClient = new HttpClient();

async Task<string> GetDataAsync()
{
    HttpResponseMessage response = await _httpClient.GetAsync("https://api.example.com/data");
    
    response.EnsureSuccessStatusCode(); // Викинути exception якщо не 2xx
    
    string content = await response.Content.ReadAsStringAsync();
    return content;
}
```

---

## Життєвий цикл HttpClient

### КРИТИЧНО ВАЖЛИВО: HttpClient Lifecycle

#### ❌ НЕПРАВИЛЬНО - НЕ створюйте HttpClient для кожного запиту!

```csharp
// ❌ ПОГАНА ПРАКТИКА - Socket exhaustion!
async Task BadExample()
{
    using (var client = new HttpClient())
    {
        var response = await client.GetAsync("https://api.example.com");
    }
}
```

**Проблема:**
- Кожен HttpClient створює нове TCP з'єднання
- Сокети не звільняються одразу після Dispose (TIME_WAIT state)
- При багатьох запитах можливе **вичерпання сокетів** (socket exhaustion)
- Серйозні проблеми з продуктивністю

#### ✅ ПРАВИЛЬНО - Reuse HttpClient

**Варіант 1: Static/Singleton HttpClient**
```csharp
// ✅ ПРАВИЛЬНО - Один екземпляр для всього додатку
private static readonly HttpClient _httpClient = new HttpClient();

async Task GoodExample()
{
    var response = await _httpClient.GetAsync("https://api.example.com");
}
```

**Варіант 2: IHttpClientFactory (.NET Core 2.1+)**
```csharp
// ✅ НАЙКРАЩЕ - Використання HttpClientFactory
public class MyService
{
    private readonly IHttpClientFactory _clientFactory;
    
    public MyService(IHttpClientFactory clientFactory)
    {
        _clientFactory = clientFactory;
    }
    
    async Task BestExample()
    {
        var client = _clientFactory.CreateClient();
        var response = await client.GetAsync("https://api.example.com");
    }
}
```

### Чому HttpClient можна reuse?

**HttpClient є thread-safe:**
- Можна безпечно використовувати з багатьох threads
- Внутрішній connection pool автоматично управляється
- Одне з'єднання може обробляти багато запитів (HTTP/1.1 keep-alive)

**Connection pooling:**
```
Thread 1 → ┐
Thread 2 → ├→ HttpClient → Connection Pool → TCP connections → Server
Thread 3 → ┘
```

### Проблема з DNS та її рішення

#### Проблема: DNS Caching

Static HttpClient кешує DNS records назавжди:

```csharp
// Проблема: Якщо DNS record змінився, HttpClient не дізнається
private static readonly HttpClient _httpClient = new HttpClient();
```

**Наслідки:**
- Якщо IP адреса сервера змінилась, HttpClient продовжує використовувати стару
- Проблеми з load balancing
- Проблеми з DNS-based failover

#### Рішення 1: Встановити ConnectionLeaseTimeout (manual)

```csharp
private static readonly HttpClient _httpClient = new HttpClient(new SocketsHttpHandler
{
    PooledConnectionLifetime = TimeSpan.FromMinutes(5) // DNS refresh кожні 5 хвилин
});
```

#### Рішення 2: IHttpClientFactory (автоматично)

`IHttpClientFactory` автоматично управляє lifecycle та DNS:

```csharp
// Додати в Program.cs / Startup.cs
services.AddHttpClient();

// Використання
public class MyService
{
    private readonly IHttpClientFactory _clientFactory;
    
    public MyService(IHttpClientFactory clientFactory)
    {
        _clientFactory = clientFactory;
    }
    
    async Task CallApi()
    {
        var client = _clientFactory.CreateClient();
        // Factory автоматично управляє lifecycle
        var response = await client.GetAsync("https://api.example.com");
    }
}
```

### Lifecycle stages HttpClient

#### 1. Створення

```csharp
HttpClient client = new HttpClient();
```

**Що відбувається:**
- Створюється HttpClient instance
- Створюється внутрішній HttpMessageHandler (зазвичай HttpClientHandler)
- Ініціалізується connection pool

#### 2. Конфігурація

```csharp
client.BaseAddress = new Uri("https://api.example.com/");
client.DefaultRequestHeaders.Add("User-Agent", "MyApp/1.0");
client.Timeout = TimeSpan.FromSeconds(30);
```

**Конфігуровані властивості:**
- **BaseAddress** - базовий URL для всіх запитів
- **DefaultRequestHeaders** - заголовки для всіх запитів
- **Timeout** - глобальний таймаут для запитів
- **MaxResponseContentBufferSize** - максимальний розмір buffer для відповіді

#### 3. Відправка запитів

```csharp
HttpResponseMessage response = await client.GetAsync("/users");
```

**Connection pooling:**
- Якщо є доступне з'єднання в pool - reuse
- Якщо немає - створюється нове TCP з'єднання
- З'єднання повертається в pool після запиту (keep-alive)

#### 4. Обробка відповіді

```csharp
if (response.IsSuccessStatusCode)
{
    string content = await response.Content.ReadAsStringAsync();
}
```

#### 5. Disposal (опціонально)

```csharp
client.Dispose();
```

**Що відбувається:**
- Закриваються всі active з'єднання
- Звільняється connection pool
- Handler dispose

**⚠️ Зазвичай НЕ потрібно викликати Dispose для static/singleton HttpClient!**

### Best Practices для lifecycle

**✅ DO:**
- Використовуйте один HttpClient instance для всього додатку (static/singleton)
- Або використовуйте IHttpClientFactory
- Встановлюйте PooledConnectionLifetime для DNS refresh

**❌ DON'T:**
- НЕ створюйте HttpClient для кожного запиту
- НЕ використовуйте `using` з HttpClient (крім короткоживучих додатків)
- НЕ dispose HttpClient якщо він reusable

---

## HttpClientHandler

### Що таке HttpClientHandler?

**HttpClientHandler** — це клас, який управляє фактичною HTTP комунікацією для HttpClient. Він дозволяє налаштовувати деталі поведінки HTTP з'єднань.

### Створення HttpClient з Handler

```csharp
HttpClientHandler handler = new HttpClientHandler();

// Конфігурація handler
handler.AutomaticDecompression = DecompressionMethods.GZip | DecompressionMethods.Deflate;
handler.AllowAutoRedirect = true;
handler.UseCookies = true;

// Створення HttpClient з handler
HttpClient client = new HttpClient(handler);
```

**⚠️ ВАЖЛИВО:** Handler disposal  
Коли HttpClient dispose, handler також dispose. НЕ reuse handler між різними HttpClient instances.

### Властивості HttpClientHandler

#### Redirects

```csharp
// Автоматично слідувати redirects (301, 302, 307, 308)
handler.AllowAutoRedirect = true; // за замовчуванням

// Максимальна кількість redirects
handler.MaxAutomaticRedirections = 50; // за замовчуванням
```

**Коли вимкнути:**
- Потрібно обробляти redirects вручну
- Потрібно отримати проміжні response headers

#### Compression

```csharp
// Автоматична деcompression відповідей
handler.AutomaticDecompression = DecompressionMethods.GZip | DecompressionMethods.Deflate | DecompressionMethods.Brotli;
```

**DecompressionMethods:**
- `None` - без decompression
- `GZip` - gzip compression
- `Deflate` - deflate compression
- `Brotli` - brotli compression (.NET Core 2.1+)

**Без налаштування:**
```csharp
// Запит
GET /data HTTP/1.1

// Відповідь (стиснута)
Content-Encoding: gzip
[compressed data]

// client.Content.ReadAsStringAsync() - потрібно manually decompress
```

**З налаштуванням:**
```csharp
handler.AutomaticDecompression = DecompressionMethods.GZip;

// Запит (автоматично додається Accept-Encoding)
GET /data HTTP/1.1
Accept-Encoding: gzip, deflate

// Відповідь автоматично decompressed
string content = await response.Content.ReadAsStringAsync(); // Вже decompressed!
```

#### Cookies

```csharp
// Використовувати cookies
handler.UseCookies = true; // за замовчуванням

// Cookie container для управління cookies
handler.CookieContainer = new CookieContainer();

// Додати cookie вручну
handler.CookieContainer.Add(new Uri("https://example.com"), new Cookie("sessionId", "abc123"));

// Після запиту cookies автоматично зберігаються
var response = await client.GetAsync("https://example.com/login");

// Читання cookies
CookieCollection cookies = handler.CookieContainer.GetCookies(new Uri("https://example.com"));
foreach (Cookie cookie in cookies)
{
    Console.WriteLine($"{cookie.Name} = {cookie.Value}");
}
```

**Відключення cookies:**
```csharp
handler.UseCookies = false;

// Тепер можна встановлювати Cookie header вручну
client.DefaultRequestHeaders.Add("Cookie", "sessionId=abc123");
```

#### Credentials та Authentication

```csharp
// Credentials для HTTP аутентифікації
handler.Credentials = new NetworkCredential("username", "password");

// Automatic fallback на default credentials
handler.UseDefaultCredentials = true; // Використати Windows credentials
```

**Схеми аутентифікації:**
- Basic Authentication
- Digest Authentication
- NTLM
- Negotiate (Kerberos)

**Приклад Basic Auth:**
```csharp
handler.Credentials = new NetworkCredential("admin", "password123");

// Запит автоматично включає Authorization header:
// Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=
```

#### Proxy

```csharp
// Використовувати системний proxy
handler.UseProxy = true; // за замовчуванням

// Встановити custom proxy
handler.Proxy = new WebProxy("http://proxy.example.com:8080");

// Proxy з credentials
WebProxy proxy = new WebProxy("http://proxy.example.com:8080")
{
    Credentials = new NetworkCredential("proxyUser", "proxyPassword")
};
handler.Proxy = proxy;

// Bypass proxy для локальних адрес
handler.UseProxy = false;
```

#### SSL/TLS

```csharp
// Мінімальна TLS версія (рекомендовано TLS 1.2+)
handler.SslProtocols = SslProtocols.Tls12 | SslProtocols.Tls13;
```

**Доступні протоколи:**
- `SslProtocols.Tls` - TLS 1.0 (⚠️ застарілий, небезпечний)
- `SslProtocols.Tls11` - TLS 1.1 (⚠️ застарілий)
- `SslProtocols.Tls12` - TLS 1.2 (✅ рекомендовано)
- `SslProtocols.Tls13` - TLS 1.3 (✅ найновіший)

#### Certificate Validation

```csharp
// Custom SSL certificate validation
handler.ServerCertificateCustomValidationCallback = (message, cert, chain, errors) =>
{
    // Логування certificate info
    Console.WriteLine($"Certificate: {cert.Subject}");
    Console.WriteLine($"Issuer: {cert.Issuer}");
    Console.WriteLine($"Errors: {errors}");
    
    // НЕБЕЗПЕЧНО: Приймати всі сертифікати (тільки для development!)
    return true;
    
    // БЕЗПЕЧНО: Приймати тільки валідні сертифікати
    // return errors == SslPolicyErrors.None;
};
```

**⚠️ УВАГА:**  
Ніколи НЕ використовуйте `return true` в production! Це відключає SSL validation і робить додаток вразливим до MITM attacks.

**Безпечний приклад (дозволити self-signed certificates для specific host):**
```csharp
handler.ServerCertificateCustomValidationCallback = (message, cert, chain, errors) =>
{
    if (errors == SslPolicyErrors.None)
        return true;
    
    // Дозволити self-signed для localhost в development
    if (message.RequestUri.Host == "localhost" && 
        errors == SslPolicyErrors.RemoteCertificateChainErrors)
        return true;
    
    return false;
};
```

#### Client Certificates

```csharp
// Додати клієнтський сертифікат для mutual TLS
X509Certificate2 clientCert = new X509Certificate2("client-cert.pfx", "password");
handler.ClientCertificates.Add(clientCert);
```

**Використання:**
- Mutual TLS authentication
- API з вимогою клієнтського сертифіката

#### Pre-authentication

```csharp
// Відправляти credentials в першому запиті (без challenge)
handler.PreAuthenticate = true;
```

**Без PreAuthenticate:**
```
Request 1: GET /api/data
Response 1: 401 Unauthorized, WWW-Authenticate: Basic realm="API"
Request 2: GET /api/data, Authorization: Basic ...
Response 2: 200 OK
```

**З PreAuthenticate:**
```
Request 1: GET /api/data, Authorization: Basic ...
Response 1: 200 OK
```

**Переваги:** Менше round-trips  
**Недоліки:** Credentials відправляються завжди, навіть коли не потрібно

#### Connection Management

```csharp
// Максимальна кількість з'єднань на endpoint
handler.MaxConnectionsPerServer = 10; // за замовчуванням

// Windows only - max response header length
handler.MaxResponseHeadersLength = 64; // KB
```

### SocketsHttpHandler (.NET Core 2.1+)

**SocketsHttpHandler** - покращена версія HttpClientHandler з кращим контролем.

```csharp
SocketsHttpHandler handler = new SocketsHttpHandler();

// Всі властивості HttpClientHandler +
handler.PooledConnectionLifetime = TimeSpan.FromMinutes(5); // DNS refresh
handler.PooledConnectionIdleTimeout = TimeSpan.FromMinutes(2);
handler.ConnectTimeout = TimeSpan.FromSeconds(10);

HttpClient client = new HttpClient(handler);
```

**Додаткові властивості:**

#### PooledConnectionLifetime

Час життя з'єднання в pool (для DNS refresh):

```csharp
handler.PooledConnectionLifetime = TimeSpan.FromMinutes(5);
```

**Вирішує проблему DNS caching:**
- Після 5 хвилин з'єднання закривається
- Нове з'єднання створюється з fresh DNS lookup

#### PooledConnectionIdleTimeout

Таймаут для idle з'єднань:

```csharp
handler.PooledConnectionIdleTimeout = TimeSpan.FromMinutes(2);
```

**Ефект:**
- З'єднання, які не використовуються 2 хвилини, закриваються
- Звільняються ресурси

#### ConnectTimeout

Таймаут для встановлення TCP з'єднання:

```csharp
handler.ConnectTimeout = TimeSpan.FromSeconds(10);
```

**Відрізняється від HttpClient.Timeout:**
- ConnectTimeout - тільки для TCP handshake
- HttpClient.Timeout - для всього запиту (connect + send + receive)

### Delegating Handlers

**DelegatingHandler** - проміжний handler для pre/post-processing запитів.

```csharp
public class LoggingHandler : DelegatingHandler
{
    protected override async Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request, 
        CancellationToken cancellationToken)
    {
        // Pre-processing
        Console.WriteLine($"→ {request.Method} {request.RequestUri}");
        
        // Виклик наступного handler
        HttpResponseMessage response = await base.SendAsync(request, cancellationToken);
        
        // Post-processing
        Console.WriteLine($"← {(int)response.StatusCode} {response.StatusCode}");
        
        return response;
    }
}

// Використання
var handler = new LoggingHandler
{
    InnerHandler = new HttpClientHandler()
};

HttpClient client = new HttpClient(handler);
```

**Pipeline з множинними handlers:**
```csharp
var pipeline = new AuthHandler
{
    InnerHandler = new RetryHandler
    {
        InnerHandler = new LoggingHandler
        {
            InnerHandler = new HttpClientHandler()
        }
    }
};

// Request flow: Client → Auth → Retry → Logging → HttpClientHandler → Network
// Response flow: Network → HttpClientHandler → Logging → Retry → Auth → Client
```

**Використання:**
- Аутентифікація (додавання tokens)
- Logging
- Retry logic
- Rate limiting
- Caching
- Custom error handling

---

## Методи HttpClient

HttpClient надає спрощені методи для типових HTTP операцій та універсальний метод `SendAsync()`.

### GET Методи

#### GetAsync()

Виконує HTTP GET запит.

```csharp
HttpResponseMessage response = await client.GetAsync("https://api.example.com/users");
```

**Повертає:** `HttpResponseMessage` (потрібно manually обробити)

#### GetStringAsync()

GET запит і повертає content як string.

```csharp
string json = await client.GetStringAsync("https://api.example.com/users");
```

**Еквівалентно:**
```csharp
var response = await client.GetAsync(url);
response.EnsureSuccessStatusCode();
string content = await response.Content.ReadAsStringAsync();
```

**Особливості:**
- Викидає exception при не-2xx статусі
- НЕ можна отримати response headers або status code
- Простіше для базових сценаріїв

#### GetByteArrayAsync()

GET запит і повертає content як byte array.

```csharp
byte[] imageBytes = await client.GetByteArrayAsync("https://example.com/image.jpg");
```

**Використання:**
- Завантаження бінарних файлів (зображення, документи)
- Коли потрібен byte[] замість string

#### GetStreamAsync()

GET запит і повертає content як Stream.

```csharp
Stream stream = await client.GetStreamAsync("https://example.com/large-file.zip");

// Зберегти у файл
using (FileStream fileStream = File.Create("downloaded.zip"))
{
    await stream.CopyToAsync(fileStream);
}
```

**Переваги:**
- НЕ буферизує весь response в пам'яті
- Ідеально для великих файлів
- Streaming processing

### POST Методи

#### PostAsync()

Виконує HTTP POST запит з контентом.

```csharp
HttpContent content = new StringContent(json, Encoding.UTF8, "application/json");
HttpResponseMessage response = await client.PostAsync("https://api.example.com/users", content);
```

**HttpContent типи:**
- `StringContent` - текстові дані
- `ByteArrayContent` - бінарні дані
- `StreamContent` - stream дані
- `FormUrlEncodedContent` - форма (application/x-www-form-urlencoded)
- `MultipartFormDataContent` - multipart форма (з файлами)

#### PostAsJsonAsync() (.NET 5+)

POST з автоматичною серіалізацією JSON.

```csharp
var user = new { Name = "John", Email = "john@example.com" };
HttpResponseMessage response = await client.PostAsJsonAsync("https://api.example.com/users", user);
```

**Еквівалентно:**
```csharp
string json = JsonSerializer.Serialize(user);
var content = new StringContent(json, Encoding.UTF8, "application/json");
var response = await client.PostAsync(url, content);
```

### PUT Методи

#### PutAsync()

Виконує HTTP PUT запит.

```csharp
var content = new StringContent(json, Encoding.UTF8, "application/json");
HttpResponseMessage response = await client.PutAsync("https://api.example.com/users/123", content);
```

#### PutAsJsonAsync() (.NET 5+)

PUT з автоматичною серіалізацією JSON.

```csharp
var user = new { Id = 123, Name = "John Updated", Email = "john@example.com" };
HttpResponseMessage response = await client.PutAsJsonAsync("https://api.example.com/users/123", user);
```

### PATCH Method

#### PatchAsync() (.NET 5+)

Виконує HTTP PATCH запит.

```csharp
var updates = new { Email = "newemail@example.com" };
var content = JsonContent.Create(updates);
HttpResponseMessage response = await client.PatchAsync("https://api.example.com/users/123", content);
```

**Примітка:** В .NET Framework немає PatchAsync, потрібно використовувати SendAsync.

### DELETE Methods

#### DeleteAsync()

Виконує HTTP DELETE запит.

```csharp
HttpResponseMessage response = await client.DeleteAsync("https://api.example.com/users/123");
```

### HEAD Method

#### SendAsync() з HEAD

HttpClient не має dedicated HeadAsync(), використовуйте SendAsync:

```csharp
var request = new HttpRequestMessage(HttpMethod.Head, "https://example.com/largefile.zip");
HttpResponseMessage response = await client.SendAsync(request);

// Отримати Content-Length без завантаження файлу
long? fileSize = response.Content.Headers.ContentLength;
```

### Універсальний SendAsync()

**SendAsync()** - найбільш гнучкий метод, дозволяє повний контроль.

```csharp
HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Get, "https://api.example.com/users");
request.Headers.Add("Authorization", "Bearer token123");
request.Headers.Add("X-Custom-Header", "value");

HttpResponseMessage response = await client.SendAsync(request);
```

**Коли використовувати:**
- Потрібен повний контроль над запитом
- Custom HTTP методи (PATCH до .NET 5, WebDAV методи)
- Складні заголовки
- Request cancellation з CancellationToken

**Приклад з cancellation:**
```csharp
CancellationTokenSource cts = new CancellationTokenSource();
cts.CancelAfter(TimeSpan.FromSeconds(5)); // Скасувати через 5 секунд

try
{
    HttpResponseMessage response = await client.SendAsync(request, cts.Token);
}
catch (TaskCanceledException)
{
    Console.WriteLine("Request was cancelled");
}
```

### Порівняння методів

| Метод | HTTP Verb | Content | Response Type | Простота | Гнучкість |
|-------|-----------|---------|---------------|----------|-----------|
| GetStringAsync() | GET | - | string | ⭐⭐⭐⭐⭐ | ⭐ |
| GetByteArrayAsync() | GET | - | byte[] | ⭐⭐⭐⭐⭐ | ⭐ |
| GetStreamAsync() | GET | - | Stream | ⭐⭐⭐⭐ | ⭐⭐ |
| GetAsync() | GET | - | HttpResponseMessage | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| PostAsync() | POST | HttpContent | HttpResponseMessage | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| PostAsJsonAsync() | POST | Object (JSON) | HttpResponseMessage | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| PutAsync() | PUT | HttpContent | HttpResponseMessage | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| DeleteAsync() | DELETE | - | HttpResponseMessage | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| SendAsync() | Any | HttpRequestMessage | HttpResponseMessage | ⭐⭐ | ⭐⭐⭐⭐⭐ |

---

*Документація продовжується... (це перша половина матеріалу)*

