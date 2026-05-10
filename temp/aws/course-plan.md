# Тематичний план курсу "Створення хмарних рішень з використанням AWS"

## Загальна інформація

- **Цільова аудиторія:** Middle .NET/React розробники (1-3 роки досвіду)
- **Рівень хмарного досвіду:** Початківці в AWS
- **Співвідношення:** 50% теорія / 50% практика
- **Структура:** Послідовна, від простого до складного
- **Особливість:** Всі теми розглядаються через призму .NET та React екосистем

---

### **Модуль 14: Amazon Cognito - User Authentication** (2 заняття)

**Теорія:**

- Cognito User Pools vs Identity Pools
- User Pool Features (Sign-up, Sign-in, MFA, Password policies)
- OAuth 2.0 та OpenID Connect
- Cognito Hosted UI
- Social Identity Providers (Google, Facebook)
- Cognito Triggers (Lambda)
- JWT tokens (ID token, Access token, Refresh token)
- Cognito Groups та Custom Attributes

**Практика:**

- Створення Cognito User Pool
- Інтеграція Cognito з React (AWS Amplify)
- Захист API Gateway через Cognito
- Налаштування MFA
- Налаштування Lambda triggers

**Лабораторна робота:**

- Створити Cognito User Pool
- Реалізувати Sign-up/Sign-in в React з Amplify
- Захистити API Gateway endpoints через Cognito authorizer
- Налаштувати MFA
- Додати Google Social Login

**Специфіка для .NET:**

- Валідація Cognito JWT tokens в .NET Web API
- AWS SDK for .NET - Cognito Admin APIs
- Microsoft.AspNetCore.Authentication.JwtBearer

**Специфіка для React:**

- AWS Amplify Auth для React
- Cognito Hosted UI інтеграція
- @aws-amplify/ui-react components

---

### **Модуль 15: AWS Amplify для React додатків** (2 заняття)

**Теорія:**

- AWS Amplify архітектура
- Amplify Hosting vs S3 + CloudFront
- Amplify CLI
- Amplify Libraries (Auth, API, Storage)
- Amplify CI/CD з GitHub
- Amplify Environment Management
- Amplify Studio

**Практика:**

- Деплой React додатку через Amplify Hosting
- Налаштування CI/CD з GitHub
- Використання Amplify Auth, API, Storage в React
- Preview deployments для Pull Requests
- Налаштування custom domain

**Лабораторна робота:**

- Задеплоїти React додаток через Amplify Hosting
- Налаштувати автоматичний деплой з GitHub
- Інтегрувати Amplify Auth та API в React
- Налаштувати environment variables

**Специфіка для React:**

- Amplify UI Components для React
- Amplify DataStore для offline-first додатків
- Server-Side Rendering з Amplify (Next.js)

---

### **Модуль 16: Amazon SQS та SNS - Messaging Services** (2 заняття)

**Теорія:**

- Amazon SQS (Simple Queue Service) - Standard vs FIFO
- SQS Message Visibility Timeout, Dead Letter Queues
- Amazon SNS (Simple Notification Service)
- SNS Topics, Subscriptions (Email, SMS, HTTP, Lambda, SQS)
- Fan-out pattern (SNS → SQS)
- EventBridge vs SNS vs SQS
- Message filtering в SNS

**Практика:**

- Створення SQS черги
- Відправка та отримання повідомлень через .NET
- Створення SNS topic з множинними subscriptions
- Реалізація fan-out pattern
- Налаштування Dead Letter Queue

**Лабораторна робота:**

- Створити SQS чергу для асинхронної обробки
- Реалізувати .NET Worker Service для обробки SQS повідомлень
- Налаштувати SNS для нотифікацій
- Реалізувати fan-out pattern (SNS → multiple SQS)

**Специфіка для .NET:**

- AWS SDK for .NET - SQS та SNS
- Background services в .NET для обробки черг
- Hosted Services для SQS polling
- AWSSDK.SQS та AWSSDK.SimpleNotificationService

---

### **Модуль 17: Amazon EventBridge** (1 заняття)

**Теорія:**

- EventBridge Event Bus
- EventBridge Rules та Targets
- Event Patterns
- Scheduled Events (Cron)
- EventBridge Schema Registry
- EventBridge vs CloudWatch Events
- EventBridge Pipes
- Cross-account event delivery

**Практика:**

- Створення EventBridge rules
- Інтеграція з Lambda та SQS
- Scheduled Lambda executions
- Custom event patterns

**Лабораторна робота:**

- Створити EventBridge rule для щоденного запуску Lambda
- Налаштувати event pattern для S3 events
- Створити custom event bus
- Налаштувати cross-account event delivery

