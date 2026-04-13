#!/bin/bash
set -euo pipefail
echo "$(date '+%Y-%m-%d %H:%M:%S') heartbeat from $(whoami)" >> ~/os-lab01/lab02/heartbeat.log
