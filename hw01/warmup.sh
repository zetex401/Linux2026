#!/bin/bash

LOG="$1"

echo "=== КОЛИЧЕСТВО СТРОК ==="
wc -l < "$LOG"

echo ""
echo "=== ПЕРВЫЕ 5 СТРОК ==="
head -n 5 "$LOG"

echo ""
echo "=== ВСЕ УНИКАЛЬНЫЕ IP (КОЛИЧЕСТВО) ==="
awk '{print $1}' "$LOG" | sort | uniq | wc -l