**Специфіка для .NET:**

- Відправка custom events з .NET через EventBridge
- AWSSDK.EventBridge

---

### **Модуль 18: AWS Secrets Manager та Parameter Store** (1 заняття)

**Теорія:**

- AWS Secrets Manager vs Systems Manager Parameter Store
- Secrets rotation
- Encryption з KMS
- IAM permissions для secrets
- Best practices для credentials management
- Secrets Manager pricing vs Parameter Store

**Практика:**

- Зберігання database connection strings в Secrets Manager
- Отримання secrets в .NET додатку
- Налаштування automatic rotation
- Використання Parameter Store для configuration

**Лабораторна робота:**

- Зберегти RDS credentials в Secrets Manager
- Отримати secrets в .NET Web API через AWS SDK
- Налаштувати Parameter Store для configuration
- Налаштувати automatic rotation для RDS password

**Специфіка для .NET:**

- AWS SDK for .NET - Secrets Manager
- Інтеграція з IConfiguration в ASP.NET Core
- AWSSDK.SecretsManager
- Caching secrets для performance

---

### **Модуль 19: Amazon CloudWatch - Monitoring та Logging** (2 заняття)

**Теорія:**

- CloudWatch Metrics (Standard, Custom)
- CloudWatch Logs (Log Groups, Log Streams)
- CloudWatch Alarms
- CloudWatch Dashboards
- CloudWatch Insights
- CloudWatch Logs Insights Query Language
- CloudWatch Agent
- CloudWatch Contributor Insights

**Практика:**

- Налаштування CloudWatch Logs для .NET додатку
- Створення custom metrics
- Налаштування alarms (CPU, Memory, HTTP errors)
- Створення dashboards
- Queries в CloudWatch Logs Insights

**Лабораторна робота:**

- Налаштувати structured logging в .NET з CloudWatch
- Створити CloudWatch dashboard для моніторингу API
- Налаштувати alarms для критичних метрик
- Написати CloudWatch Logs Insights queries

**Специфіка для .NET:**

- Serilog з CloudWatch Logs sink
- AWS.Logger.AspNetCore для ASP.NET Core
- Custom metrics через AWS SDK
- Structured logging best practices

---

### **Модуль 20: AWS X-Ray - Distributed Tracing** (1 заняття)

**Теорія:**

- X-Ray архітектура
- X-Ray Daemon
- Service Map
- Traces, Segments, Subsegments
- X-Ray Sampling Rules
- X-Ray Annotations та Metadata
- X-Ray Groups

**Практика:**

- Налаштування X-Ray для .NET додатку
- Трейсинг Lambda функцій
- Аналіз performance bottlenecks
- Налаштування sampling rules

**Лабораторна робота:**

- Налаштувати X-Ray для .NET Web API
- Проаналізувати distributed traces
- Знайти performance issues через Service Map
- Налаштувати custom segments

**Специфіка для .NET:**

- AWS X-Ray SDK for .NET
- Інтеграція з ASP.NET Core middleware
- AWSXRayRecorder.Core NuGet package

---

### **Модуль 21: CI/CD з GitHub Actions та AWS** (2 заняття)

**Теорія:**

- GitHub Actions workflows
- AWS credentials в GitHub Secrets
- OIDC для GitHub Actions з AWS
- Deployment strategies (Blue/Green, Canary)
- Infrastructure as Code (CloudFormation, CDK) - огляд
- GitHub Actions best practices

**Практика:**

- Створення GitHub Actions workflow для .NET
- Автоматичний build та деплой на ECS
- Деплой React на S3 + CloudFront invalidation
- Автоматичне тестування перед деплоєм
- Multi-environment deployments

**Лабораторна робота:**

- Налаштувати GitHub Actions для .NET Web API (build → test → deploy to ECS)
- Налаштувати GitHub Actions для React (build → deploy to S3 → invalidate CloudFront)
- Реалізувати multi-environment deployments (dev, staging, prod)
- Налаштувати OIDC authentication з AWS

**Специфіка для .NET:**

- dotnet build, test, publish в GitHub Actions
- Docker build для .NET в CI/CD
- NuGet package caching

**Специфіка для React:**

- npm build в GitHub Actions
- S3 sync та CloudFront invalidation
- Environment-specific builds

---

### **Модуль 22: AWS AI/ML Services - Amazon Bedrock** (2 заняття)

**Теорія:**

- Amazon Bedrock архітектура
- Foundation Models (Claude, Llama, Titan, Stable Diffusion)
- Bedrock Agents
- Bedrock Knowledge Bases
- Prompt Engineering
- Bedrock Pricing
- Bedrock Guardrails
- Model customization

