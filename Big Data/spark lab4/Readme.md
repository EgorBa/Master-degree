### Лабораторная работа #8
### Миграция на Kubernetes
В рамках данной работы была произведена миграция сервиса модели, витрины данных и источника данных 
на Kubernetes.

Для равертывания кластера, была использована [платформа VK Cloud](https://mcs.mail.ru/).

[Реализация флоу работы модели](python_main/main.py).

В качестве источника данных используется [Hadoop File System](https://mcs.mail.ru/app/mcs3129233031/services/storage/buckets)
, который также был развернут на платформе VK Cloud.

Скрипты для [собирания образа](Dockerfile) и [деплоя](spark_kubernetes.yaml).

В результате обчуения модели была получена следующая метрика : 
Silhouette with squared euclidean distance = 0.9999993029872573

