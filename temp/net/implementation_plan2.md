# Мережеве Програмування — План Навчального Курсу

## Мета

Створити академічно структурований, книжковий курс **«Мережеве програмування»** на платформі `kostyl.dev`. Курс побудований за еволюційним принципом: від фізичних основ мережі до високорівневих протоколів прикладного рівня, з усіма прикладами на **C# .NET**.

## Огляд Джерел

Контент базується на 15 файлах у `temp/net/`:

| Файл | Обсяг | Покриття |
|------|-------|----------|
| `Вступ-до-мережі,-сокети-Урок-1.md` | 38 KB | Історія мереж, OSI, сокети |
| `IP_Protocol_Guide.md` | 67 KB | IPv4/IPv6, адресація, CIDR |
| `TCP_Protocol_Guide.md` | 62 KB | TCP надійність, flow control |
| `UDP_Protocol_Guide.md` | 56 KB | UDP, датаграми, real-time |
| `HTTP_Protocol_Guide.md` | 100 KB | HTTP 0.9–3, методи, статуси |
| `HTTP_CSharp_Examples.md` | 136 KB | TcpListener, HttpListener |
| `HttpListener_HttpClient_Documentation.md` | 86 KB | API документація |
| `TLS_SSL_Protocol_Guide.md` | 142 KB | Криптографія, TLS handshake |
| `Self_Signed_Certificate_Guide.md` | 18 KB | OpenSSL, сертифікати |
| `WebSocket_Protocol_Guide.md` | 30 KB | Фрейми, handshake, C# |
| `Email_Protocols_Guide.md` | 26 KB | SMTP, POP3, IMAP |
| `SMTP_CSharp_Guide.md` | 19 KB | SmtpClient, MailKit |
| `FTP_Protocol_Guide.md` | 23 KB | FTP, FTPS, SFTP |
| `SSH_Protocol_Guide.md` | 133 KB | SSH архітектура, тунелі |
| `HLS_Protocol_Guide.md` | 112 KB | Стрімінг, ABR, сегментація |

---

## Структура Курсу

Курс розміщується у `content/01.csharp/13.network-programming/` і складається з 15 модулів.

### Файлова структура

```
content/01.csharp/13.network-programming/
├── .navigation.yml          # title: Network Programming, icon: i-lucide-network
├── 01.foundations.md         # Модуль 1: Основи комп'ютерних мереж
├── 02.osi-model.md           # Модуль 2: Модель OSI та TCP/IP
├── 03.ip-addressing.md       # Модуль 3: IP-протокол та адресація
├── 04.tcp-protocol.md        # Модуль 4: TCP — надійна передача
├── 05.udp-protocol.md        # Модуль 5: UDP — швидка передача
├── 06.sockets-fundamentals.md # Модуль 6: Сокети в .NET
├── 07.dns-resolution.md      # Модуль 7: DNS — система доменних імен
├── 08.http-protocol.md       # Модуль 8: HTTP-протокол
├── 09.http-csharp.md         # Модуль 9: HTTP-сервер та клієнт у C#
├── 10.tls-security.md        # Модуль 10: TLS/SSL та криптографія
├── 11.websocket.md           # Модуль 11: WebSocket — real-time
├── 12.email-protocols.md     # Модуль 12: Email — SMTP, POP3, IMAP
├── 13.ftp-ssh.md             # Модуль 13: FTP та SSH
├── 14.streaming-hls.md       # Модуль 14: Потокове відео (HLS)
└── 15.project.md             # Модуль 15: Фінальний проєкт
```

---

## Proposed Changes

### Навігація

#### [NEW] `.navigation.yml`
```yaml
title: Network Programming
icon: i-lucide-network
```

---

### Модуль 1 — Основи комп'ютерних мереж

#### [NEW] [01.foundations.md](file:///Users/arakviel/Work/kostyl.dev/content/01.csharp/13.network-programming/01.foundations.md)

**Джерела:** `Вступ-до-мережі,-сокети-Урок-1.md` (розділи 1–3)

**Зміст:**
1. **Вступ** — Що таке мережа? Навіщо комп'ютерам спілкуватися? Еволюція від ARPANET до сучасного Інтернету
2. **Типи мереж** — LAN, WAN, MAN, PAN. Топології (зірка, кільце, шина, mesh)
3. **Мережеве обладнання** — Хаб, свіч, маршрутизатор, точка доступу. Що робить кожен пристрій і чому
4. **Адресація** — MAC-адреси vs IP-адреси. Фізична vs логічна адресація
5. **Пакетна комутація** — Чому дані розбиваються на пакети? Circuit switching vs packet switching
6. **Клієнт-серверна архітектура** — Концепція, запит-відповідь, порти

