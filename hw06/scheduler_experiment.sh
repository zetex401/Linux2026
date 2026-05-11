#!/bin/bash
set -euo pipefail

if [ "$EUID" -ne 0 ]; then
    echo "Запустите скрипт через sudo"
    echo "sudo bash scheduler_experiment.sh"
    exit 1
fi

cleanup() {
    kill "${BG_PIDS[@]}" 2>/dev/null || true
}
trap cleanup EXIT

BG_PIDS=()

echo "Запуск фоновой нагрузкиыоаоао"
for i in $(seq 1 3); do
    dd if=/dev/urandom of=/dev/null bs=1M &
    BG_PIDS+=($!)
done

echo "Запуск эксперимента: nice -10 vs nice +10"

{ time nice -n -10 dd if=/dev/urandom of=/dev/null bs=1M count=200 2>/dev/null; } 2> time_minus10.txt &
PID_HIGH=$!

{ time nice -n 10 dd if=/dev/urandom of=/dev/null bs=1M count=200 2>/dev/null; } 2> time_plus10.txt &
PID_LOW=$!

wait $PID_HIGH
wait $PID_LOW

echo ""
echo "===== RESULTS ====="
echo "nice -10:"
cat time_minus10.txt

echo ""
echo "nice +10:"
cat time_plus10.txt

echo ""
echo "Таблица сравнения:"
echo "nice | file"
echo "-10  | time_minus10.txt"
echo "+10  | time_plus10.txt"