**Практика:**

- Виклик Bedrock API з .NET
- Інтеграція Claude в React чат-додаток
- Створення RAG (Retrieval-Augmented Generation) з Knowledge Bases
- Streaming responses

**Лабораторна робота:**

- Створити .NET API для Bedrock Claude
- Реалізувати React чат-інтерфейс
- Налаштувати streaming responses
- Створити Knowledge Base з S3 документами

**Специфіка для .NET:**

- AWS SDK for .NET - Bedrock Runtime
- Streaming responses в ASP.NET Core
- AWSSDK.BedrockRuntime

**Специфіка для React:**

- Server-Sent Events для streaming в React
- Markdown rendering для AI responses
- Chat UI components

---

### **Модуль 23: AWS AI/ML Services - Rekognition, Transcribe, Polly** (2 заняття)

**Теорія:**

- Amazon Rekognition (Image/Video analysis)
    - Face detection, recognition
    - Object and scene detection
    - Text in image (OCR)
    - Content moderation
- Amazon Transcribe (Speech-to-Text)
    - Real-time transcription
    - Batch transcription
    - Custom vocabulary
- Amazon Polly (Text-to-Speech)
    - Neural voices
    - SSML support
- Amazon Translate
- Use cases для кожного сервісу

**Практика:**

- Розпізнавання облич через Rekognition
- Транскрипція аудіо через Transcribe
- Генерація мовлення через Polly
- Інтеграція з React для upload та обробки

**Лабораторна робота:**

- Створити .NET API для upload зображень в S3
- Обробити зображення через Rekognition
- Відобразити результати в React додатку
- Реалізувати audio transcription з Transcribe

**Специфіка для .NET:**

- AWS SDK for .NET - Rekognition, Transcribe, Polly
- AWSSDK.Rekognition, AWSSDK.TranscribeService, AWSSDK.Polly

**Специфіка для React:**

- File upload в React з progress bar
- Відображення AI результатів
- Audio player для Polly output

---

### **Модуль 24: AWS VPC - Virtual Private Cloud** (2 заняття)

**Теорія:**

- VPC основи (CIDR blocks, Subnets)
- Public vs Private Subnets
- Internet Gateway та NAT Gateway
- Route Tables
- Security Groups vs Network ACLs
- VPC Peering
- VPC Endpoints (Gateway, Interface)
- VPC Flow Logs

**Практика:**

- Створення custom VPC
- Налаштування public та private subnets
- Деплой EC2 в private subnet
- Налаштування NAT Gateway
- Налаштування VPC Endpoints для S3

**Лабораторна робота:**

- Створити custom VPC з public та private subnets
- Задеплоїти .NET API в private subnet
- Налаштувати ALB в public subnet
- Налаштувати VPC Endpoint для S3
- Налаштувати VPC Flow Logs

---

### **Модуль 25: AWS Route 53 - DNS Service** (1 заняття)

**Теорія:**

- Route 53 Hosted Zones
- DNS Record Types (A, AAAA, CNAME, MX, TXT)
- Routing Policies (Simple, Weighted, Latency, Failover, Geolocation)
- Route 53 Health Checks
- Domain Registration
- Route 53 Alias Records

**Практика:**

- Створення Hosted Zone
- Налаштування custom domain для ALB
- Налаштування custom domain для CloudFront
- Налаштування health checks

**Лабораторна робота:**

- Налаштувати custom domain для React додатку (CloudFront)
- Налаштувати custom domain для .NET API (ALB)
- Налаштувати health checks та failover routing

**Специфіка для React:**

- Custom domain для React SPA на CloudFront

---

### **Модуль 26: AWS Cost Optimization та Best Practices** (1 заняття)

**Теорія:**

- AWS Pricing Calculator
- AWS Cost Explorer
- AWS Budgets та Alerts
- Cost Optimization Strategies
- Reserved Instances vs Savings Plans
- Spot Instances
- S3 Lifecycle Policies
- Right-sizing EC2 instances
- AWS Well-Architected Framework Review
- AWS Trusted Advisor

**Практика:**

- Аналіз поточних витрат через Cost Explorer
- Налаштування Budget alerts
- Оптимізація S3 storage з Lifecycle Policies
- Right-sizing recommendations

**Лабораторна робота:**

- Створити AWS Budget з email alerts
- Проаналізувати витрати через Cost Explorer
- Налаштувати S3 Lifecycle Policy для архівування
- Переглянути Trusted Advisor recommendations

---

