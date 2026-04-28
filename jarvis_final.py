#!/usr/bin/env python3
"""
J.A.R.V.I.S. Final Edition - Полная версия с системными функциями
Использует ТОЛЬКО оригинальные звуки из Iron Man, никакого синтеза речи
Автор: SteelRework AI
"""

import os
import sys
import subprocess
import speech_recognition as sr
import pygame
import re
import time
from datetime import datetime
import random
from pathlib import Path
import webbrowser
import urllib.parse

class JARVIS:
    def __init__(self, sounds_dir=None):
        # Путь к папке со звуками
        if sounds_dir:
            self.sounds_dir = Path(sounds_dir)
        else:
            self.sounds_dir = Path.home() / '.jarvis' / 'sounds'

        if not self.sounds_dir.exists():
            print(f"⚠️  Папка со звуками не найдена: {self.sounds_dir}")
            print("   Создайте папку и поместите туда .wav файлы JARVIS")
            sys.exit(1)

        # Инициализация pygame для воспроизведения звуков
        pygame.mixer.init()

        # Инициализация распознавания речи
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Настройка параметров распознавания
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True

        # Имя пользователя
        self.user_name = "сэр"

        # Текущий уровень громкости
        self.current_volume = None

        # Мапинг приложений
        self.apps_map = {
            'firefox': 'Firefox',
            'фаерфокс': 'Firefox',
            'браузер': 'Firefox',
            'telegram': 'Telegram',
            'телеграм': 'Telegram',
            'телега': 'Telegram',
            'discord': 'Discord',
            'дискорд': 'Discord',
            'код': 'Visual Studio Code',
            'vscode': 'Visual Studio Code',
            'vs code': 'Visual Studio Code',
            'figma': 'Figma',
            'фигма': 'Figma',
            'spotify': 'Spotify',
            'спотифай': 'Spotify',
            'музыка': 'Spotify',
            'music': 'Music',
            'notion': 'Notion',
            'obsidian': 'Obsidian',
            'обсидиан': 'Obsidian',
            'заметки': 'Notes',
            'notes': 'Notes',
            'календарь': 'Calendar',
            'терминал': 'Terminal',
            'terminal': 'Terminal',
            'настройки': 'System Preferences',
            'finder': 'Finder',
            'файлы': 'Finder'
        }

        # Загружаем ВСЕ доступные звуки
        self.setup_all_sounds()

    def setup_all_sounds(self):
        """Мапинг ВСЕХ звуков JARVIS на ситуации"""
        self.sound_map = {
            # === ПРИВЕТСТВИЯ И БАЗОВЫЕ ОТВЕТЫ ===
            'greeting': 'Джарвис - приветствие.wav',
            'greeting_full': 'Джарвис - приветствие (Песня целиком).wav',
            'morning': 'Доброе утро.wav',
            'yes_sir': ['Да сэр.wav', 'Да сэр(второй).wav'],
            'есть': 'Есть.wav',
            'at_service': 'К вашим услугам сэр.wav',
            'always_at_service': 'Всегда к вашим услугам сэр.wav',
            'as_you_wish': 'Как пожелаете .wav',

            # === ПРОЦЕССЫ И ОПЕРАЦИИ ===
            'loading': 'Загружаю сэр.wav',
            'request_complete': 'Запрос выполнен сэр.wav',
            'connected': 'Мы подключены и готовы.wav',
            'working_on_project': 'Мы работаем над проектом сэр 2.wav',
            'auto_assembly': 'Начинаю автоматическую сборку.wav',
            'calibrating': 'Импортирую установки, начинаю калибровку виртуальной среды.wav',
            'diagnostics': ['Начинаю диагностику системы.wav', 'Начинаю диагностику системы (второй).wav'],
            'check_complete': 'Проверка завершена.wav',
            'scan_complete': 'Сканирование макета завершено.wav',
            'image_created': ['Образ создан.wav', 'Образ создан (второй).wav'],
            'create_visual': 'Создать визуальный образ по новым спецификациям.wav',
            'oracle_grid': 'Выхожу на грид оракл.wav',

            # === ПИТАНИЕ И СИСТЕМА ===
            'power_off': 'Отключаю питание.wav',
            'power_off_diagnostic': 'Отключаю питание, начинаю диагностику системы.wav',
            'emergency_power': 'Включилось аварийное резервное питание.wav',
            'rebooted': 'Я перезагрузился сэр.wav',
            'battery': 'Заряд батареи, %.wav',
            'charge_depleted': 'Еще один заряд израсходован.wav',

            # === ТЕХНИЧЕСКИЕ И НАУЧНЫЕ ===
            'simulations': 'Я провел симуляции со всеми известными элементами.wav',
            'new_element': 'Вы создали новый элемент.wav',
            'reactor_modified': 'Реактор принял модифицированное ядро.wav',
            'reactor_warning': 'Реактор не предназначен для длительных полетов.wav',
            'cant_synthesize': 'К сожалению его невозможно синтезировать.wav',
            'palladium_replacement': 'Предлагаемый элемент может стать безвредной заменой палладию.wav',
            'save_to_stark': 'Сохранить его в центральной базе данных Stark Industries.wav',
            'exosystems': 'Для полетов на другие планеты слелует усовершенствовать экзосистемы.wav',

            # === ПРЕДУПРЕЖДЕНИЯ ===
            'under_fire': 'Сэр, вы под прицелом, нужен обманный маневр.wav',
            'flight_data': 'Сэр, для реальной попытки полета не просчитаны еще террабайты данных.wav',
            'health_warning': 'К сожалению устройство которое сохраняет вам жизнь в то же время убивает вас.wav',
            'suit_condition': 'Судя по всему, использование костюма железного человека усугубляет ваше состояние.wav',
            'time_running_out': 'У вас на исходе и время, и варианты решения проблемы.wav',
            'enemy_can_fly': 'Сэр, похоже его костюм может летать.wav',

            # === ИНФОРМАЦИЯ И СТАТУС ===
            'no_other_info': 'Другой информации нет.wav',
            'call_tracking': 'Отслеживание звонка не завершено.wav',
            'very_clever': 'Очень тонкое замечание сэр.wav',
            'congratulations': 'Поздравляю сэр.wav',
            'what_trying': 'Чего вы пытаетесь добиться сэр.wav',

            # === ЮМОР И ПЕРСОНАЛЬНОСТЬ ===
            'miss_potts': 'Приближается мисс поттс =).wav',
            'thinking': 'О чем я думал, обычно у нас все веселенькое.wav',
            'dont_move': 'Сэр, не будете дергаться больно не будет.wav',
            'stealth_mode': 'Да, это поможет вам оставаться незамеченным.wav',

            # === ЛОКАЦИИ ===
            'east_coast': 'Восточное побережье.wav',
            'new_york': 'Район Нью-Йорка, Манхэттэн и окрестности.wav',

            # === ИСТОРИЯ ===
            'ivan_vanko': 'Рассказ про Ивана Ванко.wav'
        }

        # Проверяем доступность файлов и создаём рабочий мапинг
        self.available_sounds = {}
        missing_sounds = []

        for key, value in self.sound_map.items():
            if isinstance(value, list):
                available = []
                for sound in value:
                    if (self.sounds_dir / sound).exists():
                        available.append(sound)
                    else:
                        missing_sounds.append(sound)
                if available:
                    self.available_sounds[key] = available
            else:
                if (self.sounds_dir / value).exists():
                    self.available_sounds[key] = value
                else:
                    missing_sounds.append(value)

        print(f"📂 Загружено {len(self.available_sounds)} из {len(self.sound_map)} звуковых категорий")

        if missing_sounds:
            print(f"⚠️  Отсутствуют звуки: {len(missing_sounds)} файлов")
            if len(missing_sounds) <= 5:
                for sound in missing_sounds:
                    print(f"   - {sound}")

    def play_sound(self, sound_key=None, sound_file=None, wait=True):
        """Воспроизвести звук JARVIS"""
        try:
            # Определяем какой файл играть
            if sound_key and sound_key in self.available_sounds:
                sounds = self.available_sounds[sound_key]
                if isinstance(sounds, list):
                    sound_file = random.choice(sounds)
                else:
                    sound_file = sounds

            if sound_file:
                file_path = self.sounds_dir / sound_file
                if file_path.exists():
                    print(f"🎵 JARVIS: {sound_file.replace('.wav', '')}")
                    pygame.mixer.music.load(str(file_path))
                    pygame.mixer.music.play()

                    if wait:
                        while pygame.mixer.music.get_busy():
                            time.sleep(0.1)
                    return True

            # Если звук не найден - используем альтернативы
            print(f"⚠️  Звук '{sound_key}' не найден")
            return False

        except Exception as e:
            print(f"❌ Ошибка воспроизведения: {e}")
            return False

    def speak(self, text, sound_key=None):
        """Говорить ТОЛЬКО оригинальными звуками JARVIS"""
        # Выводим текст для понимания что происходит
        print(f"💭 [{text}]")

        # Играем соответствующий звук
        if sound_key:
            self.play_sound(sound_key)
        else:
            # Если нет конкретного звука - используем базовый ответ
            self.play_sound('yes_sir')

    def listen(self, timeout=5):
        """Слушать команду от пользователя"""
        with self.microphone as source:
            print("🎧 Калибрую микрофон...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

            print("🎤 Слушаю...")
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
                print("⏳ Распознаю...")
                text = self.recognizer.recognize_google(audio, language='ru-RU')
                print(f"👤 Вы: {text}")
                return text.lower()
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                print("❓ Не удалось распознать")
                return None
            except sr.RequestError as e:
                print(f"❌ Ошибка сервиса распознавания: {e}")
                return None

    # === СИСТЕМНЫЕ ФУНКЦИИ ===

    def change_volume(self, action):
        """Управление громкостью системы"""
        if action == 'up':
            # Увеличить громкость
            script = "set volume output volume (output volume of (get volume settings) + 10)"
            self.play_sound('yes_sir')
        elif action == 'down':
            # Уменьшить громкость
            script = "set volume output volume (output volume of (get volume settings) - 10)"
            self.play_sound('yes_sir')
        elif action == 'mute':
            # Выключить звук
            script = "set volume output muted true"
            self.play_sound('power_off')
        elif action == 'unmute':
            # Включить звук
            script = "set volume output muted false"
            self.play_sound('connected')
        elif action == 'max':
            # Максимальная громкость
            script = "set volume output volume 100"
            self.play_sound('emergency_power')
        elif action == 'half':
            # Половина громкости
            script = "set volume output volume 50"
            self.play_sound('yes_sir')
        else:
            return False

        subprocess.run(['osascript', '-e', script], check=False)
        return True

    def change_brightness(self, action):
        """Управление яркостью экрана"""
        if action == 'up':
            # Увеличить яркость
            script = 'tell application "System Events" to key code 113'
        elif action == 'down':
            # Уменьшить яркость
            script = 'tell application "System Events" to key code 107'
        elif action == 'max':
            # Максимальная яркость
            for _ in range(16):
                subprocess.run(['osascript', '-e',
                    'tell application "System Events" to key code 113'], check=False)
            self.play_sound('yes_sir')
            return True
        else:
            return False

        subprocess.run(['osascript', '-e', script], check=False)
        self.play_sound('yes_sir')
        return True

    def control_spotify(self, action):
        """Управление Spotify"""
        try:
            if action == 'play':
                script = 'tell application "Spotify" to play'
                self.play_sound('yes_sir')
            elif action == 'pause':
                script = 'tell application "Spotify" to pause'
                self.play_sound('yes_sir')
            elif action == 'next':
                script = 'tell application "Spotify" to next track'
                self.play_sound('yes_sir')
            elif action == 'previous':
                script = 'tell application "Spotify" to previous track'
                self.play_sound('yes_sir')
            elif 'play_song' in action:
                # Воспроизвести конкретную песню
                song_name = action.replace('play_song:', '')
                script = f'''
                tell application "Spotify"
                    play track whose name contains "{song_name}"
                end tell
                '''
                self.play_sound('loading')
            else:
                return False

            subprocess.run(['osascript', '-e', script], check=False)
            time.sleep(1)
            self.play_sound('request_complete')
            return True
        except:
            return False

    def take_screenshot(self):
        """Сделать скриншот"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"~/Desktop/Screenshot_{timestamp}.png"

        # Команда для скриншота
        subprocess.run(['screencapture', '-x', os.path.expanduser(screenshot_path)], check=False)
        self.play_sound('scan_complete')
        return True

    def lock_screen(self):
        """Заблокировать экран"""
        self.play_sound('stealth_mode')
        time.sleep(1)
        # Блокировка экрана через горячие клавиши
        script = '''
        tell application "System Events"
            key code 12 using {control down, command down}
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=False)
        return True

    def open_application(self, app_name):
        """Открыть приложение"""
        try:
            subprocess.run(['open', '-a', app_name], check=True)
            return True
        except:
            return False

    def open_firefox(self, url=None):
        """Открыть Firefox"""
        try:
            if url:
                subprocess.run(['open', '-a', 'Firefox', url], check=True)
            else:
                subprocess.run(['open', '-a', 'Firefox'], check=True)
            return True
        except:
            if url:
                webbrowser.open(url)
            return False

    def search_web(self, query, engine='google'):
        """Поиск в интернете"""
        query_encoded = urllib.parse.quote(query)

        if engine == 'google':
            url = f'https://www.google.com/search?q={query_encoded}'
        elif engine == 'youtube':
            url = f'https://www.youtube.com/results?search_query={query_encoded}'
        else:
            url = f'https://www.google.com/search?q={query_encoded}'

        self.open_firefox(url)

    def execute_mode_command(self, mode):
        """Выполнить mode команду"""
        print(f"🔧 Выполняю: mode {mode}")

        env = os.environ.copy()
        env['PATH'] = f"/opt/homebrew/bin:/usr/local/bin:{env.get('PATH', '')}"

        try:
            result = subprocess.run(
                ['/bin/zsh', '-i', '-c', f'mode {mode}'],
                capture_output=True,
                text=True,
                env=env,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False

    def process_command(self, command):
        """Обработать голосовую команду"""
        if not command:
            return

        print(f"\n📝 Команда: '{command}'")

        # === УПРАВЛЕНИЕ ГРОМКОСТЬЮ ===
        if any(phrase in command for phrase in [
            'громче', 'увеличь громкость', 'сделай громче', 'прибавь звук'
        ]):
            self.change_volume('up')
            return

        if any(phrase in command for phrase in [
            'тише', 'уменьши громкость', 'сделай тише', 'убавь звук'
        ]):
            self.change_volume('down')
            return

        if any(phrase in command for phrase in [
            'выключи звук', 'без звука', 'mute', 'заглуши'
        ]):
            self.change_volume('mute')
            return

        if any(phrase in command for phrase in [
            'включи звук', 'верни звук', 'unmute'
        ]):
            self.change_volume('unmute')
            return

        if 'максимальная громкость' in command or 'максимум громкости' in command:
            self.change_volume('max')
            return

        # === УПРАВЛЕНИЕ ЯРКОСТЬЮ ===
        if 'ярче' in command or 'увеличь яркость' in command:
            self.change_brightness('up')
            return

        if 'темнее' in command or 'уменьши яркость' in command:
            self.change_brightness('down')
            return

        if 'максимальная яркость' in command:
            self.change_brightness('max')
            return

        # === УПРАВЛЕНИЕ МУЗЫКОЙ (SPOTIFY) ===
        if any(phrase in command for phrase in [
            'включи музыку', 'запусти музыку', 'play', 'играй'
        ]):
            self.play_sound('loading')
            self.control_spotify('play')
            return

        if any(phrase in command for phrase in [
            'пауза', 'останови музыку', 'pause', 'стоп музыка'
        ]):
            self.control_spotify('pause')
            return

        if any(phrase in command for phrase in [
            'следующая песня', 'следующий трек', 'next', 'дальше'
        ]):
            self.control_spotify('next')
            return

        if any(phrase in command for phrase in [
            'предыдущая песня', 'предыдущий трек', 'previous', 'назад'
        ]):
            self.control_spotify('previous')
            return

        if 'включи песню' in command or 'поставь песню' in command:
            # Извлекаем название песни
            song = command.replace('включи песню', '').replace('поставь песню', '').strip()
            if song:
                self.control_spotify(f'play_song:{song}')
            return

        # === СИСТЕМНЫЕ КОМАНДЫ ===
        if 'скриншот' in command or 'снимок экрана' in command:
            self.take_screenshot()
            return

        if any(phrase in command for phrase in [
            'заблокируй', 'блокировка', 'lock', 'заблокировать экран'
        ]):
            self.lock_screen()
            return

        # === БРАУЗЕР И ПОИСК ===
        if 'открой сайт' in command:
            words = command.split()
            for word in words:
                if '.' in word and len(word) > 4:
                    url = f'https://{word}' if not word.startswith('http') else word
                    self.play_sound('oracle_grid')
                    self.open_firefox(url)
                    time.sleep(1)
                    self.play_sound('connected')
                    return
            self.play_sound('no_other_info')
            return

        if 'найди' in command or 'поищи' in command:
            search_terms = command.split('найди', 1)[1].strip() if 'найди' in command else command.split('поищи', 1)[1].strip()
            if search_terms:
                self.play_sound('oracle_grid')
                self.search_web(search_terms)
                time.sleep(1)
                self.play_sound('request_complete')
            return

        if 'youtube' in command or 'ютуб' in command:
            self.play_sound('loading')
            self.open_firefox('https://youtube.com')
            time.sleep(1)
            self.play_sound('connected')
            return

        # === ОТКРЫТИЕ ПРИЛОЖЕНИЙ ===
        if 'открой' in command or 'запусти' in command:
            app_found = False
            for key, app_name in self.apps_map.items():
                if key in command:
                    self.play_sound('loading')
                    if self.open_application(app_name):
                        time.sleep(1)
                        self.play_sound('request_complete')
                    else:
                        self.play_sound('no_other_info')
                    app_found = True
                    break

            if not app_found:
                self.play_sound('no_other_info')
            return

        # === MODE КОМАНДЫ ===

        # ОТКЛЮЧИ ВСЁ
        if any(phrase in command for phrase in [
            'отключи всё', 'выключи всё', 'закрой всё',
            'конец работы', 'завершить всё'
        ]):
            self.play_sound('power_off')
            if self.execute_mode_command('off'):
                time.sleep(2)
                self.play_sound('check_complete')
            return

        # Личный режим
        if 'личный' in command or 'персональный' in command or 'смайл' in command:
            self.play_sound('calibrating')
            if self.execute_mode_command('sm1le'):
                time.sleep(2)
                self.play_sound('image_created')
            return

        # Рабочий режим
        if 'рабочий' in command or 'работа' in command:
            self.play_sound('working_on_project')
            if self.execute_mode_command('work'):
                time.sleep(2)
                self.play_sound('connected')
            return

        # Учебный режим
        if 'учебный' in command or 'учёба' in command:
            self.play_sound('loading')
            if self.execute_mode_command('study'):
                time.sleep(2)
                self.play_sound('connected')
            return

        # SEO режим
        if 'seo' in command or 'сео' in command:
            self.play_sound('simulations')
            if self.execute_mode_command('seo'):
                time.sleep(2)
                self.play_sound('connected')
            return

        # Отдых
        if 'отдых' in command or 'отдохнуть' in command or 'чилл' in command:
            self.play_sound('thinking')
            if self.execute_mode_command('chill'):
                time.sleep(2)
                self.play_sound('at_service')
            return

        # Фокус
        if 'фокус' in command or 'концентрация' in command:
            self.play_sound('stealth_mode')
            if self.execute_mode_command('focus'):
                time.sleep(2)
                self.play_sound('request_complete')
            return

        # Встреча
        if 'встреча' in command or 'созвон' in command:
            self.play_sound('loading')
            if self.execute_mode_command('meeting'):
                time.sleep(2)
                self.play_sound('connected')
            return

        # === УТИЛИТЫ ===

        # Очистка системы
        if 'очисти' in command or 'почисти' in command:
            self.play_sound('diagnostics')
            if self.execute_mode_command('clean'):
                time.sleep(3)
                self.play_sound('check_complete')
            return

        # IP адрес
        if 'ip' in command or 'айпи' in command:
            self.play_sound('loading')
            self.execute_mode_command('ip')
            return

        # Статус системы
        if 'статус' in command or 'диагностика' in command:
            self.play_sound('diagnostics')
            # Батарея
            battery = subprocess.run(
                "pmset -g batt | grep -Eo '[0-9]+%' | head -1",
                shell=True, capture_output=True, text=True
            ).stdout.strip()

            if battery:
                self.play_sound('battery')
                time.sleep(0.5)
                print(f"🔋 Заряд: {battery}")

                # Если низкий заряд - предупреждаем
                battery_int = int(battery.replace('%', ''))
                if battery_int < 20:
                    self.play_sound('charge_depleted')
                elif battery_int < 10:
                    self.play_sound('time_running_out')

            time.sleep(1)
            self.play_sound('check_complete')
            return

        # === СПЕЦИАЛЬНЫЕ КОМАНДЫ ===

        # Приветствие
        if any(word in command for word in ['привет', 'здравствуй', 'добрый']):
            hour = datetime.now().hour
            if hour < 12:
                self.play_sound('morning')
            else:
                self.play_sound('always_at_service')
            return

        # Экстренный режим
        if 'экстренный' in command or 'аварийный' in command:
            self.play_sound('emergency_power')
            time.sleep(1)
            self.play_sound('power_off_diagnostic')
            self.execute_mode_command('focus')
            return

        # Перезагрузка JARVIS
        if 'перезагрузись' in command or 'рестарт' in command:
            self.play_sound('power_off')
            time.sleep(2)
            self.play_sound('rebooted')
            time.sleep(1)
            self.play_sound('connected')
            return

        # Спасибо
        if 'спасибо' in command:
            responses = ['at_service', 'always_at_service', 'yes_sir']
            self.play_sound(random.choice(responses))
            return

        # Помощь
        if 'помощь' in command or 'что ты умеешь' in command:
            self.play_sound('at_service')
            print("\n📋 Доступные команды:")
            print("🔊 Громкость: громче, тише, выключи/включи звук")
            print("🎵 Музыка: включи музыку, пауза, следующая, предыдущая")
            print("💡 Яркость: ярче, темнее")
            print("📸 Система: скриншот, заблокируй экран")
            print("🌐 Интернет: найди X, открой сайт X")
            print("📱 Приложения: открой Telegram/Spotify/VS Code")
            print("🏠 Режимы: личный/рабочий/учебный режим")
            print("🛑 Управление: отключи всё")
            return

        # Выход
        if any(word in command for word in ['выход', 'пока', 'до свидания']):
            self.play_sound('always_at_service')
            return 'exit'

        # Неизвестная команда
        self.play_sound('no_other_info')

    def start(self):
        """Основной цикл работы"""
        print("\n" + "="*50)
        print("🤖 J.A.R.V.I.S. FINAL EDITION")
        print("="*50)

        # Приветствие оригинальным звуком
        if (self.sounds_dir / 'Джарвис - приветствие.wav').exists():
            self.play_sound(sound_file='Джарвис - приветствие.wav')
        else:
            self.play_sound('connected')

        print("\n💡 Примеры команд:")
        print("   🔊 'Джарвис, громче/тише'")
        print("   🎵 'Джарвис, включи музыку'")
        print("   🛑 'Джарвис, отключи всё'")
        print("   🌐 'Джарвис, найди рецепт'")
        print("   📸 'Джарвис, сделай скриншот'\n")

        while True:
            print("\n⏳ Жду 'Джарвис'...")
            activation = self.listen(timeout=3)

            if activation and ('джарвис' in activation or 'jarvis' in activation):
                # Случайный ответ JARVIS
                responses = ['yes_sir', 'at_service', 'есть']
                self.play_sound(random.choice(responses))

                # Слушаем команду
                command = self.listen(timeout=10)
                if command:
                    result = self.process_command(command)
                    if result == 'exit':
                        break
                else:
                    self.play_sound('no_other_info')

            elif activation and 'выход' in activation:
                self.play_sound('power_off')
                break

        print("\n👋 JARVIS завершил работу")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='JARVIS Final Edition')
    parser.add_argument('--sounds', '-s', type=str, help='Путь к папке со звуками')
    args = parser.parse_args()

    try:
        jarvis = JARVIS(sounds_dir=args.sounds)
        jarvis.start()
    except KeyboardInterrupt:
        print("\n⛔ Прервано пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()