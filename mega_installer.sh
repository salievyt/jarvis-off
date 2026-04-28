#!/bin/bash
# МЕГА УСТАНОВЩИК - Mode System + JARVIS Ultimate
# Автоматическая установка всей системы автоматизации
# SteelRework AI

set -e

# Цвета для красивого вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Заголовок
clear
echo -e "${PURPLE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║         🚀 МЕГА УСТАНОВЩИК СИСТЕМЫ АВТОМАТИЗАЦИИ 🚀         ║"
echo "║                                                              ║"
echo "║          Mode System + JARVIS Final Edition                 ║"
echo "║                     для macOS (M1/Intel)                    ║"
echo "║                                                              ║"
echo "║                    by SteelRework AI                        ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Проверка системы
echo -e "${CYAN}🔍 Проверка системы...${NC}"
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}❌ Этот установщик работает только на macOS${NC}"
    exit 1
fi

# Определяем архитектуру
ARCH=$(uname -m)
if [[ "$ARCH" == "arm64" ]]; then
    echo -e "${GREEN}✓ Обнаружен Mac M1/M2 (Apple Silicon)${NC}"
    BREW_PATH="/opt/homebrew"
else
    echo -e "${GREEN}✓ Обнаружен Intel Mac${NC}"
    BREW_PATH="/usr/local"
fi

# ===============================================
# ЧАСТЬ 1: УСТАНОВКА ЗАВИСИМОСТЕЙ
# ===============================================

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════${NC}"
echo -e "${YELLOW}     ЧАСТЬ 1: УСТАНОВКА ЗАВИСИМОСТЕЙ${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════${NC}"
echo ""