**Теорія:**

- S3 Buckets, Objects, Keys
- S3 Storage Classes (Standard, IA, Glacier, Intelligent-Tiering)
- S3 Versioning, Lifecycle Policies
- S3 Security (Bucket Policies, ACLs, Encryption)
- S3 Static Website Hosting
- S3 CORS configuration
- S3 Transfer Acceleration
- S3 Event Notifications
- S3 Presigned URLs

**Практика:**

- Створення S3 bucket
- Завантаження файлів через консоль та AWS CLI
- Налаштування static website hosting для React SPA
- Робота з S3 через AWS SDK for .NET
- Налаштування S3 bucket policies

**Лабораторна робота:**

- Створити S3 bucket для React додатку
- Налаштувати static website hosting
- Завантажити build React додатку
- Налаштувати CORS для API запитів
- Створити presigned URL для приватних файлів

**Специфіка для .NET:**

- AWS SDK for .NET - робота з S3 (upload, download, presigned URLs)
- Інтеграція S3 з .NET для зберігання файлів
- Streaming uploads для великих файлів
- S3 Transfer Utility для .NET

**Специфіка для React:**

- Деплой React SPA на S3
- Налаштування routing для SPA (index.html fallback)
- Upload файлів з React на S3

---

### **Модуль 7: Amazon CloudFront - Content Delivery Network** (1 заняття)

**Теорія:**

- CloudFront Origins (S3, ALB, Custom)
- CloudFront Distributions
- Edge Locations та Regional Edge Caches
- CloudFront Cache Behaviors
- CloudFront SSL/TLS certificates (ACM)
- CloudFront Functions vs Lambda@Edge
- CloudFront Invalidations
- CloudFront Origin Access Identity (OAI)

**Практика:**

- Створення CloudFront distribution для React SPA
- Налаштування custom domain з Route 53
- Інвалідація кешу після деплою
- HTTPS налаштування з ACM
- Налаштування cache behaviors

**Лабораторна робота:**

- Створити CloudFront distribution для S3 bucket з React додатком
- Налаштувати SSL сертифікат через ACM
- Налаштувати custom error pages (404 → index.html)
- Протестувати cache invalidation

**Специфіка для React:**

- Оптимізація React SPA з CloudFront
- Cache-Control headers для React assets
- Versioning стратегії для React builds

---

### **Модуль 8: Amazon RDS - Relational Database Service** (3 заняття)

**Теорія:**

- RDS Engines (PostgreSQL, MySQL, SQL Server, Oracle, MariaDB)
- RDS Instance Types та Pricing
- Multi-AZ Deployments для High Availability
- Read Replicas для масштабування читання
- RDS Backups (Automated, Manual Snapshots)
- RDS Security (Security Groups, Encryption at rest/in transit)
- Amazon Aurora (MySQL/PostgreSQL compatible)
- Aurora Serverless v2
- RDS Proxy для connection pooling

**Практика:**

- Створення RDS PostgreSQL інстансу
- Створення RDS SQL Server для .NET Framework додатків
- Підключення до RDS з .NET через Entity Framework Core
- Налаштування Multi-AZ та Read Replicas
- Міграція локальної БД на RDS
- Налаштування RDS Proxy

**Лабораторна робота:**

- Створити RDS PostgreSQL інстанс
- Підключити .NET Web API через EF Core
- Виконати Code-First міграції на RDS
- Налаштувати automated backups
- Створити Read Replica та протестувати

**Специфіка для .NET:**

- Entity Framework Core з RDS PostgreSQL/MySQL
- SQL Server на RDS для .NET Framework додатків
- Connection strings та secrets management
- EF Core migrations на RDS
- Npgsql для PostgreSQL
- Pomelo.EntityFrameworkCore.MySql для MySQL

---

### **Модуль 9: Amazon DynamoDB - NoSQL Database** (2 заняття)

**Теорія:**

- DynamoDB Tables, Items, Attributes
- Primary Keys (Partition Key, Sort Key)
- Secondary Indexes (GSI, LSI)
- DynamoDB Capacity Modes (Provisioned, On-Demand)
- DynamoDB Streams
- DynamoDB Transactions
- DynamoDB Best Practices (Hot Partitions, Query vs Scan)
- DynamoDB TTL (Time To Live)
- DynamoDB Global Tables

**Практика:**

- Створення DynamoDB таблиці
- CRUD операції через консоль та AWS CLI
- Робота з DynamoDB через AWS SDK for .NET
- Проектування схеми для NoSQL
- Налаштування GSI та LSI

**Лабораторна робота:**

