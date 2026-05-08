# 📘 Повний посібник з протоколу UDP

## Зміст

1. [Вступ до UDP](#вступ-до-udp)
2. [Історія UDP](#історія-udp)
3. [Як працює UDP: основи](#як-працює-udp-основи)
4. [Структура UDP пакету](#структура-udp-пакету)
5. [UDP vs TCP: ключові відмінності](#udp-vs-tcp-ключові-відмінності)
6. [Переваги UDP](#переваги-udp)
7. [Недоліки UDP](#недоліки-udp)
8. [Випадки використання UDP](#випадки-використання-udp)
9. [UDP сокети](#udp-сокети)
10. [Робота з UDP в C#](#робота-з-udp-в-c)
11. [Broadcasting та Multicasting](#broadcasting-та-multicasting)
12. [Найкращі практики](#найкращі-практики)
13. [Поширені проблеми та їх рішення](#поширені-проблеми-та-їх-рішення)

---

## Вступ до UDP

### Що таке UDP?

**UDP** (User Datagram Protocol) — це **протокол транспортного рівня**, який забезпечує швидку передачу даних без встановлення з'єднання та без гарантії доставки.

**Простими словами:** UDP — це як відправити листівку поштою: ти кидаєш її в поштову скриньку і сподіваєшся, що вона дійде, але ніхто не гарантує доставку і не підтверджує отримання. Зате це швидко і просто!

### Ключові характеристики UDP:

1. **Протокол транспортного рівня** — працює на 4-му рівні моделі OSI
2. **Connectionless (без встановлення з'єднання)** — дані відправляються без попереднього "рукостискання"
3. **Unreliable (ненадійний)** — немає гарантії доставки пакетів
4. **Без підтвердження доставки** — відправник не знає, чи дійшов пакет
5. **Без контролю послідовності** — пакети можуть прийти в іншому порядку
6. **Легкий і швидкий** — мінімальні накладні витрати
7. **Без контролю потоку** — відправник не адаптується до швидкості отримувача

### Приклад простого UDP обміну:

```
Клієнт                          Сервер
  |                                |
  |--------- Дані (пакет 1) ----->|
  |                                |
  |--------- Дані (пакет 2) ----->|
  |                                |
  |<-------- Дані (відповідь) -----|
  |                                |
```

**Що тут відбувається?**

- Клієнт просто відправляє пакети
- Немає встановлення з'єднання (як TCP handshake)
- Немає підтвердження отримання
- Швидко і просто!

---

## Історія UDP

### Витоки (1980)

**UDP** був визначений в **RFC 768** Джоном Постелом (Jon Postel) у **серпні 1980 року**.

**Чому створили UDP?**

До UDP існував тільки TCP, який був надійним, але:
- ❌ Повільніше через встановлення з'єднання
- ❌ Надмірні накладні витрати для простих запитів
- ❌ Не підходив для real-time додатків

**Рішення:** Створити простий, швидкий протокол без гарантій доставки.

### Еволюція використання:

**1980-ті:** DNS (Domain Name System) став першим масовим застосуванням UDP

**1990-ті:** Розвиток мультимедійних додатків (відео, аудіо стримінг)

**2000-ті:** Онлайн ігри масово переходять на UDP

**2010-ті:** VoIP (Skype, WhatsApp calls) використовують UDP

**2020+:** QUIC протокол (HTTP/3) будується поверх UDP

---

## Як працює UDP: основи

### Модель передачі даних

UDP працює за моделлю "fire and forget" (відправив і забув):

```
┌──────────┐                  ┌──────────┐
│ Відправник│ ────пакет 1─────>│ Отримувач│
│          │                  │          │
│          │ ────пакет 2─────>│          │
│          │                  │          │
│          │ ────пакет 3─────>│          │
└──────────┘                  └──────────┘

Немає підтвердження! Немає повторної відправки!
```

### Етапи UDP комунікації:

#### 1. **Створення UDP сокету**

```
Додаток створює UDP сокет (socket)
```

#### 2. **Відправка даних**

```
Дані → UDP заголовок → IP заголовок → Відправка в мережу
```

#### 3. **Отримання даних**

```
Мережа → IP заголовок → UDP заголовок → Дані → Додаток
```

#### 4. **Закриття сокету**

```
Закрити сокет (якщо більше не потрібен)
```

### Connectionless природа UDP

**Що означає Connectionless?**

UDP не встановлює з'єднання перед відправкою даних. Кожен пакет (datagram) — це незалежна одиниця.

**Порівняння з TCP:**

**TCP (Connection-oriented):**
```
1. SYN →
2. ← SYN-ACK
3. ACK →
4. [Дані передаються]
5. FIN →
6. ← ACK
7. ← FIN
8. ACK →
```

**UDP (Connectionless):**
```
1. [Дані відправляються негайно]
```

**Переваги:**
- ⚡ Швидший старт
- 📉 Менше накладних витрат
- 💪 Підходить для коротких повідомлень

**Недоліки:**
- ❌ Немає гарантій
- ❌ Втрачені пакети не відновлюються
- ❌ Може прийти в неправильному порядку

---

## Структура UDP пакету

### Анатомія UDP датаграми

UDP пакет (датаграма) має **дуже просту структуру** — всього **8 байтів заголовка**!

```
 0                   16                  31
┌────────────────────┬────────────────────┐
│   Source Port      │  Destination Port  │ (4 байти)
├────────────────────┼────────────────────┤
│      Length        │     Checksum       │ (4 байти)
├────────────────────┴────────────────────┤
│                                         │
│             Data (Payload)              │
│                                         │
└─────────────────────────────────────────┘
```

### Поля UDP заголовка:

#### 1. Source Port (Порт відправника) — 16 біт (2 байти)

**Призначення:** Номер порту програми-відправника.

**Діапазон:** 0-65535

**Приклад:**
```
Source Port: 54321
```

**Особливості:**
- Опціональне поле (може бути 0, якщо відповідь не потрібна)
- Використовується для отримання відповіді

#### 2. Destination Port (Порт отримувача) — 16 біт (2 байти)

**Призначення:** Номер порту програми-отримувача.

**Діапазон:** 0-65535

**Приклад:**
```
Destination Port: 53 (DNS)
```

**Популярні UDP порти:**
```
53    → DNS (Domain Name System)
67/68 → DHCP (Dynamic Host Configuration Protocol)
69    → TFTP (Trivial File Transfer Protocol)
123   → NTP (Network Time Protocol)
161   → SNMP (Simple Network Management Protocol)
514   → Syslog
5060  → SIP (Session Initiation Protocol)
```

#### 3. Length (Довжина) — 16 біт (2 байти)

**Призначення:** Загальна довжина UDP датаграми (заголовок + дані) в байтах.

**Мінімальне значення:** 8 байтів (тільки заголовок, без даних)

**Максимальне значення:** 65535 байтів

**Приклад:**
```
Length: 520 (8 байт заголовок + 512 байт даних)
```

**Формула:**
```
Length = 8 (заголовок) + розмір даних
```

#### 4. Checksum (Контрольна сума) — 16 біт (2 байти)

**Призначення:** Перевірка цілісності даних (виявлення помилок).

**Особливості:**
- Опціональна в IPv4 (може бути 0)
- **Обов'язкова** в IPv6
- Перевіряє заголовок + дані + псевдо-заголовок IP

**Приклад:**
```
Checksum: 0x3A4F
```

**Що таке псевдо-заголовок?**

Для обчислення checksum використовуються деякі поля IP заголовка:

```
IPv4 псевдо-заголовок:
┌────────────────────────────────┐
│  Source IP Address (32 біти)   │
├────────────────────────────────┤
│  Destination IP (32 біти)      │
├─────────────┬──────────────────┤
│   Zero (8)  │  Protocol (8)    │
├─────────────┴──────────────────┤
│     UDP Length (16 біт)        │
└────────────────────────────────┘
```

### Повний приклад UDP пакету:

**Сценарій:** DNS запит до 8.8.8.8

```
UDP Заголовок (8 байт):
┌─────────────────────────────────────┐
│ Source Port: 54321 (0xD431)         │ 2 байти
├─────────────────────────────────────┤
│ Destination Port: 53 (0x0035)       │ 2 байти
├─────────────────────────────────────┤
│ Length: 40 (0x0028)                 │ 2 байти
├─────────────────────────────────────┤
│ Checksum: 0x3A4F                    │ 2 байти
└─────────────────────────────────────┘

Data (32 байти):
[DNS запит для example.com]
```

**В hex форматі:**
```
D4 31 00 35 00 28 3A 4F [DNS дані...]
│  │  │  │  │  │  │  │
│  │  │  │  │  │  │  └─ Checksum (частина 2)
│  │  │  │  │  │  └──── Checksum (частина 1)
│  │  │  │  │  └─────── Length (частина 2)
│  │  │  │  └────────── Length (частина 1)
│  │  │  └───────────── Dest Port (частина 2)
│  │  └──────────────── Dest Port (частина 1)
│  └─────────────────── Source Port (частина 2)
└────────────────────── Source Port (частина 1)
```

### Порівняння розмірів заголовків:

```
UDP заголовок:     8 байт  (фіксований)
TCP заголовок:    20-60 байт (мінімум 20)
IP заголовок:     20-60 байт (мінімум 20)
```

**Висновок:** UDP має мінімальні накладні витрати!

---

## UDP vs TCP: ключові відмінності

### Візуальне порівняння:

```
TCP (Telephone Call)          UDP (Postcard)
┌──────────────────┐          ┌──────────────┐
│  Дзвонить        │          │  Пише        │
│      ↓           │          │      ↓       │
│  Підняли трубку? │          │  Відправляє  │
│      ↓           │          │      ↓       │
│  Розмова         │          │  Надія що    │
│      ↓           │          │  дійде       │
│  Кладе трубку    │          └──────────────┘
└──────────────────┘
```

### Детальна порівняльна таблиця:

| Характеристика | TCP | UDP |
|----------------|-----|-----|
| **З'єднання** | Connection-oriented (потрібен handshake) | Connectionless (без встановлення з'єднання) |
| **Надійність** | Надійний (guaranteed delivery) | Ненадійний (no guarantees) |
| **Порядок доставки** | Гарантується правильна послідовність | Пакети можуть прийти в будь-якому порядку |
| **Підтвердження** | ACK для кожного пакету | Немає підтверджень |
| **Повторна відправка** | Автоматична при втраті | Немає автоматичної повторної відправки |
| **Контроль потоку** | Так (Flow Control) | Ні |
| **Контроль перевантаження** | Так (Congestion Control) | Ні |
| **Швидкість** | Повільніше (через накладні витрати) | Швидше (мінімальні накладні витрати) |
| **Розмір заголовка** | 20-60 байт | 8 байт (фіксований) |
| **Overhead** | Високі накладні витрати | Мінімальні накладні витрати |
| **Broadcasting/Multicasting** | Не підтримується | Підтримується |
| **Застосування** | HTTP, FTP, Email, SSH | DNS, Streaming, Gaming, VoIP |

### Встановлення з'єднання:

**TCP Three-Way Handshake:**
```
Client                    Server
  |                          |
  |--------- SYN ----------->|  (1. Прохання про з'єднання)
  |                          |
  |<------ SYN-ACK ----------|  (2. Підтвердження + своє прохання)
  |                          |
  |--------- ACK ----------->|  (3. Підтвердження)
  |                          |
  |    [З'єднання встановлено]
  |                          |
  |====== DATA =============>|
```

**UDP (немає встановлення):**
```
Client                    Server
  |                          |
  |====== DATA =============>|  (Одразу відправка!)
  |                          |
  |====== DATA =============>|
```

### Доставка даних:

**TCP (з підтвердженням):**
```
Sender                  Receiver
  |                        |
  |------ Пакет 1 -------->|
  |<------- ACK 1 ---------|
  |                        |
  |------ Пакет 2 -------->|
  |<------- ACK 2 ---------|
  |                        |
  |------ Пакет 3 ---X     | (втрачено)
  |                        |
  [Timeout]                |
  |------ Пакет 3 -------->| (повторна відправка)
  |<------- ACK 3 ---------|
```

**UDP (без підтвердження):**
```
Sender                  Receiver
  |                        |
  |------ Пакет 1 -------->|
  |                        |
  |------ Пакет 2 -------->|
  |                        |
  |------ Пакет 3 ---X     | (втрачено - ніхто не знає!)
  |                        |
  |------ Пакет 4 -------->|
```

### Контроль послідовності:

**TCP:**
```
Відправлено:  1 → 2 → 3 → 4 → 5
Прийшло:      1 → 3 → 2 → 5 → 4
              ↓
Додаток отримує: 1 → 2 → 3 → 4 → 5 (правильний порядок!)
```

**UDP:**
```
Відправлено:  1 → 2 → 3 → 4 → 5
Прийшло:      1 → 3 → 2 → 5 → 4
              ↓
Додаток отримує: 1 → 3 → 2 → 5 → 4 (як прийшло!)
```

### Коли використовувати TCP?

✅ **Використовуй TCP коли:**
- Потрібна гарантія доставки
- Важлива послідовність даних
- Можна пожертвувати швидкістю заради надійності
- Передача великих обсягів даних

**Приклади:**
- HTTP/HTTPS (веб-сторінки)
- FTP (передача файлів)
- Email (SMTP, POP3, IMAP)
- SSH (віддалений доступ)
- Database запити

### Коли використовувати UDP?

✅ **Використовуй UDP коли:**
- Швидкість важливіша за надійність
- Real-time застосування
- Втрата кількох пакетів не критична
- Потрібен broadcasting/multicasting
- Короткі запити-відповіді

**Приклади:**
- DNS (швидкі запити)
- Streaming (відео, аудіо)
- Online gaming
- VoIP (голосові дзвінки)
- IoT сенсори
- Live broadcasting

---

## Переваги UDP

### 1. ⚡ Швидкість

**Чому швидше?**
- Немає встановлення з'єднання (3-way handshake)
- Немає очікування підтверджень (ACK)
- Мінімальний заголовок (8 байт)

**Приклад:**
```
TCP: Handshake (50ms) + Передача (10ms) = 60ms
UDP: Передача (10ms) = 10ms

UDP швидше в 6 разів!
```

### 2. 📉 Низькі накладні витрати

**Overhead порівняння:**
```
UDP:  8 байт заголовок
TCP: 20 байт заголовок (мінімум) + ACK пакети

Для 100 байт даних:
UDP: 108 байт (7.4% overhead)
TCP: 120+ байт (20%+ overhead)
```

### 3. 🔄 Підтримка Broadcasting та Multicasting

**Broadcasting:**
```
Sender → 255.255.255.255 → Всі в мережі отримують
```

**Multicasting:**
```
Sender → 239.0.0.1 → Тільки підписані отримують
```

TCP не підтримує це!

### 4. 🎮 Ідеально для Real-Time

**Чому?**
- Старі дані не потрібні (краще втратити пакет ніж чекати)
- Низька затримка (latency)
- Передбачувана продуктивність

**Приклад в грі:**
```
Позиція гравця в момент T:
Пакет 1 (T+0ms):  X=100, Y=200
Пакет 2 (T+50ms): X=105, Y=203
Пакет 3 (T+100ms): X=110, Y=206 (втрачено)
Пакет 4 (T+150ms): X=115, Y=209

TCP: Чекає на пакет 3, затримка!
UDP: Використовує пакет 4, ігнорує втрачений 3
```

### 5. 💪 Простота реалізації

**UDP код простіше:**
```csharp
// UDP - одразу відправка
socket.SendTo(data, endPoint);

// TCP - потрібно встановлення з'єднання
socket.Connect(endPoint);
socket.Send(data);
```

### 6. 🔌 Не потребує встановленого з'єднання

**Переваги:**
- Можна відправляти різним адресатам
- Менше споживання пам'яті (не зберігаємо стан з'єднання)
- Масштабованість

---

## Недоліки UDP

### 1. ❌ Втрата пакетів

**Проблема:**
```
Відправлено: [1] [2] [3] [4] [5]
Отримано:    [1] [2] [ ] [4] [5]
                      ↑
                 Пакет 3 втрачено назавжди!
```

**Наслідки:**
- Неповні дані
- Потрібна власна логіка відновлення

### 2. 🔄 Дублікати пакетів

**Проблема:**
```
Відправлено: [1] [2] [3]
Отримано:    [1] [2] [2] [3]
                     ↑
                Дублікат!
```

**Рішення:** Додати sequence number в дані.

### 3. 📊 Неправильний порядок

**Проблема:**
```
Відправлено: [1] [2] [3] [4]
Отримано:    [1] [3] [2] [4]
                  ↑  ↑
            Не в порядку!
```

**Рішення:** Додати sequence number і сортувати.

### 4. 🚫 Немає контролю потоку

**Проблема:**
```
Швидкий відправник → | | | | | | → Повільний отримувач
                                      ↓
                                 Переповнення буфера!
                                 Втрата пакетів!
```

**TCP рішення:** Flow control (window size)
**UDP:** Немає! Потрібно реалізовувати власний.

### 5. 🚦 Немає контролю перевантаження

**Проблема:**
```
Багато UDP трафіку → Перевантаження мережі → Втрата пакетів для всіх!
```

**TCP:** Зменшує швидкість при перевантаженні
**UDP:** Не зменшує! Може "забити" мережу.

### 6. 🛡️ Вразливість до атак

**DDoS атаки на UDP:**
```
Атакуючий → UDP Flood → Сервер перевантажений
```

Легше провести атаку через UDP (не потрібно встановлювати з'єднання).

**UDP Amplification атака:**
```
1. Атакуючий відправляє UDP запит з підробленою IP жертви
2. Сервер відправляє велику відповідь жертві
3. Жертва перевантажена
```

---

## Випадки використання UDP

### 1. 📺 Streaming (Відео та Аудіо)

**Чому UDP?**
- Швидкість важливіша за надійність
- Втрата кадру не критична
- Затримка повинна бути мінімальною

**Приклади:**
- YouTube Live
- Twitch
- Netflix (частково)
- Zoom відео

**Як працює:**
```
Сервер                  Клієнт
  |                        |
  |------ Кадр 1 --------->|
  |------ Кадр 2 --------->|
  |------ Кадр 3 ---X      | (втрачено)
  |------ Кадр 4 --------->|
  |                        |
                           ↓
              Кадр 3 пропущений,
              але відео йде далі!
```

### 2. 🎮 Online Gaming

**Чому UDP?**
- Низька затримка (latency) критична
- Старі дані непотрібні
- Високий tick rate

**Приклади:**
- Counter-Strike
- Fortnite
- League of Legends
- Valorant

**Приклад:**
```
Гравець натискає "стрілять" →
  UDP пакет з позицією/дією →
    Сервер отримує за 20ms →
      Інші гравці бачать за 40ms

З TCP було б 100-200ms затримка!
```

### 3. 🌐 DNS (Domain Name System)

**Чому UDP?**
- Короткі запити-відповіді
- Швидкість критична
- Якщо не дійшло — повторити легко

**Приклад:**
```
Клієнт                  DNS Сервер
  |                         |
  |--- Що IP для google.com? ---|>
  |                         |
  |<--- 142.250.185.46 -----|
  |                         |
```

Якщо відповідь не прийшла — клієнт просто повторить запит.

### 4. 📞 VoIP (Voice over IP)

**Чому UDP?**
- Real-time аудіо
- Невелика втрата прийнятна (людина не помітить 1-2% втрат)
- Затримка повинна бути < 150ms

**Приклади:**
- Skype
- WhatsApp calls
- Discord voice
- Zoom audio

### 5. 📡 IoT та Сенсори

**Чому UDP?**
- Прості дані (температура, вологість)
- Енергоефективність
- Втрата одного значення не критична

**Приклад:**
```
Сенсор температури відправляє кожні 10 секунд:
T+0s:  22.5°C
T+10s: 22.7°C
T+20s: [втрачено]
T+30s: 23.1°C

Наступне значення компенсує втрачене!
```

### 6. 📻 Broadcasting та Multicasting

**Broadcasting:**
```
DHCP сервер → Broadcast → Всі клієнти в мережі
```

**Multicasting:**
```
IPTV сервер → Multicast group → Підписані телевізори
```

### 7. ⏰ NTP (Network Time Protocol)

**Чому UDP?**
- Короткі запити
- Точність часу важлива
- Швидкість критична

**Приклад:**
```
Клієнт → NTP сервер: "Який час?"
NTP сервер → Клієнт: "12:34:56.789"
```

### 8. 🎤 Live Streaming Events

**Приклади:**
- Спортивні трансляції
- Концерти online
- Webinars

**Особливість:**
```
Затримка 1-2 секунди прийнятна,
але потік не повинен зупинятися!
```

---

## UDP сокети

### Що таке UDP сокет?

**Сокет (Socket)** — це кінцева точка для відправки або отримання даних.

**UDP сокет** — це інтерфейс для роботи з UDP протоколом в програмі.

### Типи UDP сокетів:

```
1. Звичайний UDP сокет (Unicast)
   Один відправник → Один отримувач

2. Broadcast сокет
   Один відправник → Всі в мережі

3. Multicast сокет
   Один відправник → Група отримувачів
```

### Основні операції з UDP сокетом:

```
1. Створення сокету
   socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)

2. Прив'язка (Bind) - для сервера
   bind(socket, address, port)

3. Відправка даних
   sendto(socket, data, address)

4. Отримання даних
   recvfrom(socket, buffer) → (data, sender_address)

5. Закриття сокету
   close(socket)
```

---

## Робота з UDP в C#

### Приклад 1: Простий UDP сервер

```csharp
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

class UdpServer
{
    static void Main()
    {
        // 1. Створюємо UDP сокет
        UdpClient udpServer = new UdpClient(8888); // Порт 8888
        
        Console.WriteLine("UDP Сервер запущено на порту 8888...");
        
        // Кінцева точка для прийому даних (будь-яка адреса)
        IPEndPoint remoteEndPoint = new IPEndPoint(IPAddress.Any, 0);
        
        try
        {
            while (true)
            {
                // 2. Очікуємо на вхідні дані
                byte[] receivedBytes = udpServer.Receive(ref remoteEndPoint);
                
                // 3. Конвертуємо bytes в string
                string receivedData = Encoding.UTF8.GetString(receivedBytes);
                
                Console.WriteLine($"Отримано від {remoteEndPoint}: {receivedData}");
                
                // 4. Відправляємо відповідь
                string responseData = $"Echo: {receivedData}";
                byte[] responseBytes = Encoding.UTF8.GetBytes(responseData);
                udpServer.Send(responseBytes, responseBytes.Length, remoteEndPoint);
                
                Console.WriteLine($"Відправлено відповідь до {remoteEndPoint}");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Помилка: {ex.Message}");
        }
        finally
        {
            // 5. Закриваємо сокет
            udpServer.Close();
        }
    }
}
```

### Приклад 2: Простий UDP клієнт

```csharp
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

class UdpClient_Example
{
    static void Main()
    {
        // 1. Створюємо UDP клієнт
        UdpClient udpClient = new UdpClient();
        
        // 2. Вказуємо адресу сервера
        string serverIP = "127.0.0.1"; // localhost
        int serverPort = 8888;
        IPEndPoint serverEndPoint = new IPEndPoint(IPAddress.Parse(serverIP), serverPort);
        
        try
        {
            // 3. Готуємо дані для відправки
            string message = "Привіт від UDP клієнта!";
            byte[] sendBytes = Encoding.UTF8.GetBytes(message);
            
            // 4. Відправляємо дані
            udpClient.Send(sendBytes, sendBytes.Length, serverEndPoint);
            Console.WriteLine($"Відправлено: {message}");
            
            // 5. Очікуємо на відповідь
            IPEndPoint remoteEndPoint = new IPEndPoint(IPAddress.Any, 0);
            byte[] receivedBytes = udpClient.Receive(ref remoteEndPoint);
            
            // 6. Отримуємо відповідь
            string receivedData = Encoding.UTF8.GetString(receivedBytes);
            Console.WriteLine($"Отримано: {receivedData}");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Помилка: {ex.Message}");
        }
        finally
        {
            // 7. Закриваємо клієнт
            udpClient.Close();
        }
    }
}
```

### Приклад 3: UDP з таймаутом

```csharp
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

class UdpClientWithTimeout
{
    static void Main()
    {
        UdpClient udpClient = new UdpClient();
        
        // Встановлюємо таймаут 5 секунд
        udpClient.Client.ReceiveTimeout = 5000;
        
        IPEndPoint serverEndPoint = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 8888);
        
        try
        {
            string message = "Привіт!";
            byte[] sendBytes = Encoding.UTF8.GetBytes(message);
            
            udpClient.Send(sendBytes, sendBytes.Length, serverEndPoint);
            Console.WriteLine($"Відправлено: {message}");
            
            IPEndPoint remoteEndPoint = new IPEndPoint(IPAddress.Any, 0);
            byte[] receivedBytes = udpClient.Receive(ref remoteEndPoint);
            
            string receivedData = Encoding.UTF8.GetString(receivedBytes);
            Console.WriteLine($"Отримано: {receivedData}");
        }
        catch (SocketException ex)
        {
            if (ex.SocketErrorCode == SocketError.TimedOut)
            {
                Console.WriteLine("Таймаут! Сервер не відповів протягом 5 секунд.");
            }
            else
            {
                Console.WriteLine($"Помилка сокету: {ex.Message}");
            }
        }
        finally
        {
            udpClient.Close();
        }
    }
}
```

### Приклад 4: Асинхронний UDP сервер

```csharp
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

class AsyncUdpServer
{
    private UdpClient udpServer;
    
    public AsyncUdpServer(int port)
    {
        udpServer = new UdpClient(port);
        Console.WriteLine($"Асинхронний UDP сервер запущено на порту {port}");
    }
    
    public async Task StartAsync()
    {
        try
        {
            while (true)
            {
                // Асинхронне очікування даних
                UdpReceiveResult result = await udpServer.ReceiveAsync();
                
                string receivedData = Encoding.UTF8.GetString(result.Buffer);
                Console.WriteLine($"Отримано від {result.RemoteEndPoint}: {receivedData}");
                
                // Обробка даних в окремому завданні
                _ = Task.Run(() => ProcessDataAsync(result.Buffer, result.RemoteEndPoint));
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Помилка: {ex.Message}");
        }
    }
    
    private async Task ProcessDataAsync(byte[] data, IPEndPoint remoteEndPoint)
    {
        // Симуляція обробки
        await Task.Delay(100);
        
        string responseData = $"Оброблено: {Encoding.UTF8.GetString(data)}";
        byte[] responseBytes = Encoding.UTF8.GetBytes(responseData);
        
        await udpServer.SendAsync(responseBytes, responseBytes.Length, remoteEndPoint);
        Console.WriteLine($"Відправлено відповідь до {remoteEndPoint}");
    }
    
    static async Task Main()
    {
        var server = new AsyncUdpServer(8888);
        await server.StartAsync();
    }
}
```

### Приклад 5: UDP з підтвердженням (Reliable UDP)

```csharp
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

// Додаємо надійність до UDP
class ReliableUdpClient
{
    private UdpClient udpClient;
    private IPEndPoint serverEndPoint;
    private int maxRetries = 3;
    private int timeout = 2000; // 2 секунди
    
    public ReliableUdpClient(string serverIP, int serverPort)
    {
        udpClient = new UdpClient();
        serverEndPoint = new IPEndPoint(IPAddress.Parse(serverIP), serverPort);
    }
    
    public string SendWithAck(string message, int sequenceNumber)
    {
        // Додаємо sequence number до повідомлення
        string dataToSend = $"{sequenceNumber}|{message}";
        byte[] sendBytes = Encoding.UTF8.GetBytes(dataToSend);
        
        for (int attempt = 1; attempt <= maxRetries; attempt++)
        {
            try
            {
                Console.WriteLine($"Спроба {attempt}: Відправка '{message}'...");
                
                // Відправляємо дані
                udpClient.Send(sendBytes, sendBytes.Length, serverEndPoint);
                
                // Встановлюємо таймаут
                udpClient.Client.ReceiveTimeout = timeout;
                
                // Очікуємо підтвердження
                IPEndPoint remoteEndPoint = new IPEndPoint(IPAddress.Any, 0);
                byte[] receivedBytes = udpClient.Receive(ref remoteEndPoint);
                string response = Encoding.UTF8.GetString(receivedBytes);
                
                // Перевіряємо ACK
                if (response.StartsWith($"ACK|{sequenceNumber}"))
                {
                    Console.WriteLine($"✓ Підтверджено! Отримано: {response}");
                    return response;
                }
            }
            catch (SocketException ex)
            {
                if (ex.SocketErrorCode == SocketError.TimedOut)
                {
                    Console.WriteLine($"✗ Таймаут на спробі {attempt}");
                    if (attempt == maxRetries)
                    {
                        throw new Exception($"Не вдалося доставити після {maxRetries} спроб");
                    }
                }
                else
                {
                    throw;
                }
            }
        }
        
        return null;
    }
    
    public void Close()
    {
        udpClient.Close();
    }
}

// Сервер з підтвердженням
class ReliableUdpServer
{
    static void Main()
    {
        UdpClient udpServer = new UdpClient(8888);
        Console.WriteLine("Reliable UDP Сервер запущено...");
        
        IPEndPoint remoteEndPoint = new IPEndPoint(IPAddress.Any, 0);
        
        while (true)
        {
            try
            {
                byte[] receivedBytes = udpServer.Receive(ref remoteEndPoint);
                string receivedData = Encoding.UTF8.GetString(receivedBytes);
                
                // Парсимо sequence number
                string[] parts = receivedData.Split('|');
                int sequenceNumber = int.Parse(parts[0]);
                string message = parts[1];
                
                Console.WriteLine($"Отримано пакет #{sequenceNumber}: {message}");
                
                // Відправляємо ACK
                string ackMessage = $"ACK|{sequenceNumber}|{message}";
                byte[] ackBytes = Encoding.UTF8.GetBytes(ackMessage);
                udpServer.Send(ackBytes, ackBytes.Length, remoteEndPoint);
                
                Console.WriteLine($"Відправлено ACK для пакету #{sequenceNumber}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Помилка: {ex.Message}");
            }
        }
    }
}
```

### Приклад 6: UDP з великими даними (фрагментація)

```csharp
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Collections.Generic;

class UdpFragmentation
{
    private const int MAX_PACKET_SIZE = 1024; // 1KB на пакет
    
    // Відправка великих даних частинами
    public static void SendLargeData(UdpClient client, string data, IPEndPoint endPoint)
    {
        byte[] dataBytes = Encoding.UTF8.GetBytes(data);
        int totalPackets = (int)Math.Ceiling((double)dataBytes.Length / MAX_PACKET_SIZE);
        
        Console.WriteLine($"Відправка {dataBytes.Length} байт в {totalPackets} пакетах...");
        
        for (int i = 0; i < totalPackets; i++)
        {
            int offset = i * MAX_PACKET_SIZE;
            int length = Math.Min(MAX_PACKET_SIZE, dataBytes.Length - offset);
            
            // Створюємо пакет з метаданими
            byte[] packet = new byte[length + 12]; // 12 байт метадані
            
            // Метадані: [TotalPackets(4)][PacketNumber(4)][DataLength(4)][Data...]
            BitConverter.GetBytes(totalPackets).CopyTo(packet, 0);
            BitConverter.GetBytes(i).CopyTo(packet, 4);
            BitConverter.GetBytes(length).CopyTo(packet, 8);
            Array.Copy(dataBytes, offset, packet, 12, length);
            
            client.Send(packet, packet.Length, endPoint);
            Console.WriteLine($"Відправлено пакет {i + 1}/{totalPackets}");
        }
    }
    
    // Отримання великих даних
    public static string ReceiveLargeData(UdpClient server)
    {
        Dictionary<int, byte[]> packets = new Dictionary<int, byte[]>();
        int totalPackets = -1;
        int receivedPackets = 0;
        
        IPEndPoint remoteEndPoint = new IPEndPoint(IPAddress.Any, 0);
        
        while (true)
        {
            byte[] receivedPacket = server.Receive(ref remoteEndPoint);
            
            // Парсимо метадані
            int total = BitConverter.ToInt32(receivedPacket, 0);
            int packetNum = BitConverter.ToInt32(receivedPacket, 4);
            int dataLength = BitConverter.ToInt32(receivedPacket, 8);
            
            if (totalPackets == -1)
            {
                totalPackets = total;
            }
            
            // Зберігаємо дані
            byte[] data = new byte[dataLength];
            Array.Copy(receivedPacket, 12, data, 0, dataLength);
            packets[packetNum] = data;
            
            receivedPackets++;
            Console.WriteLine($"Отримано пакет {packetNum + 1}/{totalPackets}");
            
            // Перевіряємо чи всі пакети отримані
            if (receivedPackets == totalPackets)
            {
                // Збираємо всі дані
                List<byte> allData = new List<byte>();
                for (int i = 0; i < totalPackets; i++)
                {
                    allData.AddRange(packets[i]);
                }
                
                return Encoding.UTF8.GetString(allData.ToArray());
            }
        }
    }
    
    static void Main()
    {
        // Приклад використання
        UdpClient client = new UdpClient();
        IPEndPoint serverEndPoint = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 8888);
        
        string largeData = new string('A', 5000); // 5KB даних
        SendLargeData(client, largeData, serverEndPoint);
        
        client.Close();
    }
}
```

---

## Broadcasting та Multicasting

### Broadcasting (Широкомовна передача)

**Broadcasting** — відправка даних всім пристроям в локальній мережі.

**Broadcast адреса:** 255.255.255.255 (або специфічна для мережі)

### Приклад: UDP Broadcasting

```csharp
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

// Відправник broadcast
class BroadcastSender
{
    static void Main()
    {
        UdpClient udpClient = new UdpClient();
        
        // Увімкнути broadcast
        udpClient.EnableBroadcast = true;
        
        IPEndPoint broadcastEndPoint = new IPEndPoint(IPAddress.Broadcast, 8888);
        
        try
        {
            while (true)
            {
                Console.Write("Введіть повідомлення для broadcast: ");
                string message = Console.ReadLine();
                
                byte[] data = Encoding.UTF8.GetBytes(message);
                udpClient.Send(data, data.Length, broadcastEndPoint);
                
                Console.WriteLine($"Broadcast відправлено: {message}");
            }
        }
        finally
        {
            udpClient.Close();
        }
    }
}

// Отримувач broadcast
class BroadcastReceiver
{
    static void Main()
    {
        UdpClient udpClient = new UdpClient(8888);
        Console.WriteLine("Очікування broadcast повідомлень на порту 8888...");
        
        IPEndPoint remoteEndPoint = new IPEndPoint(IPAddress.Any, 0);
        
        try
        {
            while (true)
            {
                byte[] receivedBytes = udpClient.Receive(ref remoteEndPoint);
                string receivedData = Encoding.UTF8.GetString(receivedBytes);
                
                Console.WriteLine($"Broadcast від {remoteEndPoint.Address}: {receivedData}");
            }
        }
        finally
        {
            udpClient.Close();
        }
    }
}
```

### Multicasting (Групова передача)

**Multicasting** — відправка даних групі підписаних пристроїв.

**Multicast адреси:** 224.0.0.0 - 239.255.255.255

**Популярні multicast групи:**
```
224.0.0.1  → Всі пристрої в локальній мережі
224.0.0.2  → Всі роутери в локальній мережі
239.0.0.0  → Організаційно-локальний scope
```

### Приклад: UDP Multicasting

```csharp
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

// Multicast відправник
class MulticastSender
{
    static void Main()
    {
        UdpClient udpClient = new UdpClient();
        
        // Multicast група та порт
        IPAddress multicastAddress = IPAddress.Parse("239.0.0.1");
        int port = 8888;
        IPEndPoint multicastEndPoint = new IPEndPoint(multicastAddress, port);
        
        try
        {
            while (true)
            {
                Console.Write("Введіть повідомлення для multicast: ");
                string message = Console.ReadLine();
                
                byte[] data = Encoding.UTF8.GetBytes(message);
                udpClient.Send(data, data.Length, multicastEndPoint);
                
                Console.WriteLine($"Multicast відправлено до {multicastAddress}:{port}");
                System.Threading.Thread.Sleep(1000);
            }
        }
        finally
        {
            udpClient.Close();
        }
    }
}

// Multicast отримувач
class MulticastReceiver
{
    static void Main()
    {
        int port = 8888;
        IPAddress multicastAddress = IPAddress.Parse("239.0.0.1");
        
        // Створюємо UDP клієнт
        UdpClient udpClient = new UdpClient();
        udpClient.ExclusiveAddressUse = false;
        
        // Дозволяємо повторне використання адреси
        IPEndPoint localEndPoint = new IPEndPoint(IPAddress.Any, port);
        udpClient.Client.SetSocketOption(
            SocketOptionLevel.Socket, 
            SocketOptionName.ReuseAddress, 
            true
        );
        udpClient.Client.Bind(localEndPoint);
        
        // Приєднуємося до multicast групи
        udpClient.JoinMulticastGroup(multicastAddress);
        
        Console.WriteLine($"Підписано на multicast групу {multicastAddress}:{port}");
        Console.WriteLine("Очікування повідомлень...");
        
        IPEndPoint remoteEndPoint = new IPEndPoint(IPAddress.Any, 0);
        
        try
        {
            while (true)
            {
                byte[] receivedBytes = udpClient.Receive(ref remoteEndPoint);
                string receivedData = Encoding.UTF8.GetString(receivedBytes);
                
                Console.WriteLine($"Multicast від {remoteEndPoint.Address}: {receivedData}");
            }
        }
        finally
        {
            // Виходимо з групи
            udpClient.DropMulticastGroup(multicastAddress);
            udpClient.Close();
        }
    }
}
```

### Порівняння Broadcasting vs Multicasting:

| Характеристика | Broadcasting | Multicasting |
|----------------|--------------|--------------|
| **Адреса** | 255.255.255.255 | 224.0.0.0 - 239.255.255.255 |
| **Отримувачі** | Всі в мережі | Тільки підписані |
| **Ефективність** | Нижча (всі отримують) | Вища (тільки зацікавлені) |
| **Підписка** | Не потрібна | Потрібна (JoinMulticastGroup) |
| **Масштабованість** | Погана (забиває мережу) | Краща |
| **Використання** | Локальні мережі | Локальні та інтернет |

---

## Найкращі практики

### 1. 🔢 Додавай Sequence Number

**Чому:** Відстеження порядку та виявлення втрачених пакетів.

```csharp
class UdpPacket
{
    public int SequenceNumber { get; set; }
    public DateTime Timestamp { get; set; }
    public byte[] Data { get; set; }
}
```

### 2. ⏱️ Використовуй таймаути

**Завжди встановлюй ReceiveTimeout!**

```csharp
udpClient.Client.ReceiveTimeout = 5000; // 5 секунд
```

### 3. 📏 Обмежуй розмір пакетів

**Рекомендований розмір:** <= 1472 байт (щоб уникнути IP фрагментації)

```
Ethernet MTU: 1500 байт
- IP заголовок: 20 байт
- UDP заголовок: 8 байт
= 1472 байт для даних
```

### 4. ✅ Додавай Checksum або CRC

**Для критичних даних:**

```csharp
using System.Security.Cryptography;

byte[] CalculateChecksum(byte[] data)
{
    using (var md5 = MD5.Create())
    {
        return md5.ComputeHash(data);
    }
}
```

### 5. 🔁 Реалізуй механізм повторної відправки

```csharp
int maxRetries = 3;
for (int i = 0; i < maxRetries; i++)
{
    try
    {
        // Відправка та очікування
        break; // Успіх
    }
    catch (SocketException)
    {
        if (i == maxRetries - 1) throw;
    }
}
```

### 6. 🛡️ Валідуй вхідні дані

```csharp
if (receivedBytes.Length < MIN_PACKET_SIZE)
{
    Console.WriteLine("Пакет занадто малий, ігноруємо");
    continue;
}

if (receivedBytes.Length > MAX_PACKET_SIZE)
{
    Console.WriteLine("Пакет занадто великий, ігноруємо");
    continue;
}
```

### 7. 🔐 Шифруй чутливі дані

UDP не має вбудованого шифрування!

```csharp
// Використовуй DTLS (Datagram TLS) або власне шифрування
byte[] EncryptData(byte[] data, byte[] key)
{
    using (var aes = Aes.Create())
    {
        aes.Key = key;
        // ... шифрування
    }
}
```

### 8. 📊 Логуй та моніторь

```csharp
Console.WriteLine($"[{DateTime.Now}] Пакет #{seq} відправлено до {endpoint}");
```

### 9. 🔄 Використовуй асинхронні операції

```csharp
// Замість
byte[] data = udpClient.Receive(ref endPoint);

// Використовуй
UdpReceiveResult result = await udpClient.ReceiveAsync();
```

### 10. 🚫 Уникай надмірного UDP трафіку

**Rate limiting:**

```csharp
int maxPacketsPerSecond = 100;
int delay = 1000 / maxPacketsPerSecond;

foreach (var packet in packets)
{
    SendPacket(packet);
    await Task.Delay(delay);
}
```

---

## Поширені проблеми та їх рішення

### Проблема 1: Пакети не доходять

**Причини:**
- Firewall блокує порт
- Неправильна адреса/порт
- Втрата в мережі

**Рішення:**
```csharp
// 1. Перевір firewall
// 2. Використовуй localhost для тестування
IPAddress.Parse("127.0.0.1")

// 3. Додай retry логіку
// 4. Логуй всі відправлення/отримання
```

### Проблема 2: "Address already in use"

**Причина:** Порт вже використовується.

**Рішення:**
```csharp
udpClient.Client.SetSocketOption(
    SocketOptionLevel.Socket,
    SocketOptionName.ReuseAddress,
    true
);
```

### Проблема 3: Пакети приходять в неправильному порядку

**Рішення:**
```csharp
class PacketReorderer
{
    private Dictionary<int, byte[]> buffer = new Dictionary<int, byte[]>();
    private int expectedSeq = 0;
    
    public List<byte[]> AddPacket(int seq, byte[] data)
    {
        buffer[seq] = data;
        List<byte[]> result = new List<byte[]>();
        
        while (buffer.ContainsKey(expectedSeq))
        {
            result.Add(buffer[expectedSeq]);
            buffer.Remove(expectedSeq);
            expectedSeq++;
        }
        
        return result;
    }
}
```

### Проблема 4: Втрата великих пакетів

**Причина:** IP фрагментація або перевищення MTU.

**Рішення:**
```csharp
const int SAFE_PACKET_SIZE = 1400; // Менше MTU

if (data.Length > SAFE_PACKET_SIZE)
{
    // Розділити на частини
    SplitAndSend(data);
}
```

### Проблема 5: Повільна продуктивність

**Рішення:**

```csharp
// 1. Збільш розмір буфера
udpClient.Client.ReceiveBufferSize = 1024 * 1024; // 1MB
udpClient.Client.SendBufferSize = 1024 * 1024;

// 2. Використовуй асинхронні операції
await udpClient.SendAsync(data, data.Length, endpoint);

// 3. Batch відправка
List<byte[]> batch = new List<byte[]>();
// ... збираємо batch
foreach (var packet in batch)
{
    await udpClient.SendAsync(packet, packet.Length, endpoint);
}
```

### Проблема 6: "Cannot assign requested address"

**Причина:** Неправильна IP адреса або мережевий інтерфейс.

**Рішення:**
```csharp
// Використовуй IPAddress.Any для прослуховування всіх інтерфейсів
IPEndPoint localEndPoint = new IPEndPoint(IPAddress.Any, port);
```

### Проблема 7: Broadcast не працює

**Рішення:**
```csharp
// Обов'язково увімкни broadcast!
udpClient.EnableBroadcast = true;

// Використовуй правильну broadcast адресу
IPEndPoint broadcast = new IPEndPoint(IPAddress.Broadcast, port);
```

### Проблема 8: Multicast не працює

**Рішення:**
```csharp
// 1. Встанови TTL (Time To Live)
udpClient.Client.SetSocketOption(
    SocketOptionLevel.IP,
    SocketOptionName.MulticastTimeToLive,
    10
);

// 2. Приєднайся до групи
udpClient.JoinMulticastGroup(multicastAddress);

// 3. Перевір що multicast адреса в правильному діапазоні
// 224.0.0.0 - 239.255.255.255
```

---

## Підсумок

### UDP - це:
✅ Швидкий і легкий протокол  
✅ Ідеальний для real-time застосувань  
✅ Простий в реалізації  

❌ Ненадійний (без гарантій доставки)  
❌ Потребує додаткової логіки для надійності  
❌ Вразливий до атак  

### Коли використовувати UDP:
- Streaming (відео, аудіо)
- Online gaming
- VoIP
- DNS
- IoT сенсори
- Broadcasting/Multicasting

### Коли НЕ використовувати UDP:
- Передача файлів
- Банківські транзакції
- Email
- Веб-сторінки
- Будь-що, де кожен байт важливий

**Пам'ятай:** UDP — це компроміс між швидкістю та надійністю! 🚀