# Проверка Homebrew
if ! command -v brew &> /dev/null; then
    echo -e "${CYAN}📦 Homebrew не найден. Устанавливаю...${NC}"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Добавляем Homebrew в PATH для M1
    if [[ "$ARCH" == "arm64" ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
else
    echo -e "${GREEN}✓ Homebrew уже установлен${NC}"
fi

# Установка portaudio (для микрофона)
echo -e "${CYAN}🎤 Проверяю portaudio...${NC}"
if ! brew list portaudio &>/dev/null; then
    echo "   Устанавливаю portaudio..."
    brew install portaudio
else
    echo -e "${GREEN}   ✓ portaudio уже установлен${NC}"
fi

# Установка SDL2 (для pygame)
echo -e "${CYAN}🎮 Проверяю SDL2...${NC}"
if ! brew list sdl2 &>/dev/null; then
    echo "   Устанавливаю SDL2 и зависимости..."
    brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
else
    echo -e "${GREEN}   ✓ SDL2 уже установлен${NC}"
fi

# Проверка Python 3
echo -e "${CYAN}🐍 Проверяю Python 3...${NC}"
if ! command -v python3 &> /dev/null; then
    echo "   Устанавливаю Python 3..."
    brew install python@3
else
    echo -e "${GREEN}   ✓ Python 3 уже установлен${NC}"
fi

# ===============================================
# ЧАСТЬ 2: MODE SYSTEM - СИСТЕМА КОМАНД
# ===============================================

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════${NC}"
echo -e "${YELLOW}     ЧАСТЬ 2: MODE SYSTEM${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════${NC}"
echo ""

ZSHRC="$HOME/.zshrc"
MARKER_START="# >>> mode work (SteelRework) >>>"
MARKER_END="# <<< mode work (SteelRework) <<<"

# Создаём .zshrc если его нет
[ -f "$ZSHRC" ] || touch "$ZSHRC"

# Удаляем старую версию mode если есть
if grep -q "$MARKER_START" "$ZSHRC"; then
    sed -i '' "/$MARKER_START/,/$MARKER_END/d" "$ZSHRC"
    echo -e "${YELLOW}   Старая версия mode удалена${NC}"
fi

echo -e "${CYAN}📝 Устанавливаю mode систему...${NC}"

# Добавляем mode функцию в .zshrc
cat >> "$ZSHRC" <<'EOF'

# >>> mode work (SteelRework) >>>
# Настройки путей
: "${OBSIDIAN_VAULT:=$HOME/Documents/Obsidian}"
: "${PROJECTS_DIR:=$HOME/projects}"

mode() {
    case "$1" in

        # === ПЕРСОНАЛЬНЫЙ РЕЖИМ ===
        sm1le|smile)
            local hour=$(date +%H)
            local day=$(date +%a)
            local name="Яхёбек"

            echo ""
            if [ "$hour" -lt 6 ]; then
                echo "🌙 Ночная смена, $name? Поработаем!"
            elif [ "$hour" -lt 12 ]; then
                echo "☀️  Доброе утро, $name! Начинаем день."
            elif [ "$hour" -lt 18 ]; then
                echo "🌤  Привет, $name! Продуктивного дня."
            else
                echo "🌆 Добрый вечер, $name! Ещё немного поработаем?"
            fi
            echo ""

            echo "📊 Быстрая сводка:"
            local battery uptime_info disk_free
            battery=$(pmset -g batt | grep -Eo "[0-9]+%" | head -1 || echo "n/a")
            uptime_info=$(uptime | sed 's/.*up //' | sed 's/,.*users.*//')
            disk_free=$(df -h / | awk 'NR==2 {print $4}')
            echo "  🔋 Батарея: $battery  |  ⏱  Аптайм: $uptime_info"
            echo "  💾 Свободно на диске: $disk_free"
            echo "  🌡  Погода в Бишкеке:"
            curl -s "wttr.in/Bishkek?format=    %c+%t+%w+%p" 2>/dev/null || echo "    (недоступно)"

            echo ""
            echo "🚀 Запускаю твой набор..."
            open -a "Telegram" || echo "  ! Telegram не найден"
            open -a "Obsidian" || echo "  ! Obsidian не найден"

            if [ "$hour" -ge 9 ] && [ "$hour" -lt 19 ] && [ "$day" != "Sat" ] && [ "$day" != "Sun" ]; then
                echo "  → Рабочее время: запускаю VS Code"
                open -a "Visual Studio Code" || true
                open -a "Firefox" "https://steelrework.ru/admin?s=dashboard" || true
            else
                echo "  → Нерабочее время: лёгкий режим"
                open -a "Spotify" || echo "  ! Spotify не найден"
            fi
            echo ""
            echo "✅ Режим sm1le активирован!"
            ;;

        # === РАБОЧИЕ РЕЖИМЫ ===
        work)
            echo "🔧 Запуск рабочего режима..."
            open -a "Spotify" || echo "  ! Spotify не найден"
            open -a "Visual Studio Code" || echo "  ! VS Code не найден"
            open -a "Figma" || echo "  ! Figma не найден"
            open -a "Telegram" || echo "  ! Telegram не найден"
            echo "✅ Готово"
            ;;

        study)
            echo "📚 Запуск учебного режима..."
            open -a "Telegram" || echo "  ! Telegram не найден"
            open -a "Firefox" "https://www.youtube.com" || echo "  ! Firefox не найден"
            open -a "Firefox" "https://online.geeks.kg/" || true
            open -a "Obsidian" || echo "  ! Obsidian не установлен"
            echo "✅ Готово"
            ;;

        seo)
            echo "🔍 Запуск SEO режима..."
            open -a "Telegram" || echo "  ! Telegram не найден"
            open -a "Obsidian" || echo "  ! Obsidian не установлен"
            open -a "Firefox" "https://steelrework.ru/admin?s=dashboard" || echo "  ! Firefox не найден"
            open -a "Firefox" "https://steelrework.ru" || true
            open -a "Firefox" "https://search.google.com/search-console" || true
            open -a "Firefox" "https://analytics.google.com" || true
            open -a "Firefox" "https://webmaster.yandex.ru" || true
            open -a "Firefox" "https://metrika.yandex.ru" || true
            echo "✅ Готово"
            ;;

        chill|rest)
            echo "🎵 Режим отдыха..."
            open -a "Spotify" || echo "  ! Spotify не найден"
            open -a "Firefox" "https://www.youtube.com" || echo "  ! Firefox не найден"
            open -a "Telegram" || echo "  ! Telegram не найден"
            echo "✅ Готово"
            ;;

        meeting|call)
            echo "📞 Режим встречи..."
            open -a "zoom.us" 2>/dev/null || open -a "Zoom" 2>/dev/null || open -a "Firefox" "https://meet.google.com"
            open -a "Telegram" || echo "  ! Telegram не найден"
            open -a "Obsidian" || open -a "Notes"
            echo "✅ Готово"
            ;;

        focus|deep)
            echo "🎯 Режим концентрации..."
            osascript -e 'tell application "Telegram" to quit' 2>/dev/null || true
            osascript -e 'tell application "Spotify" to quit' 2>/dev/null || true
            open -a "Visual Studio Code" || echo "  ! VS Code не найден"
            open -a "Obsidian" || true
            echo "✅ Telegram и Spotify закрыты — не отвлекайся"
            ;;

        off|stop)
            echo "🛑 Закрываю всё..."
            for app in "Spotify" "Visual Studio Code" "Figma" "Telegram" \
                       "Obsidian" "Firefox" "zoom.us" "Zoom"; do
                osascript -e "tell application \"$app\" to quit" 2>/dev/null || true
            done
            echo "✅ Все приложения закрыты"
            ;;

        # === УТИЛИТЫ ===
        clean)
            echo "🧹 Очистка системы..."
            local before=$(df -h / | awk 'NR==2 {print $4}')
            command -v brew >/dev/null && { echo "  brew cleanup..."; brew cleanup -s 2>/dev/null; } || true
            command -v npm >/dev/null && { echo "  npm cache..."; npm cache clean --force 2>/dev/null; } || true
            rm -rf "$HOME/Library/Developer/Xcode/DerivedData/"* 2>/dev/null || true
            rm -rf "$HOME/.Trash/"* 2>/dev/null || true
            local after=$(df -h / | awk 'NR==2 {print $4}')
            echo "✅ Готово. Свободно: $before → $after"
            ;;

        ip)
            echo "🌐 IP адреса:"
            local wifi=$(ipconfig getifaddr en0 2>/dev/null || true)
            local pub=$(curl -s --max-time 5 ifconfig.me 2>/dev/null || echo "недоступно")
            [ -n "$wifi" ] && echo "  Wi-Fi: $wifi"
            echo "  Публичный: $pub"
            ;;

        seo-speed)
            local url="$2"
            if [ -z "$url" ]; then
                echo "Использование: mode seo-speed <url>"
                return 1
            fi
            [[ "$url" != http* ]] && url="https://$url"
            echo "⚡ Анализ скорости: $url"
            open -a "Firefox" "https://pagespeed.web.dev/report?url=$url" 2>/dev/null || true
            ;;

        # === ПРОЕКТЫ ===
        project)
            local name="$2"
            if [ -z "$name" ]; then
                echo "Использование: mode project <name>"
                return 1
            fi
            local dir="$PROJECTS_DIR/$name"
            if [ ! -d "$dir" ]; then
                echo "❌ Проект $name не найден"
                return 1
            fi
            echo "📂 Открываю проект $name..."
            cd "$dir" || return 1
            open -a "Visual Studio Code" "$dir"
            echo "✅ Готово"
            ;;

        cp)
            local name="$2"
            if [ -z "$name" ]; then
                echo "Использование: mode cp <name> [-front] [-back] [-mobile]"
                return 1
            fi
            shift 2
            local root="$PROJECTS_DIR/$name"
            if [ -d "$root" ]; then
                echo "❌ Проект уже существует"
                return 1
            fi
            echo "🔨 Создаю проект $name..."
            mkdir -p "$root"
            echo "# $name" > "$root/README.md"
            echo "Создан: $(date '+%Y-%m-%d')" >> "$root/README.md"
            open -a "Visual Studio Code" "$root" 2>/dev/null || true
            echo "✅ Проект создан: $root"
            ;;

        # === СПРАВКА ===
        help|-h|--help)
            echo "🎯 MODE SYSTEM - Команды:"
            echo ""
            echo "РЕЖИМЫ:"
            echo "  mode sm1le    — персональный режим с дашбордом"
            echo "  mode work     — рабочий режим"
            echo "  mode study    — учебный режим"
            echo "  mode seo      — SEO режим"
            echo "  mode chill    — режим отдыха"
            echo "  mode meeting  — режим встречи"
            echo "  mode focus    — режим концентрации"
            echo "  mode off      — закрыть все приложения"
            echo ""
            echo "УТИЛИТЫ:"
            echo "  mode clean           — очистка системы"
            echo "  mode ip              — показать IP"
            echo "  mode seo-speed <url> — проверка скорости сайта"
            echo ""
            echo "ПРОЕКТЫ:"
            echo "  mode project <name>  — открыть проект"
            echo "  mode cp <name>       — создать проект"
            ;;

        "")
            echo "Использование: mode <команда>"
            echo "Справка: mode help"
            return 1
            ;;

        *)
            echo "❌ Неизвестная команда: $1"
            echo "Справка: mode help"
            return 1
            ;;
    esac
}
# <<< mode work (SteelRework) <<<
EOF

