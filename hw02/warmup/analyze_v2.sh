#!/bin/bash
set -euo pipefail

validate_args() {
    local log_file="${1:-}"
    if [[ $# -ne 1 ]]; then
        echo "Usage: $0 <log_file>"
        exit 1
    fi
    if [[ ! -f "$log_file" ]]; then
        echo "Error: '$log_file' not found or is not a file"
        exit 1
    fi
}

top_ips() {
    local log_file="$1"
    echo "=== Top-5 IP ==="
    awk '{print $1}' "$log_file" | sort | uniq -c | sort -rn | head -5
}

count_404() {
    local log_file="$1"
    echo
    echo "=== Number of 404 ==="
    grep -c " 404 " "$log_file"
}

top_url() {
    local log_file="$1"
    echo
    echo "=== Most popular URL ==="
    awk '{print $7}' "$log_file" | sort | uniq -c | sort -rn | head -1
}

main() {
    local log_file="${1:-}"
    validate_args "$@"
    top_ips "$log_file"
    count_404 "$log_file"
    top_url "$log_file"
}

main "$@"
