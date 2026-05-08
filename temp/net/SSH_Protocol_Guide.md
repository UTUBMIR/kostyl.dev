# SSH Protocol - Повний посібник

**SSH (Secure Shell)** - криптографічний мережевий протокол для безпечного віддаленого доступу до комп'ютерів та виконання команд через незахищену мережу.

---

## Зміст

1. [Вступ до SSH](#вступ-до-ssh)
2. [Історія та еволюція](#історія-та-еволюція)
3. [Навіщо потрібен SSH](#навіщо-потрібен-ssh)
4. [Архітектура SSH](#архітектура-ssh)
5. [Криптографія в SSH](#криптографія-в-ssh)
6. [SSH аутентифікація](#ssh-аутентифікація)
7. [SSH Connection Protocol](#ssh-connection-protocol)
8. [SSH тунелювання та Port Forwarding](#ssh-тунелювання-та-port-forwarding)
9. [Конфігурація клієнта та сервера](#конфігурація-клієнта-та-сервера)
10. [Безпека SSH](#безпека-ssh)
11. [Практичні приклади](#практичні-приклади)
12. [Найкращі практики](#найкращі-практики)

---

## Вступ до SSH

### Що таке SSH?

**SSH (Secure Shell)** — це протокол прикладного рівня, який забезпечує:

```
┌─────────────────────────────────────────┐
│         SSH - Три основні цілі          │
├─────────────────────────────────────────┤
│                                         │
│  1. Конфіденційність (Confidentiality) │
│     └─ Шифрування всього трафіку        │
│                                         │
│  2. Цілісність (Integrity)              │
│     └─ Захист від підміни даних         │
│                                         │
│  3. Аутентифікація (Authentication)     │
│     └─ Перевірка клієнта та сервера     │
│                                         │
└─────────────────────────────────────────┘
```

### Основні можливості SSH:

#### 1. Віддалене виконання команд

```bash
# Підключення до віддаленого сервера
ssh user@example.com

# Виконання команди без інтерактивної сесії
ssh user@example.com "ls -la /var/www"

# Виконання команди з sudo
ssh user@example.com "sudo systemctl restart nginx"
```

#### 2. Безпечне копіювання файлів

```bash
# SCP (Secure Copy)
scp file.txt user@example.com:/home/user/

# SFTP (SSH File Transfer Protocol)
sftp user@example.com
```

#### 3. Тунелювання (Port Forwarding)

```bash
# Local port forwarding
ssh -L 8080:localhost:80 user@example.com

# Remote port forwarding
ssh -R 8080:localhost:80 user@example.com

# Dynamic port forwarding (SOCKS proxy)
ssh -D 1080 user@example.com
```

#### 4. X11 Forwarding

```bash
# Запуск GUI додатків віддалено
ssh -X user@example.com
firefox  # Відкриється на локальному екрані
```

---

## Історія та еволюція

### Хронологія розвитку SSH:

```
1995 ┌──────────────────────────────────────────┐
     │  SSH-1 (Tatu Ylönen, Фінляндія)          │
     │  - Заміна Telnet, rlogin, rsh            │
     │  - Перша публічна версія                  │
     └──────────────────────────────────────────┘
       ↓
1996 ┌──────────────────────────────────────────┐
     │  SSH-1.5 (покращення)                    │
     │  - Усунення вразливостей                 │
     └──────────────────────────────────────────┘
       ↓
1997 ┌──────────────────────────────────────────┐
     │  SSH Communications Security Corp        │
     │  - Комерціалізація SSH                   │
     └──────────────────────────────────────────┘
       ↓
1999 ┌──────────────────────────────────────────┐
     │  OpenSSH (OpenBSD)                       │
     │  - Безкоштовна open-source реалізація    │
     │  - Найпопулярніша реалізація             │
     └──────────────────────────────────────────┘
       ↓
2006 ┌──────────────────────────────────────────┐
     │  SSH-2 (RFC 4251-4254)                   │
     │  - Несумісний з SSH-1                    │
     │  - Покращена безпека                     │
     │  - Більше можливостей                    │
     │  - Стандарт з 2006 року                  │
     └──────────────────────────────────────────┘
       ↓
2020+ ┌─────────────────────────────────────────┐
      │  Сучасний SSH                           │
      │  - Нові алгоритми шифрування            │
      │  - Ed25519 ключі                        │
      │  - Certificates authentication          │
      │  - FIDO2/U2F підтримка                  │
      └─────────────────────────────────────────┘
```

### Порівняння SSH-1 vs SSH-2:

| Характеристика | SSH-1 | SSH-2 |
|----------------|-------|-------|
| **Безпека** | Вразливості (MITM, CRC-32) | Значно безпечніший |
| **Алгоритми шифрування** | Обмежені | Множина сучасних алгоритмів |
| **Key exchange** | Слабкий | Diffie-Hellman, ECDH |
| **Модульність** | Монолітний | Модульна архітектура |
| **SFTP** | Ні | Так |
| **Port forwarding** | Базовий | Розширений |
| **Сумісність** | - | Не сумісний з SSH-1 |
| **Статус** | ❌ Застарілий, вразливий | ✅ Сучасний стандарт |

**Висновок:** SSH-1 **НІКОЛИ** не повинен використовуватися. Тільки SSH-2!

---

## Навіщо потрібен SSH

### Проблеми незахищених протоколів:

#### До SSH використовувалися:

**1. Telnet (порт 23)**
```
┌──────────┐                              ┌──────────┐
│  Client  │──── login: admin ───────────→│  Server  │
│          │──── password: secret123 ────→│          │
└──────────┘                              └──────────┘
           ❌ ВСЕ ВІДКРИТО!
           ❌ Хакер може перехопити паролі
           ❌ Man-in-the-middle атаки легкі
```

**2. rsh/rlogin (Remote Shell)**
```
❌ Автентифікація по IP (легко підробити)
❌ Без шифрування
❌ .rhosts файли - дірка в безпеці
```

**3. FTP (File Transfer Protocol)**
```
❌ Логіни та паролі відкрито
❌ Дані передаються без шифрування
❌ Вразливий до перехоплення
```

### SSH вирішує ці проблеми:

```
┌──────────┐                              ┌──────────┐
│  Client  │════ Зашифроване з'єднання ═══│  Server  │
│          │                              │          │
└──────────┘                              └──────────┘
     ✅ Шифрування всього трафіку (AES, ChaCha20)
     ✅ Аутентифікація сервера (host keys)
     ✅ Аутентифікація клієнта (пароль або ключ)
     ✅ Цілісність даних (HMAC)
     ✅ Perfect Forward Secrecy
```

### Переваги SSH:

| Переваги | Опис |
|----------|------|
| **Шифрування** | Весь трафік зашифрований (команди, паролі, файли) |
| **Сильна аутентифікація** | Public key, certificates, MFA |
| **Цілісність** | Виявлення підміни даних |
| **Стискання** | Опціональне стискання трафіку |
| **Тунелювання** | Port forwarding, VPN через SSH |
| **X11 Forwarding** | Віддалені GUI додатки |
| **Agent Forwarding** | Використання локальних ключів на віддалених серверах |
| **Multiplexing** | Множинні сесії через одне з'єднання |

---

## Архітектура SSH

SSH складається з **трьох основних протоколів**:

```
┌─────────────────────────────────────────────────────────┐
│                 SSH Architecture                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  SSH Connection Protocol (RFC 4254)               │ │
│  │  - Channels (сесії, port forwarding, X11)         │ │
│  │  - Interactive shell, commands                    │ │
│  │  - SFTP, SCP                                      │ │
│  └───────────────────────────────────────────────────┘ │
│                         ↓↑                              │
│  ┌───────────────────────────────────────────────────┐ │
│  │  SSH User Authentication Protocol (RFC 4252)      │ │
│  │  - Password authentication                        │ │
│  │  - Public key authentication                      │ │
│  │  - Keyboard-interactive                           │ │
│  │  - GSSAPI (Kerberos)                              │ │
│  └───────────────────────────────────────────────────┘ │
│                         ↓↑                              │
│  ┌───────────────────────────────────────────────────┐ │
│  │  SSH Transport Layer Protocol (RFC 4253)          │ │
│  │  - Key exchange (DH, ECDH)                        │ │
│  │  - Server authentication                          │ │
│  │  - Encryption (AES, ChaCha20)                     │ │
│  │  - MAC (HMAC)                                     │ │
│  │  - Compression                                    │ │
│  └───────────────────────────────────────────────────┘ │
│                         ↓↑                              │
│  ┌───────────────────────────────────────────────────┐ │
│  │              TCP (port 22)                        │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 1. Transport Layer Protocol

**Завдання:**
- Встановлення захищеного з'єднання
- Key exchange (обмін ключами)
- Аутентифікація сервера
- Шифрування та MAC

**Процес:**
```
1. TCP connection (порт 22)
2. Protocol version exchange
3. Algorithm negotiation
4. Key exchange (Diffie-Hellman / ECDH)
5. Service request (authentication)
```

### 2. User Authentication Protocol

**Завдання:**
- Аутентифікація користувача на сервері

**Методи:**
```
1. password       - Пароль (зашифрований)
2. publickey      - Public key authentication
3. keyboard-interactive - Інтерактивна (MFA, OTP)
4. gssapi-with-mic - Kerberos
5. hostbased      - Аутентифікація по хосту
```

### 3. Connection Protocol

**Завдання:**
- Мультиплексування (множинні канали)
- Interactive shell
- Command execution
- Port forwarding
- X11 forwarding
- SFTP

**Канали (Channels):**
```
SSH Connection
    ├─ Channel 0: Interactive shell
    ├─ Channel 1: Port forwarding (local → remote:3306)
    ├─ Channel 2: X11 forwarding
    └─ Channel 3: SFTP session
```

---

## Типи SSH з'єднань

### 1. Interactive Shell

```bash
# Стандартне підключення
ssh user@example.com

# З конкретним портом
ssh -p 2222 user@example.com

# Інтерактивна сесія з PTY (pseudo-terminal)
user@remote:~$ ls
user@remote:~$ cd /var/www
user@remote:/var/www$ vim index.html
```

### 2. Command Execution

```bash
# Виконання однієї команди
ssh user@example.com "uptime"

# Виконання множинних команд
ssh user@example.com "cd /var/www && ls -la"

# З stdin/stdout pipe
echo "SELECT * FROM users;" | ssh user@db.example.com "mysql -u root -p database"

# Backup через SSH
ssh user@example.com "tar czf - /var/www" > backup.tar.gz
```

### 3. File Transfer

**SCP (Secure Copy):**
```bash
# Копіювання на сервер
scp file.txt user@example.com:/home/user/

# Копіювання з сервера
scp user@example.com:/home/user/file.txt .

# Рекурсивне копіювання директорії
scp -r /local/dir user@example.com:/remote/dir

# З прогресом
scp -v file.txt user@example.com:/home/user/
```

**SFTP (SSH File Transfer Protocol):**
```bash
# Інтерактивна сесія
sftp user@example.com

sftp> ls
sftp> cd /var/www
sftp> get index.html
sftp> put local.txt
sftp> mget *.log
sftp> exit

# Batch mode
echo "get /remote/file.txt" | sftp user@example.com
```

### 4. Port Forwarding (Тунелювання)

**Local Port Forwarding:**
```bash
# Локальний порт 3306 → remote:3306 (MySQL)
ssh -L 3306:localhost:3306 user@db.example.com

# Тепер можна підключитись локально:
mysql -h 127.0.0.1 -P 3306 -u dbuser -p
```

**Remote Port Forwarding:**
```bash
# Remote:8080 → localhost:80
ssh -R 8080:localhost:80 user@example.com

# Тепер remote:8080 доступний ззовні
```

**Dynamic Port Forwarding (SOCKS proxy):**
```bash
# SOCKS5 proxy на локальному порту 1080
ssh -D 1080 user@example.com

# Налаштувати браузер: SOCKS5 proxy 127.0.0.1:1080
# Весь трафік браузера йде через SSH
```

### 5. X11 Forwarding

```bash
# Увімкнути X11 forwarding
ssh -X user@example.com

# Або з trusted forwarding
ssh -Y user@example.com

# Запустити GUI додаток
user@remote:~$ firefox
user@remote:~$ gedit file.txt
# Вікна відкриються на локальному екрані!
```

---

## Версії SSH та їх відмінності

### SSH-1 (1995-1996)

```
❌ ЗАСТАРІЛИЙ! НЕ ВИКОРИСТОВУВАТИ!

Вразливості:
- CRC-32 collision attacks
- Integer overflow
- MITM attacks
- Weak session key recovery

Статус: Заборонений з ~2010 року
```

### SSH-2 (2006 - сьогодні)

```
✅ Сучасний стандарт (RFC 4251-4254)

Переваги:
✅ Сильніші алгоритми (AES, ChaCha20)
✅ Diffie-Hellman / ECDH key exchange
✅ Модульна архітектура
✅ SFTP протокол
✅ Розширений port forwarding
✅ Multiple channels в одному з'єднанні
✅ Periodic key re-exchange
✅ Compression

Підтримувані алгоритми:
- Key Exchange: diffie-hellman-group14-sha256, ecdh-sha2-nistp256, curve25519-sha256
- Host Key: ssh-rsa, ecdsa-sha2-nistp256, ssh-ed25519
- Encryption: aes128-ctr, aes256-ctr, aes128-gcm@openssh.com, chacha20-poly1305@openssh.com
- MAC: hmac-sha2-256, hmac-sha2-512, hmac-sha2-256-etm@openssh.com
```

### Перевірка версії SSH:

```bash
# Версія SSH клієнта
ssh -V
# OpenSSH_9.0p1, OpenSSL 3.0.5

# Перевірка підтримуваних алгоритмів
ssh -Q cipher       # Алгоритми шифрування
ssh -Q mac          # MAC алгоритми
ssh -Q kex          # Key exchange алгоритми
ssh -Q key          # Host key алгоритми

# Підключення з verbose (показує алгоритми)
ssh -vv user@example.com 2>&1 | grep "kex:"
```

---

## Порти та транспорт

### Стандартний порт SSH:

```
SSH: TCP порт 22 (за замовчуванням)
```

**Зміна порту (безпека через obscurity):**
```bash
# На сервері (/etc/ssh/sshd_config)
Port 2222

# Підключення до нестандартного порту
ssh -p 2222 user@example.com
```

**Чому змінювати порт 22?**
```
✅ Зменшує кількість автоматичних атак (ботів)
✅ Знижує навантаження (логи спаму)
⚠️ Не захищає від цілеспрямованих атак
⚠️ Security through obscurity - НЕ є справжньою безпекою!
```

### TCP connection process:

```
┌─────────┐                                    ┌─────────┐
│ Client  │                                    │ Server  │
└────┬────┘                                    └────┬────┘
     │                                              │
     │──────── TCP SYN (порт 22) ──────────────────→│
     │                                              │
     │←──────── TCP SYN-ACK ───────────────────────│
     │                                              │
     │──────── TCP ACK ────────────────────────────→│
     │                                              │
     │═══════ TCP Connection встановлено ═══════════│
     │                                              │
     │──────── SSH Protocol Exchange ──────────────→│
     │         "SSH-2.0-OpenSSH_9.0"                │
     │                                              │
     │←──────── SSH Protocol Exchange ──────────────│
     │          "SSH-2.0-OpenSSH_8.9"               │
     │                                              │
```

---

## SSH vs інші протоколи

### Порівняльна таблиця:

| Протокол | Порт | Шифрування | Аутентифікація | Використання | Статус |
|----------|------|------------|----------------|--------------|--------|
| **SSH** | 22 | ✅ Так (AES, ChaCha20) | ✅ Strong (keys, certs) | Віддалений доступ, SFTP | ✅ Безпечний |
| **Telnet** | 23 | ❌ Ні | ❌ Weak (plaintext) | Віддалений доступ | ❌ Застарілий |
| **rlogin** | 513 | ❌ Ні | ❌ IP-based | Віддалений доступ | ❌ Застарілий |
| **rsh** | 514 | ❌ Ні | ❌ .rhosts | Remote shell | ❌ Застарілий |
| **FTP** | 21 | ❌ Ні | ❌ Plaintext | File transfer | ❌ Використовувати SFTP |
| **FTPS** | 990 | ✅ Так (TLS) | ✅ Strong | File transfer | ✅ Альтернатива SFTP |
| **SFTP** | 22 | ✅ Так (SSH) | ✅ Strong | File transfer | ✅ Рекомендується |
| **SCP** | 22 | ✅ Так (SSH) | ✅ Strong | File copy | ✅ Але SFTP краще |
| **RDP** | 3389 | ✅ Так (TLS) | ✅ Strong | Windows remote desktop | ✅ Для Windows |
| **VNC** | 5900+ | ⚠️ Опціонально | ⚠️ Weak | Remote desktop | ⚠️ Тунелювати через SSH |

### Міграція з застарілих протоколів:

```bash
# Замість Telnet → SSH
telnet example.com 23  ❌
ssh user@example.com   ✅

# Замість FTP → SFTP
ftp example.com        ❌
sftp user@example.com  ✅

# Замість rsh → SSH
rsh example.com ls     ❌
ssh user@example.com ls ✅

# VNC через SSH тунель
ssh -L 5901:localhost:5901 user@example.com ✅
vncviewer localhost:5901
```

---

## Криптографія в SSH

SSH використовує комбінацію **симетричної**, **асиметричної** криптографії та **хеш-функцій** для забезпечення безпеки.

```
┌─────────────────────────────────────────────────────────┐
│          Криптографічні компоненти SSH                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Асиметрична криптографія (Public Key)              │
│     └─ Key exchange (обмін ключами)                    │
│     └─ Аутентифікація сервера (host keys)              │
│     └─ Аутентифікація клієнта (user keys)              │
│                                                         │
│  2. Симетрична криптографія                            │
│     └─ Шифрування даних сесії (AES, ChaCha20)          │
│     └─ Швидке шифрування великих обсягів даних         │
│                                                         │
│  3. Хеш-функції (Hash functions)                       │
│     └─ MAC (Message Authentication Code)               │
│     └─ Key derivation                                  │
│     └─ Fingerprints                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Key Exchange (Обмін ключами)

**Key Exchange** — це процес, коли клієнт і сервер домовляються про спільний секретний ключ через незахищений канал.

### Алгоритми Key Exchange в SSH:

#### 1. Diffie-Hellman (DH)

**diffie-hellman-group14-sha256** (2048-bit MODP Group)

```
Клієнт                                    Сервер
  │                                         │
  │─── Обирає приватне число a ────────────│
  │                                         │─── Обирає приватне число b
  │                                         │
  │─── Обчислює A = g^a mod p ─────────────│
  │                                         │─── Обчислює B = g^b mod p
  │                                         │
  │──────── Відправляє A ──────────────────→│
  │                                         │
  │←─────── Отримує B ─────────────────────│
  │                                         │
  │─── Обчислює K = B^a mod p ─────────────│
  │                                         │─── Обчислює K = A^b mod p
  │                                         │
  └─────────── Спільний ключ K ────────────┘

K (session key) - НІКОЛИ не передається мережею!
```

**Параметри:**
- `g` (generator) - публічне значення (зазвичай 2 або 5)
- `p` (prime) - велике просте число (2048+ біт)
- `a, b` - приватні числа (секретні)
- `A, B` - публічні значення (передаються мережею)
- `K` - спільний секретний ключ

**Групи Diffie-Hellman:**
```bash
# Підтримувані групи (OpenSSH)
diffie-hellman-group1-sha1          # 1024-bit ❌ Слабкий
diffie-hellman-group14-sha1         # 2048-bit ⚠️  SHA-1 застарілий
diffie-hellman-group14-sha256       # 2048-bit ✅ Рекомендується
diffie-hellman-group16-sha512       # 4096-bit ✅ Сильніший
diffie-hellman-group18-sha512       # 8192-bit ✅ Найсильніший (повільний)
```

#### 2. Elliptic Curve Diffie-Hellman (ECDH)

**ecdh-sha2-nistp256, ecdh-sha2-nistp384, ecdh-sha2-nistp521**

```
Переваги ECDH над DH:
✅ Менший розмір ключів (256-bit ECDH ≈ 3072-bit DH)
✅ Швидше обчислення
✅ Менше bandwidth

Криві:
- nistp256 (P-256, secp256r1) - 128-bit security
- nistp384 (P-384, secp384r1) - 192-bit security
- nistp521 (P-521, secp521r1) - 256-bit security
```

#### 3. Curve25519 (сучасний стандарт)

**curve25519-sha256, curve25519-sha256@libssh.org**

```
✅ Найкращий вибір для SSH (2024)

Переваги:
✅ Швидкість (швидше за NIST curves)
✅ Безпека (immune to timing attacks)
✅ Простота реалізації (менше помилок)
✅ 128-bit security level
✅ Не патентований
✅ Не контролюється NSA (на відміну від NIST curves)

Використовується за замовчуванням у сучасному OpenSSH
```

### Порівняння Key Exchange алгоритмів:

| Алгоритм | Розмір ключа | Безпека | Швидкість | Рекомендація |
|----------|--------------|---------|-----------|--------------|
| `diffie-hellman-group1-sha1` | 1024-bit | ❌ Слабкий | Середня | ❌ Не використовувати |
| `diffie-hellman-group14-sha256` | 2048-bit | ✅ Добрий | Повільна | ✅ OK |
| `diffie-hellman-group16-sha512` | 4096-bit | ✅ Сильний | Дуже повільна | ✅ Висока безпека |
| `ecdh-sha2-nistp256` | 256-bit | ✅ Добрий | Швидка | ⚠️ NIST curve |
| `ecdh-sha2-nistp384` | 384-bit | ✅ Сильний | Швидка | ⚠️ NIST curve |
| `curve25519-sha256` | 256-bit | ✅ Відмінний | Дуже швидка | ✅ Найкращий вибір |

---

## Host Keys (Ключі сервера)

**Host Key** — це ключ сервера, який використовується для аутентифікації сервера клієнту.

### Типи Host Keys:

#### 1. RSA (ssh-rsa, rsa-sha2-256, rsa-sha2-512)

```bash
# Генерація RSA ключа
ssh-keygen -t rsa -b 4096 -f /etc/ssh/ssh_host_rsa_key -N ""

Розміри:
- 1024-bit ❌ СЛАБКИЙ, не використовувати
- 2048-bit ⚠️  Мінімум (за замовчуванням)
- 3072-bit ✅ Добре
- 4096-bit ✅ Рекомендується

Переваги:
✅ Підтримується всюди (сумісність)
✅ Перевірений часом

Недоліки:
❌ Великий розмір ключа (4096-bit)
❌ Повільніший
❌ rsa-sha2-256/512 замість застарілого ssh-rsa
```

#### 2. ECDSA (ecdsa-sha2-nistp256, ecdsa-sha2-nistp384, ecdsa-sha2-nistp521)

```bash
# Генерація ECDSA ключа
ssh-keygen -t ecdsa -b 256 -f /etc/ssh/ssh_host_ecdsa_key -N ""

Розміри:
- 256-bit (nistp256) - Стандарт
- 384-bit (nistp384) - Сильніший
- 521-bit (nistp521) - Найсильніший

Переваги:
✅ Менший розмір
✅ Швидше за RSA

Недоліки:
⚠️ NIST curves (підозри щодо NSA backdoor)
⚠️ Вразливий до weak RNG
```

#### 3. Ed25519 (ssh-ed25519) - НАЙКРАЩИЙ ВИБІР!

```bash
# Генерація Ed25519 ключа
ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key -N ""

Розмір: 256-bit (фіксований)

Переваги:
✅ Найбезпечніший (2024)
✅ Найшвидший
✅ Малий розмір ключа (68 байтів public key)
✅ Не контролюється NSA
✅ Immune to timing attacks
✅ Простий у реалізації

Недоліки:
⚠️ Старі клієнти можуть не підтримувати (OpenSSH 6.5+, 2014)

Fingerprint приклад:
256 SHA256:AAAAE2VjZHNhLXNoYTItbmlzdHAyNTY... (ED25519)
```

#### 4. DSA (ssh-dss) - ЗАСТАРІЛИЙ!

```bash
❌ НЕ ВИКОРИСТОВУВАТИ!

- Застарілий з 2015 року
- Вимкнено у OpenSSH 7.0+ за замовчуванням
- 1024-bit максимум (слабкий)
- Вразливий до weak RNG
```

### Порівняння Host Key типів:

| Тип | Розмір ключа | Fingerprint розмір | Безпека | Швидкість | Рекомендація |
|-----|--------------|--------------------|---------|-----------| ------------|
| **ssh-rsa** | 2048-4096 bit | 2048+ bit | ⚠️ OK з SHA-256 | Повільна | ⚠️ Сумісність |
| **ecdsa-sha2-nistp256** | 256 bit | 256 bit | ⚠️ Підозри NSA | Швидка | ⚠️ Якщо Ed25519 немає |
| **ssh-ed25519** | 256 bit | 256 bit | ✅ Найкращий | Найшвидша | ✅ Використовувати |
| **ssh-dss** | 1024 bit | 1024 bit | ❌ Слабкий | Середня | ❌ Застарілий |

### Перевірка Host Keys:

```bash
# Показати host keys сервера
ssh-keyscan example.com

# Показати fingerprint host key
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
# 256 SHA256:abc123... root@server (ED25519)

# Перевірка fingerprint при першому підключенні
ssh user@example.com
# The authenticity of host 'example.com (192.0.2.1)' can't be established.
# ED25519 key fingerprint is SHA256:abc123...
# Are you sure you want to continue connecting (yes/no)? yes

# Після підтвердження зберігається в ~/.ssh/known_hosts
```

### known_hosts файл:

```bash
# ~/.ssh/known_hosts
example.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAbc123...
192.0.2.1 ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbml...

# Формат:
# hostname algorithm public-key

# Хешовані hosts (для приватності)
|1|abc123...|def456... ssh-ed25519 AAAAC3NzaC1lZDI1NTE5...
```

**MITM Attack Warning:**
```bash
ssh user@example.com

# Якщо host key змінився:
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!

# ⚠️ НЕ ІГНОРУВАТИ! Можлива MITM атака!
# Можливі причини:
# 1. MITM атака ❌
# 2. Сервер переінстальовано (нові ключі) ✅
# 3. IP адресу перевикористано ✅

# Видалити старий ключ (ТІЛЬКИ якщо впевнені!)
ssh-keygen -R example.com
# або
ssh-keygen -R 192.0.2.1
```

---

## Симетричне шифрування (Session Encryption)

Після key exchange, SSH використовує **симетричне шифрування** для шифрування всієї сесії.

### Алгоритми шифрування:

#### 1. AES (Advanced Encryption Standard)

**aes128-ctr, aes192-ctr, aes256-ctr**

```
AES в CTR (Counter) режимі

Розміри ключів:
- AES-128: 128-bit ключ (16 байтів)
- AES-192: 192-bit ключ (24 байти)
- AES-256: 256-bit ключ (32 байти)

CTR режим:
✅ Паралелізація (швидше)
✅ Без padding
✅ Random access
✅ Не потребує feedback
```

**aes128-gcm@openssh.com, aes256-gcm@openssh.com**

```
AES в GCM (Galois/Counter Mode) режимі

✅ AEAD (Authenticated Encryption with Associated Data)
✅ Шифрування + MAC в одному
✅ Швидше (апаратне прискорення AES-NI)
✅ Краще за AES-CTR + HMAC

Рекомендується!
```

#### 2. ChaCha20-Poly1305

**chacha20-poly1305@openssh.com**

```
ChaCha20 (шифрування) + Poly1305 (MAC)

✅ Найкращий вибір для SSH (2024)

Переваги:
✅ Швидкий на пристроях без AES-NI
✅ AEAD (як AES-GCM)
✅ Immune to timing attacks
✅ Простіша реалізація
✅ Не патентований

Використання:
ssh -c chacha20-poly1305@openssh.com user@example.com
```

#### 3. 3DES (Triple DES) - ЗАСТАРІЛИЙ!

**3des-cbc**

```
❌ НЕ ВИКОРИСТОВУВАТИ!

- Застарілий з ~2010 року
- 64-bit blocks (Sweet32 attack)
- Повільний
- Вимкнено у сучасному OpenSSH за замовчуванням
```

#### 4. RC4 (Arcfour) - ЗАСТАРІЛИЙ!

```
❌ НЕ ВИКОРИСТОВУВАТИ!

- Критично вразливий (RC4 NOMORE attack)
- Заборонений з 2015
```

### Порівняння алгоритмів шифрування:

| Алгоритм | Розмір ключа | AEAD | Швидкість | Безпека | Рекомендація |
|----------|--------------|------|-----------|---------|--------------|
| `aes128-ctr` | 128-bit | ❌ | Швидкий (з AES-NI) | ✅ Добрий | ✅ OK |
| `aes256-ctr` | 256-bit | ❌ | Швидкий (з AES-NI) | ✅ Сильний | ✅ OK |
| `aes128-gcm@openssh.com` | 128-bit | ✅ | Дуже швидкий | ✅ Відмінний | ✅ Рекомендується |
| `aes256-gcm@openssh.com` | 256-bit | ✅ | Дуже швидкий | ✅ Відмінний | ✅ Рекомендується |
| `chacha20-poly1305@openssh.com` | 256-bit | ✅ | Швидкий (без AES-NI) | ✅ Відмінний | ✅ Найкращий вибір |
| `3des-cbc` | 168-bit | ❌ | Дуже повільний | ❌ Вразливий | ❌ Застарілий |
| `arcfour` (RC4) | 128-bit | ❌ | Швидкий | ❌ Зламаний | ❌ Заборонений |

**Рекомендація 2024:**
```bash
# Клієнт (~/.ssh/config)
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com

# Сервер (/etc/ssh/sshd_config)
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
```

---

## MAC (Message Authentication Code)

**MAC** забезпечує **цілісність** даних - підтверджує, що дані не були змінені.

### MAC алгоритми:

#### 1. HMAC-SHA2

**hmac-sha2-256, hmac-sha2-512**

```
HMAC (Hash-based Message Authentication Code) з SHA-2

hmac-sha2-256: SHA-256 hash (256-bit output)
hmac-sha2-512: SHA-512 hash (512-bit output)

✅ Безпечний
✅ Стандарт
⚠️  Додаткові обчислення (якщо не AEAD)
```

#### 2. ETM (Encrypt-then-MAC)

**hmac-sha2-256-etm@openssh.com, hmac-sha2-512-etm@openssh.com**

```
Encrypt-then-MAC (замість MAC-then-Encrypt)

Процес:
1. Encrypt plaintext → ciphertext
2. MAC(ciphertext) → tag

✅ Краще за стандартний HMAC (більш безпечний)
✅ Захищає від padding oracle attacks

Рекомендується!
```

#### 3. UMAC

**umac-64@openssh.com, umac-128@openssh.com**

```
Universal MAC

✅ Дуже швидкий
⚠️  Менш поширений
```

#### 4. MD5 / SHA-1 - ЗАСТАРІЛІ!

```
❌ НЕ ВИКОРИСТОВУВАТИ!

hmac-md5      - MD5 collision attacks
hmac-sha1     - SHA-1 deprecated
hmac-sha1-96  - Короткий output (96 біт)
```

### Порівняння MAC алгоритмів:

| MAC | Hash | Output | Безпека | Рекомендація |
|-----|------|--------|---------|--------------|
| `hmac-sha2-256` | SHA-256 | 256-bit | ✅ Добрий | ✅ OK |
| `hmac-sha2-512` | SHA-512 | 512-bit | ✅ Сильний | ✅ OK |
| `hmac-sha2-256-etm@openssh.com` | SHA-256 | 256-bit | ✅ Відмінний | ✅ Рекомендується |
| `hmac-sha2-512-etm@openssh.com` | SHA-512 | 512-bit | ✅ Відмінний | ✅ Рекомендується |
| `umac-128@openssh.com` | UMAC | 128-bit | ✅ Добрий | ✅ Швидкий |
| `hmac-sha1` | SHA-1 | 160-bit | ⚠️ Застарілий | ❌ Уникати |
| `hmac-md5` | MD5 | 128-bit | ❌ Зламаний | ❌ Не використовувати |

**Примітка:** З AEAD cipher suites (AES-GCM, ChaCha20-Poly1305) MAC не потрібен!

```bash
# Перевірка, який MAC використовується
ssh -v user@example.com 2>&1 | grep "MAC alg:"
# MAC alg: hmac-sha2-256-etm@openssh.com
```

---

## Хеш-функції в SSH

### Використання хеш-функцій:

#### 1. Key Derivation (Генерація ключів)

```
З спільного секрету (K) від key exchange генеруються:
- Encryption key (клієнт → сервер)
- Encryption key (сервер → клієнт)
- MAC key (клієнт → сервер)
- MAC key (сервер → клієнт)
- Initial IV (Initialization Vector)

Використовується:
- SHA-256 (з SHA-256/SHA-512 key exchange)
- SHA-512 (з SHA-512 key exchange)
```

#### 2. Fingerprints (Відбитки ключів)

```bash
# MD5 fingerprint (старий формат)
ssh-keygen -lf ~/.ssh/id_rsa.pub -E md5
# 2048 MD5:ab:cd:ef:12:34:56:78:90:ab:cd:ef:12:34:56:78:90 user@host

# SHA256 fingerprint (сучасний формат)
ssh-keygen -lf ~/.ssh/id_rsa.pub
# 2048 SHA256:abc123def456ghi789jkl012mno345pqr678stu901vwx234yz user@host

SHA256 - стандарт з OpenSSH 6.8 (2015)
```

#### 3. HMAC (для MAC)

```
HMAC-SHA256, HMAC-SHA512 - для перевірки цілісності пакетів
```

### Підтримувані хеш-алгоритми:

| Алгоритм | Output | Статус | Використання в SSH |
|----------|--------|--------|--------------------|
| **SHA-256** | 256-bit | ✅ Безпечний | Key exchange, fingerprints, HMAC |
| **SHA-512** | 512-bit | ✅ Безпечний | Key exchange, HMAC |
| **SHA-1** | 160-bit | ⚠️ Застарілий | Legacy key exchange (не рекомендується) |
| **MD5** | 128-bit | ❌ Зламаний | Тільки fingerprints (legacy) |

---

## Стискання (Compression)

SSH підтримує опціональне стискання даних для зменшення bandwidth.

### Алгоритми стискання:

```bash
# none - без стискання (за замовчуванням)
# zlib - zlib compression
# zlib@openssh.com - delayed compression (після аутентифікації)

# Увімкнути compression
ssh -C user@example.com

# Або в конфігурації
Compression yes
```

**Коли використовувати:**
```
✅ Повільне з'єднання (dial-up, satellite)
✅ Текстові файли, логи

❌ Швидке з'єднання (compression overhead > bandwidth savings)
❌ Вже стиснені файли (zip, jpg, mp4)
❌ Вразливість до CRIME-подібних атак
```

**Рекомендація:** Зазвичай compression вимкнено для безпеки та продуктивності.

---

## Перегляд використовуваних алгоритмів

### Перевірка підтримуваних алгоритмів:

```bash
# Key exchange
ssh -Q kex
curve25519-sha256
curve25519-sha256@libssh.org
ecdh-sha2-nistp256
ecdh-sha2-nistp384
ecdh-sha2-nistp521
diffie-hellman-group14-sha256
...

# Ciphers
ssh -Q cipher
chacha20-poly1305@openssh.com
aes128-gcm@openssh.com
aes256-gcm@openssh.com
aes128-ctr
aes192-ctr
aes256-ctr
...

# MAC
ssh -Q mac
hmac-sha2-256-etm@openssh.com
hmac-sha2-512-etm@openssh.com
hmac-sha2-256
hmac-sha2-512
umac-128@openssh.com
...

# Host key types
ssh -Q key
ssh-ed25519
ecdsa-sha2-nistp256
ecdsa-sha2-nistp384
ecdsa-sha2-nistp521
rsa-sha2-512
rsa-sha2-256
ssh-rsa
```

### Перевірка при підключенні:

```bash
# Verbose режим (показує всі деталі)
ssh -vv user@example.com 2>&1 | grep -E "kex:|host key|cipher:|MAC alg:"

# Приклад виводу:
debug1: kex: algorithm: curve25519-sha256
debug1: host key algorithm: ssh-ed25519
debug1: cipher: chacha20-poly1305@openssh.com
debug1: MAC alg: <implicit> (з AEAD cipher)
```

### Примусове використання конкретного алгоритму:

```bash
# Конкретний cipher
ssh -c aes256-gcm@openssh.com user@example.com

# Конкретний MAC
ssh -m hmac-sha2-512-etm@openssh.com user@example.com

# Конкретний host key
ssh -o HostKeyAlgorithms=ssh-ed25519 user@example.com

# Конкретний key exchange
ssh -o KexAlgorithms=curve25519-sha256 user@example.com
```

---

## Найкращі криптографічні налаштування (2024)

### Рекомендована конфігурація:

```bash
# ~/.ssh/config (клієнт)
Host *
    # Key Exchange (найбезпечніші, від найкращого до гіршого)
    KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512
    
    # Host Keys (від найкращого до гіршого)
    HostKeyAlgorithms ssh-ed25519,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,rsa-sha2-512,rsa-sha2-256
    
    # Ciphers (AEAD тільки)
    Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
    
    # MACs (ETM тільки, якщо не AEAD)
    MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
    
    # Compression (вимкнено для безпеки)
    Compression no
```

```bash
# /etc/ssh/sshd_config (сервер)

# Key Exchange
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512

# Host Keys (перегенерувати, якщо потрібно)
HostKey /etc/ssh/ssh_host_ed25519_key
HostKey /etc/ssh/ssh_host_rsa_key

# Ciphers
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com

# MACs
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com

# Compression
Compression no
```

### Що видалити (застарілі/вразливі):

```bash
❌ diffie-hellman-group1-sha1        # 1024-bit DH, SHA-1
❌ diffie-hellman-group14-sha1        # SHA-1
❌ ssh-dss                            # DSA ключі
❌ ssh-rsa (без sha2)                 # RSA з SHA-1
❌ ecdh-sha2-nistp256 (опціонально)   # NIST curves (підозри NSA)
❌ 3des-cbc                           # 3DES
❌ aes*-cbc                           # CBC mode (POODLE-подібні атаки)
❌ arcfour*                           # RC4
❌ hmac-sha1*                         # SHA-1 MAC
❌ hmac-md5*                          # MD5 MAC
❌ umac-64*                           # Короткий MAC
```

---

## SSH Аутентифікація

Після встановлення захищеного з'єднання (Transport Layer), клієнт повинен **аутентифікуватися** на сервері.

```
┌─────────────────────────────────────────────────────────┐
│          Методи аутентифікації SSH                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Password Authentication                             │
│     └─ Найпростіший, але найменш безпечний              │
│                                                         │
│  2. Public Key Authentication (НАЙКРАЩИЙ!)              │
│     └─ Криптографічні ключі                            │
│                                                         │
│  3. Keyboard-Interactive                                │
│     └─ MFA, OTP, challenge-response                    │
│                                                         │
│  4. Certificate-Based Authentication                    │
│     └─ SSH Certificates (CA підпис)                    │
│                                                         │
│  5. Host-Based Authentication                           │
│     └─ Аутентифікація по хосту                         │
│                                                         │
│  6. GSSAPI (Kerberos)                                   │
│     └─ Single Sign-On (SSO)                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 1. Password Authentication

Найпростіший метод - користувач вводить пароль.

### Як працює:

```
┌─────────┐                                    ┌─────────┐
│ Client  │                                    │ Server  │
└────┬────┘                                    └────┬────┘
     │                                              │
     │════ Встановлено зашифроване з'єднання ══════│
     │                                              │
     │───── SSH_MSG_USERAUTH_REQUEST ──────────────→│
     │      method: "password"                      │
     │      username: "john"                        │
     │      password: "secret123" (зашифровано!)    │
     │                                              │
     │                                              │─── Перевірка /etc/shadow
     │                                              │    або PAM
     │                                              │
     │←──── SSH_MSG_USERAUTH_SUCCESS ───────────────│
     │      (якщо пароль правильний)                │
     │                                              │
     └──────── Аутентифіковано! ─────────────────────┘
```

### Налаштування на сервері:

```bash
# /etc/ssh/sshd_config

# Увімкнути password authentication
PasswordAuthentication yes

# Вимкнути empty passwords
PermitEmptyPasswords no

# Вимкнути root login з паролем (безпека!)
PermitRootLogin prohibit-password

# Перезапустити SSH daemon
sudo systemctl restart sshd
```

### Підключення з паролем:

```bash
# SSH попросить ввести пароль
ssh user@example.com

# З явним username
ssh -l user example.com

# Нестандартний порт
ssh -p 2222 user@example.com
```

### Переваги та недоліки:

**Переваги:**
```
✅ Простота (не потрібні ключі)
✅ Працює одразу
✅ Зрозуміло користувачам
```

**Недоліки:**
```
❌ Вразливий до brute-force атак
❌ Слабкі паролі легко зламати
❌ Фішинг, social engineering
❌ Немає захисту від keylogger
❌ Не підходить для автоматизації
```

### Захист від brute-force:

```bash
# 1. Fail2ban - блокує IP після кількох невдалих спроб
sudo apt install fail2ban

# /etc/fail2ban/jail.local
[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600

# 2. Обмежити спроби на сервері (/etc/ssh/sshd_config)
MaxAuthTries 3

# 3. Обмежити кількість одночасних підключень
MaxSessions 10
MaxStartups 10:30:60

# 4. Змінити порт (security through obscurity)
Port 2222

# 5. Використовувати DenyUsers/AllowUsers
AllowUsers john jane admin
DenyUsers root

# 6. Використовувати DenyGroups/AllowGroups
AllowGroups sshusers
```

---

## 2. Public Key Authentication (РЕКОМЕНДОВАНО!)

**Найбезпечніший** метод аутентифікації в SSH.

### Концепція:

```
Приватний ключ (Private Key)          Публічний ключ (Public Key)
┌─────────────────────────┐           ┌─────────────────────────┐
│  ~/.ssh/id_ed25519      │           │  ~/.ssh/id_ed25519.pub  │
│  (СЕКРЕТНИЙ!)           │           │  (можна поширювати)     │
│                         │           │                         │
│  Зберігається на        │◄─────────►│  Розміщується на        │
│  клієнті                │  Pair     │  сервері                │
│                         │           │  ~/.ssh/authorized_keys │
└─────────────────────────┘           └─────────────────────────┘
```

### Як працює:

```
┌─────────┐                                    ┌─────────┐
│ Client  │                                    │ Server  │
└────┬────┘                                    └────┬────┘
     │                                              │
     │════ Встановлено зашифроване з'єднання ══════│
     │                                              │
     │───── SSH_MSG_USERAUTH_REQUEST ──────────────→│
     │      method: "publickey"                     │
     │      username: "john"                        │
     │      public key                              │
     │                                              │
     │                                              │─── Перевірка
     │                                              │    ~/.ssh/authorized_keys
     │                                              │
     │←──── Challenge (random data) ────────────────│
     │                                              │
     │─── Signature (підпис private key) ──────────→│
     │                                              │
     │                                              │─── Перевірка підпису
     │                                              │    public key
     │                                              │
     │←──── SSH_MSG_USERAUTH_SUCCESS ───────────────│
     │                                              │
     └──────── Аутентифіковано! ─────────────────────┘

Приватний ключ НЕ передається мережею!
Тільки підпис, який можна перевірити публічним ключем.
```

### Генерація SSH ключів:

#### Ed25519 (НАЙКРАЩИЙ ВИБІР 2024):

```bash
# Генерація Ed25519 ключа
ssh-keygen -t ed25519 -C "john@example.com"

# З кастомним ім'ям файлу
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_work -C "john@work.com"

# З паролем (passphrase) для захисту приватного ключа
ssh-keygen -t ed25519 -C "john@example.com"
# Enter passphrase (empty for no passphrase): ********
# Enter same passphrase again: ********

Генерується:
~/.ssh/id_ed25519       # Приватний ключ (НІКОЛИ не поширювати!)
~/.ssh/id_ed25519.pub   # Публічний ключ (можна поширювати)

Переваги Ed25519:
✅ Найбезпечніший (2024)
✅ Малий розмір (256-bit)
✅ Швидкий
✅ Immune to timing attacks
```

#### RSA (сумісність зі старими системами):

```bash
# Генерація RSA ключа (4096-bit рекомендується)
ssh-keygen -t rsa -b 4096 -C "john@example.com"

Генерується:
~/.ssh/id_rsa           # Приватний ключ
~/.ssh/id_rsa.pub       # Публічний ключ

Розміри:
- 1024-bit ❌ СЛАБКИЙ
- 2048-bit ⚠️  Мінімум
- 3072-bit ✅ Добре
- 4096-bit ✅ Рекомендується
```

#### ECDSA (альтернатива):

```bash
# Генерація ECDSA ключа
ssh-keygen -t ecdsa -b 256 -C "john@example.com"

⚠️ NIST curves (підозри щодо NSA backdoor)
⚠️ Краще використовувати Ed25519
```

### Копіювання публічного ключа на сервер:

#### Метод 1: ssh-copy-id (найпростіший):

```bash
# Копіювати публічний ключ на сервер
ssh-copy-id user@example.com

# Якщо кілька ключів
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@example.com

# Нестандартний порт
ssh-copy-id -i ~/.ssh/id_ed25519.pub -p 2222 user@example.com

Що робить:
1. Підключається до сервера (з паролем)
2. Додає публічний ключ до ~/.ssh/authorized_keys
3. Встановлює правильні permissions
```

#### Метод 2: Вручну:

```bash
# 1. Показати публічний ключ
cat ~/.ssh/id_ed25519.pub
# ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAbc123def456... john@example.com

# 2. На сервері:
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# 3. Додати ключ до authorized_keys
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAbc123def456... john@example.com" >> ~/.ssh/authorized_keys

# 4. Встановити permissions
chmod 600 ~/.ssh/authorized_keys
```

#### Метод 3: Через pipe:

```bash
# Копіювати публічний ключ через SSH
cat ~/.ssh/id_ed25519.pub | ssh user@example.com "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

### Структура authorized_keys:

```bash
# ~/.ssh/authorized_keys на сервері

# Простий формат
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAbc123... john@laptop
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDdef456... john@desktop

# З обмеженнями (options)
command="/usr/bin/backup" ssh-ed25519 AAAAC3NzaC1lZDI1NTE5... backup-script

# Обмеження по IP
from="192.0.2.0/24" ssh-ed25519 AAAAC3NzaC1lZDI1NTE5... john@work

# Без port forwarding
no-port-forwarding,no-X11-forwarding ssh-ed25519 AAAAC3... restricted

# Тільки конкретна команда
command="git-shell -c \"$SSH_ORIGINAL_COMMAND\"" ssh-ed25519 AAAAC3... git-user
```

### Підключення з ключем:

```bash
# SSH автоматично використовує ключі з ~/.ssh/
ssh user@example.com

# Явно вказати ключ
ssh -i ~/.ssh/id_ed25519 user@example.com

# З verbose (для debugging)
ssh -v -i ~/.ssh/id_ed25519 user@example.com

# Якщо ключ захищений passphrase, SSH попросить його
Enter passphrase for key '/home/john/.ssh/id_ed25519': ********
```

### SSH Agent (уникати повторного введення passphrase):

```bash
# Запустити ssh-agent
eval $(ssh-agent)
# Agent pid 12345

# Додати ключ до агента (попросить passphrase один раз)
ssh-add ~/.ssh/id_ed25519
# Enter passphrase for /home/john/.ssh/id_ed25519: ********
# Identity added: /home/john/.ssh/id_ed25519 (john@example.com)

# Тепер SSH не питатиме passphrase

# Список ключів у агенті
ssh-add -l
# 256 SHA256:abc123def456... john@example.com (ED25519)

# Видалити всі ключі з агента
ssh-add -D

# Видалити конкретний ключ
ssh-add -d ~/.ssh/id_ed25519

# Автоматичний запуск ssh-agent (додати до ~/.bashrc або ~/.zshrc)
if [ -z "$SSH_AUTH_SOCK" ]; then
   eval $(ssh-agent -s)
   ssh-add ~/.ssh/id_ed25519
fi
```

### SSH Agent Forwarding (використання локальних ключів на віддаленому сервері):

```bash
# Підключитись з agent forwarding
ssh -A user@example.com

# Тепер на example.com можна підключитись до інших серверів
# з використанням локальних ключів
user@example.com:~$ ssh user@another-server.com
# Використовується ключ з локальної машини!

# Налаштування в ~/.ssh/config
Host example.com
    ForwardAgent yes

⚠️ УВАГА: Використовувати тільки на довірених серверах!
⚠️ Root на example.com може використати ваші ключі!
```

### Permissions (КРИТИЧНО ВАЖЛИВО!):

```bash
# Правильні permissions для SSH файлів

# Директорія ~/.ssh
chmod 700 ~/.ssh

# Приватні ключі (ТІЛЬКИ власник може читати)
chmod 600 ~/.ssh/id_ed25519
chmod 600 ~/.ssh/id_rsa

# Публічні ключі (можна читати всім)
chmod 644 ~/.ssh/id_ed25519.pub
chmod 644 ~/.ssh/id_rsa.pub

# authorized_keys (ТІЛЬКИ власник може писати)
chmod 600 ~/.ssh/authorized_keys

# known_hosts
chmod 600 ~/.ssh/known_hosts

# config
chmod 600 ~/.ssh/config

# Якщо permissions неправильні, SSH відмовляється працювати!
```

### Вимкнути password authentication (тільки ключі):

```bash
# /etc/ssh/sshd_config

# Вимкнути password authentication
PasswordAuthentication no

# Вимкнути challenge-response
ChallengeResponseAuthentication no

# Увімкнути публічний ключ
PubkeyAuthentication yes

# Перезапустити
sudo systemctl restart sshd

⚠️ ПЕРЕД ВИМКНЕННЯМ password auth переконатись, що:
   1. Публічний ключ скопійовано на сервер
   2. Можна підключитись з ключем
   3. Є backup доступ (console access)!
```

### Переваги Public Key Authentication:

```
✅ Найбезпечніше (2024)
✅ Немає brute-force (ключ неможливо вгадати)
✅ Підходить для автоматизації (scripts, CI/CD)
✅ Можна захистити passphrase
✅ SSH Agent (зручність)
✅ Agent Forwarding
✅ Можна обмежити (command=, from=)
```

---

## 3. Keyboard-Interactive Authentication

Інтерактивний метод, який дозволяє **множинні challenge/response**.

### Використання:

**1. Multi-Factor Authentication (MFA / 2FA):**
```bash
# Google Authenticator (OTP)
# Після встановлення google-authenticator на сервері:

ssh user@example.com
# Password: ********
# Verification code: 123456  ← OTP з телефону
```

**2. Custom challenges:**
```bash
# Може питати кілька питань:
# Question 1: ********
# Question 2: ********
```

### Налаштування на сервері:

```bash
# /etc/ssh/sshd_config
KbdInteractiveAuthentication yes
ChallengeResponseAuthentication yes

# Використовувати PAM
UsePAM yes

# /etc/pam.d/sshd
auth required pam_google_authenticator.so
```

### Переваги:

```
✅ MFA / 2FA підтримка
✅ Гнучкість (кастомні challenges)
✅ Інтеграція з PAM
```

---

## 4. Certificate-Based Authentication

SSH підтримує **сертифікати** (подібно до TLS, але інший формат).

### Концепція:

```
┌────────────────────────────────────────────────────────┐
│              SSH Certificate Authority (CA)            │
│                                                        │
│  CA Private Key → підписує публічні ключі користувачів│
│  CA Public Key → розміщується на серверах              │
└────────────────────────────────────────────────────────┘
         │                                │
         │ підпис                         │ перевірка
         ↓                                ↓
┌─────────────────┐              ┌─────────────────┐
│  User Key       │              │  Server         │
│  + Certificate  │─────────────→│  (trusted CA)   │
└─────────────────┘   login      └─────────────────┘

Переваги:
✅ Централізоване управління
✅ Можна відкликати (validity period)
✅ Додаткові обмеження (principals, extensions)
✅ Масштабованість (багато серверів)
```

### Генерація CA:

```bash
# 1. Створити CA ключ (тільки один раз)
ssh-keygen -t ed25519 -f ~/.ssh/ca_user_key -C "SSH CA"

Генерується:
~/.ssh/ca_user_key       # CA приватний ключ (ЗАХИСТИТИ!)
~/.ssh/ca_user_key.pub   # CA публічний ключ
```

### Підписати user key:

```bash
# 2. Користувач генерує свій ключ
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -C "john@example.com"

# 3. CA підписує публічний ключ користувача
ssh-keygen -s ~/.ssh/ca_user_key \
           -I john \
           -n john,root \
           -V +52w \
           ~/.ssh/id_ed25519.pub

Параметри:
-s           CA приватний ключ
-I           Certificate identity (ім'я)
-n           Principals (usernames, які дозволені)
-V           Validity period (+52w = 52 тижні)

Генерується:
~/.ssh/id_ed25519-cert.pub   # Сертифікат
```

### Налаштування сервера:

```bash
# /etc/ssh/sshd_config

# Довіряти CA
TrustedUserCAKeys /etc/ssh/ca_user_key.pub

# Копіювати CA публічний ключ на сервер
sudo cp ca_user_key.pub /etc/ssh/ca_user_key.pub

# Перезапустити
sudo systemctl restart sshd
```

### Підключення:

```bash
# SSH автоматично використовує сертифікат
ssh john@example.com

# Перевірка сертифіката
ssh-keygen -L -f ~/.ssh/id_ed25519-cert.pub
# Type: user certificate
# Public key: ED25519-CERT ...
# Signing CA: ED25519 ...
# Key ID: "john"
# Principals:
#         john
#         root
# Valid: from 2024-01-01T00:00:00 to 2025-01-01T00:00:00
```

### Переваги сертифікатів:

```
✅ Централізоване управління
✅ Автоматичне закінчення (validity period)
✅ Додаткові обмеження (principals, force-command, source-address)
✅ Масштабованість (багато серверів довіряють одному CA)
✅ Не потрібно додавати ключі в authorized_keys на кожному сервері
```

---

## 5. Host-Based Authentication

Аутентифікація по **хосту** (не користувачу).

```bash
# /etc/ssh/sshd_config
HostbasedAuthentication yes

# /etc/ssh/shosts.equiv або ~/.shosts
client.example.com john

⚠️ НЕ РЕКОМЕНДУЄТЬСЯ!
⚠️ IP-based (легко підробити)
⚠️ Застарілий метод
```

---

## 6. GSSAPI / Kerberos (SSO)

**Single Sign-On** через Kerberos.

```bash
# /etc/ssh/sshd_config
GSSAPIAuthentication yes
GSSAPICleanupCredentials yes

# Клієнт
ssh -o GSSAPIAuthentication=yes user@example.com

Використання:
✅ Enterprise середовища (Active Directory)
✅ Kerberos infrastructure
✅ SSO (Single Sign-On)
```

---

## Порівняння методів аутентифікації:

| Метод | Безпека | Зручність | Автоматизація | Використання |
|-------|---------|-----------|---------------|--------------|
| **Password** | ⚠️ Низька | ✅ Висока | ❌ Ні | Проста початкова настройка |
| **Public Key** | ✅ Висока | ✅ Висока (з agent) | ✅ Так | **РЕКОМЕНДОВАНО** |
| **Keyboard-Interactive** | ✅ Висока (з MFA) | ⚠️ Середня | ❌ Ні | MFA, 2FA |
| **Certificate** | ✅ Висока | ✅ Висока | ✅ Так | Enterprise, масштаб |
| **Host-Based** | ❌ Низька | ✅ Висока | ✅ Так | ❌ Не рекомендується |
| **GSSAPI** | ✅ Висока | ✅ Висока | ✅ Так | Kerberos, AD, SSO |

---

## Множинна аутентифікація (Multi-Factor):

SSH може вимагати **кілька методів** аутентифікації одночасно.

```bash
# /etc/ssh/sshd_config (OpenSSH 6.2+)

# Вимагати публічний ключ ТА пароль
AuthenticationMethods publickey,password

# Вимагати публічний ключ ТА keyboard-interactive (OTP)
AuthenticationMethods publickey,keyboard-interactive

# Альтернативи (АБО)
AuthenticationMethods publickey password keyboard-interactive

# Для конкретних користувачів
Match User admin
    AuthenticationMethods publickey,keyboard-interactive

✅ Максимальна безпека!
```

---

## Налаштування безпечної аутентифікації (рекомендації 2024):

```bash
# /etc/ssh/sshd_config

# ===== Аутентифікація =====

# Тільки публічний ключ (найбезпечніше)
PubkeyAuthentication yes
PasswordAuthentication no
ChallengeResponseAuthentication no

# АБО публічний ключ + MFA
PubkeyAuthentication yes
AuthenticationMethods publickey,keyboard-interactive

# Вимкнути root login (використовувати sudo)
PermitRootLogin no

# Обмежити користувачів
AllowUsers john jane admin
# або
AllowGroups sshusers

# Обмежити спроби
MaxAuthTries 3

# Timeout для аутентифікації
LoginGraceTime 30

# ===== Інше =====

# Вимкнути empty passwords
PermitEmptyPasswords no

# Вимкнути X11 forwarding (якщо не потрібно)
X11Forwarding no

# Strict mode (перевіряти permissions файлів)
StrictModes yes

# Використовувати PAM
UsePAM yes

# Перезапустити
sudo systemctl restart sshd
```

---

## SSH Connection Protocol та сесії

Після успішної аутентифікації починається **Connection Protocol** - верхній рівень SSH, який надає функціональність для роботи з сесіями.

```
┌─────────────────────────────────────────────────────────┐
│          SSH Connection Protocol Features               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Channels (Канали)                                   │
│     └─ Множинні логічні канали в одному з'єднанні      │
│                                                         │
│  2. Interactive Shell                                   │
│     └─ Інтерактивна сесія з PTY                        │
│                                                         │
│  3. Command Execution                                   │
│     └─ Виконання команд без сесії                      │
│                                                         │
│  4. SFTP / SCP                                          │
│     └─ Передача файлів                                 │
│                                                         │
│  5. Port Forwarding                                     │
│     └─ Local, Remote, Dynamic                          │
│                                                         │
│  6. X11 Forwarding                                      │
│     └─ Віддалені GUI додатки                           │
│                                                         │
│  7. Agent Forwarding                                    │
│     └─ Використання локальних ключів                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## SSH Channels (Канали)

SSH використовує **мультиплексування** - можливість мати множинні логічні канали в одному TCP з'єднанні.

### Структура:

```
┌────────────────────────────────────────────────────────┐
│           SSH Connection (TCP port 22)                 │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │  Channel 0: Interactive shell (PTY)              │ │
│  │  stdin/stdout/stderr                             │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │  Channel 1: Port forwarding (local:3306)         │ │
│  │  MySQL traffic                                   │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │  Channel 2: X11 forwarding                       │ │
│  │  GUI application display                         │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │  Channel 3: SFTP subsystem                       │ │
│  │  File transfer operations                        │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
└────────────────────────────────────────────────────────┘

Всі канали шифруються разом в одному TCP з'єднанні!
```

### Типи каналів:

#### 1. Session Channel (Сесійний канал):

```
Використання:
- Interactive shell
- Command execution
- Subsystems (SFTP, SCP)

SSH повідомлення:
SSH_MSG_CHANNEL_OPEN (type: "session")
SSH_MSG_CHANNEL_OPEN_CONFIRMATION
```

#### 2. Direct TCP/IP Channel (Port Forwarding):

```
Використання:
- Local port forwarding
- Remote port forwarding

SSH повідомлення:
SSH_MSG_CHANNEL_OPEN (type: "direct-tcpip")
```

#### 3. Forwarded TCP/IP Channel:

```
Використання:
- Віддалений сервер ініціює підключення назад

SSH повідомлення:
SSH_MSG_CHANNEL_OPEN (type: "forwarded-tcpip")
```

### Lifecycle каналу:

```
┌─────────┐                                    ┌─────────┐
│ Client  │                                    │ Server  │
└────┬────┘                                    └────┬────┘
     │                                              │
     │──── SSH_MSG_CHANNEL_OPEN ───────────────────→│
     │     channel_type: "session"                  │
     │     sender_channel: 0                        │
     │     window_size: 65536                       │
     │     max_packet_size: 32768                   │
     │                                              │
     │←─── SSH_MSG_CHANNEL_OPEN_CONFIRMATION ───────│
     │     recipient_channel: 0                     │
     │     sender_channel: 0                        │
     │     window_size: 65536                       │
     │                                              │
     │═════════ Канал відкритий ════════════════════│
     │                                              │
     │──── SSH_MSG_CHANNEL_REQUEST ────────────────→│
     │     request_type: "shell" або "exec"         │
     │                                              │
     │──── SSH_MSG_CHANNEL_DATA ───────────────────→│
     │     data: команди, input                     │
     │                                              │
     │←─── SSH_MSG_CHANNEL_DATA ────────────────────│
     │     data: output                             │
     │                                              │
     │──── SSH_MSG_CHANNEL_EOF ────────────────────→│
     │                                              │
     │──── SSH_MSG_CHANNEL_CLOSE ──────────────────→│
     │                                              │
     │←─── SSH_MSG_CHANNEL_CLOSE ───────────────────│
     │                                              │
     └─────────── Канал закритий ───────────────────┘
```

### Flow Control (Контроль потоку):

SSH використовує **window-based flow control**:

```bash
# Початковий window size (скільки даних можна відправити)
window_size: 65536 байтів

# Відправка даних зменшує window
sent 1024 bytes → window = 65536 - 1024 = 64512

# SSH_MSG_CHANNEL_WINDOW_ADJUST збільшує window
window_adjust 32768 → window = 64512 + 32768 = 97280

Це запобігає переповненню буферів!
```

---

## Interactive Shell

**Інтерактивна сесія** з псевдо-терміналом (PTY).

### Процес:

```bash
# 1. Підключення
ssh user@example.com

# 2. SSH відкриває session channel
# 3. Запит PTY (pseudo-terminal)
SSH_MSG_CHANNEL_REQUEST (type: "pty-req")
    TERM: xterm-256color
    width: 80 columns
    height: 24 rows
    pixel_width: 640
    pixel_height: 480

# 4. Запит shell
SSH_MSG_CHANNEL_REQUEST (type: "shell")

# 5. Інтерактивна сесія
user@server:~$ ls
user@server:~$ cd /var/www
user@server:/var/www$ vim index.html
```

### PTY (Pseudo-Terminal):

```
┌───────────────┐         SSH         ┌───────────────┐
│  Local        │    (зашифровано)    │  Remote       │
│  Terminal     │◄════════════════════►│  PTY          │
│               │                     │               │
│  stdin  ──────┼────────────────────→│  stdin        │
│  stdout ◄─────┼────────────────────┤  stdout       │
│  stderr ◄─────┼────────────────────┤  stderr       │
│               │                     │               │
│  Ctrl+C ──────┼────────────────────→│  SIGINT       │
│  Ctrl+Z ──────┼────────────────────→│  SIGTSTP      │
│  Window size ─┼────────────────────→│  SIGWINCH     │
└───────────────┘                     └───────────────┘
```

**PTY features:**
- Line editing (backspace, Ctrl+A, Ctrl+E)
- Job control (Ctrl+C, Ctrl+Z, fg, bg)
- Window resize handling
- Terminal modes (raw, cooked)

### Terminal типи:

```bash
# Перевірити поточний TERM
echo $TERM
# xterm-256color

# SSH автоматично передає TERM
ssh user@example.com
echo $TERM  # той самий xterm-256color

# Примусово встановити TERM
TERM=vt100 ssh user@example.com

# Або в ~/.ssh/config
Host example.com
    SetEnv TERM=xterm-256color
```

### Escape sequences:

SSH підтримує **escape sequences** для керування з'єднанням:

```bash
# Натиснути Enter, потім ~
ssh user@example.com

# ~. - закрити з'єднання (якщо зависло)
~.

# ~^Z - призупинити SSH (background)
~^Z
[1]+  Stopped                 ssh user@example.com
fg  # повернутись

# ~C - відкрити SSH command line
~C
ssh> help
Commands:
      -L[bind_address:]port:host:hostport    Request local forward
      -R[bind_address:]port:host:hostport    Request remote forward
      -D[bind_address:]port                  Request dynamic forward
      KR[bind_address:]port                  Cancel remote forward
      ?                                      Display this help
      exit                                   Exit command line

# ~# - список forwarded connections
~#

# ~~ - надіслати символ ~
~~
```

---

## Command Execution

Виконання **однієї команди** без інтерактивної сесії.

### Приклади:

```bash
# Проста команда
ssh user@example.com "ls -la /var/www"

# Множинні команди (через ; або &&)
ssh user@example.com "cd /var/www && ls -la && pwd"

# З pipeline
ssh user@example.com "ps aux | grep nginx"

# Команда з аргументами (одинарні лапки на віддаленому сервері)
ssh user@example.com "find /var/log -name '*.log' -mtime +7"

# З sudo (може попросити пароль)
ssh user@example.com "sudo systemctl restart nginx"
```

### Input/Output redirection:

```bash
# STDIN через pipe
echo "SELECT * FROM users;" | ssh user@db.example.com "mysql -u root -p database"

# Віддалений output в локальний файл
ssh user@example.com "cat /var/log/nginx/access.log" > local_access.log

# Локальний файл на віддалений сервер
cat local.txt | ssh user@example.com "cat > /tmp/remote.txt"

# Backup через SSH
ssh user@example.com "tar czf - /var/www" > backup.tar.gz

# Restore через SSH
cat backup.tar.gz | ssh user@example.com "tar xzf - -C /"
```

### Exit codes:

```bash
# SSH повертає exit code команди
ssh user@example.com "exit 42"
echo $?  # 42

# Використання в scripts
if ssh user@example.com "test -f /etc/nginx/nginx.conf"; then
    echo "Nginx config exists"
else
    echo "Nginx config not found"
fi

# Логування помилок
ssh user@example.com "command_that_might_fail" || echo "Command failed with exit code $?"
```

### Відмінності від interactive shell:

| Характеристика | Interactive Shell | Command Execution |
|----------------|-------------------|-------------------|
| **PTY** | ✅ Так | ❌ Ні |
| **Shell initialization** | ~/.bashrc, ~/.profile | Мінімальний |
| **Job control** | ✅ Ctrl+C, Ctrl+Z | ⚠️ Обмежений |
| **Output buffering** | Line-buffered | Може бути fully-buffered |
| **$PS1 prompt** | ✅ Так | ❌ Ні |
| **Aliases** | ✅ Так | ⚠️ Залежить від shell |

---

## SFTP (SSH File Transfer Protocol)

**SFTP** - протокол передачі файлів через SSH (НЕ плутати з FTPS!).

### SFTP vs SCP vs FTP:

| Характеристика | SFTP | SCP | FTP | FTPS |
|----------------|------|-----|-----|------|
| **Шифрування** | ✅ SSH | ✅ SSH | ❌ Ні | ✅ TLS |
| **Порт** | 22 | 22 | 21 | 990 |
| **Інтерактивний** | ✅ Так | ❌ Ні | ✅ Так | ✅ Так |
| **Resume download** | ✅ Так | ❌ Ні | ✅ Так | ✅ Так |
| **Directory listing** | ✅ Так | ❌ Ні | ✅ Так | ✅ Так |
| **Permissions** | ✅ Так | ✅ Так | ✅ Так | ✅ Так |
| **Рекомендація** | ✅ Використовувати | ⚠️ Legacy | ❌ Вразливий | ⚠️ Альтернатива |

### SFTP інтерактивна сесія:

```bash
# Підключення
sftp user@example.com

# Команди (подібні до FTP)
sftp> pwd
Remote working directory: /home/user

sftp> lpwd
Local working directory: /home/local_user

sftp> ls
file1.txt    file2.txt    directory

sftp> lls
local_file1.txt    local_file2.txt

# Зміна директорій
sftp> cd /var/www
sftp> lcd /home/local_user/downloads

# Завантаження (з сервера на локальну машину)
sftp> get remote_file.txt
Fetching /var/www/remote_file.txt to remote_file.txt
remote_file.txt                               100%  1024     1.0KB/s   00:01

# Завантаження директорії (рекурсивно)
sftp> get -r remote_directory

# Вивантаження (з локальної машини на сервер)
sftp> put local_file.txt
Uploading local_file.txt to /var/www/local_file.txt
local_file.txt                                100%  2048     2.0KB/s   00:01

# Вивантаження директорії
sftp> put -r local_directory

# Множинні файли (wildcard)
sftp> mget *.txt
sftp> mput *.log

# Permissions
sftp> chmod 644 file.txt
sftp> chown user:group file.txt

# Видалення
sftp> rm file.txt
sftp> rmdir directory

# Створення директорії
sftp> mkdir new_directory

# Rename/move
sftp> rename old.txt new.txt

# Exit
sftp> exit
```

### SFTP batch mode:

```bash
# Виконати команди з файлу
cat > sftp_commands.txt << EOF
cd /var/www
get index.html
put local.html
exit
EOF

sftp -b sftp_commands.txt user@example.com

# Або через echo
echo "get /remote/file.txt" | sftp user@example.com
```

### SFTP через скрипти:

```bash
# Bash script для backup через SFTP
#!/bin/bash

HOST="example.com"
USER="backup_user"
REMOTE_DIR="/backups"
LOCAL_DIR="/home/user/backups"

# Створити backup
BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).tar.gz"
tar czf "/tmp/${BACKUP_FILE}" /var/www

# Відправити через SFTP
sftp ${USER}@${HOST} << EOF
cd ${REMOTE_DIR}
put /tmp/${BACKUP_FILE}
ls -l
exit
EOF

# Очистити
rm -f "/tmp/${BACKUP_FILE}"
```

### SFTP configuration:

```bash
# /etc/ssh/sshd_config

# SFTP subsystem (за замовчуванням)
Subsystem sftp /usr/lib/openssh/sftp-server

# Або з логуванням
Subsystem sftp /usr/lib/openssh/sftp-server -f AUTH -l VERBOSE

# Chroot jail (обмежити доступ до директорії)
Match User sftponly
    ChrootDirectory /home/sftponly
    ForceCommand internal-sftp
    AllowTcpForwarding no
    X11Forwarding no
```

---

## SCP (Secure Copy)

**SCP** - протокол копіювання файлів через SSH.

### Основні команди:

```bash
# Копіювати файл на сервер
scp file.txt user@example.com:/home/user/

# Копіювати з сервера на локальну машину
scp user@example.com:/home/user/file.txt .

# Рекурсивне копіювання директорії
scp -r directory user@example.com:/home/user/

# З нестандартним портом
scp -P 2222 file.txt user@example.com:/home/user/

# З прогресом (verbose)
scp -v file.txt user@example.com:/home/user/

# Preserve permissions and timestamps
scp -p file.txt user@example.com:/home/user/

# Обмежити bandwidth (KB/s)
scp -l 1024 large_file.zip user@example.com:/home/user/

# З конкретним ключем
scp -i ~/.ssh/id_ed25519 file.txt user@example.com:/home/user/

# Compression (корисно для повільних з'єднань)
scp -C file.txt user@example.com:/home/user/
```

### SCP між двома серверами:

```bash
# Копіювати з server1 на server2 (через локальну машину)
scp user1@server1.com:/path/file.txt user2@server2.com:/path/

# Примітка: трафік йде через локальну машину!
```

### SCP vs SFTP:

```
SCP:
✅ Простіший для разових копіювань
✅ Швидше для простих операцій
❌ Не інтерактивний
❌ Не можна resume
❌ Не можна list files

SFTP:
✅ Інтерактивний
✅ Можна resume
✅ Directory listing
✅ Більше функцій
⚠️ Трохи складніший

Рекомендація: використовувати SFTP для більшості завдань.
```

---

## SSH Connection Multiplexing

**Мультиплексування** дозволяє використовувати одне TCP з'єднання для множинних SSH сесій.

### Переваги:

```
✅ Швидше (не потрібен handshake для кожної сесії)
✅ Менше навантаження на сервер
✅ Менше мережевих ресурсів
```

### Налаштування:

```bash
# ~/.ssh/config

Host *
    # Увімкнути multiplexing
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h:%p
    ControlPersist 10m

# Створити директорію для sockets
mkdir -p ~/.ssh/sockets
```

**Параметри:**
- `ControlMaster auto` - автоматично створювати master з'єднання
- `ControlPath` - шлях до socket файлу
- `ControlPersist 10m` - зберігати з'єднання 10 хвилин після останньої сесії

### Використання:

```bash
# Перше підключення (створює master connection)
ssh user@example.com
# Вводить пароль/passphrase

# Друге підключення (використовує існуюче з'єднання)
ssh user@example.com
# НЕ питає пароль! Миттєво підключається!

# Третє, четверте... (всі через одне TCP з'єднання)
ssh user@example.com
ssh user@example.com
```

### Управління мультиплексуванням:

```bash
# Перевірити статус
ssh -O check user@example.com
# Master running (pid=12345)

# Закрити всі з'єднання
ssh -O exit user@example.com
# Exit request sent.

# Перезавантажити конфігурацію
ssh -O forward -L 8080:localhost:80 user@example.com

# Зупинити прийом нових з'єднань
ssh -O stop user@example.com
```

---

## Keep-Alive механізм

**Keep-Alive** запобігає розриву з'єднання при неактивності.

### Проблема:

```
Firewall/NAT може розривати неактивні TCP з'єднання після timeout
SSH сесія може зависнути якщо немає трафіку
```

### Рішення 1: Client-side keep-alive:

```bash
# ~/.ssh/config

Host *
    # Відправляти keep-alive пакети кожні 60 секунд
    ServerAliveInterval 60
    
    # Максимум 3 спроби без відповіді, потім розірвати
    ServerAliveCountMax 3
    
    # Загальний timeout: 60 * 3 = 180 секунд
```

### Рішення 2: Server-side keep-alive:

```bash
# /etc/ssh/sshd_config

# Відправляти keep-alive кожні 60 секунд
ClientAliveInterval 60

# Максимум 3 спроби
ClientAliveCountMax 3
```

### Рекомендації:

```bash
# Для нестабільних з'єднань (Wi-Fi, mobile)
ServerAliveInterval 30
ServerAliveCountMax 5

# Для стабільних з'єднань
ServerAliveInterval 120
ServerAliveCountMax 2

# Для production серверів за firewall
ClientAliveInterval 60
ClientAliveCountMax 3
```

---

## Session Recording (логування)

SSH підтримує логування всіх команд та виводу.

### Server-side logging:

```bash
# /etc/ssh/sshd_config

# Рівень логування
LogLevel VERBOSE

# Файл логів (зазвичай /var/log/auth.log або /var/log/secure)
SyslogFacility AUTH

# Лог всіх команд
ForceCommand /usr/bin/log-wrapper.sh

# Script для логування
# /usr/bin/log-wrapper.sh
#!/bin/bash
LOG="/var/log/ssh-sessions/$(date +%Y%m%d_%H%M%S)_${USER}_${SSH_CLIENT%% *}.log"
script -q -c "/bin/bash" "$LOG"
```

### Client-side recording:

```bash
# Записати всю сесію в файл
ssh user@example.com | tee session.log

# Використовувати 'script' для запису
script -c "ssh user@example.com" session.log

# Automatic logging в ~/.ssh/config
Host *
    # Логувати всі команди
    LogLevel DEBUG3
```

---

## SSH Тунелювання та Port Forwarding

SSH дозволяє **перенаправляти** TCP порти через зашифроване з'єднання - це називається **SSH тунелювання** або **Port Forwarding**.

```
┌─────────────────────────────────────────────────────────┐
│          Типи SSH Port Forwarding                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Local Port Forwarding (-L)                          │
│     └─ Локальний порт → віддалений сервіс               │
│                                                         │
│  2. Remote Port Forwarding (-R)                         │
│     └─ Віддалений порт → локальний сервіс               │
│                                                         │
│  3. Dynamic Port Forwarding (-D)                        │
│     └─ SOCKS proxy для всього трафіку                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Local Port Forwarding (-L)

**Local Port Forwarding** перенаправляє локальний порт на віддалений сервіс через SSH.

### Синтаксис:

```bash
ssh -L [local_bind_addr:]local_port:remote_host:remote_port user@ssh_server

# Спрощений варіант
ssh -L local_port:remote_host:remote_port user@ssh_server
```

### Приклад 1: Доступ до віддаленої бази даних

```
Проблема: MySQL на сервері слухає тільки localhost (порт 3306)
Рішення: SSH тунель

┌──────────────┐         SSH Tunnel        ┌──────────────┐
│  Local PC    │◄═════════════════════════►│  Server      │
│  localhost:  │                           │              │
│  3306        │                           │ MySQL:3306   │
└──────────────┘                           └──────────────┘
```

```bash
# Створити тунель
ssh -L 3306:localhost:3306 user@db.example.com

# Тепер можна підключитись до MySQL локально:
mysql -h 127.0.0.1 -P 3306 -u dbuser -p

# Або
mysql -h localhost -P 3306 -u dbuser -p

# З'єднання йде через SSH тунель!
```

### Приклад 2: Доступ до веб-сервера

```bash
# Перенаправити локальний порт 8080 на віддалений порт 80
ssh -L 8080:localhost:80 user@web.example.com

# Відкрити в браузері:
http://localhost:8080

# Бачимо сайт з web.example.com!
```

### Приклад 3: Доступ до сервісу на іншому сервері

```
┌──────────┐    SSH     ┌──────────┐         ┌──────────┐
│  Local   │═══════════►│  Jump    │────────►│ Database │
│          │            │  Server  │         │ Server   │
│ :3306    │            │          │         │ :3306    │
└──────────┘            └──────────┘         └──────────┘
```

```bash
# Перенаправити на інший сервер (не localhost)
ssh -L 3306:db-internal.example.com:3306 user@jump.example.com

# Тепер localhost:3306 → db-internal.example.com:3306
mysql -h 127.0.0.1 -P 3306 -u dbuser -p
```

### Приклад 4: Множинні тунелі

```bash
# Можна створити кілька тунелів одразу
ssh -L 3306:localhost:3306 \
    -L 5432:localhost:5432 \
    -L 6379:localhost:6379 \
    user@example.com

# Тепер доступні:
# localhost:3306 → MySQL
# localhost:5432 → PostgreSQL
# localhost:6379 → Redis
```

### Bind address (слухати не тільки localhost):

```bash
# За замовчуванням SSH слухає тільки localhost (127.0.0.1)
ssh -L 3306:localhost:3306 user@example.com

# Слухати всі інтерфейси (0.0.0.0) - НЕБЕЗПЕЧНО!
ssh -L 0.0.0.0:3306:localhost:3306 user@example.com

# Тепер інші комп'ютери в мережі можуть підключитись до вашого порту 3306

⚠️ Використовувати тільки в довіреній мережі!

# Конкретний IP
ssh -L 192.168.1.100:3306:localhost:3306 user@example.com
```

### Background mode:

```bash
# Запустити SSH в фоновому режимі
ssh -f -N -L 3306:localhost:3306 user@example.com

# -f : запустити в background
# -N : не виконувати команди (тільки forwarding)

# Перевірити процес
ps aux | grep ssh

# Завершити
pkill -f "ssh.*3306"
```

### У конфігурації ~/.ssh/config:

```bash
Host db-tunnel
    HostName db.example.com
    User dbuser
    LocalForward 3306 localhost:3306
    LocalForward 5432 localhost:5432

# Використання
ssh -f -N db-tunnel
```

---

## Remote Port Forwarding (-R)

**Remote Port Forwarding** робить локальний сервіс доступним на віддаленому сервері.

### Синтаксис:

```bash
ssh -R [remote_bind_addr:]remote_port:local_host:local_port user@ssh_server
```

### Приклад 1: Показати локальний веб-сайт клієнту

```
Ситуація: Розробляємо сайт локально, хочемо показати клієнту

┌──────────────┐         SSH Tunnel        ┌──────────────┐
│  Local PC    │═════════════════════════►│  Public      │
│  localhost:  │                           │  Server      │
│  3000        │                           │  :8080       │
└──────────────┘                           └──────────────┘
                                                 ▲
                                                 │
                                         ┌───────┴────────┐
                                         │  Client access │
                                         │ server:8080    │
                                         └────────────────┘
```

```bash
# На локальній машині (де працює dev server на порту 3000)
ssh -R 8080:localhost:3000 user@public-server.com

# Тепер клієнт може відкрити:
http://public-server.com:8080

# Бачить ваш локальний сайт!
```

### Приклад 2: SSH через NAT/Firewall

```
Проблема: Домашній сервер за NAT, немає публічного IP
Рішення: Reverse SSH tunnel

┌──────────────┐         SSH (initiated)   ┌──────────────┐
│  Home Server │═════════════════════════►│  Public VPS  │
│  (за NAT)    │                           │  (固定 IP)    │
│  SSH:22      │                           │  :2222       │
└──────────────┘                           └──────────────┘
                                                 ▲
                                                 │ SSH to :2222
                                         ┌───────┴────────┐
                                         │   Your laptop  │
                                         └────────────────┘
```

```bash
# На домашньому сервері (за NAT)
ssh -f -N -R 2222:localhost:22 user@public-vps.com

# Тепер з будь-якого місця можна підключитись до домашнього сервера:
ssh -p 2222 user@public-vps.com
# Автоматично перенаправиться на домашній сервер!

# Це називається "Reverse SSH tunnel"
```

### Приклад 3: Обхід корпоративного firewall

```bash
# Firewall блокує вихідні підключення, крім SSH?
# Можна через reverse tunnel отримати доступ ззовні

# На робочому комп'ютері (за firewall)
ssh -R 3389:localhost:3389 user@home-server.com

# Тепер з дому можна підключитись RDP:
rdesktop localhost:3389  # на home-server
```

### GatewayPorts (дозволити зовнішні підключення):

```bash
# За замовчуванням remote forwarding слухає тільки localhost на сервері

# /etc/ssh/sshd_config на сервері
GatewayPorts yes

# Або
GatewayPorts clientspecified

# Перезапустити sshd
sudo systemctl restart sshd

# Тепер можна вказати 0.0.0.0
ssh -R 0.0.0.0:8080:localhost:3000 user@server.com

# Сервер буде слухати на всіх інтерфейсах
```

### autossh (автоматичне перепідключення):

```bash
# autossh автоматично відновлює тунель при розриві

# Встановити
sudo apt install autossh

# Використання
autossh -M 0 -f -N -R 2222:localhost:22 user@public-vps.com

# -M 0 : не використовувати моніторинг порт
# Використовує ServerAliveInterval замість цього

# Systemd service для autossh
# /etc/systemd/system/reverse-tunnel.service
[Unit]
Description=Reverse SSH Tunnel
After=network.target

[Service]
Type=simple
User=username
ExecStart=/usr/bin/autossh -M 0 -N -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" -R 2222:localhost:22 user@public-vps.com
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Запустити
sudo systemctl enable reverse-tunnel
sudo systemctl start reverse-tunnel
```

---

## Dynamic Port Forwarding (-D) - SOCKS Proxy

**Dynamic Port Forwarding** створює **SOCKS proxy** через SSH.

### Синтаксис:

```bash
ssh -D [local_bind_addr:]local_port user@ssh_server
```

### Приклад 1: SOCKS proxy для браузера

```
┌──────────────┐    SOCKS5 Proxy    ┌──────────────┐        ┌──────────┐
│  Browser     │══════════════════►│  SSH Server  │───────►│ Internet │
│  (proxy:     │                    │              │        │          │
│  localhost:  │                    │              │        │          │
│  1080)       │                    │              │        │          │
└──────────────┘                    └──────────────┘        └──────────┘

Весь трафік браузера йде через SSH!
```

```bash
# Створити SOCKS proxy на порту 1080
ssh -D 1080 user@server.example.com

# Налаштувати браузер (Firefox):
# Settings → Network Settings → Manual proxy configuration
# SOCKS Host: 127.0.0.1
# Port: 1080
# SOCKS v5

# Тепер весь трафік браузера йде через SSH tunnel!
```

### Приклад 2: Обхід цензури

```bash
# Якщо певні сайти заблоковані, але є доступ до SSH сервера в іншій країні
ssh -D 1080 user@server-in-free-country.com

# Налаштувати браузер на використання SOCKS proxy
# Всі заблоковані сайти стають доступними!
```

### Приклад 3: Використання з командами

```bash
# curl з SOCKS proxy
curl --socks5 localhost:1080 http://example.com

# wget з SOCKS proxy
wget -e use_proxy=yes -e http_proxy=socks5://localhost:1080 http://example.com

# git з SOCKS proxy
git config --global http.proxy socks5://127.0.0.1:1080

# Вся система через SOCKS (proxychains)
sudo apt install proxychains
# Edit /etc/proxychains.conf
# socks5 127.0.0.1 1080

proxychains firefox
proxychains curl http://example.com
```

### Приклад 4: FoxyProxy (розширення для браузера)

```
FoxyProxy дозволяє легко перемикати між proxy:

1. Встановити FoxyProxy в Firefox/Chrome
2. Додати новий proxy:
   - Title: SSH Tunnel
   - Type: SOCKS5
   - Host: 127.0.0.1
   - Port: 1080
3. Налаштувати patterns для автоматичного використання
```

---

## X11 Forwarding

**X11 Forwarding** дозволяє запускати GUI додатки на віддаленому сервері, але бачити їх на локальному екрані.

### Налаштування:

```bash
# На сервері (/etc/ssh/sshd_config)
X11Forwarding yes
X11DisplayOffset 10
X11UseLocalhost yes

# Перезапустити
sudo systemctl restart sshd

# На клієнті (потрібен X server)
# Linux: вже є
# macOS: встановити XQuartz
# Windows: встановити VcXsrv або Xming
```

### Використання:

```bash
# Підключитись з X11 forwarding
ssh -X user@example.com

# Або trusted X11 forwarding (швидше, але менш безпечно)
ssh -Y user@example.com

# Запустити GUI додаток
user@remote:~$ firefox
# Firefox відкриється на локальному екрані!

user@remote:~$ gedit file.txt
# Gedit відкриється локально

user@remote:~$ nautilus
# File manager відкриється локально
```

### Перевірка:

```bash
# Перевірити чи працює X11 forwarding
echo $DISPLAY
# localhost:10.0

# Тестовий GUI додаток
xeyes
xclock
```

### У конфігурації:

```bash
# ~/.ssh/config
Host gui-server
    HostName example.com
    User username
    ForwardX11 yes
    ForwardX11Trusted yes

# Використання
ssh gui-server
```

### Compression для X11:

```bash
# X11 forwarding може бути повільним через мережу
# Увімкнути compression
ssh -X -C user@example.com

# Або в ~/.ssh/config
Host *
    ForwardX11 yes
    Compression yes
```

---

## Комбінації та складні сценарії

### Jump Host (ProxyJump):

```
┌──────────┐        ┌──────────┐        ┌──────────┐
│  Local   │───────►│  Jump    │───────►│  Target  │
│          │        │  Server  │        │  Server  │
└──────────┘        └──────────┘        └──────────┘
```

```bash
# Стара версія (з ProxyCommand)
ssh -o ProxyCommand="ssh -W %h:%p user@jump.example.com" user@target.example.com

# Нова версія (OpenSSH 7.3+)
ssh -J user@jump.example.com user@target.example.com

# Множинні jump hosts
ssh -J user@jump1.com,user@jump2.com user@target.com

# У конфігурації
# ~/.ssh/config
Host target
    HostName target.example.com
    User targetuser
    ProxyJump jump.example.com

# Використання
ssh target
```

### Тунель через Jump Host:

```bash
# Port forwarding через jump host
ssh -J user@jump.com -L 3306:db.internal:3306 user@internal-network.com
```

### VPN через SSH (sshuttle):

```bash
# sshuttle - "poor man's VPN"
sudo apt install sshuttle

# Весь трафік до підмережі через SSH
sshuttle -r user@server.com 192.168.0.0/16

# Весь трафік (крім локальної мережі)
sshuttle -r user@server.com 0.0.0.0/0

# З DNS
sshuttle -r user@server.com --dns 0.0.0.0/0

# Тепер вся система використовує SSH як VPN!
```

### SSH через HTTP proxy:

```bash
# Якщо можна тільки через корпоративний HTTP proxy

# Встановити corkscrew або netcat
sudo apt install corkscrew

# ~/.ssh/config
Host external-server
    HostName server.example.com
    User username
    ProxyCommand corkscrew proxy.company.com 8080 %h %p

# Підключення
ssh external-server
```

### Keepalive для тунелів:

```bash
# ~/.ssh/config для надійних тунелів
Host tunnel-*
    ServerAliveInterval 30
    ServerAliveCountMax 3
    TCPKeepAlive yes
    ExitOnForwardFailure yes
```

---

## Практичні приклади та use cases

### Use Case 1: Безпечний доступ до корпоративної бази даних з дому

```bash
#!/bin/bash
# db-tunnel.sh

# Створити тунель до корпоративної БД
ssh -f -N -L 3306:db-internal.company.com:3306 user@vpn.company.com

echo "Database tunnel active on localhost:3306"
echo "Connect with: mysql -h 127.0.0.1 -P 3306 -u username -p"

# Або додати в ~/.ssh/config:
# Host work-db-tunnel
#     HostName vpn.company.com
#     User work_user
#     LocalForward 3306 db-internal.company.com:3306
#     LocalForward 5432 postgres-internal.company.com:5432

# Запуск: ssh -f -N work-db-tunnel
```

### Use Case 2: Розробка з локального Docker на віддаленому сервері

```bash
# Перенаправити Docker socket
ssh -L /tmp/docker.sock:/var/run/docker.sock user@docker-server.com

# Використовувати локально
export DOCKER_HOST=unix:///tmp/docker.sock
docker ps
docker run ...
```

### Use Case 3: Моніторинг через Grafana

```bash
# Grafana на internal-server:3000
ssh -L 3000:internal-server:3000 user@gateway.company.com

# Відкрити в браузері
http://localhost:3000
```

### Use Case 4: Експонувати локальний webhook для тестування

```bash
# Webhook endpoint на localhost:3000
# Зробити доступним через public server для GitHub webhooks

ssh -R 8080:localhost:3000 user@public.example.com

# Налаштувати GitHub webhook:
# http://public.example.com:8080/webhook

# Тепер GitHub може відправляти webhooks на ваш локальний сервер!
```

---

## Конфігурація SSH клієнта та сервера

### SSH Client Config (~/.ssh/config)

**~/.ssh/config** дозволяє налаштувати SSH клієнт для зручності та автоматизації.

### Базовий приклад:

```bash
# ~/.ssh/config

# Загальні налаштування для всіх хостів
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    Compression yes
    
# Конкретний сервер
Host myserver
    HostName example.com
    User john
    Port 2222
    IdentityFile ~/.ssh/id_ed25519

# Тепер замість:
# ssh -p 2222 -i ~/.ssh/id_ed25519 john@example.com
# Можна просто:
# ssh myserver
```

### Розширений приклад з різними сценаріями:

```bash
# ~/.ssh/config

# ===== Робочі сервери =====

Host work-*
    User work_username
    IdentityFile ~/.ssh/id_rsa_work
    ForwardAgent no
    
Host work-web
    HostName web.company.com
    LocalForward 8080 localhost:80

Host work-db
    HostName db.company.com
    LocalForward 3306 localhost:3306
    LocalForward 5432 localhost:5432

# ===== Особисті сервери =====

Host personal-*
    User personal_username
    IdentityFile ~/.ssh/id_ed25519
    
Host personal-vps
    HostName vps.mydomain.com
    Port 2222

# ===== GitHub =====

Host github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_github
    IdentitiesOnly yes

# ===== Jump hosts =====

Host internal-server
    HostName 10.0.1.100
    User admin
    ProxyJump jump.company.com

Host jump.company.com
    User jumpuser
    IdentityFile ~/.ssh/id_rsa_jump

# ===== Multiplexing =====

Host *
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h:%p
    ControlPersist 10m

# ===== Безпека =====

Host untrusted-*
    ForwardAgent no
    ForwardX11 no
    PasswordAuthentication no
    ChallengeResponseAuthentication no

# ===== Keep-alive =====

Host long-running-*
    ServerAliveInterval 30
    ServerAliveCountMax 10
    TCPKeepAlive yes
```

### Параметри ~/.ssh/config:

| Параметр | Опис | Приклад |
|----------|------|---------|
| **Host** | Alias для підключення | `Host myserver` |
| **HostName** | Реальний hostname або IP | `HostName example.com` |
| **User** | Username для підключення | `User john` |
| **Port** | SSH порт | `Port 2222` |
| **IdentityFile** | Приватний ключ | `IdentityFile ~/.ssh/id_ed25519` |
| **IdentitiesOnly** | Використовувати тільки вказаний ключ | `IdentitiesOnly yes` |
| **ForwardAgent** | Agent forwarding | `ForwardAgent yes` |
| **ForwardX11** | X11 forwarding | `ForwardX11 yes` |
| **LocalForward** | Local port forwarding | `LocalForward 8080 localhost:80` |
| **RemoteForward** | Remote port forwarding | `RemoteForward 8080 localhost:80` |
| **DynamicForward** | SOCKS proxy | `DynamicForward 1080` |
| **ProxyJump** | Jump host | `ProxyJump jump.example.com` |
| **ProxyCommand** | Proxy command | `ProxyCommand ssh -W %h:%p jump.com` |
| **ServerAliveInterval** | Keep-alive інтервал | `ServerAliveInterval 60` |
| **ServerAliveCountMax** | Keep-alive спроби | `ServerAliveCountMax 3` |
| **Compression** | Стискання | `Compression yes` |
| **ControlMaster** | Multiplexing | `ControlMaster auto` |
| **ControlPath** | Socket path | `ControlPath ~/.ssh/sockets/%r@%h:%p` |
| **ControlPersist** | Час збереження з'єднання | `ControlPersist 10m` |

### Wildcards та patterns:

```bash
# Використання wildcards
Host *.company.com
    User corporate_user
    IdentityFile ~/.ssh/id_rsa_work

# Негативний match
Host * !untrusted.com
    ForwardAgent yes

# Множинні patterns
Host web* db* app*
    User admin
    Port 2222
```

---

### SSH Server Config (/etc/ssh/sshd_config)

**sshd_config** - конфігурація SSH сервера (daemon).

### Рекомендована безпечна конфігурація (2024):

```bash
# /etc/ssh/sshd_config

# ===== Network =====

# Порт (змінити для obscurity)
Port 22
# Port 2222

# Listen адреси
ListenAddress 0.0.0.0
# ListenAddress ::

# Protocol (тільки SSH-2!)
Protocol 2

# ===== Аутентифікація =====

# Тільки public key authentication (НАЙБЕЗПЕЧНІШЕ!)
PubkeyAuthentication yes
PasswordAuthentication no
PermitEmptyPasswords no
ChallengeResponseAuthentication no

# АБО public key + MFA
# AuthenticationMethods publickey,keyboard-interactive

# Root login (вимкнути або тільки з ключем)
PermitRootLogin no
# PermitRootLogin prohibit-password

# Login grace time
LoginGraceTime 30

# Max authentication tries
MaxAuthTries 3

# Max sessions per connection
MaxSessions 10

# Max startups (anti-DoS)
MaxStartups 10:30:60

# ===== Обмеження користувачів =====

# Дозволити тільки конкретних користувачів
AllowUsers john jane admin
# AllowGroups sshusers

# Заборонити користувачів
# DenyUsers baduser
# DenyGroups badgroup

# ===== Криптографія =====

# Key exchange algorithms
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512

# Host keys
HostKey /etc/ssh/ssh_host_ed25519_key
HostKey /etc/ssh/ssh_host_rsa_key

# Ciphers
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com

# MACs
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com

# ===== Features =====

# X11 Forwarding
X11Forwarding no
# X11Forwarding yes

# TCP Forwarding
AllowTcpForwarding yes
# AllowTcpForwarding no

# Agent Forwarding
AllowAgentForwarding yes
# AllowAgentForwarding no

# SFTP
Subsystem sftp /usr/lib/openssh/sftp-server

# ===== Keep-alive =====

# Client alive (keep-alive)
ClientAliveInterval 60
ClientAliveCountMax 3

# TCP keep-alive
TCPKeepAlive yes

# ===== Logging =====

# Log level
LogLevel VERBOSE
# LogLevel INFO

# Syslog facility
SyslogFacility AUTH

# ===== Security =====

# Strict modes
StrictModes yes

# Use PAM
UsePAM yes

# Use DNS
UseDNS no

# Print last log
PrintLastLog yes

# Print MOTD
PrintMotd yes

# Compression
Compression yes
# Compression delayed

# ===== Per-user configuration =====

# Приклад для конкретного користувача
Match User sftponly
    ForceCommand internal-sftp
    ChrootDirectory /home/sftponly
    AllowTcpForwarding no
    X11Forwarding no

# Приклад для групи
Match Group developers
    AllowTcpForwarding yes
    X11Forwarding yes
    
# Приклад для IP адреси
Match Address 192.168.1.0/24
    PasswordAuthentication yes

# ===== Banner =====

# Banner перед login
# Banner /etc/ssh/banner.txt

# Перезапустити після змін
# sudo systemctl restart sshd

# Перевірити конфігурацію
# sudo sshd -t
```

### Перевірка конфігурації:

```bash
# Перевірити синтаксис
sudo sshd -t

# Перевірити конфігурацію з verbose
sudo sshd -T

# Перевірити для конкретного користувача
sudo sshd -T -C user=john,host=example.com,addr=192.168.1.100

# Перезапустити sshd
sudo systemctl restart sshd

# Перевірити статус
sudo systemctl status sshd

# Переглянути логи
sudo tail -f /var/log/auth.log
# або
sudo journalctl -u sshd -f
```

### SFTP-only користувачі (chroot jail):

```bash
# /etc/ssh/sshd_config

# SFTP-only група
Match Group sftponly
    ChrootDirectory /home/%u
    ForceCommand internal-sftp
    AllowTcpForwarding no
    X11Forwarding no
    PermitTunnel no

# Створити користувача
sudo useradd -m -G sftponly -s /sbin/nologin sftpuser

# Налаштувати директорію для chroot
sudo chown root:root /home/sftpuser
sudo chmod 755 /home/sftpuser
sudo mkdir /home/sftpuser/uploads
sudo chown sftpuser:sftponly /home/sftpuser/uploads

# Встановити пароль або додати SSH ключ
sudo passwd sftpuser
```

---

## Безпека SSH

### Загрози та атаки на SSH:

#### 1. Brute-force атаки

**Проблема:** Автоматичні спроби підібрати пароль.

```bash
# Ознаки brute-force в логах
sudo grep "Failed password" /var/log/auth.log

# Приклад:
# Failed password for root from 192.0.2.100 port 42345 ssh2
# Failed password for admin from 192.0.2.100 port 42346 ssh2
# Failed password for user from 192.0.2.100 port 42347 ssh2
```

**Захист:**

```bash
# 1. Вимкнути password authentication
PasswordAuthentication no

# 2. Fail2ban
sudo apt install fail2ban

# /etc/fail2ban/jail.local
[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600

sudo systemctl restart fail2ban

# Перевірити статус
sudo fail2ban-client status sshd

# 3. MaxAuthTries
MaxAuthTries 3

# 4. Змінити порт (security through obscurity)
Port 2222

# 5. AllowUsers whitelist
AllowUsers john jane
```

#### 2. Man-in-the-Middle (MITM) атаки

**Проблема:** Хакер перехоплює з'єднання між клієнтом і сервером.

```bash
# При першому підключенні
ssh user@new-server.com
The authenticity of host 'new-server.com (192.0.2.1)' can't be established.
ED25519 key fingerprint is SHA256:abc123...
Are you sure you want to continue connecting (yes/no)?

# ⚠️ ЗАВЖДИ ПЕРЕВІРЯТИ FINGERPRINT!
```

**Захист:**

```bash
# 1. Перевірити fingerprint через альтернативний канал
# (телефон, SMS, інший secure channel)

# На сервері показати fingerprint
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
# 256 SHA256:abc123def456... root@server (ED25519)

# 2. Використовувати SSH certificates
# (CA підписує ключі → не потрібно перевіряти кожен сервер)

# 3. StrictHostKeyChecking
# ~/.ssh/config
Host *
    StrictHostKeyChecking ask
    # або
    StrictHostKeyChecking yes  # (для автоматизації)
```

#### 3. SSH Key Theft

**Проблема:** Крадіжка приватного ключа.

**Захист:**

```bash
# 1. Завжди використовувати passphrase
ssh-keygen -t ed25519 -C "john@example.com"
Enter passphrase (empty for no passphrase): ********

# 2. Правильні permissions
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
chmod 600 ~/.ssh/authorized_keys

# 3. Обмежити ключ в authorized_keys
# ~/.ssh/authorized_keys
command="/usr/bin/backup",no-port-forwarding,no-X11-forwarding,no-agent-forwarding ssh-ed25519 AAAAC3... backup-key

from="192.0.2.0/24" ssh-ed25519 AAAAC3... office-key

# 4. Certificate expiration
# Використовувати SSH certificates з validity period

# 5. Регулярно ротувати ключі
# Генерувати нові ключі кожні 6-12 місяців
```

#### 4. Timing Attacks

**Проблема:** Аналіз часу відповідей для витягування інформації.

**Захист:**

```bash
# Використовувати сучасні алгоритми
# Ed25519 - immune to timing attacks
# ChaCha20-Poly1305 - immune to timing attacks

KexAlgorithms curve25519-sha256
HostKeyAlgorithms ssh-ed25519
Ciphers chacha20-poly1305@openssh.com
```

#### 5. Port Scanning та Service Enumeration

**Проблема:** Хакери сканують порти для знаходження SSH серверів.

**Захист:**

```bash
# 1. Змінити стандартний порт
Port 2222

# 2. Firewall (iptables / ufw)
sudo ufw allow from 192.168.1.0/24 to any port 22
sudo ufw enable

# 3. Port knocking
# Складна техніка: потрібна послідовність підключень до портів перед відкриттям SSH

# 4. VPN перед SSH
# Доступ до SSH тільки через VPN
```

### Моніторинг та аудит SSH:

```bash
# 1. Переглянути активні SSH сесії
who
w
last

# 2. Переглянути SSH логи
sudo tail -f /var/log/auth.log
sudo journalctl -u sshd -f

# 3. Переглянути невдалі спроби входу
sudo grep "Failed password" /var/log/auth.log | tail -20

# 4. Переглянути успішні входи
sudo grep "Accepted" /var/log/auth.log | tail -20

# 5. Netstat - активні SSH з'єднання
sudo netstat -tnpa | grep 'ESTABLISHED.*sshd'

# 6. Моніторинг з Fail2ban
sudo fail2ban-client status sshd

# 7. Аудит SSH ключів
# Перевірити authorized_keys на всіх серверах
for key in $(cat ~/.ssh/authorized_keys); do
    ssh-keygen -lf /dev/stdin <<< "$key"
done
```

### Найкращі практики SSH (2024):

```
✅ Використовувати Ed25519 ключі (не RSA 2048)
✅ Вимкнути password authentication
✅ Вимкнути root login
✅ Використовувати Fail2ban
✅ Обмежити користувачів (AllowUsers)
✅ Змінити стандартний порт (опціонально)
✅ Використовувати SSH certificates для масштабу
✅ Увімкнути MFA (publickey + keyboard-interactive)
✅ Регулярно аудитувати authorized_keys
✅ Використовувати SSH agent з обмеженим часом життя
✅ Обмежувати agent forwarding
✅ Моніторити логи
✅ Оновлювати OpenSSH регулярно
✅ Використовувати firewall
✅ Обмежувати IP адреси (якщо можливо)
✅ Використовувати StrictHostKeyChecking
✅ Backup приватних ключів в безпечному місці
✅ Використовувати різні ключі для різних серверів
✅ Не використовувати один ключ для всього
✅ Документувати всі ключі та їх призначення
```

### Security Checklist:

```bash
# /etc/ssh/sshd_config перевірка

✅ Protocol 2
✅ PermitRootLogin no
✅ PasswordAuthentication no
✅ PermitEmptyPasswords no
✅ ChallengeResponseAuthentication no
✅ PubkeyAuthentication yes
✅ AuthorizedKeysFile .ssh/authorized_keys
✅ MaxAuthTries 3
✅ AllowUsers john jane
✅ ClientAliveInterval 60
✅ ClientAliveCountMax 3
✅ UsePAM yes
✅ X11Forwarding no  (якщо не потрібно)
✅ AllowTcpForwarding yes  (якщо потрібно)
✅ AllowAgentForwarding yes  (обережно)
✅ Compression yes
✅ UseDNS no
✅ LogLevel VERBOSE
✅ Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com
✅ MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
✅ KexAlgorithms curve25519-sha256
✅ HostKey /etc/ssh/ssh_host_ed25519_key
```

### Інструменти для перевірки безпеки SSH:

```bash
# 1. ssh-audit (автоматична перевірка)
# https://github.com/jtesta/ssh-audit
python3 ssh-audit.py example.com

# 2. Lynis (security audit)
sudo apt install lynis
sudo lynis audit system

# 3. OpenVAS / Nessus (vulnerability scanner)

# 4. nmap
nmap -p 22 --script ssh2-enum-algos example.com
nmap -p 22 --script ssh-auth-methods example.com

# 5. Власний скрипт перевірки
ssh -vv user@example.com 2>&1 | grep -E "kex:|cipher:|MAC:"
```

---

## Висновок

SSH - потужний та безпечний протокол для віддаленого доступу. Ключові моменти:

### Сучасний SSH стек (2024):

```
✅ Protocol: SSH-2 (ТІЛЬКИ!)
✅ Key Exchange: Curve25519
✅ Host Key: Ed25519
✅ Cipher: ChaCha20-Poly1305 або AES-GCM
✅ MAC: HMAC-SHA2-ETM (або implicit з AEAD)
✅ Authentication: Public Key (Ed25519)
✅ MFA: Public Key + Keyboard-Interactive
✅ Port Forwarding: Local, Remote, Dynamic
✅ Multiplexing: Для швидкості
✅ Keep-Alive: Для надійності
✅ Monitoring: Логи + Fail2ban
```

### Основні переваги SSH:

```
✅ Шифрування всього трафіку
✅ Сильна криптографія (Ed25519, ChaCha20)
✅ Множинні методи аутентифікації
✅ Port forwarding / тунелювання
✅ File transfer (SFTP, SCP)
✅ X11 forwarding
✅ Мультиплексування
✅ Стабільність та надійність
✅ Open source (OpenSSH)
✅ Підтримується всюди
```

### Ресурси для вивчення:

- **RFC 4251-4254** - SSH Protocol specifications
- **OpenSSH Manual** - https://www.openssh.com/manual.html
- **SSH Mastery** (книга Michael W. Lucas)
- **Mozilla SSH Guidelines** - https://infosec.mozilla.org/guidelines/openssh
- **ssh-audit** - https://github.com/jtesta/ssh-audit

**Успіхів у безпечному використанні SSH!** 🔒

---

**Кінець посібника SSH Protocol**