echo -e "${GREEN}✅ Mode система установлена${NC}"

# ===============================================
# ЧАСТЬ 3: JARVIS - ГОЛОСОВОЙ АССИСТЕНТ
# ===============================================

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════${NC}"
echo -e "${YELLOW}     ЧАСТЬ 3: JARVIS ГОЛОСОВОЙ АССИСТЕНТ${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════${NC}"
echo ""

JARVIS_DIR="$HOME/.jarvis"
mkdir -p "$JARVIS_DIR"
mkdir -p "$JARVIS_DIR/sounds"

echo -e "${CYAN}🤖 Копирую файлы JARVIS...${NC}"

# Копируем основной скрипт JARVIS (ищем в разных местах)
JARVIS_FOUND=false
for file in "jarvis_final.py" "jarvis_ultimate.py" "jarvis_advanced.py" "jarvis_voice.py" "jarvis.py"; do
    for dir in "." "$HOME/Desktop" "$HOME/Downloads"; do
        if [ -f "$dir/$file" ]; then
            cp "$dir/$file" "$JARVIS_DIR/jarvis.py"
            JARVIS_FOUND=true
            echo -e "${GREEN}   ✓ Скопирован $file${NC}"
            break 2
        fi
    done
done

if [ "$JARVIS_FOUND" = false ]; then
    echo -e "${YELLOW}   ⚠️ Файл JARVIS не найден, создаю базовую версию${NC}"
    # Создаём минимальный JARVIS
    cat > "$JARVIS_DIR/jarvis.py" <<'JARVIS_PY'
