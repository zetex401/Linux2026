# Фин

AI-агент для диагностики Linux-систем с function calling через Google Gemini API и Telegram-интеграцией.

Проект разработан для финального проекта по дисциплине «Операционные системы».

# Возможности

- Работа с файловой системой Linux
- Анализ процессов и оперативной памяти
- Получение uptime системы
- Сравнение файлов
- Просмотр директорий
- Поиск файлов по шаблону
- Получение погоды
- Получение мирового времени
- Telegram-бот для взаимодействия с агентом
- Agent loop через Gemini Function Calling

# Используемые технологии

- Python 3
- Google Gemini API
- python-telegram-bot
- ChatGpt
- Open-Meteo API
- Linux utilities: ps, free, uptime

# Реализованные tools

Tool | Описание | Пример запроса |

 find_files | Поиск файлов по шаблону | Найди все .py файлы в /home |
 read_file | Чтение содержимого файла | Покажи содержимое README.md |
 file_info | Информация о файле | Покажи информацию о файле agent.py |
 disk_usage | Использование диска | Покажи использование диска / |
 create_file | Создание файла | Создай файл test.txt с текстом hello |
 list_dir | Просмотр директории | Покажи содержимое папки /home |
 search_in_file | Поиск текста внутри файла | Найди слово error в файле logs.txt |
 process_list | Список Linux-процессов | Покажи процессы Python |
 memory_info | Использование RAM | Покажи использование оперативной памяти |
 system_uptime | Uptime системы | Покажи uptime системы |
 find_large_files | Поиск больших файлов | Найди файлы больше 10 MB в /home |
 create_backup | Создание backup файла | Сделай backup файла README.md |
 compare_files | Сравнение файлов | Сравни file1.txt и file2.txt |
 weather_now | Текущая погода | Покажи погоду в Алматы |
 world_time | Мировое время | Покажи время в Токио |

# Требования

- Ubuntu 22.04
- Python 3.10+
- Telegram Bot Token
- Gemini API Key

# Установка зависимостей

```bash
pip install google-genai python-telegram-bot requests


# Переменные окружения

```bash
export G_API_KEY="AIzaSyC7XjdhwWmAy8cFTtySi5I0NiMEac_4X6s"
export TELEGRAM_BOT_TOKEN="8575805196:AAEvSwwi9471ZMU22MNs4TvjZBlWWqb3AnU"


# Запуск проекта

```bash
python3 final_project_mukhitov.py


Если Telegram Token не указан, агент автоматически запускается в CLI-режиме.

# Примеры запросов для demo

text
Покажи содержимое текущей папки
Найди все .py файлы в текущей папке
Покажи использование оперативной памяти
Покажи процессы Python
Покажи uptime системы
Найди файлы больше 10 MB в /home
Сделай backup файла README.md
Сравни README.md и README.md.backup
Покажи погоду в Алматы
Покажи время в Токио

# Архитектура агента

Пользователь отправляет запрос. Модель Gemini анализирует запрос и выбирает нужный tool. После этого Python выполняет функцию, возвращает результат модели, а модель формирует итоговый ответ для пользователя.

# Структура проекта

```text
final/
README.md
agent.py
demo.mp4
```

# Telegram Demo

Агент поддерживает работу через Telegram-бота. Пользователь отправляет сообщение в Telegram, агент передает запрос в Gemini, Gemini вызывает нужный tool, после чего бот отправляет ответ обратно пользователю.

# Автор

Студент первого курса ФИТ факультет

Мухитов Арсений Адильбекович

с помощью ai_edu_kaznu_2026

ChatGpt 
