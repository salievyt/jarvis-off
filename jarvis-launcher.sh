#!/bin/bash
JARVIS_DIR="$HOME/.jarvis"
cd "$JARVIS_DIR"

if [ ! -d "$JARVIS_DIR/sounds" ] || [ -z "$(ls -A $JARVIS_DIR/sounds/*.wav 2>/dev/null)" ]; then
    echo "⚠️  Добавьте звуки JARVIS в папку:"
    echo "   $JARVIS_DIR/sounds/"
fi

if [[ $(uname -m) == "arm64" ]]; then
    export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
else
    export DYLD_LIBRARY_PATH="/usr/local/lib:$DYLD_LIBRARY_PATH"
fi

source venv/bin/activate
python3 jarvis.py "$@"
deactivate