#!/usr/bin/env python3
print("🤖 JARVIS: Базовая версия установлена")
print("   Поместите jarvis_final.py в ~/.jarvis/")
JARVIS_PY
fi

echo -e "${CYAN}🐍 Создаю виртуальное окружение Python...${NC}"
cd "$JARVIS_DIR"
python3 -m venv venv

echo -e "${CYAN}📚 Устанавливаю Python библиотеки...${NC}"
source venv/bin/activate

pip install --upgrade pip --quiet

echo "   • SpeechRecognition..."
pip install SpeechRecognition --quiet 2>/dev/null || true

echo "   • pyttsx3..."
pip install pyttsx3 --quiet 2>/dev/null || true

echo "   • pygame..."
if [[ "$ARCH" == "arm64" ]]; then
    export CFLAGS="-I/opt/homebrew/include -I/opt/homebrew/include/SDL2"
    export LDFLAGS="-L/opt/homebrew/lib"
    pip install pygame --no-cache-dir --quiet 2>/dev/null || true
else
    export CFLAGS="-I/usr/local/include -I/usr/local/include/SDL2"
    export LDFLAGS="-L/usr/local/lib"
    pip install pygame --no-cache-dir --quiet 2>/dev/null || true
fi

echo "   • pyaudio..."
if [[ "$ARCH" == "arm64" ]]; then
    CFLAGS="-I/opt/homebrew/include" LDFLAGS="-L/opt/homebrew/lib" \
    pip install pyaudio --quiet 2>/dev/null || true
else
    pip install pyaudio --quiet 2>/dev/null || true
fi

deactivate