- Створити DynamoDB таблицю для сесій користувачів
- Реалізувати CRUD API на .NET з DynamoDB
- Налаштувати GSI для пошуку
- Реалізувати pagination з LastEvaluatedKey

**Специфіка для .NET:**

- AWS SDK for .NET - DynamoDB Document Model
- DynamoDB Object Persistence Model для .NET
- Порівняння EF Core (RDS) vs DynamoDB підходів
- AWSSDK.DynamoDBv2 NuGet package

---

### **Модуль 10: Amazon ElastiCache - In-Memory Caching** (1 заняття)

**Теорія:**

- ElastiCache Redis vs Memcached
- Redis Cluster Mode
- ElastiCache для сесій та кешування
- Redis data structures
- ElastiCache Security (Encryption, Auth)
- Redis persistence options

**Практика:**

- Створення ElastiCache Redis cluster
- Інтеграція Redis з .NET (StackExchange.Redis)
- Кешування API responses
- Distributed caching для ASP.NET Core

**Лабораторна робота:**

- Створити ElastiCache Redis cluster
- Налаштувати distributed cache в .NET Web API
- Реалізувати кешування для дорогих запитів
- Налаштувати session state в Redis

**Специфіка для .NET:**

- IDistributedCache з ElastiCache Redis
- Session state в Redis для ASP.NET Core
- StackExchange.Redis для .NET
- Cache-aside pattern реалізація

---

### **Модуль 11: AWS Lambda - Serverless Compute** (3 заняття)

**Теорія:**

- Serverless архітектура
- Lambda функції, Runtimes, Layers
- Lambda Triggers (S3, DynamoDB, API Gateway, EventBridge)
- Lambda Pricing та Limits
- Cold Start vs Warm Start
- Lambda Environment Variables та Secrets
- Lambda Destinations
- Lambda Performance Optimization
- Lambda Provisioned Concurrency

**Практика:**

- Створення Lambda функції на .NET 8
- Деплой Lambda через AWS CLI та Visual Studio
- Налаштування triggers (S3, API Gateway)
- Моніторинг Lambda через CloudWatch
- Оптимізація cold start

**Лабораторна робота:**

- Створити Lambda функцію на .NET для обробки S3 events
- Створити HTTP API через API Gateway + Lambda
- Налаштувати Lambda Layer для спільних залежностей
- Налаштувати environment variables та secrets

**Специфіка для .NET:**

- AWS Lambda .NET Runtime
- AWS Toolkit for Visual Studio/Rider
- Lambda function handlers в .NET
- Оптимізація cold start для .NET Lambda
- Amazon.Lambda.Core NuGet package
- Lambda Annotations framework для .NET

---

### **Модуль 12: Amazon API Gateway** (2 заняття)

**Теорія:**

- REST API vs HTTP API vs WebSocket API
- API Gateway Integration Types (Lambda, HTTP, AWS Services)
- API Gateway Stages та Deployments
- API Gateway Authorization (IAM, Cognito, Lambda Authorizers)
- API Gateway Throttling та Usage Plans
- API Gateway CORS
- API Gateway Request/Response Transformations
- API Gateway Caching
- API Gateway Custom Domains

**Практика:**

- Створення REST API для .NET Lambda функцій
- Налаштування CORS для React додатку
- Створення API Keys та Usage Plans
- Інтеграція з Cognito для авторизації
- Налаштування custom domain

**Лабораторна робота:**

- Створити REST API з кількома endpoints (Lambda backend)
- Налаштувати Cognito authorizer
- Підключити React додаток до API Gateway
- Налаштувати throttling та usage plans

**Специфіка для .NET:**

- Lambda proxy integration з .NET
- Request/Response mapping для .NET Lambda

**Специфіка для React:**

- Axios/Fetch з API Gateway
- Обробка CORS в React + API Gateway
- JWT token management в React

---

### **Модуль 13: AWS Elastic Beanstalk** (2 заняття)

**Теорія:**

- Elastic Beanstalk архітектура
- Beanstalk Environments (Web Server, Worker)
- Beanstalk Platforms (.NET, Node.js, Docker)
- Beanstalk Deployment Strategies (All at once, Rolling, Blue/Green)
- Beanstalk Configuration Files (.ebextensions)
- Beanstalk vs ECS vs Lambda
- Beanstalk Environment Properties
- Beanstalk Health Monitoring

**Практика:**

- Деплой .NET Web API на Elastic Beanstalk
- Налаштування environment variables
- Blue/Green deployment
- Інтеграція з RDS
- Налаштування Auto Scaling

**Лабораторна робота:**

