#!/usr/bin/env bash
set -euo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
exec "${KK_TEST_PYTHON:-python3}" -I -B "$here/kk/test_install.py"
