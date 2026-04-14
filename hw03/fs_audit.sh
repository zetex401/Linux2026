#!/bin/bash
set -euo pipefail

show_mounted_fs() {
    echo "=== Смонтированные файловые системы ==="
    df -Th | grep -E 'Filesystem|ext4|tmpfs'
    echo
}

show_dir_stats() {
    local dir="$1"
    echo "=== Статистика: $dir ==="

    local files
    local dirs
    local links

    files=$(find "$dir" -type f 2>/dev/null | wc -l)
    dirs=$(find "$dir" -type d 2>/dev/null | wc -l)
    links=$(find "$dir" -type l 2>/dev/null | wc -l)

    echo "  Файлов:      $files"
    echo "  Директорий:  $dirs"
    echo "  Симлинков:   $links"
    echo
}

show_top_files() {
    local dir="$1"
    echo "=== Топ-5 крупнейших файлов в $dir ==="
    echo -e "  Inode\tРазмер\tПуть"

    find "$dir" -type f -printf '%i\t%s\t%p\n' 2>/dev/null \
        | sort -t$'\t' -k2 -rn \
        | head -5
    echo
}

show_df_vs_du() {
    local dir="$1"
    echo "=== df vs du ($dir) ==="

    local df_used
    local du_used

    df_used=$(df --output=used "$dir" | tail -1)
    du_used=$(du -sk "$dir" 2>/dev/null | awk '{print $1}')

    local diff
    diff=$((df_used - du_used))

    local percent
    percent=$((diff * 100 / df_used))

    echo "  df used:   ${df_used} KB"
    echo "  du used:   ${du_used} KB"
    echo "  Разница:   ${diff} KB (${percent}%)"
    echo
}

main() {
    if [[ $# -ne 1 ]]; then
        echo "Usage: $0 <directory>"
        exit 1
    fi

    local dir="$1"

    if [[ ! -d "$dir" ]]; then
        echo "Error: directory does not exist"
        exit 1
    fi

    show_mounted_fs
    show_dir_stats "$dir"
    show_top_files "$dir"
    show_df_vs_du "$dir"
}

main "$@"
