#!/bin/sh
set -e

if [ "${MODE}" = "web" ]; then
    exec python web.py
else
    exec python summarize.py "$@"
fi
