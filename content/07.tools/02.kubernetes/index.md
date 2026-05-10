# Kubernetes: від розробки до production

Ласкаво просимо до повного практичного курсу з Kubernetes на **kostyl.dev**.

Цей курс розроблений для того, щоб провести вас від базового розуміння оркестрації контейнерів до налаштування та управління стійкими до відмов застосунками у реальному кластері.

---

## Програма курсу

:::card-group

::card{title="1. Навіщо потрібен Kubernetes" to="/tools/kubernetes/why-kubernetes" icon="i-lucide-network"}
Від одного сервера до кластера — чому виникає потреба в оркестрації, що таке Kubernetes і яке місце він займає в сучасній інфраструктурі.
::

::card{title="2. Анатомія кластера" to="/tools/kubernetes/kubernetes-architecture" icon="i-lucide-cpu"}
Внутрішня будова Kubernetes-кластера — control plane, worker nodes, ключові компоненти та їхня взаємодія.
::

::card{title="3. Локальний кластер" to="/tools/kubernetes/local-environment" icon="i-lucide-terminal"}
Встановлення та налаштування локального Kubernetes-кластера (minikube, kind, k3s) для розробки та навчання.
::

::card{title="4. Pod — атомарна одиниця" to="/tools/kubernetes/pods-and-containers" icon="i-lucide-box"}
Глибоке розуміння Pod — від базових концепцій до повної специфікації YAML, життєвого циклу та практичних прикладів.
::

::card{title="5. Патерни використання Pod" to="/tools/kubernetes/pod-patterns" icon="i-lucide-layers"}
Init-контейнери та Sidecar — розв'язання реальних архітектурних проблем у Kubernetes з прикладами на .NET.
::

::card{title="6. Основи Deployment" to="/tools/kubernetes/deployment-basics" icon="i-lucide-refresh-cw"}
Від ручного управління Pod до автоматизованої оркестрації — self-healing, масштабування та декларативні оновлення.
::

::card{title="7. Rolling Updates та життєвий цикл" to="/tools/kubernetes/deployment-rolling-updates" icon="i-lucide-activity"}
Оновлення застосунків без downtime — від теорії до практики з детальною візуалізацією, розрахунками та реальними прикладами.
::

::card{title="8. Service — мережева абстракція" to="/tools/kubernetes/services-networking" icon="i-lucide-git-branch"}
Від ефемерних IP-адрес Pod до стабільних Service endpoints — service discovery, балансування навантаження та мережева архітектура.
::

:::