- Задеплоїти .NET Web API на Elastic Beanstalk
- Налаштувати RDS PostgreSQL через Beanstalk
- Виконати rolling deployment
- Налаштувати custom domain

**Специфіка для .NET:**

- Elastic Beanstalk для .NET Core/.NET 8
- Деплой через AWS Toolkit for Visual Studio
- Налаштування IIS через .ebextensions
- aws-windows-deployment-manifest.json

---

**Теорія:**

- Що таке хмарні обчислення (IaaS, PaaS, SaaS, FaaS)
- Порівняння AWS vs Azure vs GCP
- AWS Global Infrastructure (Regions, Availability Zones, Edge Locations)
- AWS Well-Architected Framework (5 pillars: Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization)
- Створення AWS Account, AWS Free Tier
- AWS Management Console, AWS CLI, AWS CloudShell
- AWS Service Categories (Compute, Storage, Database, Networking, Security, etc.)

**Практика:**

- Реєстрація AWS акаунту (якщо не зроблено в Модулі 0)
- Налаштування AWS CLI на локальній машині
- Перший запуск EC2 інстансу через консоль
- Базові команди AWS CLI (aws s3 ls, aws ec2 describe-instances)
- Огляд AWS Management Console

**Лабораторна робота:**

- Створити AWS акаунт, налаштувати MFA
- Встановити AWS CLI та виконати базові команди
- Запустити безкоштовний EC2 t2.micro інстанс
- Підключитись до EC2 через SSH
- Зупинити та видалити EC2 інстанс

---

### **Модуль 2: AWS IAM - Identity and Access Management** (2 заняття)

**Теорія:**

- IAM Users, Groups, Roles, Policies
- Принцип найменших привілеїв (Least Privilege)
- IAM Policy структура (JSON)
- MFA (Multi-Factor Authentication)
- AWS Organizations для управління множинними акаунтами
- Service Control Policies (SCPs)
- IAM Best Practices для розробників
- IAM Access Analyzer
- AWS STS (Security Token Service)

**Практика:**

- Створення IAM користувачів та груп
- Написання custom IAM policies
- Налаштування IAM ролей для EC2 та Lambda
- Використання AWS STS для temporary credentials
- Налаштування MFA для IAM користувачів

**Лабораторна робота:**

- Створити IAM користувача для розробника з обмеженими правами
- Налаштувати IAM роль для EC2 з доступом до S3
- Написати custom policy для Lambda функції
- Протестувати доступ через AWS CLI з різними credentials

**Специфіка для .NET:**

- Використання AWS SDK for .NET з IAM credentials
- Налаштування AWS credentials в Visual Studio/Rider
- AWS Toolkit for Visual Studio
- Профілі credentials (~/.aws/credentials)

---

### **Модуль 3: Docker та контейнеризація в AWS** (2 заняття)

**Теорія:**

- Amazon ECR (Elastic Container Registry)
- Amazon ECS (Elastic Container Service) - архітектура
- AWS Fargate vs EC2 launch types
- ECS Task Definitions, Services, Clusters
- Amazon EKS (Elastic Kubernetes Service) - огляд
- Порівняння ECS vs EKS vs Fargate
- ECS Service Auto Scaling
- ECS Task Networking (awsvpc mode)

**Практика:**

- Створення Docker образу для .NET Web API
- Push образу в Amazon ECR
- Деплой .NET додатку на ECS Fargate
- Налаштування Auto Scaling для ECS
- Налаштування Application Load Balancer для ECS

**Лабораторна робота:**

- Контейнеризувати простий .NET Web API
- Завантажити образ в ECR
- Задеплоїти на ECS Fargate з публічним доступом
- Налаштувати health checks
- Протестувати rolling updates

**Специфіка для .NET:**

- Dockerfile для .NET 8 додатків
- Multi-stage builds для оптимізації розміру образу
- Налаштування health checks для .NET в ECS
- Environment variables в ECS Task Definitions

---

### **Модуль 4: Amazon EC2 - Elastic Compute Cloud** (3 заняття)

**Теорія:**

- EC2 Instance Types (General Purpose, Compute Optimized, Memory Optimized)
- AMI (Amazon Machine Images)
- EC2 Pricing Models (On-Demand, Reserved, Spot, Savings Plans)
- Security Groups vs NACLs
- EC2 User Data для автоматизації
- Elastic IP addresses
- EC2 Instance Metadata Service (IMDS)
- EBS (Elastic Block Store) volumes
- EC2 Instance Connect

**Практика:**

