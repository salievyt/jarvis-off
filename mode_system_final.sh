#!/bin/bash
# MODE SYSTEM FINAL - Полная система команд с JARVIS
# Добавить в ~/.zshrc
# by SteelRework AI

# Настройки
: "${OBSIDIAN_VAULT:=$HOME/Documents/Obsidian}"
: "${PROJECTS_DIR:=$HOME/projects}"
: "${JARVIS_DIR:=$HOME/.jarvis}"

# Функция запуска JARVIS в фоне
start_jarvis_background() {
    if ! pgrep -f "jarvis.py" > /dev/null; then
        echo "🤖 Запускаю JARVIS в фоновом режиме..."
        cd "$JARVIS_DIR"
        source venv/bin/activate 2>/dev/null || true
        nohup python3 jarvis.py > /dev/null 2>&1 &
        local jarvis_pid=$!
        echo "   ✅ JARVIS запущен (PID: $jarvis_pid)"
        echo "   🎤 Скажите 'Джарвис' для активации"
        deactivate 2>/dev/null || true
    else
        echo "   ℹ️ JARVIS уже работает"
    fi
}

# ГЛАВНАЯ ФУНКЦИЯ MODE
mode() {
    case "$1" in
        # === ПЕРСОНАЛЬНЫЙ РЕЖИМ С JARVIS ===
        sm1le|smile)
            local hour=$(date +%H)
            local day=$(date +%a)
            local name="${USER}"

            echo ""
            echo "╔══════════════════════════════════════════════╗"
            echo "║         🤖 ПЕРСОНАЛЬНЫЙ РЕЖИМ JARVIS 🤖      ║"
            echo "╚══════════════════════════════════════════════╝"
            echo ""

            # Приветствие по времени
            if [ "$hour" -lt 6 ]; then
                echo "🌙 Ночная смена, $name? JARVIS к вашим услугам!"
            elif [ "$hour" -lt 12 ]; then
                echo "☀️  Доброе утро, $name! JARVIS готов к работе."
            elif [ "$hour" -lt 18 ]; then
                echo "🌤  Привет, $name! JARVIS активирован."
            else
                echo "🌆 Добрый вечер, $name! JARVIS онлайн."
            fi
            echo ""

            # Системная информация
            echo "📊 Системная информация:"
            battery=$(pmset -g batt | grep -Eo "[0-9]+%" | head -1 || echo "n/a")
            uptime_info=$(uptime | sed 's/.*up //' | sed 's/,.*users.*//')
            disk_free=$(df -h / | awk 'NR==2 {print $4}')

            echo "  🔋 Батарея: $battery  |  ⏱  Аптайм: $uptime_info"
            echo "  💾 Диск: $disk_free свободно"

            # IP адреса
            local_ip=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "n/a")
            public_ip=$(curl -s --max-time 2 ifconfig.me 2>/dev/null || echo "n/a")
            echo "  🌐 IP: $local_ip (локальный) | $public_ip (публичный)"

            # Погода
            echo ""
            echo "  🌡  Погода в Бишкеке:"
            curl -s --max-time 3 "wttr.in/Bishkek?format=    %c+%t+%w+%p" 2>/dev/null || echo "    недоступно"

            # Запуск приложений
            echo ""
            echo "🚀 Запускаю персональный набор..."
            open -a "Telegram" 2>/dev/null || echo "  ! Telegram не найден"
            open -a "Obsidian" 2>/dev/null || echo "  ! Obsidian не найден"

            # В зависимости от времени
            if [ "$hour" -ge 9 ] && [ "$hour" -lt 19 ] && [ "$day" != "Sat" ] && [ "$day" != "Sun" ]; then
                echo "  📅 Рабочее время"
                open -a "Visual Studio Code" 2>/dev/null || true
                open -a "Firefox" 2>/dev/null || true
            else
                echo "  🎵 Нерабочее время"
                open -a "Spotify" 2>/dev/null || true
            fi

            # ЗАПУСК JARVIS
            echo ""
            start_jarvis_background

            echo ""
            echo "✅ Режим sm1le с JARVIS активирован!"
            echo ""
            echo "💡 Голосовые команды:"
            echo "   'Джарвис, рабочий режим'"
            echo "   'Джарвис, отключи всё'"
            echo "   'Джарвис, громче/тише'"
            echo "   'Джарвис, скриншот'"
            ;;

        # === РАБОЧИЙ РЕЖИМ ===
        work)
            echo "🔧 Запуск рабочего режима..."
            open -a "Spotify" 2>/dev/null || true
            open -a "Visual Studio Code" 2>/dev/null || true
            open -a "Figma" 2>/dev/null || true
            open -a "Telegram" 2>/dev/null || true
            open -a "Firefox" 2>/dev/null || true
            echo "✅ Рабочий режим активирован"
            ;;

        # === УЧЕБНЫЙ РЕЖИМ ===
        study)
            echo "📚 Запуск учебного режима..."
            open -a "Telegram" 2>/dev/null || true
            open -a "Firefox" "https://www.youtube.com" 2>/dev/null || true
            open -a "Firefox" "https://online.geeks.kg/" 2>/dev/null || true
            open -a "Obsidian" 2>/dev/null || true
            echo "✅ Учебный режим активирован"
            ;;

        # === SEO РЕЖИМ ===
        seo)
            echo "🔍 Запуск SEO режима..."
            open -a "Telegram" 2>/dev/null || true
            open -a "Obsidian" 2>/dev/null || true
            open -a "Firefox" "https://steelrework.ru/admin" 2>/dev/null || true
            open -a "Firefox" "https://search.google.com/search-console" 2>/dev/null || true
            open -a "Firefox" "https://analytics.google.com" 2>/dev/null || true
            echo "✅ SEO режим активирован"
            ;;

        # === РЕЖИМ ОТДЫХА ===
        chill|rest)
            echo "🎵 Режим отдыха..."
            open -a "Spotify" 2>/dev/null || true
            open -a "Firefox" "https://www.youtube.com" 2>/dev/null || true
            open -a "Telegram" 2>/dev/null || true
            echo "✅ Режим отдыха активирован"
            ;;

        # === РЕЖИМ ВСТРЕЧИ ===
        meeting|call)
            echo "📞 Режим встречи..."
            open -a "zoom.us" 2>/dev/null || open -a "Zoom" 2>/dev/null || true
            open -a "Telegram" 2>/dev/null || true
            open -a "Obsidian" 2>/dev/null || open -a "Notes" 2>/dev/null || true

            # Отключаем уведомления
            osascript -e 'tell application "System Events" to keystroke "d" using {option down, shift down}' 2>/dev/null || true
            echo "✅ Режим встречи активирован"
            echo "   🔕 Уведомления отключены"
            ;;

        # === РЕЖИМ ФОКУСА ===
        focus|deep)
            echo "🎯 Режим глубокой концентрации..."

            # Закрываем отвлекающие приложения
            for app in "Telegram" "Spotify" "Discord" "Slack"; do
                osascript -e "tell application \"$app\" to quit" 2>/dev/null || true
            done

            # Открываем рабочие инструменты
            open -a "Visual Studio Code" 2>/dev/null || true
            open -a "Obsidian" 2>/dev/null || true

            # Включаем Do Not Disturb
            osascript -e 'tell application "System Events" to keystroke "d" using {option down, shift down}' 2>/dev/null || true

            echo "✅ Режим фокуса активирован"
            echo "   🔕 Уведомления отключены"
            echo "   🚫 Мессенджеры закрыты"
            ;;

        # === ВЫКЛЮЧИТЬ ВСЁ ===
        off|stop)
            echo "🛑 Закрываю все приложения..."

            # Останавливаем JARVIS
            if pgrep -f "jarvis.py" > /dev/null; then
                echo "   🤖 Останавливаю JARVIS..."
                pkill -f "jarvis.py"
            fi

            # Закрываем все приложения
            local apps=("Spotify" "Visual Studio Code" "Figma" "Telegram"
                       "Discord" "Slack" "Obsidian" "Firefox" "Safari"
                       "Chrome" "zoom.us" "Zoom" "Terminal")

            for app in "${apps[@]}"; do
                osascript -e "tell application \"$app\" to quit" 2>/dev/null || true
            done

            echo "✅ Все приложения закрыты"
            ;;

        # === ОЧИСТКА СИСТЕМЫ ===
        clean)
            echo "🧹 Глубокая очистка системы..."
            local before=$(df -h / | awk 'NR==2 {print $4}')

            # Homebrew
            command -v brew >/dev/null && {
                echo "  • Homebrew..."
                brew cleanup -s 2>/dev/null
                brew autoremove 2>/dev/null
            }

            # NPM
            command -v npm >/dev/null && {
                echo "  • NPM..."
                npm cache clean --force 2>/dev/null
            }

            # Python
            command -v pip3 >/dev/null && {
                echo "  • Python pip..."
                pip3 cache purge 2>/dev/null
            }

            # Системные кэши
            echo "  • Системные кэши..."
            rm -rf ~/Library/Caches/* 2>/dev/null
            rm -rf ~/Library/Developer/Xcode/DerivedData/* 2>/dev/null
            rm -rf ~/.Trash/* 2>/dev/null

            # Docker
            command -v docker >/dev/null && {
                echo "  • Docker..."
                docker system prune -af 2>/dev/null
            }

            local after=$(df -h / | awk 'NR==2 {print $4}')
            echo "✅ Очистка завершена"
            echo "   Было: $before → Стало: $after"
            ;;

        # === IP ИНФОРМАЦИЯ ===
        ip)
            echo "🌐 Сетевая информация:"
            echo "━━━━━━━━━━━━━━━━━━━━━"

            # Локальные адреса
            echo "📍 Локальные адреса:"
            for interface in en0 en1; do
                local ip=$(ipconfig getifaddr $interface 2>/dev/null)
                [ -n "$ip" ] && echo "  $interface: $ip"
            done

            # Публичный IP
            echo ""
            echo "🌍 Публичный адрес:"
            local pub_ip=$(curl -s ifconfig.me 2>/dev/null || echo "недоступно")
            local location=$(curl -s ipinfo.io/city 2>/dev/null || echo "")
            echo "  IP: $pub_ip"
            [ -n "$location" ] && echo "  Локация: $location"

            # DNS
            echo ""
            echo "📡 DNS серверы:"
            scutil --dns | grep nameserver | head -3 | sed 's/^/  /'
            ;;

        # === SEO СКОРОСТЬ ===
        seo-speed)
            local url="$2"
            if [ -z "$url" ]; then
                echo "❌ Использование: mode seo-speed <url>"
                return 1
            fi

            [[ "$url" != http* ]] && url="https://$url"
            echo "⚡ Анализ скорости: $url"

            # Проверка
            echo "📊 Время ответа:"
            curl -o /dev/null -s -w "  Общее: %{time_total}s\n  DNS: %{time_namelookup}s\n  Соединение: %{time_connect}s\n" "$url"

            # PageSpeed
            echo ""
            echo "🔍 Открываю детальный анализ..."
            open -a "Firefox" "https://pagespeed.web.dev/report?url=$url" 2>/dev/null
            ;;

        # === JARVIS КОМАНДЫ ===
        jarvis|j)
            echo "🤖 Запуск JARVIS..."
            cd "$JARVIS_DIR"
            source venv/bin/activate 2>/dev/null || {
                echo "❌ JARVIS не установлен"
                return 1
            }
            python3 jarvis.py
            deactivate
            ;;

        jarvis-stop)
            echo "🛑 Останавливаю JARVIS..."
            pkill -f "jarvis.py" 2>/dev/null && echo "✅ JARVIS остановлен" || echo "ℹ️ JARVIS не запущен"
            ;;

        jarvis-status)
            if pgrep -f "jarvis.py" > /dev/null; then
                local pid=$(pgrep -f "jarvis.py")
                echo "✅ JARVIS работает (PID: $pid)"
            else
                echo "❌ JARVIS не запущен"
            fi
            ;;

        # === ПРОЕКТЫ ===
        project)
            local name="$2"
            if [ -z "$name" ]; then
                echo "📁 Доступные проекты:"
                ls -1 "$PROJECTS_DIR" 2>/dev/null | sed 's/^/  • /' || echo "  Проектов нет"
                return 0
            fi

            local dir="$PROJECTS_DIR/$name"
            if [ ! -d "$dir" ]; then
                echo "❌ Проект $name не найден"
                return 1
            fi

            echo "📂 Открываю проект $name..."
            cd "$dir"
            open -a "Visual Studio Code" "$dir"
            echo "✅ Проект открыт"
            ;;

        cp|create-project)
            local name="$2"
            local template="$3"

            if [ -z "$name" ]; then
                echo "❌ Использование: mode cp <name> [template]"
                echo "   Шаблоны: react, vue, next, python, rust, go"
                return 1
            fi

            local root="$PROJECTS_DIR/$name"
            if [ -d "$root" ]; then
                echo "❌ Проект уже существует"
                return 1
            fi

            echo "🔨 Создаю проект $name..."
            mkdir -p "$root"
            cd "$root"

            case "$template" in
                react)
                    npx create-react-app . --template typescript
                    ;;
                vue)
                    npm create vue@latest .
                    ;;
                next)
                    npx create-next-app@latest . --typescript --tailwind --app
                    ;;
                python)
                    python3 -m venv venv
                    echo "venv/" > .gitignore
                    echo "# $name" > README.md
                    touch requirements.txt main.py
                    ;;
                rust)
                    cargo init
                    ;;
                go)
                    go mod init "$name"
                    echo "package main\n\nfunc main() {\n    println(\"Hello!\")\n}" > main.go
                    ;;
                *)
                    echo "# $name" > README.md
                    git init
                    ;;
            esac

            open -a "Visual Studio Code" "$root"
            echo "✅ Проект создан: $root"
            ;;

        # === СПРАВКА ===
        help|-h|--help)
            echo "🎯 MODE SYSTEM FINAL - Полный список команд"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo ""
            echo "📋 РЕЖИМЫ:"
            echo "  mode sm1le        — персональный режим + JARVIS"
            echo "  mode work         — рабочий режим"
            echo "  mode study        — учебный режим"
            echo "  mode seo          — SEO режим"
            echo "  mode chill        — режим отдыха"
            echo "  mode meeting      — режим встречи"
            echo "  mode focus        — режим концентрации"
            echo "  mode off          — закрыть всё"
            echo ""
            echo "🤖 JARVIS:"
            echo "  mode jarvis       — запустить JARVIS"
            echo "  mode jarvis-stop  — остановить JARVIS"
            echo "  mode jarvis-status — статус JARVIS"
            echo ""
            echo "🛠 УТИЛИТЫ:"
            echo "  mode clean        — очистка системы"
            echo "  mode ip           — сетевая информация"
            echo "  mode seo-speed URL — анализ скорости"
            echo ""
            echo "📁 ПРОЕКТЫ:"
            echo "  mode project      — список проектов"
            echo "  mode project NAME — открыть проект"
            echo "  mode cp NAME TYPE — создать проект"
            echo ""
            echo "💡 mode sm1le автоматически запускает JARVIS!"
            ;;

        *)
            echo "❌ Неизвестная команда: $1"
            echo "   Используйте: mode help"
            return 1
            ;;
    esac
}

# Алиасы для быстрого доступа
alias j="mode jarvis"
alias jarvis="mode jarvis"
alias work="mode work"
alias chill="mode chill"
alias focus="mode focus"
alias smile="mode sm1le"