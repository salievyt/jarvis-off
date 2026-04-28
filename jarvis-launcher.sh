#!/bin/bash
# Запускатель JARVIS с активацией виртуального окружения

JARVIS_DIR="$HOME/.jarvis"
cd "$JARVIS_DIR"

# Проверяем папку со звуками
if [ ! -d "$JARVIS_DIR/sounds" ] || [ -z "$(ls -A $JARVIS_DIR/sounds/*.wav 2>/dev/null)" ]; then
    echo "⚠️  Папка со звуками пуста или не найдена!"
    echo ""
    echo "📂 Поместите .wav файлы JARVIS в папку:"
    echo "   $JARVIS_DIR/sounds/"
    echo ""
    echo "Или укажите свою папку:"
    echo "   jarvis --sounds /путь/к/папке/со/звуками"
    echo ""
fi

# Экспортируем пути SDL для pygame (для M1 Mac)
if [[ $(uname -m) == "arm64" ]]; then
    export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
else
    export DYLD_LIBRARY_PATH="/usr/local/lib:$DYLD_LIBRARY_PATH"
fi

# Активируем виртуальное окружение и запускаем JARVIS
source venv/bin/activate
python3 jarvis.py "$@"
deactivate