- Запуск Windows Server для .NET Framework додатків
- Запуск Linux для .NET Core/.NET 8 додатків
- Налаштування Security Groups
- Підключення до EC2 через SSH/RDP
- Деплой .NET додатку на EC2
- Створення custom AMI

**Лабораторна робота:**

- Запустити EC2 з Windows Server
- Встановити .NET SDK та IIS
- Задеплоїти ASP.NET Core додаток
- Налаштувати Security Group для HTTP/HTTPS доступу
- Створити AMI з налаштованим сервером

**Специфіка для .NET:**

- Вибір AMI для .NET додатків
- Налаштування IIS на Windows Server EC2
- Деплой .NET Framework vs .NET Core додатків
- Systemd service для .NET на Linux

---

### **Модуль 5: Elastic Load Balancing та Auto Scaling** (2 заняття)

**Теорія:**

- Application Load Balancer (ALB) - Layer 7
- Network Load Balancer (NLB) - Layer 4
- Gateway Load Balancer
- Target Groups, Health Checks
- Auto Scaling Groups (ASG)
- Scaling Policies (Target Tracking, Step Scaling, Scheduled)
- Launch Templates vs Launch Configurations
- ALB Listener Rules та Path-based routing

**Практика:**

- Створення ALB для .NET Web API
- Налаштування Target Groups
- Створення Auto Scaling Group
- Тестування масштабування під навантаженням
- Налаштування SSL/TLS на ALB

**Лабораторна робота:**

- Створити ALB з двома EC2 інстансами (.NET додаток)
- Налаштувати Auto Scaling Group (min: 2, max: 5)
- Протестувати health checks та автоматичне масштабування
- Налаштувати HTTPS з ACM сертифікатом

**Специфіка для .NET:**

- Налаштування sticky sessions для ASP.NET додатків
- Health check endpoints в .NET (IHealthCheck)
- Distributed caching для масштабованих додатків

---

Модуль 6: Amazon S3 - Simple Storage Service (2 заняття)
Теорія:

- S3 Buckets, Objects, Keys
- S3 Storage Classes (Standard, IA, Glacier, Intelligent-Tiering)
- S3 Versioning, Lifecycle Policies
- S3 Security (Bucket Policies, ACLs, Encryption)
- S3 Static Website Hosting
- S3 CORS configuration
- S3 Transfer Acceleration
  Практика:
- Створення S3 bucket
- Завантаження файлів через консоль та AWS CLI
- Налаштування static website hosting для React SPA
- Робота з S3 через AWS SDK for .NET
  Лабораторна робота:
- Створити S3 bucket для React додатку
- Налаштувати static website hosting
- Завантажити build React додатку
- Налаштувати CORS для API запитів
  Специфіка для .NET:
- AWS SDK for .NET - робота з S3 (upload, download, presigned URLs)
- Інтеграція S3 з .NET для зберігання файлів
  Специфіка для React:
- Деплой React SPA на S3
- Налаштування routing для SPA (index.html fallback)

---

---

### **Модуль 0: Реєстрація AWS акаунту та студентські програми** (1 заняття)

**Теорія:**

**1. AWS Educate - Безкоштовна програма для студентів та викладачів**

- AWS Educate Member Account (без кредитної картки!)
    - $100 AWS credits на рік для студентів
    - $200 AWS credits на рік для викладачів
    - Доступ до AWS Educate Starter Account (обмежений набір сервісів)
    - Безкоштовні навчальні матеріали та labs
- AWS Educate Classroom
    - Викладач створює classroom
    - Студенти отримують promotional credits
    - Централізоване управління доступом

**Реєстрація AWS Educate:**

- Перейти на https://aws.amazon.com/education/awseducate/
- Зареєструватись з університетською email адресою (.edu, .ac.uk, тощо)
- Підтвердити статус студента/викладача (студентський квиток, довідка)
- Отримати доступ до credits та ресурсів

**2. AWS Academy - Офіційна програма для навчальних закладів**

- AWS Academy Learner Lab
    - $100 AWS credits для практичних завдань
    - Sandbox environment з автоматичним reset
    - Доступ до реальних AWS сервісів
- AWS Academy Cloud Foundations
- AWS Academy Cloud Developing
- Вимоги: Навчальний заклад повинен бути членом AWS Academy

**3. GitHub Student Developer Pack + AWS**

- GitHub Student Developer Pack включає AWS credits
- $100-200 AWS promotional credits
- Реєстрація через https://education.github.com/pack
- Вимоги: Студентський email або фото студентського квитка

**4. AWS Free Tier - Безкоштовний рівень для всіх**

