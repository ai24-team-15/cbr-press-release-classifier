## Разворачивание приложения в Yandex Cloud

1. В консоли управления создаем реестр контейнеров: Все сервисы - Контейнеры - Container Registry.
2. На блид-сервере аутентифицируемся в созданном реестре (oauth-токен получаем в консоли управления):
```
echo <OAuth-токен>|docker login \
  --username oauth \
  --password-stdin \
 cr.yandex
```

3. Назначаем собранным образам с приложениями теги с указанием реестра:
```
docker tag cbr-api cr.yandex/<ID реестра>/cbr-api:latest
docker tag cbr-ui cr.yandex/<ID реестра>/cbr-ui:latest
```

4. Отправляем образы в реестр:
```
docker push cr.yandex/<ID реестра>/cbr-api:latest
docker push cr.yandex/<ID реестра>/cbr-ui:latest
```

5. В консоли управления в разделе Все сервисы - Compute Cloud - Виртуальный машины создаем новую виртуальную машину, на которой будет работать приложение.
6. Подключаемся к созданному инстансу, устанавливаем Docker обычным образом.
7. Аутентифицируемся в реестре образов, как в п. 1.2.
8. Задаем необходимые настройки в `.env`-файлах, копируем `docker-compose.deploy.yml` (убрав `.deploy`) и `docker-compose.elk.yml` (опционально).
9. Поднимаем приложение `docker compose up -d` и `docker compose -f docker-compose.elk.yml up -d` (опционально).
