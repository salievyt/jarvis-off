#!/bin/bash
# FINAL INSTALLER - JARVIS + Mode System
# by SteelRework AI

set -e

# Цвета
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo -e "${PURPLE}"
echo "╔════════════════════════════════════════════╗"
echo "║        🤖 JARVIS FINAL INSTALLER 🤖       ║"
echo "║                                            ║"
echo "║          by SteelRework AI                ║"
echo "╚════════════════════════════════════════════╝"
echo -e "${NC}"

# Проверка системы
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Требуется macOS"
    exit 1
fi

ARCH=$(uname -m)
if [[ "$ARCH" == "arm64" ]]; then
    BREW_PATH="/opt/homebrew"
else
    BREW_PATH="/usr/local"
fi

# Установка Homebrew
if ! command -v brew &> /dev/null; then
    echo "📦 Установка Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    if [[ "$ARCH" == "arm64" ]]; then
        echo "eval \"$(/opt/homebrew/bin/brew shellenv)\"" >> ~/.zshrc
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
fi

# Зависимости
echo "📦 Установка зависимостей..."
brew list portaudio &>/dev/null || brew install portaudio
brew list sdl2 &>/dev/null || brew install sdl2
brew list sdl2_mixer &>/dev/null || brew install sdl2_mixer
brew list ffmpeg &>/dev/null || brew install ffmpeg

# Python
if ! command -v python3 &> /dev/null; then
    brew install python@3
fi

# Mode System
echo ""
echo -e "${CYAN}⚙️ Установка Mode System${NC}"

ZSHRC="$HOME/.zshrc"
[ -f "$ZSHRC" ] || touch "$ZSHRC"

# Удаляем старые версии
sed -i '' '/# >>> JARVIS MODE SYSTEM/,/# <<< JARVIS MODE SYSTEM/d' "$ZSHRC" 2>/dev/null || true
sed -i '' '/# >>> mode work/,/# <<< mode work/d' "$ZSHRC" 2>/dev/null || true

# Копируем mode_system_final.sh в .zshrc
if [ -f "mode_system_final.sh" ]; then
    echo "" >> "$ZSHRC"
    echo "# >>> JARVIS MODE SYSTEM FINAL >>>" >> "$ZSHRC"
    cat mode_system_final.sh >> "$ZSHRC"
    echo "# <<< JARVIS MODE SYSTEM FINAL <<<" >> "$ZSHRC"
else
    # Если файла нет, добавляем базовую версию
    cat >> "$ZSHRC" << 'MODE_BASE'

# >>> JARVIS MODE SYSTEM FINAL >>>
mode() {
    case "$1" in
        sm1le)
            echo "🤖 Персональный режим с JARVIS"
            open -a "Telegram" 2>/dev/null || true
            open -a "Obsidian" 2>/dev/null || true

            # Запуск JARVIS
            if [ -d "$HOME/.jarvis" ]; then
                cd "$HOME/.jarvis"
                source venv/bin/activate 2>/dev/null || true
                nohup python3 jarvis.py > /dev/null 2>&1 &
                echo "✅ JARVIS запущен"
                deactivate 2>/dev/null || true
            fi
            ;;
        work)
            echo "🔧 Рабочий режим"
            open -a "Visual Studio Code" 2>/dev/null || true
            open -a "Firefox" 2>/dev/null || true
            open -a "Telegram" 2>/dev/null || true
            ;;
        off)
            echo "🛑 Закрываю всё"
            pkill -f "jarvis.py" 2>/dev/null || true
            osascript -e 'tell application "System Events" to set quitapps to name of every application process whose visible is true and name is not "Finder"' \
                      -e 'repeat with appName in quitapps' \
                      -e 'tell application appName to quit' \
                      -e 'end repeat' 2>/dev/null || true
            ;;
        help)
            echo "MODE SYSTEM:"
            echo "  mode sm1le - персональный режим + JARVIS"
            echo "  mode work  - рабочий режим"
            echo "  mode off   - закрыть всё"
            ;;
        *)
            echo "Используйте: mode help"
            ;;
    esac
}
# <<< JARVIS MODE SYSTEM FINAL <<<
MODE_BASE
fi

echo "✅ Mode System установлена"

# JARVIS
echo ""
echo -e "${CYAN}🤖 Установка JARVIS${NC}"

JARVIS_DIR="$HOME/.jarvis"
mkdir -p "$JARVIS_DIR/sounds"
mkdir -p "$JARVIS_DIR/config"

# Копируем JARVIS
if [ -f "jarvis_final.py" ]; then
    cp jarvis_final.py "$JARVIS_DIR/jarvis.py"
elif [ -f "JARVIS_FINAL_COMPLETE.py" ]; then
    cp JARVIS_FINAL_COMPLETE.py "$JARVIS_DIR/jarvis.py"
else
    echo "⚠️  Файл JARVIS не найден, создаю базовую версию"
    cat > "$JARVIS_DIR/jarvis.py" << 'BASE'
#!/usr/bin/env python3
print("🤖 JARVIS базовая версия")
print("Поместите jarvis_final.py сюда")
BASE
fi

chmod +x "$JARVIS_DIR/jarvis.py"

# Python окружение
cd "$JARVIS_DIR"
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip --quiet
pip install SpeechRecognition --quiet
pip install pyttsx3 --quiet

# Pygame
if [[ "$ARCH" == "arm64" ]]; then
    export CFLAGS="-I${BREW_PATH}/include -I${BREW_PATH}/include/SDL2"
    export LDFLAGS="-L${BREW_PATH}/lib"
fi
pip install pygame --quiet

# PyAudio
if [[ "$ARCH" == "arm64" ]]; then
    CFLAGS="-I${BREW_PATH}/include" LDFLAGS="-L${BREW_PATH}/lib" pip install pyaudio --quiet
else
    pip install pyaudio --quiet
fi

deactivate

echo "✅ JARVIS установлен"

# Проверка звуков
echo ""
echo -e "${CYAN}🔊 Установка звуков${NC}"

SOUND_COUNT=$(ls -1 "$JARVIS_DIR/sounds"/*.wav 2>/dev/null | wc -l)

if [ $SOUND_COUNT -gt 0 ]; then
    echo "✅ Найдено $SOUND_COUNT звуковых файлов"
else
    echo "⚠️  Звуки не найдены"

    # Пытаемся найти и скопировать
    for dir in "." "$HOME/Desktop" "$HOME/Downloads"; do
        if ls "$dir"/*.wav 1> /dev/null 2>&1; then
            cp "$dir"/*.wav "$JARVIS_DIR/sounds/" 2>/dev/null
            echo "✅ Звуки скопированы из $dir"
            break
        fi
    done
fi

# Финал
echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}        ✅ УСТАНОВКА ЗАВЕРШЕНА!         ${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "🚀 БЫСТРЫЙ СТАРТ:"
echo ""
echo "1. Перезапустите терминал или:"
echo "   source ~/.zshrc"
echo ""
echo "2. Запустите персональный режим с JARVIS:"
echo "   mode sm1le"
echo ""
echo "💡 КОМАНДЫ:"
echo "   mode sm1le - персональный режим + JARVIS"
echo "   mode work  - рабочий режим"
echo "   mode off   - закрыть всё"
echo "   mode help  - справка"
echo ""

if [ $SOUND_COUNT -eq 0 ]; then
    echo "⚠️  Добавьте звуки (.wav) в:"
    echo "   ~/.jarvis/sounds/"
fi

echo ""
echo "by SteelRework AI"