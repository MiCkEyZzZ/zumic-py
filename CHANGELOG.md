# Changelog

[Unrealized]

### Добавлено
- Базовая реализация класса `Connection` для работы с сокетом (подключение, отправка, получение данных).
- Реализация упаковки и отправки команд в формате, совместимом с протоколом Redis.
- Базовые методы обработки ответов от сервера с поддержкой строк, чисел и ошибок.
- Модуль тестов с покрытием основных сценариев: подключение, отправка/получение данных, обработка ошибок.
- Мок-объект `MockConnection` для тестирования клиента без реального подключения.
- Поддержка контекстного менеджера (`with`) для безопасного открытия и закрытия соединений в `Connection` и `Client`.
- Обработка исключений, введена иерархия исключений для различных типов ошибок клиента Zumic.
- Настроены и пройдены тесты с использованием `pytest` со стабильно проходящим покрытием.
- Добавлена поддержка строгой типизации с помощью аннотаций и исправлены ошибки Pyright/mypy.
- Добавлен Makefile с командами для lint, typecheck, тестов, сборки и релиза.
- Настроен CI с GitHub Actions для автоматического запуска lint, typecheck и тестов при push/pull request.
- Добавлены шаблоны Issue (`enhancement.yml`, `question.yml`) для стандартизации работы с задачами и вопросами.

### Исправлено
- Обработка исключений в `Connection.connect`: расширено перехватываемое исключение на общий `OSError` вместо устаревших `(socket.timeout, socket.error)` для корректной обработки в Python 3.
- Исправлены тесты для имитации ошибок соединения (`test_connect_fail`): переход на использование явной функции, бросающей `OSError`, вместо генератора с `.throw()`.
- Исправлена строгая типизация при подмене приватного атрибута `_sock` в тестах — добавлены комментарии `# type: ignore[assignment]`.
- Устранены проблемы с импортами библиотеки `pytest` в средах с Poetry и статическим анализом (`Pyright`), добавлены рекомендации по настройке виртуального окружения.
- Корректное расположение функций и порядок объявлений в тестах для предотвращения ошибок рантайма (например, определение функции `raise_oserror` перед её использованием в тестах).
- Улучшена инициализация и обработка ответов сервера, включая поддержку `None` в Bulk String, а также корректное декодирование байтов.

### Изменено
- Внесены улучшения в архитектуру клиента и тестов для повышения расширяемости и удобства поддержки.
- Переработана логика тестирования ошибок подключения и взаимодействия с сокетом для более надежного покрытия.
- Улучшена структура проекта с явным соблюдением лучших практик Python-разработки и модульности.