**Docus-компоненти:**
- `::mermaid` — топології мереж, схема пакетної комутації
- `::steps` — еволюція мереж (ARPANET → Інтернет)
- `::card-group` — типи мережевого обладнання
- `::tip` / `::note` — аналогії з реальним світом (пошта, телефон)

---

### Модуль 2 — Модель OSI та стек TCP/IP

#### [NEW] [02.osi-model.md](file:///Users/arakviel/Work/kostyl.dev/content/01.csharp/13.network-programming/02.osi-model.md)

**Джерела:** `Вступ-до-мережі,-сокети-Урок-1.md` (OSI model), `IP_Protocol_Guide.md` (вступ)

**Зміст:**
1. **Навіщо потрібна модель?** — Проблема стандартизації, аналогія з поштовою службою
2. **7 рівнів OSI** — Детальний розбір кожного рівня з прикладами
3. **Стек TCP/IP** — 4 рівні, порівняння з OSI
4. **Інкапсуляція даних** — Як дані "обгортаються" заголовками на кожному рівні
5. **PDU на кожному рівні** — Біти → Фрейми → Пакети → Сегменти → Дані
6. **Практичне значення** — Чому розробнику важливо розуміти рівні

**Docus-компоненти:**
- `::mermaid` — діаграма OSI з PDU на кожному рівні
- `::tabs` — OSI vs TCP/IP порівняння
- `::accordion` — детальний опис кожного рівня
- Таблиця порівняння моделей

---

### Модуль 3 — IP-протокол та адресація

#### [NEW] [03.ip-addressing.md](file:///Users/arakviel/Work/kostyl.dev/content/01.csharp/13.network-programming/03.ip-addressing.md)

**Джерела:** `IP_Protocol_Guide.md`

**Зміст:**
1. **Мережевий рівень** — Роль IP у стеку, маршрутизація
2. **IPv4** — Формат адреси, класи (A, B, C, D, E), приватні діапазони
3. **Маски підмережі та CIDR** — Навіщо потрібні маски, нотація /24
4. **Структура IP-пакета** — Заголовок IPv4 (TTL, Protocol, Checksum)
5. **IPv6** — Навіщо потрібен, формат, порівняння з IPv4
6. **NAT** — Трансляція адрес, як працює домашній роутер
7. **C# практика** — `IPAddress`, `IPEndPoint`, `Dns.GetHostAddresses()`

**Docus-компоненти:**
- `::mermaid` — структура IP-пакета, схема NAT
- `::code-group` — IPv4 vs IPv6 приклади в C#
- Таблиці класів адрес, приватних діапазонів
- `::warning` — вичерпання IPv4

---

### Модуль 4 — TCP: Надійна передача даних

#### [NEW] [04.tcp-protocol.md](file:///Users/arakviel/Work/kostyl.dev/content/01.csharp/13.network-programming/04.tcp-protocol.md)

**Джерела:** `TCP_Protocol_Guide.md`

**Зміст:**
1. **Проблема надійності** — Чому пакети губляться? Аналогія з рекомендованим листом
2. **TCP як рішення** — З'єднання, потоки, гарантії
3. **Трьохстороннє рукостискання** — SYN, SYN-ACK, ACK покроково
4. **Структура TCP-сегмента** — Порти, Sequence/Acknowledgment Numbers, Flags
5. **Механізми надійності** — Retransmission, Sliding Window, Flow Control
6. **Congestion Control** — Slow Start, Congestion Avoidance
7. **Завершення з'єднання** — FIN, чотиристороннє рукостискання
8. **Стани TCP** — LISTEN, ESTABLISHED, TIME_WAIT тощо

**Docus-компоненти:**
- `::mermaid` — sequence diagram рукостискання, діаграма станів TCP
- `::steps` — покрокове встановлення з'єднання
- `::accordion` — поля TCP-заголовка
- `::warning` — типові проблеми (TIME_WAIT accumulation)

---

### Модуль 5 — UDP: Швидка передача даних

#### [NEW] [05.udp-protocol.md](file:///Users/arakviel/Work/kostyl.dev/content/01.csharp/13.network-programming/05.udp-protocol.md)

**Джерела:** `UDP_Protocol_Guide.md`

