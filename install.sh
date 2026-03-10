#!/bin/bash

set -e

SCRIPT_NAME="portctl.py"
EXEC_NAME="portctl"
TARGET_DIR="$HOME/bin"

echo "Installing $EXEC_NAME..."

mkdir -p "$TARGET_DIR"

cp "$SCRIPT_NAME" "$TARGET_DIR/$EXEC_NAME"

chmod +x "$TARGET_DIR/$EXEC_NAME"

echo "Successfully installed, try running with '$EXEC_NAME'"
echo "Type '$EXEC_NAME -h' for help"
