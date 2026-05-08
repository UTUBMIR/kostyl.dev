# 🔧 HTTP на C#: Від TCP до нативних бібліотек

## Зміст

1. [Рівень 1: Базовий TCP сервер (TcpListener)](#рівень-1-базовий-tcp-сервер-tcplistener)
2. [Рівень 2: Парсинг HTTP запитів вручну](#рівень-2-парсинг-http-запитів-вручну)
3. [Рівень 3: HTTP сервер з TcpListener](#рівень-3-http-сервер-з-tcplistener)
4. [Рівень 4: HttpListener - нативна HTTP бібліотека](#рівень-4-httplistener---нативна-http-бібліотека)
5. [Рівень 5: HttpClient - HTTP клієнт](#рівень-5-httpclient---http-клієнт)
6. [Робота з HTTP методами](#робота-з-http-методами)
7. [HTTP заголовки та cookies](#http-заголовки-та-cookies)
8. [Статус коди на практиці](#статус-коди-на-практиці)
9. [Compression і Content Negotiation](#compression-і-content-negotiation)
10. [Chunked Transfer Encoding](#chunked-transfer-encoding)
11. [Кешування](#кешування)
12. [HTTPS (SSL/TLS)](#https-ssltls)
13. [Rate Limiting](#rate-limiting)
14. [Повний приклад: REST API](#повний-приклад-rest-api)

---

## Рівень 1: Базовий TCP сервер (TcpListener)

### Простий Echo сервер

Почнемо з найнижчого рівня - чистого TCP без HTTP.

```csharp
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

class SimpleTcpServer
{
    static async Task Main(string[] args)
    {
        // Створюємо TCP listener на порту 8080
        TcpListener listener = new TcpListener(IPAddress.Any, 8080);
        listener.Start();
        
        Console.WriteLine("TCP сервер запущено на порту 8080");
        Console.WriteLine("Очікування з'єднань...\n");

        while (true)
        {
            // Приймаємо вхідне з'єднання
            TcpClient client = await listener.AcceptTcpClientAsync();
            Console.WriteLine($"Клієнт підключився: {client.Client.RemoteEndPoint}");
            
            // Обробляємо клієнта в окремій задачі
            _ = Task.Run(() => HandleClient(client));
        }
    }

    static async Task HandleClient(TcpClient client)
    {
        using (client)
        {
            NetworkStream stream = client.GetStream();
            byte[] buffer = new byte[1024];
            
            // Читаємо дані від клієнта
            int bytesRead = await stream.ReadAsync(buffer, 0, buffer.Length);
            string received = Encoding.UTF8.GetString(buffer, 0, bytesRead);
            
            Console.WriteLine($"Отримано: {received}");
            
            // Відправляємо echo назад
            string response = $"Echo: {received}";
            byte[] responseBytes = Encoding.UTF8.GetBytes(response);
            await stream.WriteAsync(responseBytes, 0, responseBytes.Length);
            
            Console.WriteLine($"Відправлено: {response}\n");
        }
    }
}
```

**Тестування з telnet:**
```bash
telnet localhost 8080
Hello from telnet!
# Отримаємо: Echo: Hello from telnet!
```

---

## Рівень 2: Парсинг HTTP запитів вручну

### HTTP Request Parser

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public class HttpRequest
{
    public string Method { get; set; }
    public string Path { get; set; }
    public string Version { get; set; }
    public Dictionary<string, string> Headers { get; set; } = new Dictionary<string, string>();
    public string Body { get; set; }

    public static HttpRequest Parse(string requestText)
    {
        var request = new HttpRequest();
        var lines = requestText.Split(new[] { "\r\n" }, StringSplitOptions.None);
        
        if (lines.Length == 0) return null;

        // Парсимо Request Line: GET /path HTTP/1.1
        var requestLine = lines[0].Split(' ');
        if (requestLine.Length >= 3)
        {
            request.Method = requestLine[0];
            request.Path = requestLine[1];
            request.Version = requestLine[2];
        }

        // Парсимо заголовки
        int i = 1;
        for (; i < lines.Length; i++)
        {
            if (string.IsNullOrWhiteSpace(lines[i]))
            {
                // Порожній рядок - кінець заголовків
                i++;
                break;
            }

            var headerParts = lines[i].Split(new[] { ": " }, 2, StringSplitOptions.None);
            if (headerParts.Length == 2)
            {
                request.Headers[headerParts[0]] = headerParts[1];
            }
        }

        // Решта - це body
        if (i < lines.Length)
        {
            request.Body = string.Join("\r\n", lines.Skip(i));
        }

        return request;
    }

    public override string ToString()
    {
        var result = $"Method: {Method}\nPath: {Path}\nVersion: {Version}\n\nHeaders:\n";
        foreach (var header in Headers)
        {
            result += $"  {header.Key}: {header.Value}\n";
        }
        if (!string.IsNullOrEmpty(Body))
        {
            result += $"\nBody:\n{Body}";
        }
        return result;
    }
}

// Приклад використання
class Program
{
    static void Main()
    {
        string rawRequest = @"GET /api/users?page=1 HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0
Accept: application/json
Authorization: Bearer token123

";

        var request = HttpRequest.Parse(rawRequest);
        Console.WriteLine(request);
    }
}
```

**Вивід:**
```
Method: GET
Path: /api/users?page=1
Version: HTTP/1.1

Headers:
  Host: example.com
  User-Agent: Mozilla/5.0
  Accept: application/json
  Authorization: Bearer token123
```

---

## Рівень 3: HTTP сервер з TcpListener

### Повноцінний HTTP сервер на TCP

```csharp
using System;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

class BasicHttpServer
{
    private readonly TcpListener _listener;
    
    public BasicHttpServer(int port)
    {
        _listener = new TcpListener(IPAddress.Any, port);
    }

    public async Task Start()
    {
        _listener.Start();
        Console.WriteLine($"HTTP сервер запущено на http://localhost:{((IPEndPoint)_listener.LocalEndpoint).Port}/");
        Console.WriteLine("Натисніть Ctrl+C для зупинки\n");

        while (true)
        {
            TcpClient client = await _listener.AcceptTcpClientAsync();
            _ = Task.Run(() => HandleHttpRequest(client));
        }
    }

    private async Task HandleHttpRequest(TcpClient client)
    {
        using (client)
        using (NetworkStream stream = client.GetStream())
        using (StreamReader reader = new StreamReader(stream, Encoding.UTF8))
        using (StreamWriter writer = new StreamWriter(stream, Encoding.UTF8) { AutoFlush = true })
        {
            try
            {
                // Читаємо HTTP запит
                string requestLine = await reader.ReadLineAsync();
                if (string.IsNullOrEmpty(requestLine)) return;

                Console.WriteLine($"→ {requestLine}");

                // Парсимо request line
                var parts = requestLine.Split(' ');
                string method = parts[0];
                string path = parts[1];
                string version = parts[2];

                // Читаємо заголовки
                var headers = new System.Collections.Generic.Dictionary<string, string>();
                string headerLine;
                while (!string.IsNullOrEmpty(headerLine = await reader.ReadLineAsync()))
                {
                    var headerParts = headerLine.Split(new[] { ": " }, 2, StringSplitOptions.None);
                    if (headerParts.Length == 2)
                    {
                        headers[headerParts[0]] = headerParts[1];
                    }
                }

                // Генеруємо відповідь на основі шляху
                string responseBody = "";
                string statusLine = "HTTP/1.1 200 OK";
                string contentType = "text/html; charset=utf-8";

                switch (path)
                {
                    case "/":
                        responseBody = GenerateHomePage();
                        break;
                    
                    case "/about":
                        responseBody = "<html><body><h1>Про нас</h1><p>Простий HTTP сервер на C#</p></body></html>";
                        break;
                    
                    case "/api/time":
                        responseBody = $"{{\"time\": \"{DateTime.Now:yyyy-MM-dd HH:mm:ss}\"}}";
                        contentType = "application/json; charset=utf-8";
                        break;
                    
                    case "/api/echo":
                        responseBody = $"{{\"method\": \"{method}\", \"path\": \"{path}\", \"headers\": {headers.Count}}}";
                        contentType = "application/json; charset=utf-8";
                        break;
                    
                    default:
                        statusLine = "HTTP/1.1 404 Not Found";
                        responseBody = "<html><body><h1>404 - Сторінку не знайдено</h1></body></html>";
                        break;
                }

                byte[] bodyBytes = Encoding.UTF8.GetBytes(responseBody);

                // Відправляємо HTTP відповідь
                await writer.WriteLineAsync(statusLine);
                await writer.WriteLineAsync($"Content-Type: {contentType}");
                await writer.WriteLineAsync($"Content-Length: {bodyBytes.Length}");
                await writer.WriteLineAsync("Server: BasicHttpServer/1.0");
                await writer.WriteLineAsync($"Date: {DateTime.UtcNow:R}");
                await writer.WriteLineAsync("Connection: close");
                await writer.WriteLineAsync(); // Порожній рядок (кінець заголовків)

                // Відправляємо body
                await stream.WriteAsync(bodyBytes, 0, bodyBytes.Length);

                Console.WriteLine($"← {statusLine} ({bodyBytes.Length} bytes)\n");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Помилка: {ex.Message}\n");
            }
        }
    }

    private string GenerateHomePage()
    {
        return @"
<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <title>HTTP Сервер на C#</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f0f0f0; }
        h1 { color: #333; }
        .endpoint { background: white; padding: 15px; margin: 10px 0; border-radius: 5px; }
        code { background: #e0e0e0; padding: 3px 8px; border-radius: 3px; }
    </style>
</head>
<body>
    <h1>🚀 Вітаємо на HTTP сервері!</h1>
    <p>Це простий HTTP сервер, побудований на TcpListener</p>
    
    <h2>Доступні endpoints:</h2>
    <div class='endpoint'>
        <strong>GET /</strong> - Ця сторінка
    </div>
    <div class='endpoint'>
        <strong>GET /about</strong> - Про сервер
    </div>
    <div class='endpoint'>
        <strong>GET /api/time</strong> - Поточний час (JSON)
    </div>
    <div class='endpoint'>
        <strong>GET /api/echo</strong> - Echo запиту (JSON)
    </div>
    
    <p>Час на сервері: " + DateTime.Now.ToString("HH:mm:ss") + @"</p>
</body>
</html>";
    }

    static async Task Main(string[] args)
    {
        var server = new BasicHttpServer(8080);
        await server.Start();
    }
}
```

**Тестування в браузері:**
```
http://localhost:8080/
http://localhost:8080/about
http://localhost:8080/api/time
http://localhost:8080/api/echo
http://localhost:8080/notfound  (404)
```

**Вивід сервера:**
```
HTTP сервер запущено на http://localhost:8080/
Натисніть Ctrl+C для зупинки

→ GET / HTTP/1.1
← HTTP/1.1 200 OK (642 bytes)

→ GET /api/time HTTP/1.1
← HTTP/1.1 200 OK (45 bytes)

→ GET /notfound HTTP/1.1
← HTTP/1.1 404 Not Found (67 bytes)
```

---

## Рівень 4: HttpListener - нативна HTTP бібліотека

`HttpListener` - це вбудований в .NET клас для створення HTTP серверів без ASP.NET.

### Базовий приклад HttpListener

```csharp
using System;
using System.Net;
using System.Text;
using System.Threading.Tasks;

class SimpleHttpListener
{
    static async Task Main(string[] args)
    {
        // Створюємо HttpListener
        HttpListener listener = new HttpListener();
        
        // Додаємо префікси (endpoints)
        listener.Prefixes.Add("http://localhost:8080/");
        
        // Запускаємо listener
        listener.Start();
        Console.WriteLine("HTTP сервер (HttpListener) запущено на http://localhost:8080/");
        Console.WriteLine("Натисніть Ctrl+C для зупинки\n");

        // Обробка запитів
        while (true)
        {
            // Чекаємо на запит
            HttpListenerContext context = await listener.GetContextAsync();
            
            // Обробляємо в окремій задачі
            _ = Task.Run(() => HandleRequest(context));
        }
    }

    static async Task HandleRequest(HttpListenerContext context)
    {
        HttpListenerRequest request = context.Request;
        HttpListenerResponse response = context.Response;

        try
        {
            Console.WriteLine($"→ {request.HttpMethod} {request.Url.PathAndQuery}");
            Console.WriteLine($"   User-Agent: {request.UserAgent}");
            Console.WriteLine($"   Remote: {request.RemoteEndPoint}");

            // Готуємо відповідь
            string responseText = $@"
<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <title>HttpListener Demo</title>
</head>
<body>
    <h1>HttpListener працює!</h1>
    <h2>Інформація про запит:</h2>
    <ul>
        <li><strong>Метод:</strong> {request.HttpMethod}</li>
        <li><strong>URL:</strong> {request.Url}</li>
        <li><strong>Path:</strong> {request.Url.PathAndQuery}</li>
        <li><strong>Protocol:</strong> {request.ProtocolVersion}</li>
        <li><strong>Content-Type:</strong> {request.ContentType}</li>
        <li><strong>User-Agent:</strong> {request.UserAgent}</li>
        <li><strong>Remote IP:</strong> {request.RemoteEndPoint}</li>
        <li><strong>Local IP:</strong> {request.LocalEndPoint}</li>
    </ul>
    
    <h2>Заголовки:</h2>
    <ul>
        {string.Join("", request.Headers.AllKeys.Select(key => 
            $"<li><strong>{key}:</strong> {request.Headers[key]}</li>"))}
    </ul>
    
    <p>Час на сервері: {DateTime.Now:yyyy-MM-dd HH:mm:ss}</p>
</body>
</html>";

            byte[] buffer = Encoding.UTF8.GetBytes(responseText);

            // Встановлюємо заголовки відповіді
            response.ContentType = "text/html; charset=utf-8";
            response.ContentLength64 = buffer.Length;
            response.StatusCode = 200;
            response.Headers.Add("Server", "SimpleHttpListener/1.0");
            response.Headers.Add("X-Custom-Header", "Hello from C#");

            // Відправляємо відповідь
            await response.OutputStream.WriteAsync(buffer, 0, buffer.Length);
            response.OutputStream.Close();

            Console.WriteLine($"← 200 OK ({buffer.Length} bytes)\n");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Помилка: {ex.Message}\n");
            response.StatusCode = 500;
            response.Close();
        }
    }
}
```

### Розширений приклад з маршрутизацією

```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

class AdvancedHttpListener
{
    private readonly HttpListener _listener;
    private readonly Dictionary<string, Func<HttpListenerContext, Task>> _routes;

    public AdvancedHttpListener(string prefix)
    {
        _listener = new HttpListener();
        _listener.Prefixes.Add(prefix);
        _routes = new Dictionary<string, Func<HttpListenerContext, Task>>();
    }

    public void AddRoute(string path, Func<HttpListenerContext, Task> handler)
    {
        _routes[path] = handler;
    }

    public async Task Start()
    {
        _listener.Start();
        Console.WriteLine($"Сервер запущено на {_listener.Prefixes.First()}");
        Console.WriteLine("Доступні маршрути:");
        foreach (var route in _routes.Keys)
        {
            Console.WriteLine($"  - {route}");
        }
        Console.WriteLine();

        while (true)
        {
            HttpListenerContext context = await _listener.GetContextAsync();
            _ = Task.Run(async () =>
            {
                try
                {
                    await RouteRequest(context);
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Помилка: {ex.Message}");
                    context.Response.StatusCode = 500;
                    context.Response.Close();
                }
            });
        }
    }

    private async Task RouteRequest(HttpListenerContext context)
    {
        string path = context.Request.Url.AbsolutePath;
        string method = context.Request.HttpMethod;
        
        Console.WriteLine($"→ {method} {path}");

        // Шукаємо точний маршрут
        string routeKey = $"{method} {path}";
        if (_routes.TryGetValue(routeKey, out var handler))
        {
            await handler(context);
            return;
        }

        // Шукаємо маршрут для будь-якого методу
        if (_routes.TryGetValue(path, out handler))
        {
            await handler(context);
            return;
        }

        // 404
        await Send404(context);
    }

    private async Task Send404(HttpListenerContext context)
    {
        var response = new { error = "Not Found", path = context.Request.Url.AbsolutePath };
        await SendJson(context, response, 404);
    }

    public static async Task SendJson(HttpListenerContext context, object data, int statusCode = 200)
    {
        string json = JsonSerializer.Serialize(data, new JsonSerializerOptions 
        { 
            WriteIndented = true,
            Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping
        });
        
        byte[] buffer = Encoding.UTF8.GetBytes(json);
        
        context.Response.ContentType = "application/json; charset=utf-8";
        context.Response.ContentLength64 = buffer.Length;
        context.Response.StatusCode = statusCode;
        
        await context.Response.OutputStream.WriteAsync(buffer, 0, buffer.Length);
        context.Response.Close();

        Console.WriteLine($"← {statusCode} ({buffer.Length} bytes)\n");
    }

    public static async Task SendHtml(HttpListenerContext context, string html, int statusCode = 200)
    {
        byte[] buffer = Encoding.UTF8.GetBytes(html);
        
        context.Response.ContentType = "text/html; charset=utf-8";
        context.Response.ContentLength64 = buffer.Length;
        context.Response.StatusCode = statusCode;
        
        await context.Response.OutputStream.WriteAsync(buffer, 0, buffer.Length);
        context.Response.Close();

        Console.WriteLine($"← {statusCode} ({buffer.Length} bytes)\n");
    }

    // Метод для читання body запиту
    public static async Task<string> ReadRequestBody(HttpListenerRequest request)
    {
        if (!request.HasEntityBody)
            return null;

        using (Stream body = request.InputStream)
        using (StreamReader reader = new StreamReader(body, request.ContentEncoding))
        {
            return await reader.ReadToEndAsync();
        }
    }

    static async Task Main(string[] args)
    {
        var server = new AdvancedHttpListener("http://localhost:8080/");

        // Головна сторінка
        server.AddRoute("/", async (context) =>
        {
            string html = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <title>Advanced HTTP Server</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f5f5f5; }
        .endpoint { background: white; padding: 15px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .method { display: inline-block; padding: 4px 12px; border-radius: 4px; font-weight: bold; color: white; }
        .get { background: #61affe; }
        .post { background: #49cc90; }
        .put { background: #fca130; }
        .delete { background: #f93e3e; }
        code { background: #e8e8e8; padding: 2px 6px; border-radius: 3px; }
    </style>
</head>
<body>
    <h1>🚀 Advanced HTTP Server</h1>
    <p>Сервер на HttpListener з маршрутизацією</p>
    
    <div class='endpoint'>
        <span class='method get'>GET</span> <code>/</code> - Ця сторінка
    </div>
    <div class='endpoint'>
        <span class='method get'>GET</span> <code>/api/users</code> - Список користувачів
    </div>
    <div class='endpoint'>
        <span class='method get'>GET</span> <code>/api/users/:id</code> - Конкретний користувач (наприклад /api/users/1)
    </div>
    <div class='endpoint'>
        <span class='method post'>POST</span> <code>/api/users</code> - Створити користувача
    </div>
    <div class='endpoint'>
        <span class='method get'>GET</span> <code>/api/time</code> - Поточний час
    </div>
    <div class='endpoint'>
        <span class='method get'>GET</span> <code>/api/headers</code> - Всі заголовки запиту
    </div>
    
    <p>Час: " + DateTime.Now.ToString("HH:mm:ss") + @"</p>
    
    <script>
        console.log('Client-side JavaScript працює!');
    </script>
</body>
</html>";
            await SendHtml(context, html);
        });

        // GET /api/users - Список користувачів
        server.AddRoute("GET /api/users", async (context) =>
        {
            var users = new[]
            {
                new { id = 1, name = "Іван", email = "ivan@example.com", age = 28 },
                new { id = 2, name = "Марія", email = "maria@example.com", age = 25 },
                new { id = 3, name = "Петро", email = "petro@example.com", age = 32 }
            };
            
            await SendJson(context, new { users, count = users.Length });
        });

        // GET /api/users/1 (з параметром)
        server.AddRoute("GET /api/users/1", async (context) =>
        {
            var user = new { id = 1, name = "Іван", email = "ivan@example.com", age = 28 };
            await SendJson(context, user);
        });

        server.AddRoute("GET /api/users/2", async (context) =>
        {
            var user = new { id = 2, name = "Марія", email = "maria@example.com", age = 25 };
            await SendJson(context, user);
        });

        // POST /api/users - Створення користувача
        server.AddRoute("POST /api/users", async (context) =>
        {
            string body = await ReadRequestBody(context.Request);
            Console.WriteLine($"   Body: {body}");
            
            if (string.IsNullOrEmpty(body))
            {
                await SendJson(context, new { error = "Body is required" }, 400);
                return;
            }

            try
            {
                var userData = JsonSerializer.Deserialize<Dictionary<string, object>>(body);
                var response = new
                {
                    message = "Користувача створено",
                    id = 4,
                    data = userData,
                    createdAt = DateTime.UtcNow
                };
                await SendJson(context, response, 201);
            }
            catch
            {
                await SendJson(context, new { error = "Invalid JSON" }, 400);
            }
        });

        // GET /api/time
        server.AddRoute("GET /api/time", async (context) =>
        {
            var response = new
            {
                utc = DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss"),
                local = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"),
                timezone = TimeZoneInfo.Local.DisplayName,
                timestamp = DateTimeOffset.UtcNow.ToUnixTimeSeconds()
            };
            await SendJson(context, response);
        });

        // GET /api/headers
        server.AddRoute("GET /api/headers", async (context) =>
        {
            var headers = new Dictionary<string, string>();
            foreach (string key in context.Request.Headers.AllKeys)
            {
                headers[key] = context.Request.Headers[key];
            }
            
            var response = new
            {
                method = context.Request.HttpMethod,
                url = context.Request.Url.ToString(),
                headers = headers,
                queryString = context.Request.QueryString.AllKeys.ToDictionary(
                    k => k ?? "null", 
                    k => context.Request.QueryString[k]
                )
            };
            await SendJson(context, response);
        });

        await server.Start();
    }
}
```

**Тестування з curl:**
```bash
# GET запити
curl http://localhost:8080/api/users
curl http://localhost:8080/api/users/1
curl http://localhost:8080/api/time
curl http://localhost:8080/api/headers

# POST запит
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Олена","email":"olena@example.com","age":27}'
```

---

## Рівень 5: HttpClient - HTTP клієнт

`HttpClient` - стандартний клієнт для HTTP запитів в .NET.

### Базові HTTP запити

```csharp
using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

class HttpClientExamples
{
    // ⚠️ ВАЖЛИВО: HttpClient повинен бути static/singleton
    private static readonly HttpClient _httpClient = new HttpClient();

    static async Task Main(string[] args)
    {
        Console.WriteLine("=== HTTP Client Examples ===\n");

        // Базові налаштування
        _httpClient.BaseAddress = new Uri("https://jsonplaceholder.typicode.com/");
        _httpClient.DefaultRequestHeaders.Add("User-Agent", "CSharp-HttpClient-Demo/1.0");
        _httpClient.Timeout = TimeSpan.FromSeconds(30);

        await GetExample();
        await GetWithHeadersExample();
        await PostJsonExample();
        await PutExample();
        await PatchExample();
        await DeleteExample();
        await ErrorHandlingExample();
    }

    // GET запит
    static async Task GetExample()
    {
        Console.WriteLine("--- GET Request ---");
        
        HttpResponseMessage response = await _httpClient.GetAsync("posts/1");
        
        Console.WriteLine($"Status: {(int)response.StatusCode} {response.StatusCode}");
        Console.WriteLine($"Content-Type: {response.Content.Headers.ContentType}");
        
        string content = await response.Content.ReadAsStringAsync();
        Console.WriteLine($"Body: {content}\n");
    }

    // GET з додатковими заголовками
    static async Task GetWithHeadersExample()
    {
        Console.WriteLine("--- GET with Headers ---");
        
        var request = new HttpRequestMessage(HttpMethod.Get, "posts/1");
        request.Headers.Add("Accept", "application/json");
        request.Headers.Add("Accept-Language", "uk-UA,uk;q=0.9");
        request.Headers.Add("X-Custom-Header", "CustomValue");

        HttpResponseMessage response = await _httpClient.SendAsync(request);
        
        Console.WriteLine("Response Headers:");
        foreach (var header in response.Headers)
        {
            Console.WriteLine($"  {header.Key}: {string.Join(", ", header.Value)}");
        }
        
        string content = await response.Content.ReadAsStringAsync();
        Console.WriteLine($"\nBody: {content.Substring(0, Math.Min(100, content.Length))}...\n");
    }

    // POST з JSON
    static async Task PostJsonExample()
    {
        Console.WriteLine("--- POST JSON ---");
        
        var postData = new
        {
            title = "Новий пост",
            body = "Це тіло поста українською мовою",
            userId = 1
        };

        string json = JsonSerializer.Serialize(postData);
        var content = new StringContent(json, Encoding.UTF8, "application/json");

        HttpResponseMessage response = await _httpClient.PostAsync("posts", content);
        
        Console.WriteLine($"Status: {(int)response.StatusCode} {response.StatusCode}");
        
        string responseBody = await response.Content.ReadAsStringAsync();
        Console.WriteLine($"Response: {responseBody}\n");
    }

    // PUT запит
    static async Task PutExample()
    {
        Console.WriteLine("--- PUT Request ---");
        
        var updateData = new
        {
            id = 1,
            title = "Оновлений заголовок",
            body = "Оновлене тіло",
            userId = 1
        };

        string json = JsonSerializer.Serialize(updateData);
        var content = new StringContent(json, Encoding.UTF8, "application/json");

        HttpResponseMessage response = await _httpClient.PutAsync("posts/1", content);
        
        Console.WriteLine($"Status: {(int)response.StatusCode} {response.StatusCode}");
        string responseBody = await response.Content.ReadAsStringAsync();
        Console.WriteLine($"Response: {responseBody}\n");
    }

    // PATCH запит
    static async Task PatchExample()
    {
        Console.WriteLine("--- PATCH Request ---");
        
        var patchData = new
        {
            title = "Тільки заголовок оновлено"
        };

        string json = JsonSerializer.Serialize(patchData);
        var content = new StringContent(json, Encoding.UTF8, "application/json");

        var request = new HttpRequestMessage(new HttpMethod("PATCH"), "posts/1")
        {
            Content = content
        };

        HttpResponseMessage response = await _httpClient.SendAsync(request);
        
        Console.WriteLine($"Status: {(int)response.StatusCode} {response.StatusCode}");
        string responseBody = await response.Content.ReadAsStringAsync();
        Console.WriteLine($"Response: {responseBody}\n");
    }

    // DELETE запит
    static async Task DeleteExample()
    {
        Console.WriteLine("--- DELETE Request ---");
        
        HttpResponseMessage response = await _httpClient.DeleteAsync("posts/1");
        
        Console.WriteLine($"Status: {(int)response.StatusCode} {response.StatusCode}");
        Console.WriteLine($"Success: {response.IsSuccessStatusCode}\n");
    }

    // Обробка помилок
    static async Task ErrorHandlingExample()
    {
        Console.WriteLine("--- Error Handling ---");
        
        try
        {
            // Запит до неіснуючого ресурсу
            HttpResponseMessage response = await _httpClient.GetAsync("posts/99999");
            
            Console.WriteLine($"Status: {(int)response.StatusCode} {response.StatusCode}");
            
            if (response.IsSuccessStatusCode)
            {
                string content = await response.Content.ReadAsStringAsync();
                Console.WriteLine($"Success: {content}");
            }
            else
            {
                Console.WriteLine($"Error: {response.StatusCode}");
                string errorContent = await response.Content.ReadAsStringAsync();
                Console.WriteLine($"Error Body: {errorContent}");
            }
        }
        catch (HttpRequestException ex)
        {
            Console.WriteLine($"Request Exception: {ex.Message}");
        }
        catch (TaskCanceledException ex)
        {
            Console.WriteLine($"Timeout: {ex.Message}");
        }
        Console.WriteLine();
    }
}
```

### Typed HttpClient з десеріалізацією

```csharp
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Text.Json;
using System.Threading.Tasks;

// Моделі даних
public class Post
{
    public int UserId { get; set; }
    public int Id { get; set; }
    public string Title { get; set; }
    public string Body { get; set; }
}

public class User
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string Email { get; set; }
    public string Phone { get; set; }
    public string Website { get; set; }
}

class TypedHttpClientExample
{
    private static readonly HttpClient _httpClient = new HttpClient
    {
        BaseAddress = new Uri("https://jsonplaceholder.typicode.com/")
    };

    static async Task Main(string[] args)
    {
        // GET з десеріалізацією
        Post post = await _httpClient.GetFromJsonAsync<Post>("posts/1");
        Console.WriteLine($"Post: {post.Title}");
        Console.WriteLine($"Body: {post.Body}\n");

        // GET список
        List<Post> posts = await _httpClient.GetFromJsonAsync<List<Post>>("posts?_limit=5");
        Console.WriteLine($"Отримано {posts.Count} постів:");
        foreach (var p in posts)
        {
            Console.WriteLine($"  - {p.Id}: {p.Title}");
        }
        Console.WriteLine();

        // POST з об'єктом
        var newPost = new Post
        {
            UserId = 1,
            Title = "Новий пост з C#",
            Body = "Це тіло нового поста"
        };

        HttpResponseMessage response = await _httpClient.PostAsJsonAsync("posts", newPost);
        Post createdPost = await response.Content.ReadFromJsonAsync<Post>();
        
        Console.WriteLine($"Створено пост з ID: {createdPost.Id}");
        Console.WriteLine($"Title: {createdPost.Title}\n");

        // PUT з об'єктом
        var updatedPost = new Post
        {
            Id = 1,
            UserId = 1,
            Title = "Оновлений заголовок",
            Body = "Оновлене тіло"
        };

        response = await _httpClient.PutAsJsonAsync("posts/1", updatedPost);
        Post result = await response.Content.ReadFromJsonAsync<Post>();
        Console.WriteLine($"Оновлено: {result.Title}\n");

        // Паралельні запити
        await ParallelRequestsExample();
    }

    static async Task ParallelRequestsExample()
    {
        Console.WriteLine("--- Parallel Requests ---");
        
        var tasks = new List<Task<User>>();
        
        // Запускаємо 5 паралельних запитів
        for (int i = 1; i <= 5; i++)
        {
            tasks.Add(_httpClient.GetFromJsonAsync<User>($"users/{i}"));
        }

        // Чекаємо на всі
        User[] users = await Task.WhenAll(tasks);
        
        Console.WriteLine($"Отримано {users.Length} користувачів паралельно:");
        foreach (var user in users)
        {
            Console.WriteLine($"  - {user.Name} ({user.Email})");
        }
    }
}
```

---

## Робота з HTTP методами

### Демонстрація всіх основних методів

```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

class HttpMethodsDemo
{
    // Імітація бази даних
    private static List<User> _users = new List<User>
    {
        new User { Id = 1, Name = "Іван", Email = "ivan@example.com", Age = 28 },
        new User { Id = 2, Name = "Марія", Email = "maria@example.com", Age = 25 },
        new User { Id = 3, Name = "Петро", Email = "petro@example.com", Age = 32 }
    };

    private static int _nextId = 4;

    static async Task Main(string[] args)
    {
        var listener = new HttpListener();
        listener.Prefixes.Add("http://localhost:8080/");
        listener.Start();

        Console.WriteLine("HTTP Methods Demo Server");
        Console.WriteLine("Запущено на http://localhost:8080/");
        Console.WriteLine("\nПідтримувані методи:");
        Console.WriteLine("  GET    /api/users       - Отримати всіх користувачів");
        Console.WriteLine("  GET    /api/users/:id   - Отримати користувача");
        Console.WriteLine("  POST   /api/users       - Створити користувача");
        Console.WriteLine("  PUT    /api/users/:id   - Повністю оновити");
        Console.WriteLine("  PATCH  /api/users/:id   - Частково оновити");
        Console.WriteLine("  DELETE /api/users/:id   - Видалити користувача");
        Console.WriteLine("  HEAD   /api/users/:id   - Тільки заголовки");
        Console.WriteLine("  OPTIONS /api/users      - Доступні методи\n");

        while (true)
        {
            var context = await listener.GetContextAsync();
            _ = Task.Run(() => HandleRequest(context));
        }
    }

    static async Task HandleRequest(HttpListenerContext context)
    {
        var request = context.Request;
        var response = context.Response;
        
        string method = request.HttpMethod;
        string path = request.Url.AbsolutePath;
        
        Console.WriteLine($"→ {method} {path}");

        try
        {
            // Встановлюємо CORS headers
            response.Headers.Add("Access-Control-Allow-Origin", "*");
            response.Headers.Add("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD");
            response.Headers.Add("Access-Control-Allow-Headers", "Content-Type, Authorization");

            // OPTIONS - preflight
            if (method == "OPTIONS")
            {
                response.StatusCode = 204;
                response.Close();
                Console.WriteLine("← 204 No Content (OPTIONS)\n");
                return;
            }

            // Маршрутизація
            if (path == "/api/users" && method == "GET")
            {
                await GetUsers(context);
            }
            else if (path.StartsWith("/api/users/") && method == "GET")
            {
                int id = int.Parse(path.Split('/').Last());
                await GetUser(context, id);
            }
            else if (path == "/api/users" && method == "POST")
            {
                await CreateUser(context);
            }
            else if (path.StartsWith("/api/users/") && method == "PUT")
            {
                int id = int.Parse(path.Split('/').Last());
                await UpdateUserPut(context, id);
            }
            else if (path.StartsWith("/api/users/") && method == "PATCH")
            {
                int id = int.Parse(path.Split('/').Last());
                await UpdateUserPatch(context, id);
            }
            else if (path.StartsWith("/api/users/") && method == "DELETE")
            {
                int id = int.Parse(path.Split('/').Last());
                await DeleteUser(context, id);
            }
            else if (path.StartsWith("/api/users/") && method == "HEAD")
            {
                int id = int.Parse(path.Split('/').Last());
                await HeadUser(context, id);
            }
            else
            {
                await SendNotFound(context);
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Помилка: {ex.Message}");
            await SendError(context, 500, "Internal Server Error");
        }
    }

    // GET /api/users
    static async Task GetUsers(HttpListenerContext context)
    {
        var response = new { users = _users, count = _users.Count };
        await SendJson(context, response, 200);
    }

    // GET /api/users/:id
    static async Task GetUser(HttpListenerContext context, int id)
    {
        var user = _users.FirstOrDefault(u => u.Id == id);
        
        if (user == null)
        {
            await SendError(context, 404, $"Користувача з ID {id} не знайдено");
            return;
        }

        await SendJson(context, user, 200);
    }

    // POST /api/users
    static async Task CreateUser(HttpListenerContext context)
    {
        string body = await ReadBody(context.Request);
        
        if (string.IsNullOrEmpty(body))
        {
            await SendError(context, 400, "Body is required");
            return;
        }

        try
        {
            var userData = JsonSerializer.Deserialize<User>(body);
            
            // Валідація
            if (string.IsNullOrEmpty(userData.Name))
            {
                await SendError(context, 400, "Name is required");
                return;
            }

            userData.Id = _nextId++;
            _users.Add(userData);

            var response = new
            {
                message = "Користувача створено",
                user = userData
            };

            await SendJson(context, response, 201);
        }
        catch (JsonException)
        {
            await SendError(context, 400, "Invalid JSON");
        }
    }

    // PUT /api/users/:id (повне оновлення)
    static async Task UpdateUserPut(HttpListenerContext context, int id)
    {
        var user = _users.FirstOrDefault(u => u.Id == id);
        
        if (user == null)
        {
            await SendError(context, 404, $"Користувача з ID {id} не знайдено");
            return;
        }

        string body = await ReadBody(context.Request);
        
        try
        {
            var userData = JsonSerializer.Deserialize<User>(body);
            
            // PUT - ПОВНА заміна
            user.Name = userData.Name ?? "";
            user.Email = userData.Email ?? "";
            user.Age = userData.Age;

            var response = new
            {
                message = "Користувача повністю оновлено (PUT)",
                user = user
            };

            await SendJson(context, response, 200);
        }
        catch (JsonException)
        {
            await SendError(context, 400, "Invalid JSON");
        }
    }

    // PATCH /api/users/:id (часткове оновлення)
    static async Task UpdateUserPatch(HttpListenerContext context, int id)
    {
        var user = _users.FirstOrDefault(u => u.Id == id);
        
        if (user == null)
        {
            await SendError(context, 404, $"Користувача з ID {id} не знайдено");
            return;
        }

        string body = await ReadBody(context.Request);
        
        try
        {
            var updates = JsonSerializer.Deserialize<Dictionary<string, JsonElement>>(body);
            
            // PATCH - тільки надані поля
            if (updates.ContainsKey("Name"))
                user.Name = updates["Name"].GetString();
            
            if (updates.ContainsKey("Email"))
                user.Email = updates["Email"].GetString();
            
            if (updates.ContainsKey("Age"))
                user.Age = updates["Age"].GetInt32();

            var response = new
            {
                message = "Користувача частково оновлено (PATCH)",
                user = user,
                updatedFields = updates.Keys
            };

            await SendJson(context, response, 200);
        }
        catch (JsonException)
        {
            await SendError(context, 400, "Invalid JSON");
        }
    }

    // DELETE /api/users/:id
    static async Task DeleteUser(HttpListenerContext context, int id)
    {
        var user = _users.FirstOrDefault(u => u.Id == id);
        
        if (user == null)
        {
            await SendError(context, 404, $"Користувача з ID {id} не знайдено");
            return;
        }

        _users.Remove(user);

        // 204 No Content (без body)
        context.Response.StatusCode = 204;
        context.Response.Close();
        Console.WriteLine($"← 204 No Content (користувача {id} видалено)\n");
    }

    // HEAD /api/users/:id
    static async Task HeadUser(HttpListenerContext context, int id)
    {
        var user = _users.FirstOrDefault(u => u.Id == id);
        
        if (user == null)
        {
            context.Response.StatusCode = 404;
            context.Response.Close();
            Console.WriteLine($"← 404 Not Found (HEAD)\n");
            return;
        }

        // HEAD - тільки заголовки, БЕЗ body
        string json = JsonSerializer.Serialize(user);
        byte[] buffer = Encoding.UTF8.GetBytes(json);

        context.Response.ContentType = "application/json; charset=utf-8";
        context.Response.ContentLength64 = buffer.Length;
        context.Response.StatusCode = 200;
        context.Response.Headers.Add("X-User-Name", user.Name);
        context.Response.Headers.Add("X-User-Age", user.Age.ToString());
        
        // НЕ відправляємо body!
        context.Response.Close();
        Console.WriteLine($"← 200 OK (HEAD, Content-Length: {buffer.Length})\n");
    }

    // Допоміжні методи
    static async Task SendJson(HttpListenerContext context, object data, int statusCode)
    {
        string json = JsonSerializer.Serialize(data, new JsonSerializerOptions 
        { 
            WriteIndented = true,
            Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping
        });
        
        byte[] buffer = Encoding.UTF8.GetBytes(json);
        
        context.Response.ContentType = "application/json; charset=utf-8";
        context.Response.ContentLength64 = buffer.Length;
        context.Response.StatusCode = statusCode;
        
        await context.Response.OutputStream.WriteAsync(buffer, 0, buffer.Length);
        context.Response.Close();

        Console.WriteLine($"← {statusCode} ({buffer.Length} bytes)\n");
    }

    static async Task SendError(HttpListenerContext context, int statusCode, string message)
    {
        var error = new { error = message, statusCode = statusCode };
        await SendJson(context, error, statusCode);
    }

    static async Task SendNotFound(HttpListenerContext context)
    {
        await SendError(context, 404, "Endpoint not found");
    }

    static async Task<string> ReadBody(HttpListenerRequest request)
    {
        if (!request.HasEntityBody)
            return null;

        using (var reader = new StreamReader(request.InputStream, request.ContentEncoding))
        {
            return await reader.ReadToEndAsync();
        }
    }
}

public class User
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string Email { get; set; }
    public int Age { get; set; }
}
```

**Тестування:**
```bash
# GET всіх користувачів
curl http://localhost:8080/api/users

# GET конкретного користувача
curl http://localhost:8080/api/users/1

# POST - створення
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"Name":"Олена","Email":"olena@example.com","Age":27}'

# PUT - повне оновлення
curl -X PUT http://localhost:8080/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"Name":"Іван Новий","Email":"ivan.new@example.com","Age":29}'

# PATCH - часткове оновлення
curl -X PATCH http://localhost:8080/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"Age":30}'

# DELETE
curl -X DELETE http://localhost:8080/api/users/3

# HEAD
curl -I http://localhost:8080/api/users/1

# OPTIONS
curl -X OPTIONS http://localhost:8080/api/users -i
```

---

## HTTP заголовки та cookies

### Робота з заголовками

```csharp
using System;
using System.Collections.Generic;
using System.Net;
using System.Text;
using System.Threading.Tasks;

class HeadersAndCookiesDemo
{
    static async Task Main(string[] args)
    {
        var listener = new HttpListener();
        listener.Prefixes.Add("http://localhost:8080/");
        listener.Start();

        Console.WriteLine("Headers & Cookies Demo");
        Console.WriteLine("http://localhost:8080/\n");

        while (true)
        {
            var context = await listener.GetContextAsync();
            _ = Task.Run(() => HandleRequest(context));
        }
    }

    static async Task HandleRequest(HttpListenerContext context)
    {
        var request = context.Request;
        var response = context.Response;
        string path = request.Url.AbsolutePath;

        Console.WriteLine($"→ {request.HttpMethod} {path}");

        switch (path)
        {
            case "/":
                await ShowHomePage(context);
                break;
            
            case "/headers":
                await ShowHeaders(context);
                break;
            
            case "/set-cookie":
                await SetCookieDemo(context);
                break;
            
            case "/read-cookie":
                await ReadCookieDemo(context);
                break;
            
            case "/custom-headers":
                await CustomHeadersDemo(context);
                break;
            
            case "/cache-demo":
                await CacheDemo(context);
                break;
            
            default:
                response.StatusCode = 404;
                response.Close();
                break;
        }
    }

    // Показати всі заголовки запиту
    static async Task ShowHeaders(HttpListenerContext context)
    {
        var request = context.Request;
        var html = new StringBuilder();
        
        html.Append("<html><head><meta charset='utf-8'><title>Headers</title>");
        html.Append("<style>body{font-family:Arial;margin:40px;}table{border-collapse:collapse;width:100%;}th,td{border:1px solid #ddd;padding:12px;text-align:left;}th{background:#4CAF50;color:white;}</style>");
        html.Append("</head><body>");
        html.Append("<h1>📋 Request Headers</h1>");
        html.Append("<table><tr><th>Header</th><th>Value</th></tr>");
        
        foreach (string key in request.Headers.AllKeys)
        {
            html.Append($"<tr><td><strong>{key}</strong></td><td>{request.Headers[key]}</td></tr>");
        }
        
        html.Append("</table>");
        html.Append($"<h2>Request Info</h2>");
        html.Append($"<p><strong>Method:</strong> {request.HttpMethod}</p>");
        html.Append($"<p><strong>URL:</strong> {request.Url}</p>");
        html.Append($"<p><strong>Protocol:</strong> {request.ProtocolVersion}</p>");
        html.Append($"<p><strong>Content-Type:</strong> {request.ContentType}</p>");
        html.Append($"<p><strong>User-Agent:</strong> {request.UserAgent}</p>");
        html.Append($"<p><strong>Remote IP:</strong> {request.RemoteEndPoint}</p>");
        html.Append("<p><a href='/'>← Назад</a></p>");
        html.Append("</body></html>");

        await SendHtml(context, html.ToString());
    }

    // Встановлення cookies
    static async Task SetCookieDemo(HttpListenerContext context)
    {
        var response = context.Response;
        
        // Встановлюємо різні типи cookies
        
        // 1. Простий cookie
        var cookie1 = new Cookie("username", "ivan_user")
        {
            Path = "/",
            Expires = DateTime.Now.AddDays(7)
        };
        response.AppendCookie(cookie1);
        
        // 2. HttpOnly cookie (безпечний)
        var cookie2 = new Cookie("sessionId", "abc123xyz789")
        {
            Path = "/",
            HttpOnly = true,
            Expires = DateTime.Now.AddHours(1)
        };
        response.AppendCookie(cookie2);
        
        // 3. Cookie з Domain
        var cookie3 = new Cookie("theme", "dark")
        {
            Path = "/",
            Expires = DateTime.Now.AddYears(1)
        };
        response.AppendCookie(cookie3);

        // 4. Session cookie (без Expires - видалиться при закритті браузера)
        var cookie4 = new Cookie("temp_data", "temporary")
        {
            Path = "/"
        };
        response.AppendCookie(cookie4);

        var html = @"
<html>
<head>
    <meta charset='utf-8'>
    <title>Cookies Set</title>
    <style>body{font-family:Arial;margin:40px;}.cookie{background:#e8f5e9;padding:15px;margin:10px 0;border-radius:5px;}</style>
</head>
<body>
    <h1>🍪 Cookies встановлено!</h1>
    
    <div class='cookie'>
        <strong>username</strong> = ivan_user (Expires: 7 днів)
    </div>
    <div class='cookie'>
        <strong>sessionId</strong> = abc123xyz789 (HttpOnly, Expires: 1 година)
    </div>
    <div class='cookie'>
        <strong>theme</strong> = dark (Expires: 1 рік)
    </div>
    <div class='cookie'>
        <strong>temp_data</strong> = temporary (Session cookie - без Expires)
    </div>
    
    <p>Відкрийте DevTools → Application → Cookies, щоб побачити cookies.</p>
    
    <p><a href='/read-cookie'>Прочитати cookies →</a></p>
    <p><a href='/'>← Назад</a></p>
    
    <script>
        console.log('Cookies (доступні через JS):');
        console.log('document.cookie:', document.cookie);
        console.log('');
        console.log('❗ sessionId не видно - він HttpOnly (захист від XSS)');
    </script>
</body>
</html>";

        await SendHtml(context, html);
    }

    // Читання cookies
    static async Task ReadCookieDemo(HttpListenerContext context)
    {
        var request = context.Request;
        var html = new StringBuilder();
        
        html.Append("<html><head><meta charset='utf-8'><title>Read Cookies</title>");
        html.Append("<style>body{font-family:Arial;margin:40px;}.cookie{background:#fff3e0;padding:15px;margin:10px 0;border-radius:5px;}</style>");
        html.Append("</head><body>");
        html.Append("<h1>🍪 Отримані Cookies</h1>");
        
        if (request.Cookies.Count == 0)
        {
            html.Append("<p>Cookies не знайдено. <a href='/set-cookie'>Встановити cookies</a></p>");
        }
        else
        {
            html.Append($"<p>Знайдено {request.Cookies.Count} cookie(s):</p>");
            
            foreach (Cookie cookie in request.Cookies)
            {
                html.Append($"<div class='cookie'>");
                html.Append($"<strong>{cookie.Name}</strong> = {cookie.Value}<br>");
                html.Append($"Path: {cookie.Path}<br>");
                html.Append($"Domain: {cookie.Domain}<br>");
                if (cookie.Expires != DateTime.MinValue)
                    html.Append($"Expires: {cookie.Expires}<br>");
                html.Append($"</div>");
            }
        }
        
        html.Append("<p><a href='/set-cookie'>Встановити нові cookies</a></p>");
        html.Append("<p><a href='/'>← Назад</a></p>");
        html.Append("</body></html>");

        await SendHtml(context, html.ToString());
    }

    // Custom headers
    static async Task CustomHeadersDemo(HttpListenerContext context)
    {
        var response = context.Response;
        
        // Додаємо різні custom headers
        response.Headers.Add("X-Powered-By", "CSharp-HttpListener");
        response.Headers.Add("X-Request-ID", Guid.NewGuid().ToString());
        response.Headers.Add("X-Response-Time", "45ms");
        response.Headers.Add("X-Server-Location", "Ukraine");
        response.Headers.Add("X-Custom-Data", "Це custom заголовок");
        
        // CORS headers
        response.Headers.Add("Access-Control-Allow-Origin", "*");
        response.Headers.Add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");
        response.Headers.Add("Access-Control-Allow-Headers", "Content-Type, Authorization");
        
        // Security headers
        response.Headers.Add("X-Content-Type-Options", "nosniff");
        response.Headers.Add("X-Frame-Options", "DENY");
        response.Headers.Add("X-XSS-Protection", "1; mode=block");
        response.Headers.Add("Strict-Transport-Security", "max-age=31536000");

        var html = @"
<html>
<head>
    <meta charset='utf-8'>
    <title>Custom Headers</title>
    <style>body{font-family:Arial;margin:40px;}.header{background:#e3f2fd;padding:10px;margin:5px 0;border-left:4px solid #2196F3;}</style>
</head>
<body>
    <h1>📨 Custom Response Headers</h1>
    <p>Відповідь містить custom та security заголовки.</p>
    <p>Відкрийте DevTools → Network → Response Headers, щоб побачити всі заголовки.</p>
    
    <h2>Додані заголовки:</h2>
    <div class='header'><strong>X-Powered-By:</strong> CSharp-HttpListener</div>
    <div class='header'><strong>X-Request-ID:</strong> [UUID]</div>
    <div class='header'><strong>X-Response-Time:</strong> 45ms</div>
    <div class='header'><strong>X-Server-Location:</strong> Ukraine</div>
    <div class='header'><strong>Access-Control-Allow-Origin:</strong> *</div>
    <div class='header'><strong>X-Content-Type-Options:</strong> nosniff</div>
    <div class='header'><strong>X-Frame-Options:</strong> DENY</div>
    <div class='header'><strong>Strict-Transport-Security:</strong> max-age=31536000</div>
    
    <p><a href='/'>← Назад</a></p>
    
    <script>
        fetch(window.location.href)
            .then(res => {
                console.log('Response Headers:');
                res.headers.forEach((value, name) => {
                    console.log(`${name}: ${value}`);
                });
            });
    </script>
</body>
</html>";

        await SendHtml(context, html);
    }

    // Cache headers demo
    static async Task CacheDemo(HttpListenerContext context)
    {
        var response = context.Response;
        
        // Cache-Control headers
        response.Headers.Add("Cache-Control", "public, max-age=3600");
        response.Headers.Add("ETag", "\"abc123def456\"");
        response.Headers.Add("Last-Modified", DateTime.UtcNow.AddHours(-1).ToString("R"));
        response.Headers.Add("Expires", DateTime.UtcNow.AddHours(1).ToString("R"));

        var html = $@"
<html>
<head>
    <meta charset='utf-8'>
    <title>Cache Demo</title>
    <style>body{{font-family:Arial;margin:40px;}}.info{{background:#fff9c4;padding:15px;border-radius:5px;}}</style>
</head>
<body>
    <h1>💾 Cache Headers Demo</h1>
    
    <div class='info'>
        <h3>Встановлені cache headers:</h3>
        <ul>
            <li><strong>Cache-Control:</strong> public, max-age=3600 (1 година)</li>
            <li><strong>ETag:</strong> ""abc123def456""</li>
            <li><strong>Last-Modified:</strong> {DateTime.UtcNow.AddHours(-1):R}</li>
            <li><strong>Expires:</strong> {DateTime.UtcNow.AddHours(1):R}</li>
        </ul>
    </div>
    
    <p>При повторному запиті цієї сторінки протягом 1 години, браузер використає закешовану версію.</p>
    <p>Час генерації: {DateTime.Now:HH:mm:ss}</p>
    
    <p><a href='/'>← Назад</a></p>
    
    <button onclick='location.reload()'>Перезавантажити сторінку</button>
    <button onclick='location.reload(true)'>Hard Reload (Ctrl+Shift+R)</button>
</body>
</html>";

        await SendHtml(context, html);
    }

    static async Task ShowHomePage(HttpListenerContext context)
    {
        var html = @"
<html>
<head>
    <meta charset='utf-8'>
    <title>Headers & Cookies Demo</title>
    <style>
        body{font-family:Arial;margin:40px;background:#f5f5f5;}
        .link{display:block;background:white;padding:20px;margin:15px 0;border-radius:8px;text-decoration:none;color:#333;box-shadow:0 2px 4px rgba(0,0,0,0.1);}
        .link:hover{box-shadow:0 4px 8px rgba(0,0,0,0.15);}
        h1{color:#333;}
    </style>
</head>
<body>
    <h1>🌐 HTTP Headers & Cookies Demo</h1>
    <p>Виберіть демо:</p>
    
    <a href='/headers' class='link'>
        <strong>📋 Показати всі заголовки запиту</strong><br>
        <small>Переглянути всі HTTP headers, що надійшли з запитом</small>
    </a>
    
    <a href='/set-cookie' class='link'>
        <strong>🍪 Встановити Cookies</strong><br>
        <small>Демонстрація встановлення різних типів cookies</small>
    </a>
    
    <a href='/read-cookie' class='link'>
        <strong>📖 Прочитати Cookies</strong><br>
        <small>Показати всі cookies, що надійшли з запитом</small>
    </a>
    
    <a href='/custom-headers' class='link'>
        <strong>📨 Custom Headers</strong><br>
        <small>Відповідь з custom та security headers</small>
    </a>
    
    <a href='/cache-demo' class='link'>
        <strong>💾 Cache Headers Demo</strong><br>
        <small>Демонстрація cache-control headers</small>
    </a>
</body>
</html>";

        await SendHtml(context, html);
    }

    static async Task SendHtml(HttpListenerContext context, string html)
    {
        byte[] buffer = Encoding.UTF8.GetBytes(html);
        context.Response.ContentType = "text/html; charset=utf-8";
        context.Response.ContentLength64 = buffer.Length;
        context.Response.StatusCode = 200;
        await context.Response.OutputStream.WriteAsync(buffer, 0, buffer.Length);
        context.Response.Close();
        Console.WriteLine($"← 200 OK ({buffer.Length} bytes)\n");
    }
}
```

---

## Статус коди на практиці

```csharp
using System;
using System.Net;
using System.Text;
using System.Threading.Tasks;

class StatusCodesDemo
{
    static async Task Main(string[] args)
    {
        var listener = new HttpListener();
        listener.Prefixes.Add("http://localhost:8080/");
        listener.Start();

        Console.WriteLine("HTTP Status Codes Demo");
        Console.WriteLine("http://localhost:8080/\n");

        while (true)
        {
            var context = await listener.GetContextAsync();
            _ = Task.Run(() => HandleRequest(context));
        }
    }

    static async Task HandleRequest(HttpListenerContext context)
    {
        string path = context.Request.Url.AbsolutePath;
        Console.WriteLine($"→ {context.Request.HttpMethod} {path}");

        switch (path)
        {
            // 2xx - Success
            case "/200": await Send200(context); break;
            case "/201": await Send201(context); break;
            case "/204": await Send204(context); break;
            
            // 3xx - Redirection
            case "/301": await Send301(context); break;
            case "/302": await Send302(context); break;
            case "/304": await Send304(context); break;
            
            // 4xx - Client Errors
            case "/400": await Send400(context); break;
            case "/401": await Send401(context); break;
            case "/403": await Send403(context); break;
            case "/404": await Send404(context); break;
            case "/405": await Send405(context); break;
            case "/409": await Send409(context); break;
            case "/429": await Send429(context); break;
            
            // 5xx - Server Errors
            case "/500": await Send500(context); break;
            case "/503": await Send503(context); break;
            
            case "/": await ShowHomePage(context); break;
            
            default:
                await Send404(context);
                break;
        }
    }

    // 200 OK
    static async Task Send200(HttpListenerContext context)
    {
        var response = new
        {
            statusCode = 200,
            status = "OK",
            message = "Запит успішно оброблено",
            data = new { id = 1, name = "Успішна відповідь" }
        };
        await SendJsonResponse(context, response, 200);
    }

    // 201 Created
    static async Task Send201(HttpListenerContext context)
    {
        var response = new
        {
            statusCode = 201,
            status = "Created",
            message = "Новий ресурс створено",
            data = new { id = 123, name = "Новий ресурс" }
        };
        
        context.Response.Headers.Add("Location", "/api/resources/123");
        await SendJsonResponse(context, response, 201);
    }

    // 204 No Content
    static async Task Send204(HttpListenerContext context)
    {
        context.Response.StatusCode = 204;
        context.Response.Close();
        Console.WriteLine("← 204 No Content (без body)\n");
    }

    // 301 Moved Permanently
    static async Task Send301(HttpListenerContext context)
    {
        context.Response.StatusCode = 301;
        context.Response.Headers.Add("Location", "http://localhost:8080/200");
        context.Response.Close();
        Console.WriteLine("← 301 Moved Permanently → /200\n");
    }

    // 302 Found (Temporary Redirect)
    static async Task Send302(HttpListenerContext context)
    {
        context.Response.StatusCode = 302;
        context.Response.Headers.Add("Location", "http://localhost:8080/200");
        context.Response.Close();
        Console.WriteLine("← 302 Found (Temporary) → /200\n");
    }

    // 304 Not Modified
    static async Task Send304(HttpListenerContext context)
    {
        context.Response.StatusCode = 304;
        context.Response.Headers.Add("ETag", "\"abc123\"");
        context.Response.Headers.Add("Cache-Control", "public, max-age=3600");
        context.Response.Close();
        Console.WriteLine("← 304 Not Modified\n");
    }

    // 400 Bad Request
    static async Task Send400(HttpListenerContext context)
    {
        var response = new
        {
            statusCode = 400,
            error = "Bad Request",
            message = "Невалідний формат запиту",
            details = "Очікується JSON, отримано text/plain"
        };
        await SendJsonResponse(context, response, 400);
    }

    // 401 Unauthorized
    static async Task Send401(HttpListenerContext context)
    {
        context.Response.Headers.Add("WWW-Authenticate", "Bearer realm=\"API\"");
        
        var response = new
        {
            statusCode = 401,
            error = "Unauthorized",
            message = "Аутентифікація required",
            hint = "Додайте заголовок: Authorization: Bearer <token>"
        };
        await SendJsonResponse(context, response, 401);
    }

    // 403 Forbidden
    static async Task Send403(HttpListenerContext context)
    {
        var response = new
        {
            statusCode = 403,
            error = "Forbidden",
            message = "Доступ заборонено",
            reason = "У вас немає прав для цієї операції"
        };
        await SendJsonResponse(context, response, 403);
    }

    // 404 Not Found
    static async Task Send404(HttpListenerContext context)
    {
        var response = new
        {
            statusCode = 404,
            error = "Not Found",
            message = "Ресурс не знайдено",
            path = context.Request.Url.AbsolutePath
        };
        await SendJsonResponse(context, response, 404);
    }

    // 405 Method Not Allowed
    static async Task Send405(HttpListenerContext context)
    {
        context.Response.Headers.Add("Allow", "GET, POST");
        
        var response = new
        {
            statusCode = 405,
            error = "Method Not Allowed",
            message = $"Метод {context.Request.HttpMethod} не підтримується",
            allowedMethods = new[] { "GET", "POST" }
        };
        await SendJsonResponse(context, response, 405);
    }

    // 409 Conflict
    static async Task Send409(HttpListenerContext context)
    {
        var response = new
        {
            statusCode = 409,
            error = "Conflict",
            message = "Конфлікт з поточним станом ресурсу",
            details = "Користувач з таким email вже існує"
        };
        await SendJsonResponse(context, response, 409);
    }

    // 429 Too Many Requests
    static async Task Send429(HttpListenerContext context)
    {
        context.Response.Headers.Add("Retry-After", "60");
        context.Response.Headers.Add("X-RateLimit-Limit", "100");
        context.Response.Headers.Add("X-RateLimit-Remaining", "0");
        context.Response.Headers.Add("X-RateLimit-Reset", DateTimeOffset.UtcNow.AddMinutes(1).ToUnixTimeSeconds().ToString());
        
        var response = new
        {
            statusCode = 429,
            error = "Too Many Requests",
            message = "Перевищено ліміт запитів",
            limit = 100,
            retryAfter = 60
        };
        await SendJsonResponse(context, response, 429);
    }

    // 500 Internal Server Error
    static async Task Send500(HttpListenerContext context)
    {
        var response = new
        {
            statusCode = 500,
            error = "Internal Server Error",
            message = "Щось пішло не так на сервері",
            errorId = Guid.NewGuid().ToString(),
            timestamp = DateTime.UtcNow
        };
        await SendJsonResponse(context, response, 500);
    }

    // 503 Service Unavailable
    static async Task Send503(HttpListenerContext context)
    {
        context.Response.Headers.Add("Retry-After", "120");
        
        var response = new
        {
            statusCode = 503,
            error = "Service Unavailable",
            message = "Сервіс тимчасово недоступний",
            reason = "Технічне обслуговування",
            estimatedDowntime = "120 seconds"
        };
        await SendJsonResponse(context, response, 503);
    }

    static async Task ShowHomePage(HttpListenerContext context)
    {
        var html = @"
<html>
<head>
    <meta charset='utf-8'>
    <title>Status Codes Demo</title>
    <style>
        body{font-family:Arial;margin:40px;background:#f5f5f5;}
        .status{display:inline-block;padding:20px;margin:10px;background:white;border-radius:8px;text-decoration:none;color:#333;box-shadow:0 2px 4px rgba(0,0,0,0.1);min-width:150px;text-align:center;}
        .status:hover{box-shadow:0 4px 8px rgba(0,0,0,0.15);}
        .success{border-left:4px solid #4CAF50;}
        .redirect{border-left:4px solid #2196F3;}
        .client-error{border-left:4px solid #FF9800;}
        .server-error{border-left:4px solid #f44336;}
        h2{color:#555;margin-top:30px;}
    </style>
</head>
<body>
    <h1>📊 HTTP Status Codes Demo</h1>
    <p>Клікніть на статус код, щоб побачити приклад відповіді</p>
    
    <h2>2xx - Success</h2>
    <a href='/200' class='status success'><strong>200</strong><br>OK</a>
    <a href='/201' class='status success'><strong>201</strong><br>Created</a>
    <a href='/204' class='status success'><strong>204</strong><br>No Content</a>
    
    <h2>3xx - Redirection</h2>
    <a href='/301' class='status redirect'><strong>301</strong><br>Moved Permanently</a>
    <a href='/302' class='status redirect'><strong>302</strong><br>Found</a>
    <a href='/304' class='status redirect'><strong>304</strong><br>Not Modified</a>
    
    <h2>4xx - Client Errors</h2>
    <a href='/400' class='status client-error'><strong>400</strong><br>Bad Request</a>
    <a href='/401' class='status client-error'><strong>401</strong><br>Unauthorized</a>
    <a href='/403' class='status client-error'><strong>403</strong><br>Forbidden</a>
    <a href='/404' class='status client-error'><strong>404</strong><br>Not Found</a>
    <a href='/405' class='status client-error'><strong>405</strong><br>Method Not Allowed</a>
    <a href='/409' class='status client-error'><strong>409</strong><br>Conflict</a>
    <a href='/429' class='status client-error'><strong>429</strong><br>Too Many Requests</a>
    
    <h2>5xx - Server Errors</h2>
    <a href='/500' class='status server-error'><strong>500</strong><br>Internal Server Error</a>
    <a href='/503' class='status server-error'><strong>503</strong><br>Service Unavailable</a>
</body>
</html>";

        await SendHtmlResponse(context, html, 200);
    }

    static async Task SendJsonResponse(HttpListenerContext context, object data, int statusCode)
    {
        string json = System.Text.Json.JsonSerializer.Serialize(data, new System.Text.Json.JsonSerializerOptions 
        { 
            WriteIndented = true,
            Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping
        });
        
        byte[] buffer = Encoding.UTF8.GetBytes(json);
        context.Response.ContentType = "application/json; charset=utf-8";
        context.Response.ContentLength64 = buffer.Length;
        context.Response.StatusCode = statusCode;
        await context.Response.OutputStream.WriteAsync(buffer, 0, buffer.Length);
        context.Response.Close();
        Console.WriteLine($"← {statusCode} ({buffer.Length} bytes)\n");
    }

    static async Task SendHtmlResponse(HttpListenerContext context, string html, int statusCode)
    {
        byte[] buffer = Encoding.UTF8.GetBytes(html);
        context.Response.ContentType = "text/html; charset=utf-8";
        context.Response.ContentLength64 = buffer.Length;
        context.Response.StatusCode = statusCode;
        await context.Response.OutputStream.WriteAsync(buffer, 0, buffer.Length);
        context.Response.Close();
        Console.WriteLine($"← {statusCode} ({buffer.Length} bytes)\n");
    }
}
```

---

## Compression і Content Negotiation

### GZIP Compression

```csharp
using System;
using System.IO;
using System.IO.Compression;
using System.Net;
using System.Text;
using System.Threading.Tasks;

class CompressionDemo
{
    static async Task Main(string[] args)
    {
        var listener = new HttpListener();
        listener.Prefixes.Add("http://localhost:8080/");
        listener.Start();

        Console.WriteLine("Compression Demo Server");
        Console.WriteLine("http://localhost:8080/\n");

        while (true)
        {
            var context = await listener.GetContextAsync();
            _ = Task.Run(() => HandleRequest(context));
        }
    }

    static async Task HandleRequest(HttpListenerContext context)
    {
        var request = context.Request;
        var response = context.Response;
        
        Console.WriteLine($"→ {request.HttpMethod} {request.Url.AbsolutePath}");
        Console.WriteLine($"   Accept-Encoding: {request.Headers["Accept-Encoding"]}");

        // Генеруємо великий response для демонстрації compression
        string originalContent = GenerateLargeHtmlContent();
        byte[] originalBytes = Encoding.UTF8.GetBytes(originalContent);
        
        Console.WriteLine($"   Original size: {originalBytes.Length} bytes");

        // Перевіряємо чи клієнт підтримує compression
        string acceptEncoding = request.Headers["Accept-Encoding"] ?? "";
        
        byte[] responseBytes;
        string contentEncoding = null;

        if (acceptEncoding.Contains("gzip"))
        {
            // Стискаємо з GZIP
            responseBytes = CompressGzip(originalBytes);
            contentEncoding = "gzip";
            Console.WriteLine($"   Compressed (gzip): {responseBytes.Length} bytes ({100 - (responseBytes.Length * 100 / originalBytes.Length)}% економії)");
        }
        else if (acceptEncoding.Contains("deflate"))
        {
            // Стискаємо з Deflate
            responseBytes = CompressDeflate(originalBytes);
            contentEncoding = "deflate";
            Console.WriteLine($"   Compressed (deflate): {responseBytes.Length} bytes");
        }
        else
        {
            // Без compression
            responseBytes = originalBytes;
            Console.WriteLine($"   No compression");
        }

        // Встановлюємо headers
        response.ContentType = "text/html; charset=utf-8";
        response.ContentLength64 = responseBytes.Length;
        
        if (contentEncoding != null)
        {
            response.Headers.Add("Content-Encoding", contentEncoding);
        }
        
        response.Headers.Add("Vary", "Accept-Encoding");
        response.StatusCode = 200;

        // Відправляємо відповідь
        await response.OutputStream.WriteAsync(responseBytes, 0, responseBytes.Length);
        response.Close();

        Console.WriteLine($"← 200 OK ({responseBytes.Length} bytes)\n");
    }

    static byte[] CompressGzip(byte[] data)
    {
        using (var outputStream = new MemoryStream())
        {
            using (var gzipStream = new GZipStream(outputStream, CompressionMode.Compress))
            {
                gzipStream.Write(data, 0, data.Length);
            }
            return outputStream.ToArray();
        }
    }

    static byte[] CompressDeflate(byte[] data)
    {
        using (var outputStream = new MemoryStream())
        {
            using (var deflateStream = new DeflateStream(outputStream, CompressionMode.Compress))
            {
                deflateStream.Write(data, 0, data.Length);
            }
            return outputStream.ToArray();
        }
    }

    static string GenerateLargeHtmlContent()
    {
        var html = new StringBuilder();
        html.Append("<!DOCTYPE html><html><head><meta charset='utf-8'><title>Compression Demo</title>");
        html.Append("<style>body{font-family:Arial;margin:40px;}table{border-collapse:collapse;width:100%;}td,th{border:1px solid #ddd;padding:8px;}th{background:#4CAF50;color:white;}</style>");
        html.Append("</head><body>");
        html.Append("<h1>🗜️ HTTP Compression Demo</h1>");
        html.Append("<p>Ця сторінка демонструє GZIP/Deflate compression.</p>");
        html.Append("<table><tr><th>ID</th><th>Name</th><th>Email</th><th>Description</th></tr>");
        
        // Генеруємо багато даних для compression
        for (int i = 1; i <= 1000; i++)
        {
            html.Append($"<tr><td>{i}</td><td>User {i}</td><td>user{i}@example.com</td><td>This is a sample description for user number {i}. Lorem ipsum dolor sit amet, consectetur adipiscing elit.</td></tr>");
        }
        
        html.Append("</table>");
        html.Append("<p>Перевірте Network tab в DevTools, щоб побачити:</p>");
        html.Append("<ul><li>Content-Encoding: gzip</li><li>Розмір до/після compression</li></ul>");
        html.Append("</body></html>");
        
        return html.ToString();
    }
}
```

### Content Negotiation

```csharp
using System;
using System.Collections.Generic;
using System.Net;
using System.Text;
using System.Text.Json;
using System.Xml.Linq;
using System.Threading.Tasks;

class ContentNegotiationDemo
{
    static async Task Main(string[] args)
    {
        var listener = new HttpListener();
        listener.Prefixes.Add("http://localhost:8080/");
        listener.Start();

        Console.WriteLine("Content Negotiation Demo");
        Console.WriteLine("http://localhost:8080/\n");

        while (true)
        {
            var context = await listener.GetContextAsync();
            _ = Task.Run(() => HandleRequest(context));
        }
    }

    static async Task HandleRequest(HttpListenerContext context)
    {
        var request = context.Request;
        string accept = request.Headers["Accept"] ?? "*/*";
        
        Console.WriteLine($"→ {request.HttpMethod} {request.Url.AbsolutePath}");
        Console.WriteLine($"   Accept: {accept}");

        // Дані для відповіді
        var userData = new
        {
            id = 1,
            name = "Іван Петренко",
            email = "ivan@example.com",
            age = 28,
            city = "Київ"
        };

        // Content Negotiation - вибираємо формат на основі Accept header
        if (accept.Contains("application/json"))
        {
            await SendJson(context, userData);
        }
        else if (accept.Contains("application/xml") || accept.Contains("text/xml"))
        {
            await SendXml(context, userData);
        }
        else if (accept.Contains("text/plain"))
        {
            await SendPlainText(context, userData);
        }
        else if (accept.Contains("text/html"))
        {
            await SendHtml(context, userData);
        }
        else
        {
            // Default - JSON
            await SendJson(context, userData);
        }
    }

    static async Task SendJson(HttpListenerContext context, object data)
    {
        string json = JsonSerializer.Serialize(data, new JsonSerializerOptions { WriteIndented = true });
        byte[] buffer = Encoding.UTF8.GetBytes(json);
        
        context.Response.ContentType = "application/json; charset=utf-8";
        context.Response.ContentLength64 = buffer.Length;
        context.Response.StatusCode = 200;
        
        await context.Response.OutputStream.WriteAsync(buffer, 0, buffer.Length);
        context.Response.Close();
        
        Console.WriteLine($"← 200 OK (JSON, {buffer.Length} bytes)\n");
    }

    static async Task SendXml(HttpListenerContext context, dynamic data)
    {
        var xml = new XElement("user",
            new XElement("id", data.id),
            new XElement("name", data.name),
            new XElement("email", data.email),
            new XElement("age", data.age),
            new XElement("city", data.city)
        );
        
        string xmlString = xml.ToString();
        byte[] buffer = Encoding.UTF8.GetBytes(xmlString);
        
        context.Response.ContentType = "application/xml; charset=utf-8";
        context.Response.ContentLength64 = buffer.Length;
        context.Response.StatusCode = 200;
        
        await context.Response.OutputStream.WriteAsync(buffer, 0, buffer.Length);
        context.Response.Close();
        
        Console.WriteLine($"← 200 OK (XML, {buffer.Length} bytes)\n");
    }

    static async Task SendPlainText(HttpListenerContext context, dynamic data)
    {
        string text = $"ID: {data.id}\nName: {data.name}\nEmail: {data.email}\nAge: {data.age}\nCity: {data.city}";
        byte[] buffer = Encoding.UTF8.GetBytes(text);
        
        context.Response.ContentType = "text/plain; charset=utf-8";
        context.Response.ContentLength64 = buffer.Length;
        context.Response.StatusCode = 200;
        
        await context.Response.OutputStream.WriteAsync(buffer, 0, buffer.Length);
        context.Response.Close();
        
        Console.WriteLine($"← 200 OK (Plain Text, {buffer.Length} bytes)\n");
    }

    static async Task SendHtml(HttpListenerContext context, dynamic data)
    {
        string html = $@"
<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <title>User Profile</title>
    <style>body{{font-family:Arial;margin:40px;}}table{{border-collapse:collapse;}}td,th{{border:1px solid #ddd;padding:12px;}}</style>
</head>
<body>
    <h1>👤 User Profile</h1>
    <table>
        <tr><th>Field</th><th>Value</th></tr>
        <tr><td><strong>ID</strong></td><td>{data.id}</td></tr>
        <tr><td><strong>Name</strong></td><td>{data.name}</td></tr>
        <tr><td><strong>Email</strong></td><td>{data.email}</td></tr>
        <tr><td><strong>Age</strong></td><td>{data.age}</td></tr>
        <tr><td><strong>City</strong></td><td>{data.city}</td></tr>
    </table>
</body>
</html>";
        
        byte[] buffer = Encoding.UTF8.GetBytes(html);
        
        context.Response.ContentType = "text/html; charset=utf-8";
        context.Response.ContentLength64 = buffer.Length;
        context.Response.StatusCode = 200;
        
        await context.Response.OutputStream.WriteAsync(buffer, 0, buffer.Length);
        context.Response.Close();
        
        Console.WriteLine($"← 200 OK (HTML, {buffer.Length} bytes)\n");
    }
}
```

**Тестування:**
```bash
# JSON
curl http://localhost:8080/ -H "Accept: application/json"

# XML
curl http://localhost:8080/ -H "Accept: application/xml"

# Plain Text
curl http://localhost:8080/ -H "Accept: text/plain"

# HTML
curl http://localhost:8080/ -H "Accept: text/html"
```

---

## Chunked Transfer Encoding

### Streaming Response з Chunks

```csharp
using System;
using System.Net;
using System.Text;
using System.Threading.Tasks;

class ChunkedTransferDemo
{
    static async Task Main(string[] args)
    {
        var listener = new HttpListener();
        listener.Prefixes.Add("http://localhost:8080/");
        listener.Start();

        Console.WriteLine("Chunked Transfer Encoding Demo");
        Console.WriteLine("http://localhost:8080/\n");

        while (true)
        {
            var context = await listener.GetContextAsync();
            _ = Task.Run(() => HandleRequest(context));
        }
    }

    static async Task HandleRequest(HttpListenerContext context)
    {
        string path = context.Request.Url.AbsolutePath;
        
        Console.WriteLine($"→ {context.Request.HttpMethod} {path}");

        switch (path)
        {
            case "/":
                await ShowHomePage(context);
                break;
            
            case "/stream":
                await StreamResponse(context);
                break;
            
            case "/large-file":
                await StreamLargeFile(context);
                break;
            
            case "/sse":
                await ServerSentEvents(context);
                break;
            
            default:
                context.Response.StatusCode = 404;
                context.Response.Close();
                break;
        }
    }

    // Звичайна сторінка
    static async Task ShowHomePage(HttpListenerContext context)
    {
        var html = @"
<html>
<head>
    <meta charset='utf-8'>
    <title>Chunked Transfer Demo</title>
</head>
<body>
    <h1>📦 Chunked Transfer Encoding</h1>
    <ul>
        <li><a href='/stream'>Streaming Response</a> - дані відправляються частинами</li>
        <li><a href='/large-file'>Large File Streaming</a> - симуляція великого файлу</li>
        <li><a href='/sse'>Server-Sent Events</a> - real-time stream</li>
    </ul>
</body>
</html>";
        
        byte[] buffer = Encoding.UTF8.GetBytes(html);
        context.Response.ContentType = "text/html; charset=utf-8";
        context.Response.ContentLength64 = buffer.Length;
        await context.Response.OutputStream.WriteAsync(buffer, 0, buffer.Length);
        context.Response.Close();
    }

    // Chunked streaming
    static async Task StreamResponse(HttpListenerContext context)
    {
        var response = context.Response;
        
        // SendChunked = true активує Transfer-Encoding: chunked
        response.SendChunked = true;
        response.ContentType = "text/html; charset=utf-8";
        
        Console.WriteLine("   Відправка chunked response...");

        // Відправляємо HTML частинами
        await WriteChunk(response, "<html><head><meta charset='utf-8'><title>Streaming</title></head><body>");
        await WriteChunk(response, "<h1>🌊 Streaming Response</h1>");
        await WriteChunk(response, "<p>Дані відправляються частинами (chunks)</p>");
        await WriteChunk(response, "<ul>");
        
        // Симулюємо затримку між chunks
        for (int i = 1; i <= 10; i++)
        {
            await Task.Delay(500); // Затримка 500ms
            await WriteChunk(response, $"<li>Chunk {i} - {DateTime.Now:HH:mm:ss.fff}</li>");
            Console.WriteLine($"   → Chunk {i} sent");
        }
        
        await WriteChunk(response, "</ul>");
        await WriteChunk(response, "<p>✅ Всі chunks відправлено!</p>");
        await WriteChunk(response, "</body></html>");
        
        response.Close();
        Console.WriteLine("← Chunked response completed\n");
    }

    // Streaming великого файлу
    static async Task StreamLargeFile(HttpListenerContext context)
    {
        var response = context.Response;
        response.SendChunked = true;
        response.ContentType = "text/plain; charset=utf-8";
        
        Console.WriteLine("   Streaming large file...");

        // Генеруємо та відправляємо великий файл по частинах
        int totalChunks = 100;
        int chunkSize = 1024; // 1KB per chunk
        
        for (int i = 0; i < totalChunks; i++)
        {
            // Генеруємо chunk даних
            string chunkData = $"Chunk {i + 1}/{totalChunks}: {new string('X', chunkSize - 50)}\n";
            byte[] buffer = Encoding.UTF8.GetBytes(chunkData);
            
            await response.OutputStream.WriteAsync(buffer, 0, buffer.Length);
            await response.OutputStream.FlushAsync();
            
            if (i % 10 == 0)
            {
                Console.WriteLine($"   → {i + 1}/{totalChunks} chunks sent ({(i + 1) * chunkSize} bytes)");
            }
            
            await Task.Delay(50); // Невелика затримка
        }
        
        response.Close();
        Console.WriteLine($"← Large file streaming completed ({totalChunks * chunkSize} bytes)\n");
    }

    // Server-Sent Events (SSE)
    static async Task ServerSentEvents(HttpListenerContext context)
    {
        var response = context.Response;
        response.ContentType = "text/event-stream";
        response.Headers.Add("Cache-Control", "no-cache");
        response.Headers.Add("Connection", "keep-alive");
        response.SendChunked = true;
        
        Console.WriteLine("   SSE connection established");

        try
        {
            // Відправляємо події кожну секунду протягом 30 секунд
            for (int i = 1; i <= 30; i++)
            {
                string eventData = $"data: {{\"time\": \"{DateTime.Now:HH:mm:ss}\", \"count\": {i}}}\n\n";
                byte[] buffer = Encoding.UTF8.GetBytes(eventData);
                
                await response.OutputStream.WriteAsync(buffer, 0, buffer.Length);
                await response.OutputStream.FlushAsync();
                
                Console.WriteLine($"   → Event {i} sent");
                
                await Task.Delay(1000);
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"   Client disconnected: {ex.Message}");
        }
        
        response.Close();
        Console.WriteLine("← SSE connection closed\n");
    }

    static async Task WriteChunk(HttpListenerResponse response, string data)
    {
        byte[] buffer = Encoding.UTF8.GetBytes(data);
        await response.OutputStream.WriteAsync(buffer, 0, buffer.Length);
        await response.OutputStream.FlushAsync();
    }
}
```

**HTML клієнт для SSE:**
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>SSE Client</title>
</head>
<body>
    <h1>Server-Sent Events Client</h1>
    <div id="events"></div>
    
    <script>
        const eventSource = new EventSource('http://localhost:8080/sse');
        const eventsDiv = document.getElementById('events');
        
        eventSource.onmessage = function(event) {
            const data = JSON.parse(event.data);
            const p = document.createElement('p');
            p.textContent = `Time: ${data.time}, Count: ${data.count}`;
            eventsDiv.appendChild(p);
        };
        
        eventSource.onerror = function(error) {
            console.error('SSE error:', error);
            eventSource.close();
        };
    </script>
</body>
</html>
```

---

## Кешування

### ETag і Last-Modified

```csharp
using System;
using System.Collections.Generic;
using System.Net;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

class CachingDemo
{
    // Зберігаємо ETags для ресурсів
    private static Dictionary<string, CacheInfo> _cache = new Dictionary<string, CacheInfo>();

    class CacheInfo
    {
        public string ETag { get; set; }
        public DateTime LastModified { get; set; }
        public string Content { get; set; }
    }

    static async Task Main(string[] args)
    {
        // Ініціалізуємо кеш з тестовими даними
        _cache["/api/users"] = new CacheInfo
        {
            ETag = GenerateETag("users-v1"),
            LastModified = DateTime.UtcNow.AddHours(-1),
            Content = "{\"users\": [{\"id\": 1, \"name\": \"Іван\"}]}"
        };

        var listener = new HttpListener();
        listener.Prefixes.Add("http://localhost:8080/");
        listener.Start();

        Console.WriteLine("HTTP Caching Demo");
        Console.WriteLine("http://localhost:8080/\n");

        while (true)
        {
            var context = await listener.GetContextAsync();
            _ = Task.Run(() => HandleRequest(context));
        }
    }

    static async Task HandleRequest(HttpListenerContext context)
    {
        var request = context.Request;
        var response = context.Response;
        string path = request.Url.AbsolutePath;

        Console.WriteLine($"→ {request.HttpMethod} {path}");

        if (path == "/")
        {
            await ShowHomePage(context);
            return;
        }

        if (!_cache.ContainsKey(path))
        {
            response.StatusCode = 404;
            response.Close();
            Console.WriteLine("← 404 Not Found\n");
            return;
        }

        var cacheInfo = _cache[path];

        // Перевіряємо If-None-Match (ETag)
        string ifNoneMatch = request.Headers["If-None-Match"];
        if (ifNoneMatch != null && ifNoneMatch == cacheInfo.ETag)
        {
            // ETag збігається - ресурс не змінився
            response.StatusCode = 304;
            response.Headers.Add("ETag", cacheInfo.ETag);
            response.Headers.Add("Cache-Control", "public, max-age=3600");
            response.Close();
            Console.WriteLine($"← 304 Not Modified (ETag match)\n");
            return;
        }

        // Перевіряємо If-Modified-Since
        string ifModifiedSince = request.Headers["If-Modified-Since"];
        if (ifModifiedSince != null)
        {
            if (DateTime.TryParse(ifModifiedSince, out DateTime clientDate))
            {
                if (cacheInfo.LastModified <= clientDate)
                {
                    response.StatusCode = 304;
                    response.Headers.Add("Last-Modified", cacheInfo.LastModified.ToString("R"));
                    response.Headers.Add("Cache-Control", "public, max-age=3600");
                    response.Close();
                    Console.WriteLine($"← 304 Not Modified (Last-Modified)\n");
                    return;
                }
            }
        }

        // Ресурс змінився або перший запит - відправляємо повну відповідь
        byte[] buffer = Encoding.UTF8.GetBytes(cacheInfo.Content);

        response.ContentType = "application/json; charset=utf-8";
        response.ContentLength64 = buffer.Length;
        response.StatusCode = 200;
        
        // Встановлюємо cache headers
        response.Headers.Add("ETag", cacheInfo.ETag);
        response.Headers.Add("Last-Modified", cacheInfo.LastModified.ToString("R"));
        response.Headers.Add("Cache-Control", "public, max-age=3600");
        response.Headers.Add("Expires", DateTime.UtcNow.AddHours(1).ToString("R"));

        await response.OutputStream.WriteAsync(buffer, 0, buffer.Length);
        response.Close();

        Console.WriteLine($"← 200 OK ({buffer.Length} bytes)");
        Console.WriteLine($"   ETag: {cacheInfo.ETag}");
        Console.WriteLine($"   Last-Modified: {cacheInfo.LastModified:R}\n");
    }

    static async Task ShowHomePage(HttpListenerContext context)
    {
        var html = @"
<html>
<head>
    <meta charset='utf-8'>
    <title>Caching Demo</title>
    <style>
        body{font-family:Arial;margin:40px;}
        button{padding:10px 20px;margin:5px;cursor:pointer;}
        #result{background:#f0f0f0;padding:15px;margin-top:20px;border-radius:5px;}
    </style>
</head>
<body>
    <h1>💾 HTTP Caching Demo</h1>
    <p>Натисніть кнопку кілька разів, щоб побачити 304 Not Modified</p>
    
    <button onclick='fetchData()'>Fetch /api/users</button>
    <button onclick='fetchData(true)'>Force Refresh (bypass cache)</button>
    
    <div id='result'></div>
    
    <script>
        async function fetchData(forceRefresh = false) {
            const resultDiv = document.getElementById('result');
            const headers = {};
            
            if (forceRefresh) {
                headers['Cache-Control'] = 'no-cache';
            }
            
            const startTime = performance.now();
            const response = await fetch('/api/users', { headers });
            const endTime = performance.now();
            
            const status = response.status;
            const etag = response.headers.get('ETag');
            const lastModified = response.headers.get('Last-Modified');
            const cacheControl = response.headers.get('Cache-Control');
            
            let bodyText = '';
            if (status === 200) {
                bodyText = await response.text();
            }
            
            resultDiv.innerHTML = `
                <strong>Status:</strong> ${status} ${response.statusText}<br>
                <strong>Time:</strong> ${(endTime - startTime).toFixed(2)}ms<br>
                <strong>ETag:</strong> ${etag}<br>
                <strong>Last-Modified:</strong> ${lastModified}<br>
                <strong>Cache-Control:</strong> ${cacheControl}<br>
                ${bodyText ? `<strong>Body:</strong> ${bodyText}` : '<em>No body (304)</em>'}
            `;
        }
    </script>
</body>
</html>";
        
        byte[] buffer = Encoding.UTF8.GetBytes(html);
        context.Response.ContentType = "text/html; charset=utf-8";
        context.Response.ContentLength64 = buffer.Length;
        await context.Response.OutputStream.WriteAsync(buffer, 0, buffer.Length);
        context.Response.Close();
    }

    static string GenerateETag(string content)
    {
        using (var md5 = MD5.Create())
        {
            byte[] hash = md5.ComputeHash(Encoding.UTF8.GetBytes(content));
            return $"\"{BitConverter.ToString(hash).Replace("-", "").ToLower()}\"";
        }
    }
}
```

---

## HTTPS (SSL/TLS)

### HttpClient з HTTPS

```csharp
using System;
using System.Net;
using System.Net.Http;
using System.Net.Security;
using System.Security.Cryptography.X509Certificates;
using System.Threading.Tasks;

class HttpsClientDemo
{
    static async Task Main(string[] args)
    {
        Console.WriteLine("=== HTTPS Client Demo ===\n");

        await BasicHttpsRequest();
        await HttpsWithCustomValidation();
        await HttpsWithClientCertificate();
    }

    // Базовий HTTPS запит
    static async Task BasicHttpsRequest()
    {
        Console.WriteLine("--- Basic HTTPS Request ---");
        
        using (var client = new HttpClient())
        {
            try
            {
                var response = await client.GetAsync("https://www.google.com");
                
                Console.WriteLine($"Status: {response.StatusCode}");
                Console.WriteLine($"Protocol: {response.Version}");
                Console.WriteLine("Security Headers:");
                
                if (response.Headers.Contains("Strict-Transport-Security"))
                    Console.WriteLine($"  HSTS: {response.Headers.GetValues("Strict-Transport-Security").First()}");
                
                Console.WriteLine($"\nContent preview:");
                string content = await response.Content.ReadAsStringAsync();
                Console.WriteLine(content.Substring(0, Math.Min(200, content.Length)) + "...\n");
            }
            catch (HttpRequestException ex)
            {
                Console.WriteLine($"Error: {ex.Message}\n");
            }
        }
    }

    // HTTPS з custom certificate validation
    static async Task HttpsWithCustomValidation()
    {
        Console.WriteLine("--- HTTPS with Custom Certificate Validation ---");
        
        var handler = new HttpClientHandler();
        
        // Custom certificate validation (для тестування - НЕ використовуйте в production!)
        handler.ServerCertificateCustomValidationCallback = (message, cert, chain, errors) =>
        {
            Console.WriteLine($"\nCertificate validation:");
            Console.WriteLine($"  Subject: {cert.Subject}");
            Console.WriteLine($"  Issuer: {cert.Issuer}");
            Console.WriteLine($"  Valid from: {cert.NotBefore}");
            Console.WriteLine($"  Valid to: {cert.NotAfter}");
            Console.WriteLine($"  Thumbprint: {cert.Thumbprint}");
            Console.WriteLine($"  Errors: {errors}");
            
            // Приймаємо сертифікат (тільки для демо!)
            return true;
        };

        using (var client = new HttpClient(handler))
        {
            var response = await client.GetAsync("https://www.google.com");
            Console.WriteLine($"\nStatus: {response.StatusCode}\n");
        }
    }

    // HTTPS з клієнтським сертифікатом
    static async Task HttpsWithClientCertificate()
    {
        Console.WriteLine("--- HTTPS with Client Certificate ---");
        
        var handler = new HttpClientHandler();
        
        // Завантаження клієнтського сертифіката (приклад)
        // var cert = new X509Certificate2("client-cert.pfx", "password");
        // handler.ClientCertificates.Add(cert);
        
        Console.WriteLine("Client certificate authentication would be configured here.");
        Console.WriteLine("For demo purposes, this step is commented out.\n");
    }
}
```

### Налаштування HttpListener для HTTPS

```csharp
/*
 * HTTPS з HttpListener вимагає налаштування сертифіката на рівні системи.
 * 
 * Кроки для налаштування HTTPS:
 * 
 * 1. Створити self-signed certificate:
 *    
 *    New-SelfSignedCertificate -DnsName "localhost" -CertStoreLocation "cert:\LocalMachine\My"
 *    
 * 2. Прив'язати сертифікат до порту (PowerShell з правами адміністратора):
 *    
 *    $cert = Get-ChildItem -Path cert:\LocalMachine\My | Where-Object {$_.Subject -like "*localhost*"}
 *    $guid = [guid]::NewGuid().ToString("B")
 *    
 *    netsh http add sslcert ipport=0.0.0.0:8443 `
 *      certhash=$($cert.Thumbprint) `
 *      appid="$guid"
 *    
 * 3. Код для HTTPS HttpListener:
 */

using System;
using System.Net;
using System.Text;
using System.Threading.Tasks;

class HttpsListenerDemo
{
    static async Task Main(string[] args)
    {
        var listener = new HttpListener();
        
        // HTTPS prefix
        listener.Prefixes.Add("https://localhost:8443/");
        
        // Також можна додати HTTP
        listener.Prefixes.Add("http://localhost:8080/");
        
        listener.Start();
        Console.WriteLine("HTTPS Server:");
        Console.WriteLine("  https://localhost:8443/");
        Console.WriteLine("  http://localhost:8080/\n");

        while (true)
        {
            var context = await listener.GetContextAsync();
            _ = Task.Run(() => HandleRequest(context));
        }
    }

    static async Task HandleRequest(HttpListenerContext context)
    {
        bool isHttps = context.Request.IsSecureConnection;
        string protocol = isHttps ? "HTTPS" : "HTTP";
        
        Console.WriteLine($"→ {protocol} {context.Request.HttpMethod} {context.Request.Url.AbsolutePath}");

        var html = $@"
<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <title>{protocol} Demo</title>
    <style>
        body{{font-family:Arial;margin:40px;}}
        .secure{{color:green;}} .insecure{{color:red;}}
    </style>
</head>
<body>
    <h1 class='{(isHttps ? "secure" : "insecure")}'>
        {(isHttps ? "🔒 Secure (HTTPS)" : "⚠️ Insecure (HTTP)")}
    </h1>
    <h2>Connection Info:</h2>
    <ul>
        <li><strong>Protocol:</strong> {protocol}</li>
        <li><strong>Is Secure:</strong> {isHttps}</li>
        <li><strong>URL:</strong> {context.Request.Url}</li>
        <li><strong>Remote:</strong> {context.Request.RemoteEndPoint}</li>
        <li><strong>Local:</strong> {context.Request.LocalEndPoint}</li>
    </ul>
    {(isHttps ? "" : "<p><a href='https://localhost:8443/'>Switch to HTTPS</a></p>")}
</body>
</html>";

        byte[] buffer = Encoding.UTF8.GetBytes(html);
        
        context.Response.ContentType = "text/html; charset=utf-8";
        context.Response.ContentLength64 = buffer.Length;
        
        if (isHttps)
        {
            // HTTPS security headers
            context.Response.Headers.Add("Strict-Transport-Security", "max-age=31536000; includeSubDomains");
        }
        
        await context.Response.OutputStream.WriteAsync(buffer, 0, buffer.Length);
        context.Response.Close();
    }
}
```

---

## Rate Limiting

```csharp
using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

class RateLimitingDemo
{
    // Зберігаємо інформацію про запити від клієнтів
    private static ConcurrentDictionary<string, ClientRateLimit> _rateLimits = 
        new ConcurrentDictionary<string, ClientRateLimit>();

    class ClientRateLimit
    {
        public Queue<DateTime> Requests { get; set; } = new Queue<DateTime>();
        public int Limit { get; set; } = 10; // 10 запитів
        public TimeSpan Window { get; set; } = TimeSpan.FromMinutes(1); // за 1 хвилину
    }

    static async Task Main(string[] args)
    {
        var listener = new HttpListener();
        listener.Prefixes.Add("http://localhost:8080/");
        listener.Start();

        Console.WriteLine("Rate Limiting Demo");
        Console.WriteLine("Ліміт: 10 запитів на хвилину на IP");
        Console.WriteLine("http://localhost:8080/\n");

        while (true)
        {
            var context = await listener.GetContextAsync();
            _ = Task.Run(() => HandleRequest(context));
        }
    }

    static async Task HandleRequest(HttpListenerContext context)
    {
        var request = context.Request;
        var response = context.Response;
        
        string clientIp = request.RemoteEndPoint.Address.ToString();
        
        Console.WriteLine($"→ {request.HttpMethod} {request.Url.AbsolutePath} from {clientIp}");

        // Отримуємо або створюємо rate limit для клієнта
        var rateLimit = _rateLimits.GetOrAdd(clientIp, _ => new ClientRateLimit());

        // Очищуємо старі запити (поза window)
        DateTime now = DateTime.UtcNow;
        while (rateLimit.Requests.Count > 0 && 
               now - rateLimit.Requests.Peek() > rateLimit.Window)
        {
            rateLimit.Requests.Dequeue();
        }

        int requestCount = rateLimit.Requests.Count;
        int remaining = rateLimit.Limit - requestCount;

        // Встановлюємо rate limit headers
        response.Headers.Add("X-RateLimit-Limit", rateLimit.Limit.ToString());
        response.Headers.Add("X-RateLimit-Remaining", Math.Max(0, remaining).ToString());
        response.Headers.Add("X-RateLimit-Reset", 
            new DateTimeOffset(now.Add(rateLimit.Window)).ToUnixTimeSeconds().ToString());

        // Перевіряємо чи не перевищено ліміт
        if (requestCount >= rateLimit.Limit)
        {
            // 429 Too Many Requests
            int retryAfter = (int)rateLimit.Window.TotalSeconds;
            response.Headers.Add("Retry-After", retryAfter.ToString());
            
            var error = new
            {
                statusCode = 429,
                error = "Too Many Requests",
                message = $"Rate limit exceeded. Limit: {rateLimit.Limit} requests per {rateLimit.Window.TotalMinutes} minutes",
                retryAfter = retryAfter,
                limit = rateLimit.Limit,
                remaining = 0,
                reset = new DateTimeOffset(now.Add(rateLimit.Window)).ToUnixTimeSeconds()
            };

            await SendJson(context, error, 429);
            Console.WriteLine($"← 429 Too Many Requests (limit: {rateLimit.Limit})\n");
            return;
        }

        // Додаємо запит до історії
        rateLimit.Requests.Enqueue(now);

        // Обробляємо запит
        string path = request.Url.AbsolutePath;

        if (path == "/")
        {
            await ShowHomePage(context, rateLimit, remaining);
        }
        else if (path == "/api/data")
        {
            var data = new
            {
                message = "Success",
                timestamp = DateTime.UtcNow,
                rateLimit = new
                {
                    limit = rateLimit.Limit,
                    remaining = remaining,
                    reset = new DateTimeOffset(now.Add(rateLimit.Window)).ToUnixTimeSeconds()
                }
            };
            await SendJson(context, data, 200);
        }
        else
        {
            response.StatusCode = 404;
            response.Close();
        }

        Console.WriteLine($"← 200 OK (requests: {requestCount + 1}/{rateLimit.Limit}, remaining: {remaining - 1})\n");
    }

    static async Task ShowHomePage(HttpListenerContext context, ClientRateLimit rateLimit, int remaining)
    {
        var html = $@"
<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <title>Rate Limiting Demo</title>
    <style>
        body{{font-family:Arial;margin:40px;}}
        button{{padding:10px 20px;margin:5px;cursor:pointer;}}
        #status{{background:#f0f0f0;padding:15px;margin-top:20px;border-radius:5px;}}
        .error{{background:#ffebee;}}
    </style>
</head>
<body>
    <h1>⏱️ Rate Limiting Demo</h1>
    <p>Ліміт: <strong>{rateLimit.Limit} запитів за {rateLimit.Window.TotalMinutes} хвилину</strong></p>
    <p>Залишилось запитів: <strong id='remaining'>{remaining}</strong></p>
    
    <button onclick='makeRequest()'>Make Request</button>
    <button onclick='makeMany()'>Make 20 Requests (spam)</button>
    <button onclick='location.reload()'>Refresh Page</button>
    
    <div id='status'></div>
    
    <script>
        async function makeRequest() {{
            const statusDiv = document.getElementById('status');
            const remainingSpan = document.getElementById('remaining');
            
            try {{
                const response = await fetch('/api/data');
                const headers = {{
                    'X-RateLimit-Limit': response.headers.get('X-RateLimit-Limit'),
                    'X-RateLimit-Remaining': response.headers.get('X-RateLimit-Remaining'),
                    'X-RateLimit-Reset': response.headers.get('X-RateLimit-Reset')
                }};
                
                remainingSpan.textContent = headers['X-RateLimit-Remaining'];
                
                if (response.status === 200) {{
                    const data = await response.json();
                    statusDiv.className = '';
                    statusDiv.innerHTML = `
                        <strong>✅ Success</strong><br>
                        Status: ${{response.status}}<br>
                        Remaining: ${{headers['X-RateLimit-Remaining']}}/${{headers['X-RateLimit-Limit']}}<br>
                        Reset: ${{new Date(headers['X-RateLimit-Reset'] * 1000).toLocaleTimeString()}}
                    `;
                }} else if (response.status === 429) {{
                    const error = await response.json();
                    statusDiv.className = 'error';
                    statusDiv.innerHTML = `
                        <strong>❌ Rate Limit Exceeded!</strong><br>
                        ${{error.message}}<br>
                        Retry after: ${{error.retryAfter}} seconds
                    `;
                }}
            }} catch (error) {{
                statusDiv.className = 'error';
                statusDiv.textContent = 'Error: ' + error.message;
            }}
        }}
        
        async function makeMany() {{
            for (let i = 0; i < 20; i++) {{
                await makeRequest();
                await new Promise(resolve => setTimeout(resolve, 100));
            }}
        }}
    </script>
</body>
</html>";

        byte[] buffer = Encoding.UTF8.GetBytes(html);
        context.Response.ContentType = "text/html; charset=utf-8";
        context.Response.ContentLength64 = buffer.Length;
        await context.Response.OutputStream.WriteAsync(buffer, 0, buffer.Length);
        context.Response.Close();
    }

    static async Task SendJson(HttpListenerContext context, object data, int statusCode)
    {
        string json = JsonSerializer.Serialize(data, new JsonSerializerOptions 
        { 
            WriteIndented = true,
            Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping
        });
        
        byte[] buffer = Encoding.UTF8.GetBytes(json);
        context.Response.ContentType = "application/json; charset=utf-8";
        context.Response.ContentLength64 = buffer.Length;
        context.Response.StatusCode = statusCode;
        await context.Response.OutputStream.WriteAsync(buffer, 0, buffer.Length);
        context.Response.Close();
    }
}
```

---

## Повний приклад: REST API

### Повнофункціональний REST API з усіма фічами

```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

// Моделі
public class Product
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string Description { get; set; }
    public decimal Price { get; set; }
    public int Stock { get; set; }
    public string Category { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime? UpdatedAt { get; set; }
}

// REST API Server
class RestApiServer
{
    private readonly HttpListener _listener;
    private static List<Product> _products = new List<Product>
    {
        new Product { Id = 1, Name = "Ноутбук", Description = "Gaming laptop", Price = 35000, Stock = 5, Category = "Electronics", CreatedAt = DateTime.UtcNow.AddDays(-10) },
        new Product { Id = 2, Name = "Миша", Description = "Wireless mouse", Price = 500, Stock = 20, Category = "Electronics", CreatedAt = DateTime.UtcNow.AddDays(-5) },
        new Product { Id = 3, Name = "Клавіатура", Description = "Mechanical keyboard", Price = 2000, Stock = 10, Category = "Electronics", CreatedAt = DateTime.UtcNow.AddDays(-3) }
    };
    private static int _nextId = 4;

    public RestApiServer(string prefix)
    {
        _listener = new HttpListener();
        _listener.Prefixes.Add(prefix);
    }

    public async Task Start()
    {
        _listener.Start();
        Console.WriteLine("🚀 REST API Server started");
        Console.WriteLine($"📍 {_listener.Prefixes.First()}");
        Console.WriteLine("\nEndpoints:");
        Console.WriteLine("  GET    /api/products          - List all products");
        Console.WriteLine("  GET    /api/products/:id      - Get product by ID");
        Console.WriteLine("  POST   /api/products          - Create product");
        Console.WriteLine("  PUT    /api/products/:id      - Update product");
        Console.WriteLine("  PATCH  /api/products/:id      - Partial update");
        Console.WriteLine("  DELETE /api/products/:id      - Delete product");
        Console.WriteLine("  GET    /api/products/search   - Search products");
        Console.WriteLine("\nQuery params: ?category=Electronics&minPrice=100&maxPrice=1000&sort=price&order=desc&page=1&limit=10\n");

        while (true)
        {
            var context = await _listener.GetContextAsync();
            _ = Task.Run(() => HandleRequest(context));
        }
    }

    private async Task HandleRequest(HttpListenerContext context)
    {
        var request = context.Request;
        var response = context.Response;
        
        // CORS
        response.Headers.Add("Access-Control-Allow-Origin", "*");
        response.Headers.Add("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, OPTIONS");
        response.Headers.Add("Access-Control-Allow-Headers", "Content-Type, Authorization");

        string method = request.HttpMethod;
        string path = request.Url.AbsolutePath;
        
        Console.WriteLine($"→ {method} {path}");

        try
        {
            if (method == "OPTIONS")
            {
                response.StatusCode = 204;
                response.Close();
                return;
            }

            // Маршрутизація
            if (path == "/api/products")
            {
                if (method == "GET")
                    await GetProducts(context);
                else if (method == "POST")
                    await CreateProduct(context);
                else
                    await MethodNotAllowed(context);
            }
            else if (path == "/api/products/search")
            {
                await SearchProducts(context);
            }
            else if (path.StartsWith("/api/products/"))
            {
                string idStr = path.Split('/').LastOrDefault();
                if (int.TryParse(idStr, out int id))
                {
                    if (method == "GET")
                        await GetProduct(context, id);
                    else if (method == "PUT")
                        await UpdateProduct(context, id);
                    else if (method == "PATCH")
                        await PatchProduct(context, id);
                    else if (method == "DELETE")
                        await DeleteProduct(context, id);
                    else
                        await MethodNotAllowed(context);
                }
                else
                {
                    await NotFound(context);
                }
            }
            else
            {
                await NotFound(context);
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"❌ Error: {ex.Message}");
            await InternalError(context, ex.Message);
        }
    }

    // GET /api/products
    private async Task GetProducts(HttpListenerContext context)
    {
        var query = context.Request.QueryString;
        var products = _products.AsEnumerable();

        // Фільтрація
        if (query["category"] != null)
            products = products.Where(p => p.Category == query["category"]);

        if (query["minPrice"] != null && decimal.TryParse(query["minPrice"], out decimal minPrice))
            products = products.Where(p => p.Price >= minPrice);

        if (query["maxPrice"] != null && decimal.TryParse(query["maxPrice"], out decimal maxPrice))
            products = products.Where(p => p.Price <= maxPrice);

        // Сортування
        string sort = query["sort"] ?? "id";
        string order = query["order"] ?? "asc";

        products = sort.ToLower() switch
        {
            "name" => order == "desc" ? products.OrderByDescending(p => p.Name) : products.OrderBy(p => p.Name),
            "price" => order == "desc" ? products.OrderByDescending(p => p.Price) : products.OrderBy(p => p.Price),
            "stock" => order == "desc" ? products.OrderByDescending(p => p.Stock) : products.OrderBy(p => p.Stock),
            _ => order == "desc" ? products.OrderByDescending(p => p.Id) : products.OrderBy(p => p.Id)
        };

        // Пагінація
        int page = int.TryParse(query["page"], out int p) ? p : 1;
        int limit = int.TryParse(query["limit"], out int l) ? Math.Min(l, 100) : 10;
        
        int total = products.Count();
        int totalPages = (int)Math.Ceiling(total / (double)limit);
        
        var paginatedProducts = products
            .Skip((page - 1) * limit)
            .Take(limit)
            .ToList();

        var response = new
        {
            products = paginatedProducts,
            pagination = new
            {
                page,
                limit,
                total,
                totalPages,
                hasNext = page < totalPages,
                hasPrev = page > 1
            }
        };

        await SendJson(context, response, 200);
    }

    // GET /api/products/:id
    private async Task GetProduct(HttpListenerContext context, int id)
    {
        var product = _products.FirstOrDefault(p => p.Id == id);
        
        if (product == null)
        {
            await NotFound(context, $"Product with ID {id} not found");
            return;
        }

        await SendJson(context, product, 200);
    }

    // POST /api/products
    private async Task CreateProduct(HttpListenerContext context)
    {
        string body = await ReadBody(context.Request);
        
        if (string.IsNullOrEmpty(body))
        {
            await BadRequest(context, "Request body is required");
            return;
        }

        try
        {
            var productData = JsonSerializer.Deserialize<Product>(body);
            
            // Валідація
            if (string.IsNullOrEmpty(productData.Name))
            {
                await BadRequest(context, "Name is required");
                return;
            }

            if (productData.Price <= 0)
            {
                await BadRequest(context, "Price must be greater than 0");
                return;
            }

            // Створення
            var product = new Product
            {
                Id = _nextId++,
                Name = productData.Name,
                Description = productData.Description,
                Price = productData.Price,
                Stock = productData.Stock,
                Category = productData.Category ?? "Uncategorized",
                CreatedAt = DateTime.UtcNow
            };

            _products.Add(product);

            context.Response.Headers.Add("Location", $"/api/products/{product.Id}");
            
            var response = new
            {
                message = "Product created successfully",
                product
            };

            await SendJson(context, response, 201);
        }
        catch (JsonException)
        {
            await BadRequest(context, "Invalid JSON");
        }
    }

    // PUT /api/products/:id
    private async Task UpdateProduct(HttpListenerContext context, int id)
    {
        var product = _products.FirstOrDefault(p => p.Id == id);
        
        if (product == null)
        {
            await NotFound(context, $"Product with ID {id} not found");
            return;
        }

        string body = await ReadBody(context.Request);
        
        try
        {
            var productData = JsonSerializer.Deserialize<Product>(body);
            
            // PUT - повна заміна
            product.Name = productData.Name ?? product.Name;
            product.Description = productData.Description;
            product.Price = productData.Price > 0 ? productData.Price : product.Price;
            product.Stock = productData.Stock;
            product.Category = productData.Category ?? product.Category;
            product.UpdatedAt = DateTime.UtcNow;

            var response = new
            {
                message = "Product updated successfully (PUT)",
                product
            };

            await SendJson(context, response, 200);
        }
        catch (JsonException)
        {
            await BadRequest(context, "Invalid JSON");
        }
    }

    // PATCH /api/products/:id
    private async Task PatchProduct(HttpListenerContext context, int id)
    {
        var product = _products.FirstOrDefault(p => p.Id == id);
        
        if (product == null)
        {
            await NotFound(context, $"Product with ID {id} not found");
            return;
        }

        string body = await ReadBody(context.Request);
        
        try
        {
            var updates = JsonSerializer.Deserialize<Dictionary<string, JsonElement>>(body);
            var updatedFields = new List<string>();

            // PATCH - тільки надані поля
            if (updates.ContainsKey("Name") && updates["Name"].ValueKind == JsonValueKind.String)
            {
                product.Name = updates["Name"].GetString();
                updatedFields.Add("Name");
            }

            if (updates.ContainsKey("Description"))
            {
                product.Description = updates["Description"].GetString();
                updatedFields.Add("Description");
            }

            if (updates.ContainsKey("Price") && updates["Price"].ValueKind == JsonValueKind.Number)
            {
                product.Price = updates["Price"].GetDecimal();
                updatedFields.Add("Price");
            }

            if (updates.ContainsKey("Stock") && updates["Stock"].ValueKind == JsonValueKind.Number)
            {
                product.Stock = updates["Stock"].GetInt32();
                updatedFields.Add("Stock");
            }

            if (updates.ContainsKey("Category"))
            {
                product.Category = updates["Category"].GetString();
                updatedFields.Add("Category");
            }

            product.UpdatedAt = DateTime.UtcNow;

            var response = new
            {
                message = "Product partially updated (PATCH)",
                product,
                updatedFields
            };

            await SendJson(context, response, 200);
        }
        catch (JsonException)
        {
            await BadRequest(context, "Invalid JSON");
        }
    }

    // DELETE /api/products/:id
    private async Task DeleteProduct(HttpListenerContext context, int id)
    {
        var product = _products.FirstOrDefault(p => p.Id == id);
        
        if (product == null)
        {
            await NotFound(context, $"Product with ID {id} not found");
            return;
        }

        _products.Remove(product);

        context.Response.StatusCode = 204;
        context.Response.Close();
        Console.WriteLine($"← 204 No Content (Product {id} deleted)\n");
    }

    // GET /api/products/search
    private async Task SearchProducts(HttpListenerContext context)
    {
        string q = context.Request.QueryString["q"];
        
        if (string.IsNullOrEmpty(q))
        {
            await BadRequest(context, "Query parameter 'q' is required");
            return;
        }

        var results = _products
            .Where(p => 
                p.Name.Contains(q, StringComparison.OrdinalIgnoreCase) ||
                (p.Description != null && p.Description.Contains(q, StringComparison.OrdinalIgnoreCase)) ||
                p.Category.Contains(q, StringComparison.OrdinalIgnoreCase))
            .ToList();

        var response = new
        {
            query = q,
            results,
            count = results.Count
        };

        await SendJson(context, response, 200);
    }

    // Допоміжні методи
    private async Task SendJson(HttpListenerContext context, object data, int statusCode)
    {
        string json = JsonSerializer.Serialize(data, new JsonSerializerOptions 
        { 
            WriteIndented = true,
            Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping
        });
        
        byte[] buffer = Encoding.UTF8.GetBytes(json);
        context.Response.ContentType = "application/json; charset=utf-8";
        context.Response.ContentLength64 = buffer.Length;
        context.Response.StatusCode = statusCode;
        await context.Response.OutputStream.WriteAsync(buffer, 0, buffer.Length);
        context.Response.Close();
        Console.WriteLine($"← {statusCode} ({buffer.Length} bytes)\n");
    }

    private async Task<string> ReadBody(HttpListenerRequest request)
    {
        if (!request.HasEntityBody) return null;
        
        using (var reader = new StreamReader(request.InputStream, request.ContentEncoding))
        {
            return await reader.ReadToEndAsync();
        }
    }

    private async Task BadRequest(HttpListenerContext context, string message)
    {
        await SendJson(context, new { error = "Bad Request", message }, 400);
    }

    private async Task NotFound(HttpListenerContext context, string message = "Resource not found")
    {
        await SendJson(context, new { error = "Not Found", message }, 404);
    }

    private async Task MethodNotAllowed(HttpListenerContext context)
    {
        await SendJson(context, new { error = "Method Not Allowed" }, 405);
    }

    private async Task InternalError(HttpListenerContext context, string message)
    {
        await SendJson(context, new { error = "Internal Server Error", message }, 500);
    }

    static async Task Main(string[] args)
    {
        var server = new RestApiServer("http://localhost:8080/");
        await server.Start();
    }
}
```

**Тестування REST API:**

```bash
# GET всі продукти
curl http://localhost:8080/api/products

# GET з фільтрами та пагінацією
curl "http://localhost:8080/api/products?category=Electronics&minPrice=100&maxPrice=5000&sort=price&order=asc&page=1&limit=5"

# GET один продукт
curl http://localhost:8080/api/products/1

# POST - створення
curl -X POST http://localhost:8080/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "Name": "Монітор",
    "Description": "4K монітор 27 дюймів",
    "Price": 8000,
    "Stock": 3,
    "Category": "Electronics"
  }'

# PUT - повне оновлення
curl -X PUT http://localhost:8080/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "Name": "Ноутбук Gaming Pro",
    "Description": "Updated description",
    "Price": 40000,
    "Stock": 8,
    "Category": "Electronics"
  }'

# PATCH - часткове оновлення
curl -X PATCH http://localhost:8080/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{"Price": 38000, "Stock": 10}'

# DELETE
curl -X DELETE http://localhost:8080/api/products/3

# Search
curl "http://localhost:8080/api/products/search?q=laptop"
```

---

## Підсумок

Цей посібник показав еволюцію від низькорівневого TCP до високорівневих HTTP бібліотек:

1. **TcpListener** - базовий TCP, повний контроль, складна реалізація
2. **Парсинг HTTP вручну** - розуміння структури HTTP
3. **HTTP сервер на TCP** - повна реалізація HTTP протоколу
4. **HttpListener** - нативна HTTP бібліотека, простота використання
5. **HttpClient** - клієнтська частина, зручний API

### Ключові концепції, які ми розглянули:

✅ HTTP методи (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS)  
✅ Статус коди (2xx, 3xx, 4xx, 5xx)  
✅ Заголовки (Request, Response, Custom)  
✅ Cookies (встановлення, читання, атрибути безпеки)  
✅ Кешування (ETag, Last-Modified, Cache-Control)  
✅ Compression (GZIP, Deflate)  
✅ Content Negotiation (JSON, XML, HTML, Plain Text)  
✅ Chunked Transfer Encoding (streaming)  
✅ HTTPS (SSL/TLS, security headers)  
✅ Rate Limiting  
✅ Повний REST API з фільтрацією, сортуванням, пагінацією

### Найкращі практики:

1. Використовуйте `HttpListener` або ASP.NET Core для production
2. Завжди встановлюйте правильні статус коди
3. Додавайте security headers для HTTPS
4. Реалізуйте rate limiting
5. Використовуйте compression для текстових даних
6. Правильно обробляйте помилки
7. Логуйте всі запити
8. Використовуйте async/await для асинхронності

🎓 **Тепер ви розумієте HTTP на глибокому рівні - від TCP до REST API!**