**Зміст:**
1. **Навіщо ще один протокол?** — Проблеми TCP для real-time додатків
2. **UDP як рішення** — Connectionless, datagram-based
3. **Структура UDP-датаграми** — Простота заголовка (8 байт)
4. **Порівняння TCP vs UDP** — Таблиця, сценарії використання
5. **Multicast та Broadcast** — Групова та широкомовна розсилка
6. **Протоколи поверх UDP** — DNS, DHCP, RTP, QUIC
7. **C# практика** — `UdpClient`, відправка/отримання датаграм

**Docus-компоненти:**
- Порівняльна таблиця TCP vs UDP
- `::mermaid` — unicast vs multicast vs broadcast
- `::code-group` — UDP sender vs receiver
- `::tip` — коли обирати UDP

---

### Модуль 6 — Сокети в .NET

#### [NEW] [06.sockets-fundamentals.md](file:///Users/arakviel/Work/kostyl.dev/content/01.csharp/13.network-programming/06.sockets-fundamentals.md)

**Джерела:** `Вступ-до-мережі,-сокети-Урок-1.md` (C# частина), `TCP_Protocol_Guide.md`, `UDP_Protocol_Guide.md`

**Зміст:**
1. **Що таке сокет?** — Абстракція ОС, endpoint комунікації, аналогія з телефонною розеткою
2. **Berkeley Sockets API** — Історія, стандарт, основні операції
3. **Класи .NET** — `Socket`, `TcpListener`, `TcpClient`, `UdpClient`, `NetworkStream`
4. **TCP Echo Server** — Покрокова побудова синхронного сервера
5. **Асинхронні сокети** — `async/await`, `AcceptTcpClientAsync`, `ReadAsync`
6. **Багатоклієнтний сервер** — Обробка декількох клієнтів одночасно
7. **UDP чат** — Простий чат на основі UDP
8. **Серіалізація даних** — Як передавати структуровані дані (`BinaryReader`/`Writer`, JSON)

**Docus-компоненти:**
- `::steps` — побудова TCP-сервера крок за кроком
- `::code-group` — синхронний vs асинхронний варіант
- `::terminal-preview` — демонстрація роботи сервера/клієнта
- `::mermaid` — sequence diagram клієнт-серверної взаємодії

---

### Модуль 7 — DNS: Система доменних імен

#### [NEW] [07.dns-resolution.md](file:///Users/arakviel/Work/kostyl.dev/content/01.csharp/13.network-programming/07.dns-resolution.md)

**Джерела:** Доповнення (немає окремого файлу в `temp/net/`). Потрібен як місток між IP та HTTP.

**Зміст:**
1. **Проблема** — Люди не запам'ятовують IP-адреси
2. **Ієрархія DNS** — Root → TLD → Authoritative
3. **Типи записів** — A, AAAA, CNAME, MX, NS, TXT
4. **Процес резолюції** — Рекурсивний vs ітеративний запит
5. **Кешування** — TTL, браузерний кеш, OS кеш
6. **C# практика** — `Dns.GetHostEntry()`, `Dns.GetHostAddresses()`
7. **Безпека** — DNS spoofing, DNSSEC

**Docus-компоненти:**
- `::mermaid` — ієрархія DNS, sequence diagram резолюції
- `::steps` — покрокова резолюція домену
- `::terminal-preview` — nslookup/dig приклади
- Таблиця типів DNS-записів

---

### Модуль 8 — HTTP-протокол

#### [NEW] [08.http-protocol.md](file:///Users/arakviel/Work/kostyl.dev/content/01.csharp/13.network-programming/08.http-protocol.md)

**Джерела:** `HTTP_Protocol_Guide.md`

**Зміст:**
1. **Еволюція HTTP** — 0.9 → 1.0 → 1.1 → 2 → 3
2. **Архітектура запит-відповідь** — Структура HTTP-запиту та відповіді
3. **Методи HTTP** — GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
4. **Статус-коди** — 1xx–5xx, найважливіші коди
5. **Заголовки** — Content-Type, Authorization, Cache-Control, Cookie
6. **Тіло запиту** — JSON, form-data, multipart
7. **Cookies та сесії** — Механізм збереження стану
8. **HTTP/2** — Мультиплексування, Server Push, HPACK
9. **HTTP/3 та QUIC** — UDP-based, переваги

**Docus-компоненти:**
- `::steps` — еволюція HTTP
- `::tabs` — HTTP/1.1 vs HTTP/2 vs HTTP/3
- `::accordion` — групи статус-кодів
- `::mermaid` — request-response flow
- `::terminal-preview` — raw HTTP запити через telnet/curl

---

### Модуль 9 — HTTP-сервер та клієнт у C#

#### [NEW] [09.http-csharp.md](file:///Users/arakviel/Work/kostyl.dev/content/01.csharp/13.network-programming/09.http-csharp.md)

**Джерела:** `HTTP_CSharp_Examples.md`, `HttpListener_HttpClient_Documentation.md`

**Зміст:**
1. **HTTP-сервер на сокетах** — Парсинг raw HTTP, формування відповідей
2. **HttpListener** — Побудова HTTP-сервера, маршрутизація, JSON API
3. **HttpClient** — Відправка запитів, конфігурація, best practices
4. **REST API клієнт** — GET/POST/PUT/DELETE з серіалізацією
5. **HttpClientFactory** — IHttpClientFactory, Named/Typed клієнти
6. **Middleware вручну** — Побудова pipeline обробки запитів

**Docus-компоненти:**
- `::steps` — від raw socket до HttpListener
- `::code-group` — Socket HTTP vs HttpListener vs HttpClient
- `::terminal-preview` — curl запити до нашого сервера
- `::mermaid` — pipeline обробки запитів

---

### Модуль 10 — TLS/SSL та мережева безпека

#### [NEW] [10.tls-security.md](file:///Users/arakviel/Work/kostyl.dev/content/01.csharp/13.network-programming/10.tls-security.md)

**Джерела:** `TLS_SSL_Protocol_Guide.md`, `Self_Signed_Certificate_Guide.md`

**Зміст:**
1. **Навіщо шифрування?** — Атаки (MITM, eavesdropping), реальні приклади
2. **Основи криптографії** — Симетричне vs асиметричне шифрування, хеш-функції
3. **Сертифікати та PKI** — X.509, CA, ланцюжок довіри
4. **TLS Handshake** — Покрокова діаграма TLS 1.2 та TLS 1.3
5. **Cipher Suites** — Вибір алгоритмів
6. **C# практика** — `SslStream`, `X509Certificate2`, самопідписаний сертифікат
7. **HTTPS сервер** — Налаштування TLS для HttpListener/Kestrel

**Docus-компоненти:**
- `::mermaid` — TLS handshake sequence diagram
- `::steps` — створення самопідписаного сертифіката
- `::tabs` — TLS 1.2 vs TLS 1.3
- `::warning` — застарілі версії SSL, відомі атаки
- Таблиця cipher suites

---

### Модуль 11 — WebSocket: комунікація в реальному часі

#### [NEW] [11.websocket.md](file:///Users/arakviel/Work/kostyl.dev/content/01.csharp/13.network-programming/11.websocket.md)

**Джерела:** `WebSocket_Protocol_Guide.md`

**Зміст:**
1. **Обмеження HTTP** — Polling, Long Polling та їх недоліки
2. **WebSocket як рішення** — Full-duplex, persistent connection
3. **Handshake** — Upgrade з HTTP, Sec-WebSocket-Key
4. **Фрейми** — Бінарна структура: FIN, Opcode, Mask, Payload
5. **Життєвий цикл** — Ping/Pong, закриття з'єднання
6. **C# сервер** — ASP.NET Core WebSocket middleware
7. **C# клієнт** — `ClientWebSocket`
8. **Практика** — Простий чат-сервер

**Docus-компоненти:**
- `::mermaid` — HTTP vs WebSocket порівняння, handshake sequence
- `::code-group` — сервер vs клієнт
- `::accordion` — opcodes, close status codes
- `::tip` — best practices (WSS, reconnection)

---

### Модуль 12 — Протоколи електронної пошти

#### [NEW] [12.email-protocols.md](file:///Users/arakviel/Work/kostyl.dev/content/01.csharp/13.network-programming/12.email-protocols.md)

**Джерела:** `Email_Protocols_Guide.md`, `SMTP_CSharp_Guide.md`

**Зміст:**
1. **Архітектура email** — MUA, MTA, MX-записи
2. **SMTP** — Команди, коди відповідей, сесія покроково
3. **POP3 vs IMAP** — Порівняння підходів до отримання пошти
4. **STARTTLS** — Безпека поштових протоколів
5. **C# практика** — `SmtpClient` (legacy), MailKit (сучасний)
6. **HTML-листи та вкладення** — `MailMessage`, `MimeMessage`

**Docus-компоненти:**
- `::mermaid` — flow відправки email (MUA → MTA → MTA → MUA)
- Порівняльна таблиця POP3 vs IMAP
- `::code-group` — SmtpClient vs MailKit
- `::terminal-preview` — SMTP-сесія (telnet)

---

### Модуль 13 — FTP та SSH

#### [NEW] [13.ftp-ssh.md](file:///Users/arakviel/Work/kostyl.dev/content/01.csharp/13.network-programming/13.ftp-ssh.md)

**Джерела:** `FTP_Protocol_Guide.md`, `SSH_Protocol_Guide.md`

**Зміст:**
1. **FTP** — Два з'єднання, активний vs пасивний режим, команди
2. **Безпека FTP** — FTPS vs SFTP порівняння
3. **SSH** — Архітектура (3 підпротоколи), Key Exchange
4. **SSH аутентифікація** — Пароль vs ключі, Ed25519
5. **Тунелювання** — Local/Remote/Dynamic port forwarding
6. **C# практика** — `FtpWebRequest` (legacy), SSH.NET бібліотека

**Docus-компоненти:**
- `::mermaid` — FTP active vs passive mode, SSH architecture layers
- `::tabs` — FTP vs FTPS vs SFTP
- `::steps` — генерація SSH ключів
- Порівняльна таблиця протоколів

---

### Модуль 14 — Потокове відео (HLS)

#### [NEW] [14.streaming-hls.md](file:///Users/arakviel/Work/kostyl.dev/content/01.csharp/13.network-programming/14.streaming-hls.md)

**Джерела:** `HLS_Protocol_Guide.md`

**Зміст:**
1. **Теорія стрімінгу** — Progressive download vs streaming, сегментація
2. **Adaptive Bitrate** — Автоматична адаптація якості
3. **Архітектура HLS** — Encoder → Origin → CDN → Player
4. **M3U8 плейлісти** — Master vs Media playlist, теги
5. **Формати сегментів** — .ts vs fMP4
6. **Live vs VOD** — Відмінності в плейлістах
7. **Low-Latency HLS** — Partial segments, HTTP/2 Push
8. **C# практика** — Простий HLS-сервер, ABR-алгоритм

**Docus-компоненти:**
- `::mermaid` — архітектура HLS pipeline, ABR decision flow
- `::code-group` — master.m3u8 vs media.m3u8
- `::steps` — як браузер відтворює HLS-відео
- Порівняльна таблиця HLS vs DASH vs RTMP

---

### Модуль 15 — Фінальний проєкт

#### [NEW] [15.project.md](file:///Users/arakviel/Work/kostyl.dev/content/01.csharp/13.network-programming/15.project.md)

**Зміст:**
1. **Проєкт «Мережевий чат»** — TCP-сервер + WebSocket клієнт
2. **Архітектура** — Multi-client, JSON-протокол, кімнати
3. **Безпека** — TLS, аутентифікація
4. **Додаткові завдання** — File transfer, history, notifications

---

## User Review Required

> [!IMPORTANT]
> **Розміщення курсу**: Курс планується у `content/01.csharp/13.network-programming/`. Це вірна позиція? Чи потрібна окрема top-level директорія (наприклад, `content/13.network-programming/`)?

> [!IMPORTANT]
> **Модуль 7 (DNS)**: У `temp/net/` немає окремого файлу про DNS. Я пропоную дописати цей модуль самостійно як необхідний «місток» між IP та HTTP. Чи погоджуєтесь?

> [!IMPORTANT]
> **Модуль 15 (Проєкт)**: Чи потрібен фінальний інтеграційний проєкт, чи достатньо практичних завдань у кожному модулі?

## Open Questions

> [!IMPORTANT]
> **Обсяг модулів**: Деякі джерела дуже об'ємні (TLS — 142 KB, SSH — 133 KB, HLS — 112 KB). Чи варто розбити їх на 2 модулі (теорія + C# практика), чи зберігати все в одному?

> [!IMPORTANT]
> **Порядок FTP/SSH та Email**: Чи влаштовує поточний порядок (спочатку WebSocket, потім Email, потім FTP/SSH, потім HLS), чи є переваги іншого порядку?

## Verification Plan

### Automated Tests
- Перевірка рендерингу кожного `.md` файлу через `pnpm dev`
- Валідація frontmatter (title, description)
- Перевірка Mermaid-діаграм на синтаксичні помилки
- Перевірка всіх внутрішніх посилань

### Manual Verification
- Візуальна перевірка кожного модуля в браузері
- Перевірка компонентів (`::mermaid`, `::steps`, `::tabs`, `::code-group`)
- Компіляція та тестування всіх C# прикладів
- Перевірка `::terminal-preview` демонстрацій
