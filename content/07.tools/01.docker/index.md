# Docker: від нуля до production

Ласкаво просимо до повного практичного курсу з Docker на **kostyl.dev**. 

Тут ви пройдете шлях від повного розуміння концепції контейнеризації до професійного розгортання складних багатоконтейнерних застосунків у production.

---

## Програма курсу

:::card-group

::card{title="1. Контейнеризація" to="/tools/docker/containerization-concept" icon="i-lucide-box"}
Концепція контейнеризації: проблеми розгортання ПЗ, еволюція від bare metal до контейнерів, принципи ізоляції Linux.
::

::card{title="2. Що таке Docker" to="/tools/docker/docker-what-and-why" icon="i-simple-icons-docker"}
Історія Docker, екосистема, роль у сучасній розробці та причини популярності.
::

::card{title="3. Архітектура Docker Engine" to="/tools/docker/docker-architecture" icon="i-lucide-cpu"}
Детальний розбір внутрішньої архітектури Docker — клієнт-серверна модель, Docker Daemon, containerd, runc та OCI стандарти.
::

::card{title="4. Встановлення Docker" to="/tools/docker/installation" icon="i-lucide-download"}
Покрокова інструкція встановлення Docker Engine на Linux, macOS та Windows з налаштуванням та перевіркою.
::

::card{title="5. Перший контейнер" to="/tools/docker/first-container" icon="i-lucide-terminal"}
Практичне знайомство з запуском контейнерів, детальний розбір команди docker run та основні операції з контейнерами.
::

::card{title="6. Життєвий цикл контейнера" to="/tools/docker/container-lifecycle" icon="i-lucide-activity"}
Глибоке розуміння станів контейнера, процесів всередині, діагностичних команд та управління життєвим циклом.
::

::card{title="7. Docker Images — концепції" to="/tools/docker/docker-images-fundamentals" icon="i-lucide-layers"}
Глибоке розуміння Docker-образів, архітектури шарів, Union File System, незмінності та управління образами.
::

::card{title="8. Dockerfile — основи" to="/tools/docker/dockerfile-basics" icon="i-lucide-file-code"}
Створення перших Docker-образів через Dockerfile, базові інструкції та практичні приклади для C# застосунків.
::

::card{title="9. Dockerfile — просунуті техніки" to="/tools/docker/dockerfile-advanced" icon="i-lucide-zap"}
Multi-stage builds, ARG, LABEL, USER, HEALTHCHECK та оптимізація Docker-образів для продакшену.
::

::card{title="10. Build Context та кешування" to="/tools/docker/build-context-and-cache" icon="i-lucide-database"}
Оптимізація швидкості збірки Docker-образів через правильне використання build context, .dockerignore та механізму кешування.
::

::card{title="11. Реєстри Docker-образів" to="/tools/docker/image-registries" icon="i-lucide-cloud-upload"}
Docker Hub, Microsoft Container Registry та приватні реєстри — публікація, завантаження та управління Docker-образами.
::

::card{title="12. Контейнеризація .NET додатків" to="/tools/docker/dotnet-containerization" icon="i-simple-icons-dotnet"}
Повний цикл контейнеризації C# додатків — від консольних програм до ASP.NET Core Web API з production-ready конфігурацією.
::

::card{title="13. Томи та збереження даних" to="/tools/docker/volumes-and-data" icon="i-lucide-hard-drive"}
Persistent storage в Docker — volumes, bind mounts, tmpfs та управління даними контейнерів.
::

::card{title="14. Основи мережі в Docker" to="/tools/docker/networking-basics" icon="i-lucide-git-branch"}
Docker networking — bridge, host, overlay мережі, комунікація між контейнерами та зовнішнім світом.
::

::card{title="15. Змінні оточення та конфігурація" to="/tools/docker/environment-and-configuration" icon="i-lucide-sliders"}
Передача конфігурації в Docker-контейнери — ENV, env files, secrets, 12-Factor App.
::

::card{title="16. Docker Compose — оркестрація" to="/tools/docker/docker-compose-basics" icon="i-lucide-layers"}
Декларативне управління multi-container застосунками через docker-compose.yml.
::

::card{title="17. Compose — Multi-Service" to="/tools/docker/compose-multi-service" icon="i-lucide-server"}
Розширена робота з Docker Compose — залежності, мережі, томи, profiles та orchestration patterns.
::

:::
