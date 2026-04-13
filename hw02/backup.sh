#!/bin/bash
set -euo pipefail

validate_args() {
    local source_dir="${1:-}"

    if [[ $# -ne 1 ]]; then
        echo "Usage: $0 <source_directory>"
        exit 1
    fi

    if [[ ! -d "$source_dir" ]]; then
        echo "Error: '$source_dir' not found or is not a directory"
        exit 1
    fi
}

create_backup() {
    local source_dir="$1"
    local backup_dir="$HOME/backups"
    local timestamp
    local archive

    mkdir -p "$backup_dir"

    timestamp="$(date '+%Y-%m-%d_%H-%M-%S')"
    archive="$backup_dir/backup_${timestamp}.tar.gz"

    tar -czf "$archive" -C "$(dirname "$source_dir")" "$(basename "$source_dir")"

    echo "$archive"
}

rotate_backups() {
    local backup_dir="$HOME/backups"

    mapfile -t files < <(find "$backup_dir" -maxdepth 1 -type f -name 'backup_*.tar.gz' | sort -r)

    if (( ${#files[@]} > 3 )); then
        for f in "${files[@]:3}"; do
            rm -f "$f"
        done
    fi
}

print_report() {
    local source="$1"
    local archive="$2"

    local size
    local count

    size="$(du -h "$archive" | awk '{print $1}')"
    count="$(find "$HOME/backups" -maxdepth 1 -type f -name 'backup_*.tar.gz' | wc -l)"

    echo "=== Резервное копирование ==="
    echo "Источник: $source"
    echo "Архив: $(basename "$archive")"
    echo "Размер: $size"
    echo "Сохранено в: $HOME/backups/"
    echo "Архивов после ротации: $count"
    echo "=== Готово ==="
}

main() {
    local source="${1:-}"
    local archive

    validate_args "$@"
    archive="$(create_backup "$source")"
    rotate_backups
    print_report "$source" "$archive"
}

main "$@"