- **Always Free** (назавжди безкоштовно):
    - Lambda: 1 млн запитів/місяць
    - DynamoDB: 25 GB storage
    - SNS: 1 млн публікацій/місяць
    - CloudWatch: 10 custom metrics
    - Cognito: 50,000 MAU
- **12 Months Free** (перший рік після реєстрації):
    - EC2: 750 годин t2.micro/t3.micro на місяць
    - S3: 5 GB Standard Storage
    - RDS: 750 годин db.t2.micro, db.t3.micro, db.t4g.micro
    - CloudFront: 1 TB data transfer out
    - Elastic Load Balancing: 750 годин/місяць
- **Trials** (короткострокові пробні періоди):
    - SageMaker: 2 місяці
    - Redshift: 2 місяці
    - Inspector: 15 днів

**5. Стандартна реєстрація AWS акаунту (з кредитною карткою)**

- Потрібна кредитна/дебетова картка для верифікації
- $1 буде списано та повернуто для перевірки
- Доступ до всіх AWS сервісів
- Автоматично активується Free Tier на 12 місяців
- Billing alerts для контролю витрат

**6. AWS Credits для стартапів та проєктів**

- AWS Activate для стартапів (до $100,000 credits)
- AWS Open Source Credits
- AWS Research Credits

**Практика:**

- Порівняння різних варіантів реєстрації
- Вибір оптимального варіанту для курсу
- Налаштування billing alerts
- Огляд AWS Free Tier Dashboard

**Лабораторна робота:**

1. **Варіант A (Рекомендований для студентів):**
    - Зареєструватись в AWS Educate з університетським email
    - Отримати AWS Educate Starter Account або promotional credits
    - Налаштувати billing alerts (якщо є повний акаунт)

2. **Варіант B (Для тих, хто має кредитну картку):**
    - Створити стандартний AWS акаунт
    - Активувати Free Tier
    - Налаштувати AWS Budgets ($10/місяць alert)
    - Налаштувати MFA для root користувача

3. **Варіант C (GitHub Student Pack):**
    - Отримати GitHub Student Developer Pack
    - Активувати AWS promotional credits через GitHub
    - Створити AWS акаунт з цими credits

**Важливі рекомендації:**

- ⚠️ **ЗАВЖДИ налаштовуйте billing alerts!**
- ⚠️ **Видаляйте ресурси після практичних завдань**
- ⚠️ **Використовуйте тільки Free Tier eligible сервіси**
- ⚠️ **Не публікуйте AWS credentials в GitHub**
- ⚠️ **Налаштуйте MFA для root акаунту**

**Корисні посилання:**

- AWS Educate: https://aws.amazon.com/education/awseducate/
- AWS Academy: https://aws.amazon.com/training/awsacademy/
- GitHub Student Pack: https://education.github.com/pack
- AWS Free Tier: https://aws.amazon.com/free/
- AWS Pricing Calculator: https://calculator.aws/

**Порівняльна таблиця:**

| Варіант                 | Credits  | Кредитна картка | Термін               | Обмеження                |
| ----------------------- | -------- | --------------- | -------------------- | ------------------------ |
| AWS Educate Student     | $100/рік | ❌ Не потрібна  | 1 рік                | Обмежений набір сервісів |
| AWS Educate Instructor  | $200/рік | ❌ Не потрібна  | 1 рік                | Обмежений набір сервісів |
| AWS Academy Learner Lab | $100     | ❌ Не потрібна  | Курс                 | Sandbox з reset          |
| GitHub Student Pack     | $100-200 | ✅ Потрібна     | 1-2 роки             | Повний доступ            |
| AWS Free Tier           | $0       | ✅ Потрібна     | 12 міс + Always Free | Ліміти Free Tier         |
| Стандартний акаунт      | $0       | ✅ Потрібна     | Безстроково          | Pay-as-you-go            |

---

Модуль 1: Вступ до хмарних обчислень та AWS (2 заняття)
Теорія:

- Що таке хмарні обчислення (IaaS, PaaS, SaaS, FaaS)
- Порівняння AWS vs Azure vs GCP
- AWS Global Infrastructure (Regions, Availability Zones, Edge Locations)
- AWS Well-Architected Framework (5 pillars)
- Створення AWS Account, AWS Free Tier
- AWS Management Console, AWS CLI, AWS CloudShell
  Практика:
- Реєстрація AWS акаунту
- Налаштування AWS CLI на локальній машині
- Перший запуск EC2 інстансу через консоль
- Базові команди AWS CLI
  Лабораторна робота:
- Створити AWS акаунт, налаштувати MFA
- Встановити AWS CLI та виконати базові команди
- Запустити безкоштовний EC2 t2.micro інстанс
