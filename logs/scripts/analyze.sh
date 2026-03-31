#!/bin/bash

if [ -z "$1" ]; then
  echo "Ошибка: укажите путь к лог-файлу"
  exit 1
fi

LOG="$1"

echo "=== ТОП-5 IP-АДРЕСОВ ==="
awk '{print $1}' "$LOG" | sort | uniq -c | sort -nr | head -n 5

echo ""
echo "=== ЗАПРОСЫ С КОДОМ 404 ==="
COUNT_404=$(awk '$9 == 404' "$LOG" | wc -l)
echo "Количество: $COUNT_404"

echo ""
echo "=== САМЫЙ ПОПУЛЯРНЫЙ URL ==="
awk '{print $7}' "$LOG" | sort | uniq -c | sort -nr | head -n 1

echo ""
echo "=== ВСЕГО СТРОК В ЛОГЕ ==="
wc -l < "$LOG"
