#!/usr/bin/env bash
set -e
set -u
set -o pipefail

stty -F /dev/ttyACM0 115200 raw -echo -hupcl
cat /dev/ttyACM0 | pv > /dev/null
