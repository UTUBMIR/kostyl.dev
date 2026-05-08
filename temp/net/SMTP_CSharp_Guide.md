# ✉️ Робота з SMTP в C#: Повний посібник

## Зміст

1.  [Вступ: `SmtpClient` та `MailMessage`](#вступ-smtpclient-та-mailmessage)
2.  [Надсилання простого текстового листа](#надсилання-простого-текстового-листа)
3.  [Налаштування SMTP-сервера та автентифікація](#налаштування-smtp-сервера-та-автентифікація)
4.  [Робота з HTML-листами](#робота-з-html-листами)
5.  [Додавання вкладень (Attachments)](#додавання-вкладень-attachments)
6.  [Безпека: SSL/TLS](#безпека-ssltls)
7.  [Асинхронне надсилання листів](#асинхронне-надсилання-листів)
8.  [Найкращі практики та обробка помилок](#найкращі-практики-та-обробка-помилок)
9.  **[Важливе зауваження: `SmtpClient` є застарілим](#важливе-зауваження-smtpclient-є-застарілим)**
10. [Рекомендована альтернатива: MailKit](#рекомендована-альтернатива-mailkit)

---

## Вступ: `SmtpClient` та `MailMessage`

Для роботи з електронною поштою в .NET Framework (і ранніх версіях .NET Core) використовуються два основні класи з простору імен `System.Net.Mail`:

1.  **`MailMessage`**: Цей клас представляє саме email-повідомлення. Ви використовуєте його, щоб вказати:

    -   `From`: Відправника.
    -   `To`, `CC`, `BCC`: Одержувачів.
    -   `Subject`: Тему листа.
    -   `Body`: Тіло листа.
    -   `Attachments`: Прикріплені файли.

2.  **`SmtpClient`**: Цей клас відповідає за підключення до SMTP-сервера та відправку створеного `MailMessage`. Ви налаштовуєте в ньому:
    -   `Host`: Адресу SMTP-сервера.
    -   `Port`: Порт сервера.
    -   `Credentials`: Логін та пароль для автентифікації.
    -   `EnableSsl`: Використання шифрування.

**Важливо:** Починаючи з .NET Core 2.0, клас `SmtpClient` вважається **застарілим (obsolete)**. Microsoft рекомендує використовувати більш сучасні та потужні бібліотеки, як-от **MailKit**. Проте, `SmtpClient` все ще працює і може використовуватися в багатьох проектах. Ми розглянемо його, а в кінці посібника наведемо приклад з MailKit.

---

## Надсилання простого текстового листа

Це найпростіший сценарій: відправка звичайного текстового повідомлення.

```csharp
using System.Net;
using System.Net.Mail;

// Створення повідомлення
var fromAddress = new MailAddress("from@example.com", "Your Name");
var toAddress = new MailAddress("to@example.com", "Recipient Name");
const string fromPassword = "your_password"; // Ваш пароль
const string subject = "Тестовий лист";
const string body = "Привіт, це тестове повідомлення, відправлене з C#.";

// Створення SMTP клієнта
var smtp = new SmtpClient
{
    Host = "smtp.example.com", // Наприклад, smtp.gmail.com
    Port = 587,
    EnableSsl = true,
    DeliveryMethod = SmtpDeliveryMethod.Network,
    UseDefaultCredentials = false,
    Credentials = new NetworkCredential(fromAddress.Address, fromPassword)
};

// Створення та відправка повідомлення
using (var message = new MailMessage(fromAddress, toAddress)
{
    Subject = subject,
    Body = body
})
{
    try
    {
        smtp.Send(message);
        Console.WriteLine("Лист успішно відправлено!");
    }
    catch (Exception ex)
    {
        Console.WriteLine($"Помилка при відправці: {ex.Message}");
    }
}
```

### Пояснення коду:

1.  **`MailAddress`**: Створюємо об'єкти для відправника та одержувача. Другий параметр (ім'я) є необов'язковим.
2.  **`SmtpClient`**:
    -   `Host` та `Port`: Вказуємо дані SMTP-сервера.
    -   `EnableSsl = true`: Вмикаємо шифрування (обов'язково для більшості сучасних серверів).
    -   `Credentials`: Надаємо логін (адреса пошти) та пароль для автентифікації на сервері.
3.  **`MailMessage`**: Створюємо лист, передаючи відправника, одержувача, тему та тіло.
4.  **`smtp.Send(message)`**: Метод, який безпосередньо відправляє лист.
5.  **`using`**: `MailMessage` реалізує `IDisposable`, тому його варто обгортати в `using` для коректного звільнення ресурсів.

---

## Налаштування SMTP-сервера та автентифікація

Налаштування `SmtpClient` є ключовим етапом.

### Властивості `SmtpClient`

-   `Host` (string): DNS-ім'я або IP-адреса вашого SMTP-сервера.
-   `Port` (int): Порт для підключення.
    -   **587**: Стандартний порт для SMTP з шифруванням `STARTTLS` (рекомендовано).
    -   **465**: Застарілий порт для `SMTPS` (SSL/TLS встановлюється одразу).
    -   **25**: Стандартний порт для незашифрованого SMTP (рідко використовується для клієнтів, переважно для зв'язку між серверами).
-   `EnableSsl` (bool): Встановіть `true`, щоб увімкнути шифрування (STARTTLS або SMTPS, залежно від порту).
-   `Credentials` (ICredentialsByHost): Об'єкт, що містить дані для автентифікації. Зазвичай використовується `NetworkCredential`.
    ```csharp
    Credentials = new NetworkCredential("your_email@example.com", "your_password")
    ```
-   `UseDefaultCredentials` (bool): Якщо `true`, клієнт спробує використати системні кредансіали поточного користувача. Зазвичай встановлюється в `false`.
-   `Timeout` (int): Час очікування відповіді від сервера в мілісекундах (за замовчуванням 100 000 мс).

### Налаштування через `App.config` або `Web.config`

Ви можете винести налаштування SMTP в конфігураційний файл, щоб не "зашивати" їх у код.

```xml
<configuration>
  <system.net>
    <mailSettings>
      <smtp from="default_from@example.com">
        <network
          host="smtp.example.com"
          port="587"
          userName="your_email@example.com"
          password="your_password"
          enableSsl="true" />
      </smtp>
    </mailSettings>
  </system.net>
</configuration>
```

В такому випадку, ви можете створювати `SmtpClient` без параметрів — він автоматично підтягне їх з конфігурації.

````csharp
// Автоматично використає налаштування з App.config
var smtp = new SmtpClient();
smtp.Send(message);
## Робота з HTML-листами

Щоб надіслати лист з HTML-розміткою, потрібно встановити властивість `IsBodyHtml` об'єкта `MailMessage` в `true`.

```csharp
string htmlBody = @"
<html>
<body>
    <h1>Привіт, це HTML-лист!</h1>
    <p>Ви можете використовувати <strong>теги</strong>, <em>зображення</em> та посилання.</p>
    <a href='https://www.google.com'>Перейти на Google</a>
</body>
</html>";

using (var message = new MailMessage(fromAddress, toAddress)
{
    Subject = "HTML Лист",
    Body = htmlBody,
    IsBodyHtml = true // Вказуємо, що тіло листа - це HTML
})
{
    smtp.Send(message);
}
````

### Вбудовування зображень (Inline Attachments)

Якщо ви хочете, щоб зображення відображалися безпосередньо в тілі листа, а не як окремі вкладення, їх потрібно додати як `LinkedResource`.

```csharp
// Створення HTML з посиланням на вбудоване зображення
string htmlBody = @"
    <h1>Лист із зображенням</h1>
    <p>Ось наш логотип:</p>
    <img src='cid:companylogo' />";

// Створення альтернативного текстового вигляду для клієнтів, що не підтримують HTML
var plainView = AlternateView.CreateAlternateViewFromString("Це лист із зображенням.", null, "text/plain");

// Створення HTML-вигляду
var htmlView = AlternateView.CreateAlternateViewFromString(htmlBody, null, "text/html");

// Створення ресурсу зображення
var logoResource = new LinkedResource("path/to/your/logo.png", "image/png")
{
    ContentId = "companylogo" // Унікальний ID, який ми вказали в тезі <img>
};
htmlView.LinkedResources.Add(logoResource);

// Створення повідомлення з обома виглядами
using (var message = new MailMessage(fromAddress, toAddress))
{
    message.Subject = "Лист із вбудованим зображенням";
    message.AlternateViews.Add(plainView);
    message.AlternateViews.Add(htmlView);

    smtp.Send(message);
}
```

**`AlternateView`** дозволяє надати кілька версій тіла листа (наприклад, текстову та HTML). Поштовий клієнт сам вибере, яку з них показати.

---

## Додавання вкладень (Attachments)

Для додавання файлів до листа використовується колекція `Attachments` об'єкта `MailMessage`.

```csharp
using (var message = new MailMessage(fromAddress, toAddress)
{
    Subject = "Лист із вкладенням",
    Body = "Будь ласка, знайдіть у вкладенні звіт."
})
{
    // Створення вкладення з файлу на диску
    var attachment = new Attachment("path/to/your/report.pdf", "application/pdf");
    message.Attachments.Add(attachment);

    // Можна додати кілька файлів
    // var attachment2 = new Attachment("path/to/image.jpg");
    // message.Attachments.Add(attachment2);

    smtp.Send(message);

    // Важливо: звільніть ресурси після відправки
    attachment.Dispose();
}
```

**Примітка:** Об'єкт `Attachment` також реалізує `IDisposable`, тому його потрібно звільняти, щоб уникнути блокування файлів. Якщо `MailMessage` обгорнуто в `using`, це відбудеться автоматично.

---

## Безпека: SSL/TLS

Більшість сучасних SMTP-серверів вимагають шифрування. В `SmtpClient` це контролюється властивістю `EnableSsl`.

-   **`EnableSsl = true`**: Ця властивість вмикає шифрування. `SmtpClient` поводиться по-різному залежно від порту:
    -   **Порт 587**: Клієнт спочатку підключається по незашифрованому каналу, а потім надсилає команду `STARTTLS` для "підвищення" з'єднання до зашифрованого. **Це сучасний і рекомендований спосіб.**
    -   **Порт 465**: Клієнт одразу намагається встановити SSL/TLS з'єднання (неявний TLS). Цей спосіб вважається застарілим, але все ще підтримується.
-   **`EnableSsl = false` (Порт 25)**: З'єднання буде незашифрованим. **Небезпечно!** Використовуйте тільки для локального тестування або якщо сервер знаходиться в захищеній мережі.

```csharp
var smtp = new SmtpClient("smtp.gmail.com", 587)
{
    Credentials = new NetworkCredential("gmail_user@gmail.com", "gmail_password"),
    EnableSsl = true // Обов'язково для Gmail
};
```

## Асинхронне надсилання листів

Метод `Send()` є синхронним, тобто він блокує основний потік виконання, поки лист не буде надіслано. У веб-додатках або UI-додатках це може призвести до "зависань". Кращою практикою є використання асинхронного методу `SendMailAsync()`.

```csharp
public async Task SendEmailAsync(MailMessage message)
{
    using (var smtp = new SmtpClient("smtp.example.com", 587)
    {
        Credentials = new NetworkCredential("user@example.com", "password"),
        EnableSsl = true
    })
    {
        try
        {
            await smtp.SendMailAsync(message);
            Console.WriteLine("Лист успішно відправлено асинхронно!");
        }
        catch (SmtpException ex)
        {
            // Обробка специфічних для SMTP помилок
            Console.WriteLine($"Помилка SMTP: {ex.StatusCode}");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Загальна помилка: {ex.Message}");
        }
    }
}
```

**Примітка:** `SendMailAsync` був доданий в .NET Framework 4.5.

---

## Найкращі практики та обробка помилок

1.  **Не "зашивайте" кредансіали в код:** Використовуйте `App.config`, `secrets.json` (для ASP.NET Core) або інші механізми для зберігання логінів та паролів.
2.  **Використовуйте `using`:** Завжди звільняйте ресурси `SmtpClient`, `MailMessage` та `Attachment` за допомогою блоку `using`.
3.  **Обробляйте помилки:** Мережеві операції можуть завершитися невдало. Завжди обгортайте виклик `Send()` або `SendMailAsync()` в блок `try...catch`.
    -   `SmtpException`: Надає специфічну інформацію про помилку SMTP (`StatusCode`).
    -   `SmtpFailedRecipientException`: Виникає, якщо сервер відхилив одного з одержувачів.
4.  **Асинхронність:** Віддавайте перевагу `SendMailAsync`, щоб не блокувати потоки.
5.  **Перевірка адрес:** Перед відправкою перевіряйте адреси на коректність, щоб уникнути помилок.

---

## Важливе зауваження: `SmtpClient` є застарілим

**Microsoft не рекомендує використовувати `SmtpClient` в нових проектах.**

**Причини:**

-   Клас не підтримує багато сучасних розширень SMTP.
-   Його API є застарілим і менш гнучким.
-   Він не підтримує міжнародні поштові адреси (IDN).
-   Робота з ним може бути складною та непередбачуваною в деяких сценаріях.

---

## Рекомендована альтернатива: MailKit

**MailKit** — це потужна, кросплатформенна та активно підтримувана бібліотека для роботи з поштою в .NET. Вона підтримує SMTP, POP3 та IMAP.

**Встановлення:**

```bash
dotnet add package MailKit
```

**Приклад відправки листа з MailKit:**

```csharp
using MailKit.Net.Smtp;
using MailKit.Security;
using MimeKit;

public async Task SendEmailWithMailKitAsync()
{
    var message = new MimeMessage();
    message.From.Add(new MailboxAddress("Your Name", "from@example.com"));
    message.To.Add(new MailboxAddress("Recipient Name", "to@example.com"));
    message.Subject = "Лист, відправлений через MailKit";

    var bodyBuilder = new BodyBuilder();
    bodyBuilder.HtmlBody = "<h1>Привіт з MailKit!</h1>";
    bodyBuilder.TextBody = "Привіт з MailKit!";

    // Додавання вкладення
    bodyBuilder.Attachments.Add("path/to/your/file.pdf");

    message.Body = bodyBuilder.ToMessageBody();

    using (var client = new SmtpClient())
    {
        try
        {
            // Підключення до сервера з STARTTLS
            await client.ConnectAsync("smtp.example.com", 587, SecureSocketOptions.StartTls);

            // Автентифікація
            await client.AuthenticateAsync("from@example.com", "your_password");

            // Відправка
            await client.SendAsync(message);

            // Відключення
            await client.DisconnectAsync(true);

            Console.WriteLine("Лист успішно відправлено через MailKit!");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Помилка MailKit: {ex.Message}");
        }
    }
}
```

**Переваги MailKit:**

-   Повна підтримка SMTP, POP3, IMAP.
-   Надійне асинхронне API.
-   Підтримка всіх сучасних механізмів автентифікації та шифрування.
-   Активна розробка та підтримка спільнотою.

---
