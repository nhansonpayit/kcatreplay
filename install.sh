#!/usr/bin/env bash
DEST='/usr/local/bin/kcatreplay'
ln -sfn "$(pwd -P)/main.py" "${DEST}"
chmod a+x ${DEST}