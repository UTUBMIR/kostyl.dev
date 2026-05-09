# Промпт для покращення статті про Deployment

## Контекст

Потрібно повністю переробити статтю про Deployment у Kubernetes за тими ж принципами, що й статті про Pod.

## Вихідні файли

- Поточна стаття: `content/07.tools/02.kubernetes/05.workloads-deployments.md` (~649 рядків)
- Попередні статті (для контексту):
  - `content/07.tools/02.kubernetes/04.pods-and-containers.md` (1368 рядків)
  - `content/07.tools/02.kubernetes/05.pod-patterns.md` (1249 рядків)

## Вимоги

### Структура: 2 статті

**Стаття 1: "Deployment — декларативне управління Pod"**
- Проблема, яку вирішує Deployment (чому не Pod напряму)
- Що таке Deployment (формальне визначення)
- Повна YAML специфікація (всі поля детально через ::field-group)
- Створення першого Deployment
- ReplicaSet (що це і навіщо)
- Self-healing у дії
- Масштабування (3 способи)
- .NET приклад: TodoApi через Deployment з 3 репліками (повний код)
- Практичні завдання

**Стаття 2: "Rolling Updates та управління життєвим циклом Deployment"**
- Що таке Rolling Updates (від А до Я, максимально детально для новачка)
- Як працює Rolling Update (візуалізація через PlantUML)
- Стратегії оновлення (RollingUpdate vs Recreate)
- Параметри: maxSurge, maxUnavailable, progressDeadlineSeconds, minReadySeconds (з математичними розрахунками)
- Health checks з .NET (readiness/liveness probes для ASP.NET Core)
- Resource management для .NET (memory, CPU limits та що відбувається при перевищенні)
- Rollback та історія версій
- .NET приклад: оновлення TodoApi з v1.0 на v2.0 з реальними змінами в коді (додавання нового endpoint)
- Troubleshooting (типові проблеми та їх вирішення)
- Практичні завдання

### Принципи написання

1. **Видалити весь існуючий контент** і почати заново
2. **Максимально детально** — новачок має зрозуміти від А до Я
3. **Багато PlantUML діаграм** для візуалізації концепцій
4. **Всі .NET приклади самодостатні** — можна копіювати і запускати
5. **Повна специфікація YAML** — кожне поле через ::field-group з детальним поясненням
6. **Поступове введення** — від простого до складного
7. **Мінімум аналогій** — лише там, де доречно
8. **Використання компонентів Docus** — field-group, card-group, terminal-preview, plant-uml
9. **Академічний підхід** — як у книзі, з детальними поясненнями
10. **Проблемно-орієнтований** — спочатку проблема, потім рішення

### .NET приклади

1. **TodoApi через Deployment** (Стаття 1):
   - Повний код ASP.NET Core Minimal API
   - Dockerfile
   - Deployment YAML з 3 репліками
   - Збірка, завантаження в Minikube, розгортання
   - Тестування через port-forward

2. **Rolling update з реальним оновленням** (Стаття 2):
   - TodoApi v1.0 (базовий CRUD)
   - TodoApi v2.0 (додавання нового endpoint, наприклад, статистика)
   - Процес оновлення з візуалізацією
   - Що відбувається з трафіком під час update

3. **Health checks з .NET** (Стаття 2):
   - Readiness probe для ASP.NET Core
   - Liveness probe для ASP.NET Core
   - Як вони впливають на rolling update
   - Приклад з затримкою старту (startup probe)

4. **Resource management** (Стаття 2):
   - Налаштування requests/limits для .NET
   - Що відбувається при OOMKilled
   - Garbage collection та memory limits

### Технічні деталі

- Використовувати Kubernetes 1.30+
- .NET 8.0
- PostgreSQL 16 (якщо потрібна БД)
- Minikube для локального тестування
- Всі команди через kubectl

### Формат прикладів

- Повний код проєкту в статті
- Детальні коментарі в YAML
- Terminal previews для демонстрації команд
- PlantUML діаграми для візуалізації процесів

### Обсяг

- Стаття 1: ~1200-1500 рядків
- Стаття 2: ~1200-1500 рядків
- Загалом: ~2400-3000 рядків

## Файли для створення

1. `content/07.tools/02.kubernetes/06.deployment-basics.md` (нова Стаття 1)
2. `content/07.tools/02.kubernetes/07.deployment-rolling-updates.md` (нова Стаття 2)

## Примітки

- Не забігати вперед (не згадувати Service, Ingress тощо, якщо вони ще не вивчені)
- Кластер вже є (Minikube)
- Читач вже знає Docker та Pod
- Фокус на практиці — кожна концепція має практичний приклад