# Создаём запускатель JARVIS
cat > "$JARVIS_DIR/jarvis-launcher.sh" <<'LAUNCHER'
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
LAUNCHER

chmod +x "$JARVIS_DIR/jarvis-launcher.sh"
chmod +x "$JARVIS_DIR/jarvis.py"

# Добавляем алиас для JARVIS
if ! grep -q "alias jarvis=" "$ZSHRC" 2>/dev/null; then
    echo "" >> "$ZSHRC"
    echo "# JARVIS голосовой ассистент" >> "$ZSHRC"
    echo "alias jarvis='$JARVIS_DIR/jarvis-launcher.sh'" >> "$ZSHRC"
fi

echo -e "${GREEN}✅ JARVIS установлен${NC}"

# ===============================================
# ЗАВЕРШЕНИЕ УСТАНОВКИ
# ===============================================

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════${NC}"
echo -e "${GREEN}     ✅ УСТАНОВКА ЗАВЕРШЕНА УСПЕШНО!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════${NC}"
echo ""

echo -e "${CYAN}📋 УСТАНОВЛЕНО:${NC}"
echo -e "${GREEN}   ✓ Mode System — система команд${NC}"
echo -e "${GREEN}   ✓ JARVIS Final — голосовой ассистент с системным управлением${NC}"
echo -e "${GREEN}   ✓ Все зависимости (SDL2, portaudio, Python)${NC}"
echo ""

echo -e "${YELLOW}📂 ДОБАВЬТЕ ЗВУКИ JARVIS:${NC}"
echo "   Скопируйте .wav файлы в папку:"
echo -e "   ${BLUE}~/.jarvis/sounds/${NC}"
echo ""

echo -e "${PURPLE}🚀 КОМАНДЫ MODE SYSTEM:${NC}"
echo "   mode sm1le    — персональный режим"
echo "   mode work     — рабочий режим"
echo "   mode study    — учебный режим"
echo "   mode seo      — SEO режим"
echo "   mode off      — закрыть всё"
echo "   mode clean    — очистить систему"
echo "   mode help     — все команды"
echo ""

echo -e "${PURPLE}🎙 КОМАНДЫ JARVIS:${NC}"
echo "   'Джарвис, личный режим'     → mode sm1le"
echo "   'Джарвис, рабочий режим'    → mode work"
echo "   'Джарвис, отключи всё'      → mode off"
echo "   'Джарвис, открой Telegram'  → запуск приложения"
echo "   'Джарвис, найди пиццу'      → поиск в Google"
echo "   'Джарвис, открой YouTube'   → открыть сайт"
echo ""
echo -e "${PURPLE}🎛 СИСТЕМНОЕ УПРАВЛЕНИЕ:${NC}"
echo "   'Джарвис, громче'           → увеличить звук"
echo "   'Джарвис, тише'             → уменьшить звук"
echo "   'Джарвис, ярче'             → увеличить яркость"
echo "   'Джарвис, темнее'           → уменьшить яркость"
echo "   'Джарвис, заблокируй'       → заблокировать экран"
echo "   'Джарвис, скриншот'         → снимок экрана"
echo ""
echo -e "${PURPLE}🎵 УПРАВЛЕНИЕ SPOTIFY:${NC}"
echo "   'Джарвис, включи музыку'    → воспроизведение"
echo "   'Джарвис, пауза'            → пауза"
echo "   'Джарвис, следующий трек'   → следующая песня"
echo "   'Джарвис, включи <песня>'   → поиск и воспроизведение"
echo ""

echo -e "${CYAN}🎯 БЫСТРЫЙ СТАРТ:${NC}"
echo "   1. Перезапустите терминал или выполните:"
echo -e "      ${BLUE}source ~/.zshrc${NC}"
echo ""
echo "   2. Попробуйте mode систему:"
echo -e "      ${BLUE}mode sm1le${NC}"
echo ""
echo "   3. Запустите JARVIS:"
echo -e "      ${BLUE}jarvis${NC}"
echo ""

echo -e "${GREEN}═══════════════════════════════════════════════${NC}"
echo -e "${GREEN}     Спасибо за использование!${NC}"
echo -e "${GREEN}     SteelRework AI${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════${NC}"
echo ""