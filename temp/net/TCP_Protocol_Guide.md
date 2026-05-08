# TCP Protocol - Повний посібник

**TCP (Transmission Control Protocol)** - протокол транспортного рівня, який забезпечує надійну, упорядковану та перевірену на помилки доставку байтів між додатками.

---

## Зміст

1. [Вступ до TCP](#вступ-до-tcp)
2. [TCP в моделі OSI/TCP-IP](#tcp-в-моделі-ositcp-ip)
3. [Структура TCP сегмента](#структура-tcp-сегмента)
4. [TCP з'єднання](#tcp-зєднання)
5. [Надійність TCP](#надійність-tcp)
6. [Контроль потоку](#контроль-потоку)
7. [Контроль перевантаження](#контроль-перевантаження)
8. [TCP опції](#tcp-опції)
9. [TCP States](#tcp-states)
10. [Проблеми та оптимізація TCP](#проблеми-та-оптимізація-tcp)
11. [TCP vs UDP](#tcp-vs-udp)
12. [Практичні інструменти](#практичні-інструменти)

---

## Вступ до TCP

### Що таке TCP?

**TCP (Transmission Control Protocol)** - один з основних протоколів Інтернету, який забезпечує:

```
┌─────────────────────────────────────────────────────────┐
│              Основні характеристики TCP                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Надійність (Reliability)                           │
│     └─ Гарантована доставка даних                      │
│                                                         │
│  2. Упорядкованість (Ordering)                         │
│     └─ Дані прибувають в правильному порядку           │
│                                                         │
│  3. Перевірка помилок (Error Checking)                 │
│     └─ Checksum для виявлення пошкоджених даних        │
│                                                         │
│  4. Контроль потоку (Flow Control)                     │
│     └─ Запобігання перевантаженню приймача             │
│                                                         │
│  5. Контроль перевантаження (Congestion Control)       │
│     └─ Адаптація до завантаженості мережі              │
│                                                         │
│  6. З'єднання (Connection-oriented)                    │
│     └─ Встановлення з'єднання перед передачею          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Історія TCP:

```
1974  ┌─────────────────────────────────────────┐
      │  Vint Cerf & Bob Kahn                   │
      │  Публікація концепції TCP               │
      └─────────────────────────────────────────┘
        ↓
1981  ┌─────────────────────────────────────────┐
      │  RFC 793 - TCP Specification            │
      │  Стандартизація TCP                      │
      └─────────────────────────────────────────┘
        ↓
1983  ┌─────────────────────────────────────────┐
      │  ARPANET перейшла на TCP/IP             │
      │  "Flag Day" - 1 січня 1983              │
      └─────────────────────────────────────────┘
        ↓
1990+ ┌─────────────────────────────────────────┐
      │  Розширення TCP                         │
      │  - TCP Fast Open                        │
      │  - TCP SACK                             │
      │  - ECN (Explicit Congestion Notification)│
      └─────────────────────────────────────────┘
```

### Навіщо потрібен TCP?

**Проблема:** IP протокол (нижній рівень) **не гарантує** доставку пакетів:

```
IP характеристики:
❌ Пакети можуть загубитися
❌ Пакети можуть прийти в неправильному порядку
❌ Пакети можуть дублюватися
❌ Пакети можуть бути пошкоджені
❌ Немає контролю потоку
```

**TCP вирішує ці проблеми:**

```
TCP характеристики:
✅ Гарантована доставка (retransmission)
✅ Упорядкованість (sequence numbers)
✅ Дедуплікація (sequence numbers)
✅ Перевірка помилок (checksums)
✅ Контроль потоку (sliding window)
✅ Контроль перевантаження (congestion algorithms)
```

---

## TCP в моделі OSI/TCP-IP

### OSI модель:

```
┌─────────────────────┐
│  7. Application     │  HTTP, FTP, SSH, SMTP
├─────────────────────┤
│  6. Presentation    │  SSL/TLS, JPEG, ASCII
├─────────────────────┤
│  5. Session         │  NetBIOS, RPC
├─────────────────────┤
│  4. Transport    ◄──┼─── TCP/UDP (тут TCP!)
├─────────────────────┤
│  3. Network         │  IP, ICMP, ARP
├─────────────────────┤
│  2. Data Link       │  Ethernet, Wi-Fi
├─────────────────────┤
│  1. Physical        │  Кабелі, радіохвилі
└─────────────────────┘
```

### TCP/IP модель (Internet Protocol Suite):

```
┌─────────────────────────────────────────────────────────┐
│  Application Layer                                      │
│  (HTTP, FTP, SSH, DNS, SMTP)                           │
└─────────────────────────────────────────────────────────┘
             ↓
┌─────────────────────────────────────────────────────────┐
│  Transport Layer                                        │
│  TCP ◄─── Ми тут!                                      │
│  (або UDP)                                             │
└─────────────────────────────────────────────────────────┘
             ↓
┌─────────────────────────────────────────────────────────┐
│  Internet Layer                                         │
│  IP (IPv4/IPv6)                                        │
└─────────────────────────────────────────────────────────┘
             ↓
┌─────────────────────────────────────────────────────────┐
│  Link Layer                                             │
│  Ethernet, Wi-Fi                                        │
└─────────────────────────────────────────────────────────┘
```

### Інкапсуляція:

```
Application Data (HTTP, etc.)
       ↓
┌──────────────────────────────────────┐
│ TCP Header │ Application Data        │ ← TCP Segment
└──────────────────────────────────────┘
       ↓
┌────────────────────────────────────────────────┐
│ IP Header │ TCP Header │ Application Data     │ ← IP Packet
└────────────────────────────────────────────────┘
       ↓
┌──────────────────────────────────────────────────────────┐
│ Ethernet │ IP Header │ TCP Header │ Application Data │CRC│ ← Ethernet Frame
└──────────────────────────────────────────────────────────┘
```

---

## Структура TCP сегмента

TCP сегмент складається з **заголовка** (мінімум 20 байт) та **даних**.

### TCP заголовок (20-60 байт):

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        Sequence Number                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Acknowledgment Number                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Data |       |C|E|U|A|P|R|S|F|                               |
| Offset| Rsrvd |W|C|R|C|S|S|Y|I|            Window             |
|       |       |R|E|G|K|H|T|N|N|                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Checksum            |         Urgent Pointer        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options                    |    Padding    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                             Data                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Детальний опис полів:

#### 1. Source Port (16 біт)

```
Порт відправника (0-65535)

Приклади:
- 80 (HTTP)
- 443 (HTTPS)
- 22 (SSH)
- Випадковий порт клієнта (ephemeral port): 49152-65535
```

#### 2. Destination Port (16 біт)

```
Порт отримувача (0-65535)

Комбінація (Source IP, Source Port, Dest IP, Dest Port)
визначає унікальне TCP з'єднання
```

#### 3. Sequence Number (32 біти)

```
Номер першого байта даних в цьому сегменті

Приклад:
Segment 1: SEQ = 1000, Data = 100 bytes
Segment 2: SEQ = 1100, Data = 200 bytes
Segment 3: SEQ = 1300, Data = 150 bytes

Використовується для:
✅ Упорядкування сегментів
✅ Виявлення втрат
✅ Дедуплікації
```

#### 4. Acknowledgment Number (32 біти)

```
Наступний очікуваний байт від відправника

Приклад:
Отримано сегмент з SEQ=1000, Data=100 bytes
Відповідь: ACK=1100 (очікую байт 1100)

ACK=1100 означає: "Я отримав все до байта 1099"
```

#### 5. Data Offset (4 біти)

```
Розмір TCP заголовка в 32-бітних словах (4-байтних блоках)

Мінімум: 5 (5 × 4 = 20 байт)
Максимум: 15 (15 × 4 = 60 байт)

60 байт - 20 байт = 40 байт для TCP Options
```

#### 6. Reserved (4 біти)

```
Зарезервовано для майбутнього використання
Повинні бути 0
```

#### 7. Flags (8 біт):

```
┌─────┬─────────────────────────────────────────────────┐
│ CWR │ Congestion Window Reduced                       │
│     │ (ECN - Explicit Congestion Notification)        │
├─────┼─────────────────────────────────────────────────┤
│ ECE │ ECN-Echo                                        │
│     │ (повідомлення про перевантаження)               │
├─────┼─────────────────────────────────────────────────┤
│ URG │ Urgent Pointer field significant                │
│     │ (терміновi дані)                                │
├─────┼─────────────────────────────────────────────────┤
│ ACK │ Acknowledgment field significant                │
│     │ (підтвердження отримання)                       │
├─────┼─────────────────────────────────────────────────┤
│ PSH │ Push function                                   │
│     │ (негайно передати дані додатку)                 │
├─────┼─────────────────────────────────────────────────┤
│ RST │ Reset the connection                            │
│     │ (примусово закрити з'єднання)                   │
├─────┼─────────────────────────────────────────────────┤
│ SYN │ Synchronize sequence numbers                    │
│     │ (встановлення з'єднання)                        │
├─────┼─────────────────────────────────────────────────┤
│ FIN │ No more data from sender                        │
│     │ (закриття з'єднання)                            │
└─────┴─────────────────────────────────────────────────┘
```

#### 8. Window Size (16 біт)

```
Розмір receive window (0-65535 байт)

Вказує скільки байт отримувач готовий прийняти

Приклад:
Window = 8192 → Можна відправити 8192 байти без ACK

З Window Scale option може бути до 1 GB!
```

#### 9. Checksum (16 біт)

```
Контрольна сума для виявлення помилок

Обчислюється для:
- TCP заголовка
- TCP даних
- Pseudo-header (частина IP заголовка)

Pseudo-header включає:
- Source IP
- Destination IP
- Protocol (TCP = 6)
- TCP Length
```

#### 10. Urgent Pointer (16 біт)

```
Вказує на кінець термінових даних (якщо URG=1)

Рідко використовується в сучасних додатках
```

#### 11. Options (змінна довжина, 0-40 байт)

```
Додаткові параметри TCP

Приклади:
- MSS (Maximum Segment Size)
- Window Scale
- SACK (Selective Acknowledgment)
- Timestamps
```

---

## TCP з'єднання

TCP - **connection-oriented** протокол. Перед передачею даних потрібно встановити з'єднання.

### 3-Way Handshake (встановлення з'єднання)

```
Client                                    Server
  │                                         │
  │────── SYN (SEQ=x) ─────────────────────→│
  │                                         │
  │       [Client: SYN-SENT]                │
  │       [Server: LISTEN → SYN-RECEIVED]   │
  │                                         │
  │←───── SYN-ACK (SEQ=y, ACK=x+1) ─────────│
  │                                         │
  │       [Client: ESTABLISHED]             │
  │                                         │
  │────── ACK (ACK=y+1) ────────────────────→│
  │                                         │
  │       [Server: ESTABLISHED]             │
  │                                         │
  └═══════ З'єднання встановлено ═══════════┘
```

**Детально:**

**Крок 1: SYN**
```
Client → Server

TCP Flags: SYN=1
Sequence Number: x (випадкове початкове значення ISN)
ACK: 0

Клієнт: "Хочу встановити з'єднання, мій ISN = x"
```

**Крок 2: SYN-ACK**
```
Server → Client

TCP Flags: SYN=1, ACK=1
Sequence Number: y (ISN сервера)
Acknowledgment: x+1

Сервер: "Погоджуюсь, мій ISN = y, отримав твій ISN = x"
```

**Крок 3: ACK**
```
Client → Server

TCP Flags: ACK=1
Sequence Number: x+1
Acknowledgment: y+1

Клієнт: "Підтверджую, отримав твій ISN = y"
```

**Чому 3 кроки?**

```
1. Двостороннє підтвердження
   - Клієнт знає, що сервер може отримувати
   - Сервер знає, що клієнт може отримувати

2. Синхронізація sequence numbers
   - Обидві сторони обмінялись ISN

3. Захист від дублікатів
   - ISN випадкові → старі пакети не плутаються з новими
```

### 4-Way Handshake (закриття з'єднання)

```
Client                                    Server
  │                                         │
  │────── FIN (SEQ=x) ─────────────────────→│
  │                                         │
  │       [Client: FIN-WAIT-1]              │
  │                                         │
  │←───── ACK (ACK=x+1) ────────────────────│
  │                                         │
  │       [Client: FIN-WAIT-2]              │
  │       [Server: CLOSE-WAIT]              │
  │                                         │
  │       Server може ще відправляти дані   │
  │                                         │
  │←───── FIN (SEQ=y) ──────────────────────│
  │                                         │
  │       [Server: LAST-ACK]                │
  │                                         │
  │────── ACK (ACK=y+1) ────────────────────→│
  │                                         │
  │       [Client: TIME-WAIT → CLOSED]      │
  │       [Server: CLOSED]                  │
  │                                         │
  └═══════ З'єднання закрито ════════════════┘
```

**Чому 4 кроки?**

```
TCP - full-duplex (двосторонній)

Закриття в одну сторону:
1. Client → Server: FIN (я більше не відправлю)
2. Server → Client: ACK (зрозумів)

Закриття в іншу сторону:
3. Server → Client: FIN (я теж більше не відправлю)
4. Client → Server: ACK (зрозумів)

Сервер може продовжувати відправляти дані між кроками 2 і 3!
```

### TIME-WAIT стан:

```
Після відправки фінального ACK клієнт чекає 2×MSL (Maximum Segment Lifetime)

MSL = 30-120 секунд (зазвичай 60 секунд)
TIME-WAIT = 2×60 = 120 секунд

Чому?
1. Фінальний ACK може загубитися
   → Сервер повторно відправить FIN
   → Клієнт повинен повторно відправити ACK

2. Старі пакети з попереднього з'єднання повинні зникнути з мережі
```

### Одночасне відкриття з'єднання:

```
Client A                                    Client B
   │                                           │
   │────── SYN (SEQ=x) ───────────────────────→│
   │                                           │
   │←───── SYN (SEQ=y) ────────────────────────│
   │                                           │
   │────── SYN-ACK (SEQ=x, ACK=y+1) ──────────→│
   │                                           │
   │←───── SYN-ACK (SEQ=y, ACK=x+1) ───────────│
   │                                           │
   └══════ З'єднання встановлено ═════════════┘

Обидві сторони одночасно відправили SYN
Рідко трапляється, але протокол це підтримує!
```

---

## Надійність TCP

TCP забезпечує **надійну доставку** через механізми підтвердження та повторної передачі.

### Sequence Numbers та Acknowledgments:

```
Sender                                    Receiver
  │                                         │
  │─── SEQ=1000, Data=100 bytes ───────────→│
  │                                         │
  │                                         │─── Отримано 1000-1099
  │                                         │
  │←──── ACK=1100 ──────────────────────────│
  │                                         │
  │     (ACK=1100 означає: очікую байт 1100)│
  │                                         │
  │─── SEQ=1100, Data=200 bytes ───────────→│
  │                                         │
  │←──── ACK=1300 ──────────────────────────│
  │                                         │
```

### Retransmission (повторна передача):

#### Сценарій 1: Втрата сегмента

```
Sender                                    Receiver
  │                                         │
  │─── SEQ=1000, Data=100 ─────────────────→│
  │                                         │
  │←──── ACK=1100 ──────────────────────────│
  │                                         │
  │─── SEQ=1100, Data=100 ───────────────X  │ Втрачено!
  │                                         │
  │─── SEQ=1200, Data=100 ─────────────────→│
  │                                         │
  │                                         │─── Отримано 1200, але
  │                                         │    очікується 1100!
  │                                         │
  │←──── ACK=1100 (duplicate ACK) ──────────│
  │                                         │
  │─── SEQ=1300, Data=100 ─────────────────→│
  │                                         │
  │←──── ACK=1100 (duplicate ACK) ──────────│
  │                                         │
  │     Після 3 duplicate ACKs:             │
  │     Fast Retransmit!                    │
  │                                         │
  │─── SEQ=1100, Data=100 (retransmit) ────→│
  │                                         │
  │←──── ACK=1400 ──────────────────────────│
  │                                         │
```

#### Сценарій 2: Втрата ACK

```
Sender                                    Receiver
  │                                         │
  │─── SEQ=1000, Data=100 ─────────────────→│
  │                                         │
  │                                      X←─│ ACK=1100 (втрачено!)
  │                                         │
  │     RTO timeout спрацював               │
  │                                         │
  │─── SEQ=1000, Data=100 (retransmit) ────→│
  │                                         │
  │                                         │─── Дублікат! Ігнорую
  │                                         │
  │←──── ACK=1100 ──────────────────────────│
  │                                         │
```

### Retransmission Timeout (RTO):

```
RTO - час очікування ACK перед повторною передачею

Занадто малий RTO:
❌ Непотрібні retransmissions
❌ Перевантаження мережі

Занадто великий RTO:
❌ Повільна реакція на втрати
❌ Погана продуктивність

Рішення: Adaptive RTO (динамічний)
```

**Обчислення RTO:**

```
1. Вимірювання RTT (Round-Trip Time)
   RTT = час від відправки до отримання ACK

2. Smooth RTT (SRTT)
   SRTT = (1 - α) × SRTT + α × RTT
   α = 1/8 = 0.125

3. RTT Variation (RTTVAR)
   RTTVAR = (1 - β) × RTTVAR + β × |SRTT - RTT|
   β = 1/4 = 0.25

4. RTO
   RTO = SRTT + 4 × RTTVAR
   Мінімум: 1 секунда

Приклад:
RTT = 100ms
SRTT = 100ms
RTTVAR = 10ms
RTO = 100 + 4×10 = 140ms
```

### Fast Retransmit:

```
Якщо отримано 3 duplicate ACKs → негайно retransmit

Не чекаємо RTO timeout!

Приклад:
ACK=1100 (перший раз - нормально)
ACK=1100 (duplicate #1)
ACK=1100 (duplicate #2)
ACK=1100 (duplicate #3) ← Fast Retransmit SEQ=1100!

Це швидше, ніж чекати timeout
```

### Selective Acknowledgment (SACK):

```
Без SACK (стандартний ACK):
- ACK=1100 означає: "Отримав все до 1099"
- Якщо втрачено 1100-1199, але отримано 1200-1299, 1300-1399
- ACK все одно =1100
- Відправник retransmit all: 1100-1199, 1200-1299, 1300-1399

З SACK:
- ACK=1100, SACK=(1200-1399)
- Відправник retransmit тільки 1100-1199!

Приклад SACK:
ACK=1100, SACK blocks:
  - 1200-1299 (отримано)
  - 1400-1499 (отримано)

Відправник retransmit тільки:
  - 1100-1199 (не отримано)
  - 1300-1399 (не отримано)
```

---

## Контроль потоку (Flow Control)

**Flow Control** запобігає переповненню receive buffer отримувача.

### Sliding Window:

```
Sender                                    Receiver
  │                                         │
  │                                         │ Receive Buffer: 8KB
  │                                         │ Window Size: 8192
  │                                         │
  │←──── ACK=1000, Window=8192 ─────────────│
  │                                         │
  │     Можу відправити 8192 байти          │
  │                                         │
  │─── SEQ=1000, Data=4096 ─────────────────→│
  │                                         │
  │                                         │ Buffer: 4096/8192
  │                                         │
  │←──── ACK=5096, Window=4096 ─────────────│
  │                                         │
  │     Тепер можу відправити ще 4096       │
  │                                         │
  │─── SEQ=5096, Data=4096 ─────────────────→│
  │                                         │
  │                                         │ Buffer: 8192/8192 (FULL!)
  │                                         │
  │←──── ACK=9192, Window=0 ────────────────│
  │                                         │
  │     Window=0! Не можу відправляти       │
  │                                         │
  │       ... додаток читає дані ...        │
  │                                         │
  │←──── ACK=9192, Window=4096 ─────────────│
  │                                         │
  │     Тепер можу відправити 4096 байт     │
  │                                         │
```

### Window Scale Option:

```
Проблема: Window Size = 16 біт = максимум 65535 байт

Для високошвидкісних мереж це замало!

Рішення: Window Scale option

Window Scale Factor: 0-14 (множник 2^0 до 2^14)

Приклад:
Window Size (в пакеті) = 65535
Window Scale = 7
Реальний Window = 65535 × 2^7 = 65535 × 128 = 8 388 480 байт ≈ 8 MB

Максимум:
Window = 65535 × 2^14 = 1 073 725 440 байт ≈ 1 GB!
```

### Zero Window Probe:

```
Якщо Window=0, відправник періодично відправляє
Zero Window Probe (1 байт даних)

Це дозволяє виявити, коли отримувач знову готовий приймати дані

Sender                                    Receiver
  │                                         │
  │←──── Window=0 ──────────────────────────│
  │                                         │
  │     ... чекаємо ...                     │
  │                                         │
  │─── Zero Window Probe (1 byte) ─────────→│
  │                                         │
  │←──── Window=0 ──────────────────────────│
  │                                         │
  │     ... чекаємо ...                     │
  │                                         │
  │─── Zero Window Probe (1 byte) ─────────→│
  │                                         │
  │←──── Window=4096 ───────────────────────│
  │                                         │
  │     Можу відправляти!                   │
  │                                         │
```

---

## Контроль перевантаження (Congestion Control)

**Congestion Control** запобігає перевантаженню мережі.

### Congestion Window (cwnd):

```
Sender має два обмеження:

1. Receiver Window (rwnd) - від отримувача
2. Congestion Window (cwnd) - від відправника

Effective Window = min(rwnd, cwnd)

rwnd - контролює отримувач (flow control)
cwnd - контролює відправник (congestion control)
```

### Congestion Control алгоритми:

#### 1. Slow Start:

```
Початок з'єднання або після timeout

cwnd починається з малого значення (зазвичай 1-10 MSS)
Кожен ACK збільшує cwnd на 1 MSS

Приклад (MSS = 1460 bytes):

RTT 1: cwnd = 1 MSS = 1460 bytes
       Відправлено: 1 segment
       Отримано: 1 ACK

RTT 2: cwnd = 2 MSS = 2920 bytes
       Відправлено: 2 segments
       Отримано: 2 ACKs

RTT 3: cwnd = 4 MSS = 5840 bytes
       Відправлено: 4 segments
       Отримано: 4 ACKs

RTT 4: cwnd = 8 MSS = 11680 bytes

cwnd зростає експоненційно: 1 → 2 → 4 → 8 → 16 → 32 → ...
```

**Slow Start Threshold (ssthresh):**

```
Коли cwnd досягає ssthresh, переходимо до Congestion Avoidance

┌─────────────────────────────────────────────────────────┐
│                                                         │
│        ┌──── Slow Start (exponential)                  │
│       /                                                 │
│      /                                                  │
│     /                                                   │
│    /                                                    │
│   /                                                     │
│  /                                                      │
│ /                                                       │
│/                                                        │
│                 ssthresh ───────────────────────────────│
│                          ┌──── Congestion Avoidance    │
│                         /        (linear)              │
│                        /                                │
│                       /                                 │
│                      /                                  │
│                     /                                   │
└─────────────────────────────────────────────────────────┘
       Time (RTT) →
```

#### 2. Congestion Avoidance:

```
Після досягнення ssthresh

cwnd зростає повільніше (лінійно)
Кожен RTT збільшує cwnd на 1 MSS

Приклад:
cwnd = 16 MSS
Відправлено 16 segments в одному RTT
Отримано 16 ACKs
cwnd = 17 MSS (зросло тільки на 1!)

Формула: cwnd += MSS / cwnd (для кожного ACK)
```

#### 3. Fast Recovery:

```
Після Fast Retransmit (3 duplicate ACKs)

1. ssthresh = cwnd / 2
2. cwnd = ssthresh + 3 × MSS
3. Для кожного додаткового duplicate ACK: cwnd += 1 MSS
4. Після нового ACK: cwnd = ssthresh

Приклад:
cwnd = 20 MSS
Втрата пакета → 3 duplicate ACKs

ssthresh = 20 / 2 = 10 MSS
cwnd = 10 + 3 = 13 MSS

Ще 2 duplicate ACKs:
cwnd = 13 + 2 = 15 MSS

Новий ACK (recovery complete):
cwnd = ssthresh = 10 MSS

Переходимо до Congestion Avoidance
```

#### 4. Timeout (Tahoe behavior):

```
Якщо RTO timeout спрацював:

1. ssthresh = cwnd / 2
2. cwnd = 1 MSS
3. Перезапускаємо Slow Start

Це жорсткіша реакція, ніж Fast Recovery
```

### TCP Congestion Control алгоритми:

#### TCP Tahoe (1988):

```
- Slow Start
- Congestion Avoidance
- Fast Retransmit
- При втраті: cwnd = 1 (Slow Start restart)

Занадто агресивне зменшення cwnd
```

#### TCP Reno (1990):

```
- Slow Start
- Congestion Avoidance
- Fast Retransmit
- Fast Recovery

При 3 duplicate ACKs:
  cwnd = cwnd / 2 (Fast Recovery)

При timeout:
  cwnd = 1 (Slow Start restart)

Стандарт довгий час
```

#### TCP NewReno (1999):

```
Покращення Reno для множинних втрат в одному window

Може відновитися від множинних втрат без timeout
```

#### TCP CUBIC (2008, Linux default):

```
Сучасний алгоритм (за замовчуванням в Linux)

cwnd зростає як кубічна функція часу

Переваги:
✅ Швидше використовує bandwidth після recovery
✅ Краща продуктивність на високошвидкісних мережах
✅ Справедливіший (RTT-fairness)

Формула:
W(t) = C × (t - K)³ + W_max

де:
C = константа масштабування
K = час до досягнення W_max
W_max = window size перед втратою
```

#### TCP BBR (2016, Google):

```
Bottleneck Bandwidth and Round-trip propagation time

Не базується на втратах пакетів!
Базується на bandwidth та RTT

Переваги:
✅ Не потребує втрат для зниження rate
✅ Краща продуктивність на втратних мережах
✅ Менша затримка
✅ Використовується Google, YouTube

Режими роботи:
1. Startup - швидке зростання
2. Drain - зниження queue
3. ProbeBW - пошук bandwidth
4. ProbeRTT - мінімізація RTT
```

### Explicit Congestion Notification (ECN):

```
Маршрутизатори можуть позначати пакети замість їх відкидання

IP Header: ECN поле (2 біти)
TCP Header: ECE і CWR флаги

Без ECN:
Router → Drop packet → 3 duplicate ACKs → Fast Retransmit

З ECN:
Router → Mark packet (ECN) → Receiver відправляє ECE flag
→ Sender зменшує cwnd БЕЗ втрати пакета!

Переваги:
✅ Немає втрат пакетів
✅ Менша затримка
✅ Краща продуктивність

Підтримка:
- Linux: підтримується
- Windows: підтримується
- Маршрутизатори: не всі підтримують
```

---

## TCP опції

TCP Options розміщуються після основного заголовка (20 байт).

### Формат опцій:

```
1 байт: Kind (тип опції)
1 байт: Length (довжина опції)
N байт: Data

Приклади:
┌──────┬────────┬──────────────────────────────┐
│ Kind │ Length │ Data                         │
├──────┼────────┼──────────────────────────────┤
│  0   │   -    │ End of Option List           │
│  1   │   -    │ No-Operation (padding)       │
│  2   │   4    │ MSS (2 bytes)                │
│  3   │   3    │ Window Scale (1 byte)        │
│  4   │   2    │ SACK Permitted               │
│  5   │  var   │ SACK (blocks)                │
│  8   │  10    │ Timestamps (8 bytes)         │
└──────┴────────┴──────────────────────────────┘
```

### 1. MSS (Maximum Segment Size):

```
Kind = 2, Length = 4

Максимальний розмір даних в TCP сегменті (без заголовків)

Використовується тільки під час handshake (SYN пакети)

Приклад:
Ethernet MTU = 1500 байт
- IP Header = 20 байт
- TCP Header = 20 байт
MSS = 1500 - 20 - 20 = 1460 байт

IPv6:
MTU = 1500
- IPv6 Header = 40 байт
- TCP Header = 20 байт
MSS = 1500 - 40 - 20 = 1440 байт

Якщо не вказано, за замовчуванням MSS = 536 байт
```

### 2. Window Scale:

```
Kind = 3, Length = 3

Множник для Window Size поля

Використовується тільки під час handshake

Приклад:
Window Scale = 7
Window Size (в пакеті) = 1000
Реальний Window = 1000 × 2^7 = 128000 байт

Важливо: обидві сторони повинні підтримувати
```

### 3. SACK Permitted:

```
Kind = 4, Length = 2

Вказує, що сторона підтримує Selective Acknowledgment

Використовується під час handshake

Якщо обидві сторони відправили SACK Permitted,
можна використовувати SACK в подальших пакетах
```

### 4. SACK (Selective Acknowledgment):

```
Kind = 5, Length = variable

Вказує діапазони отриманих байтів

Приклад:
ACK = 1000
SACK blocks:
  - 2000-2999  (отримано)
  - 4000-4999  (отримано)

Означає:
- 1000-1999: НЕ отримано (retransmit)
- 2000-2999: отримано
- 3000-3999: НЕ отримано (retransmit)
- 4000-4999: отримано

Формат:
┌───────────────────────────────────────┐
│ Kind=5 │ Length │ Left Edge │ Right Edge │
├───────────────────────────────────────┤
│   5    │   10   │   2000    │   3000     │
│               │   4000    │   5000     │
└───────────────────────────────────────┘
```

### 5. Timestamps:

```
Kind = 8, Length = 10

Два значення по 4 байти:
- TSval (Timestamp Value)
- TSecr (Timestamp Echo Reply)

Використання:

1. RTT вимірювання
   Sender: TSval = current_time
   Receiver: TSecr = TSval (echo back)
   RTT = current_time - TSecr

2. PAWS (Protection Against Wrapped Sequence numbers)
   Sequence numbers - 32 біти, можуть обнулитися (wrap around)
   Timestamps допомагають відрізнити старі пакети від нових

Приклад:
Sender → TSval=12345678, TSecr=0
Receiver → TSval=87654321, TSecr=12345678

Sender обчислює RTT = current_time - 12345678
```

### 6. TCP Fast Open (TFO):

```
Kind = 34, Length = variable

Дозволяє відправляти дані в SYN пакеті!

Без TFO:
RTT 1: SYN
RTT 2: SYN-ACK
RTT 3: ACK + Data ← Дані тільки тут

З TFO:
RTT 1: SYN + Data ← Дані відразу!
RTT 2: SYN-ACK + Data response

Економія: 1 RTT

Використання:
Client → SYN + TFO Cookie + Data
Server → SYN-ACK + Response Data

TFO Cookie - криптографічний token від сервера
Запобігає SYN flood attacks
```

---

## TCP States

TCP з'єднання проходить через різні стани.

### TCP State Diagram:

```
                              +---------+
                              |  CLOSED |
                              +---------+
                                   |
                         (passive) | (active)
                           LISTEN  |  SYN_SENT
                                   |
                              +---------+
               +------------->|  LISTEN |
               |              +---------+
               |                   |
               |         rcv SYN   |   snd SYN
               |       snd SYN,ACK |
               |                   |
               |              +----v------+
               |              | SYN_RCVD  |
               |              +-----------+
               |                   | rcv ACK
               |                   |
          +----v------+       +----v------+
          | SYN_SENT  |       |ESTABLISHED|<---+
          +-----------+       +-----------+    |
                |                   |          |
          rcv SYN,ACK|       (close)|          |
          snd ACK    |       snd FIN|          | transfer data
                |                   |          |
                +----->ESTABLISHED  |          |
                             +------v-----+    |
                             | FIN_WAIT_1 |----+
                             +------------+
                                   |
                            rcv FIN|    rcv ACK
                            snd ACK|
                                   |
                         +---------v---+ +------------+
                         | FIN_WAIT_2  | | CLOSING    |
                         +-------------+ +------------+
                                   |          |
                            rcv FIN|    rcv ACK
                            snd ACK|
                                   |          |
                            +------v----------v---+
                            |    TIME_WAIT        |
                            +---------------------+
                                   |
                            (timeout)|
                                   |
                              +----v----+
                              | CLOSED  |
                              +---------+
```

### Опис станів:

```
CLOSED
  Початковий стан, з'єднання не існує

LISTEN (Server)
  Сервер чекає на вхідні з'єднання

SYN-SENT (Client)
  Клієнт відправив SYN, чекає на SYN-ACK

SYN-RECEIVED (Server)
  Сервер отримав SYN, відправив SYN-ACK, чекає на ACK

ESTABLISHED
  З'єднання встановлено, можна передавати дані
  Це нормальний робочий стан

FIN-WAIT-1 (Active Close)
  Відправив FIN, чекає на ACK

FIN-WAIT-2 (Active Close)
  Отримав ACK на FIN, чекає на FIN від іншої сторони

CLOSE-WAIT (Passive Close)
  Отримав FIN, відправив ACK, чекаємо поки додаток закриє сокет

CLOSING (Simultaneous Close)
  Обидві сторони одночасно відправили FIN

LAST-ACK (Passive Close)
  Відправив FIN, чекає на фінальний ACK

TIME-WAIT (Active Close)
  Чекаємо 2×MSL (60-120 секунд) перед остаточним закриттям
  Це гарантує, що:
  - Фінальний ACK дійшов
  - Всі старі пакети з мережі зникли
```

### Перегляд TCP з'єднань:

```bash
# Linux / macOS
netstat -tan

# Приклад виводу:
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN
tcp        0      0 192.168.1.100:54321     93.184.216.34:80        ESTABLISHED
tcp        0      0 192.168.1.100:54322     93.184.216.34:443       TIME_WAIT

# Тільки ESTABLISHED
netstat -tan | grep ESTABLISHED

# ss (сучасна альтернатива netstat)
ss -tan

# Детальна інформація
ss -tan -o  # показує timers

# Приклад:
State      Recv-Q Send-Q Local:Port  Peer:Port
ESTAB      0      0      10.0.0.1:80  10.0.0.2:12345  timer:(keepalive,19min,0)
TIME-WAIT  0      0      10.0.0.1:80  10.0.0.2:12346  timer:(timewait,58sec,0)
```

---

## Проблеми та оптимізація TCP

### 1. Head-of-Line Blocking:

```
Проблема:
TCP гарантує порядок байтів
Якщо один пакет втрачено, всі наступні чекають

┌─────────────────────────────────────────────────────────┐
│  Packet 1 │ Packet 2 │ Packet 3 │ Packet 4 │ Packet 5 │
│     ✅    │    ❌    │    ✅    │    ✅    │    ✅    │
│                                                         │
│  Додаток не може отримати Packets 3-5,                 │
│  поки не отримає Packet 2!                             │
└─────────────────────────────────────────────────────────┘

Рішення:
- HTTP/2: multiplexing (але все ще є HOL blocking на TCP рівні)
- HTTP/3: QUIC (UDP-based, незалежні streams)
```

### 2. Slow Start на коротких з'єднаннях:

```
Проблема:
HTTP/1.1: кожен request = нове з'єднання
Кожне з'єднання починається з Slow Start

┌────────────────────────────────────────────────┐
│ Time to download 1 image (100KB):             │
│                                                │
│ 1. TCP handshake       50ms (1 RTT)           │
│ 2. TLS handshake       100ms (2 RTT)          │
│ 3. HTTP request/resp   50ms (1 RTT)           │
│ 4. Slow Start overhead 100ms                  │
│ Total: 300ms                                   │
│                                                │
│ 10 images = 3000ms = 3 seconds!               │
└────────────────────────────────────────────────┘

Рішення:
- HTTP/1.1 Keep-Alive (reuse connection)
- HTTP/2 multiplexing (one connection for everything)
- TCP Fast Open (data in SYN)
```

### 3. Bufferbloat:

```
Проблема:
Великі buffers в маршрутизаторах → велика затримка

Без перевантаження:
RTT = 20ms

З перевантаженням (великі buffers):
RTT = 200ms (buffer delay) + 20ms (propagation) = 220ms!

Symptoms:
- Високий RTT під навантаженням
- Погана інтерактивність (gaming, VoIP)
- Normal bandwidth, але повільні відповіді

Рішення:
- ECN (Explicit Congestion Notification)
- AQM (Active Queue Management): CoDel, fq_codel, PIE
- TCP BBR (не заповнює buffers)
```

### 4. TCP Incast:

```
Проблема:
Багато серверів одночасно відправляють дані одному клієнту

Приклад (Data Center):
100 серверів → 1 client
Кожен відправляє 1MB одночасно

Результат:
- Switch buffer overflow
- Масові втрати пакетів
- Синхронізовані timeouts
- Колапс throughput

Рішення:
- Smaller RTO min (datacenter: 1ms замість 1000ms)
- ECN
- Larger switch buffers
- Jitter в відповідях серверів
```

### 5. TCP Window Size обмеження:

```
Bandwidth-Delay Product (BDP):

BDP = Bandwidth × RTT

Приклад:
Bandwidth = 1 Gbps = 125 MB/s
RTT = 100ms = 0.1s
BDP = 125 MB/s × 0.1s = 12.5 MB

TCP Window потрібен мінімум 12.5 MB для повного використання!

Без Window Scale:
Max Window = 64 KB
Max Throughput = 64 KB / 0.1s = 640 KB/s = 5 Mbps

Тільки 5 Mbps з 1 Gbps link! 0.5% використання!

З Window Scale:
Window = 12.5 MB
Max Throughput ≈ 1 Gbps ✅
```

### Оптимізації TCP:

#### Linux sysctl параметри:

```bash
# /etc/sysctl.conf

# TCP Timestamps (для RTT measurement)
net.ipv4.tcp_timestamps = 1

# TCP Window Scale
net.ipv4.tcp_window_scaling = 1

# SACK
net.ipv4.tcp_sack = 1

# TCP Fast Open
net.ipv4.tcp_fastopen = 3  # 1=client, 2=server, 3=both

# Congestion Control
net.ipv4.tcp_congestion_control = bbr  # або cubic

# TCP buffers (auto-tuning)
net.ipv4.tcp_rmem = 4096 87380 6291456  # min default max (read)
net.ipv4.tcp_wmem = 4096 65536 4194304  # min default max (write)

# TCP KeepAlive
net.ipv4.tcp_keepalive_time = 600      # 10 minutes
net.ipv4.tcp_keepalive_intvl = 60      # 60 seconds
net.ipv4.tcp_keepalive_probes = 3      # 3 probes

# SYN cookies (захист від SYN flood)
net.ipv4.tcp_syncookies = 1

# Reuse TIME-WAIT sockets швидше
net.ipv4.tcp_tw_reuse = 1

# Зменшити кількість TIME-WAIT sockets
net.ipv4.tcp_fin_timeout = 30

# Збільшити SYN backlog
net.ipv4.tcp_max_syn_backlog = 8192

# ECN
net.ipv4.tcp_ecn = 1

# Застосувати
sudo sysctl -p
```

---

## TCP vs UDP

### Порівняльна таблиця:

| Характеристика | TCP | UDP |
|----------------|-----|-----|
| **Connection** | Connection-oriented | Connectionless |
| **Надійність** | ✅ Guaranteed delivery | ❌ Best-effort |
| **Порядок** | ✅ Ordered | ❌ Unordered |
| **Overhead** | Високий (20+ байт header) | Низький (8 байт header) |
| **Швидкість** | Повільніший | Швидший |
| **Flow Control** | ✅ Так | ❌ Ні |
| **Congestion Control** | ✅ Так | ❌ Ні |
| **Retransmission** | ✅ Автоматично | ❌ Немає |
| **Checksums** | ✅ Обов'язково | ⚠️ Опціонально |
| **Використання** | Web, Email, FTP, SSH | Video, Gaming, DNS, VoIP |

### Коли використовувати TCP:

```
✅ Потрібна надійна доставка
   - Файли, документи
   - Email
   - Веб-сторінки

✅ Порядок даних критичний
   - Text-based протоколи
   - Transactions

✅ Немає обмежень за часом
   - Background downloads
   - Batch processing

Приклади: HTTP, HTTPS, FTP, SMTP, SSH, Telnet
```

### Коли використовувати UDP:

```
✅ Швидкість важливіша за надійність
   - Real-time video/audio streaming
   - Gaming
   - VoIP

✅ Втрата пакетів прийнятна
   - Live broadcasts
   - Sensor data

✅ Малі повідомлення
   - DNS queries
   - DHCP
   - NTP

✅ Multicast/Broadcast
   - Discovery protocols
   - Streaming до множинних клієнтів

Приклади: DNS, DHCP, NTP, SNMP, RTP, QUIC (HTTP/3)
```

### UDP заголовок:

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|            Length             |           Checksum            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                             Data                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

Всього 8 байт! (TCP мінімум 20 байт)
```

---

## Практичні інструменти

### 1. netstat:

```bash
# Всі TCP з'єднання
netstat -tan

# Listening ports
netstat -tln

# З PID процесів
netstat -tlnp

# Continuous monitoring
watch -n 1 "netstat -tan | grep ESTABLISHED | wc -l"

# Статистика TCP
netstat -s -t
```

### 2. ss (Socket Statistics):

```bash
# Швидша альтернатива netstat

# Всі TCP
ss -tan

# ESTABLISHED
ss -tan state established

# Listening
ss -tln

# З process info
ss -tlnp

# Детальна інформація
ss -tani

# Показує:
# - TCP Options (SACK, Window Scale, Timestamps)
# - cwnd, ssthresh
# - RTT, RTO
# - Retransmits

# Приклад:
ss -tani | grep -A 10 "192.168.1.100"
```

### 3. tcpdump:

```bash
# Capture TCP traffic
sudo tcpdump -i eth0 tcp

# Конкретний порт
sudo tcpdump -i eth0 tcp port 80

# Зберегти в файл
sudo tcpdump -i eth0 tcp -w capture.pcap

# Показати тільки SYN пакети
sudo tcpdump -i eth0 'tcp[tcpflags] & tcp-syn != 0'

# Показати тільки FIN пакети
sudo tcpdump -i eth0 'tcp[tcpflags] & tcp-fin != 0'

# Детальний вивід
sudo tcpdump -i eth0 -vvv tcp port 80

# Показати payload
sudo tcpdump -i eth0 -A tcp port 80
```

### 4. Wireshark:

```
GUI інструмент для аналізу пакетів

Filters:
- tcp.port == 80
- tcp.flags.syn == 1
- tcp.flags.fin == 1
- tcp.analysis.retransmission
- tcp.analysis.duplicate_ack

TCP Stream Analysis:
Right-click → Follow → TCP Stream

Statistics:
Statistics → TCP Stream Graphs → Time-Sequence Graph

Показує:
- Sequence numbers
- ACKs
- Retransmissions
- Window size
- RTT
```

### 5. iperf3:

```bash
# Тестування TCP throughput

# Сервер
iperf3 -s

# Клієнт
iperf3 -c server.example.com

# З детальним виводом
iperf3 -c server.example.com -i 1 -t 60

# Множинні паралельні streams
iperf3 -c server.example.com -P 4

# Reverse (server → client)
iperf3 -c server.example.com -R

# З congestion control
iperf3 -c server.example.com -C cubic
iperf3 -c server.example.com -C bbr

# Вивід:
[  5]   0.00-10.00  sec  1.10 GBytes   941 Mbits/sec
[  5]   Retr: 123
[  5]   cwnd: 1234 KB
```

### 6. ncat (nc):

```bash
# TCP server
nc -l -p 8080

# TCP client
nc example.com 80
GET / HTTP/1.1
Host: example.com

# Transfer file через TCP
# Receiver
nc -l -p 8080 > received_file.txt

# Sender
nc receiver.example.com 8080 < file.txt
```

### 7. traceroute with TCP:

```bash
# Traceroute з TCP SYN
sudo traceroute -T -p 80 example.com

# Показує маршрут TCP пакетів
```

### 8. sysctl (перегляд параметрів):

```bash
# Всі TCP параметри
sysctl -a | grep tcp

# Congestion control
sysctl net.ipv4.tcp_congestion_control

# Доступні congestion control алгоритми
sysctl net.ipv4.tcp_available_congestion_control

# Window scaling
sysctl net.ipv4.tcp_window_scaling

# SACK
sysctl net.ipv4.tcp_sack
```

### 9. ip route:

```bash
# MTU для маршруту
ip route get example.com

# Показує MTU link
```

### 10. tcptrack:

```bash
# Real-time TCP connection monitoring
sudo tcptrack -i eth0

# Показує:
# - Source/Destination
# - State
# - Idle time
# - Bandwidth usage
```

---

## Висновок

TCP - надійний протокол транспортного рівня з багатою історією та складними механізмами.

### Ключові характеристики:

```
✅ Надійна доставка (retransmissions)
✅ Упорядкованість (sequence numbers)
✅ Перевірка помилок (checksums)
✅ Контроль потоку (sliding window)
✅ Контроль перевантаження (congestion control)
✅ Full-duplex communication
✅ Connection-oriented
```

### Сучасний TCP стек (2024):

```
✅ Congestion Control: BBR або CUBIC
✅ TCP Fast Open (TFO)
✅ TCP SACK
✅ TCP Timestamps
✅ Window Scaling
✅ ECN (Explicit Congestion Notification)
✅ Proper buffer tuning
```

### Ресурси для вивчення:

- **RFC 793** - TCP Specification
- **RFC 2581** - TCP Congestion Control
- **RFC 7323** - TCP Extensions for High Performance
- **RFC 8312** - CUBIC Congestion Control
- **TCP/IP Illustrated** (книга Stevens)
- **High Performance Browser Networking** (книга Ilya Grigorik)

**Успіхів у розумінні TCP!** 📡

---

**Кінець посібника TCP Protocol**
