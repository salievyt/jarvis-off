#!/usr/bin/env python3
"""
J.A.R.V.I.S. Ultimate - Полная версия с управлением браузером и приложениями
Автор: SteelRework AI
"""

import os
import sys
import subprocess
import speech_recognition as sr
import pyttsx3
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

        # Инициализация синтеза речи как fallback
        self.engine = pyttsx3.init()
        self.setup_voice()

        # Инициализация распознавания речи
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Настройка параметров распознавания
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True

        # Имя пользователя
        self.user_name = "сэр"

        # Мапинг приложений
        self.apps_map = {
            # Браузеры
            'firefox': 'Firefox',
            'фаерфокс': 'Firefox',
            'браузер': 'Firefox',
            'chrome': 'Google Chrome',
            'хром': 'Google Chrome',
            'safari': 'Safari',
            'сафари': 'Safari',
            'андроид': 'Android Studio',
            'андроид студио': 'Android Studio',
            'Android Studio': 'Android Studio',

            # Коммуникация
            'telegram': 'Telegram',
            'телеграм': 'Telegram',
            'discord': 'Discord',
            'дискорд': 'Discord',
            'slack': 'Slack',
            'слак': 'Slack',
            'zoom': 'zoom.us',
            'зум': 'zoom.us',

            # Разработка
            'код': 'Visual Studio Code',
            'vscode': 'Visual Studio Code',
            'vs code': 'Visual Studio Code',
            'xcode': 'Xcode',

            # Дизайн
            'figma': 'Figma',
            'фигма': 'Figma',
            'photoshop': 'Adobe Photoshop',
            'фотошоп': 'Adobe Photoshop',

            # Музыка и видео
            'spotify': 'Spotify',
            'спотифай': 'Spotify',
            'music': 'Music',
            'музыка': 'Music',

            # Продуктивность
            'notion': 'Notion',
            'obsidian': 'Obsidian',
            'обсидиан': 'Obsidian',
            'notes': 'Notes',
            'заметки': 'Notes',
            'календарь': 'Calendar',
            'calendar': 'Calendar',

            # Системные
            'терминал': 'Terminal',
            'terminal': 'Terminal',
            'настройки': 'System Preferences',
            'settings': 'System Preferences',
            'finder': 'Finder',
            'файлы': 'Finder'
        }

        # Загружаем мапинг звуков
        self.setup_sound_mappings()

    def setup_voice(self):
        """Настройка голоса для fallback синтеза"""
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'daniel' in voice.id.lower() or 'british' in voice.id.lower():
                self.engine.setProperty('voice', voice.id)
                break
        self.engine.setProperty('rate', 175)
        self.engine.setProperty('volume', 0.9)

    def setup_sound_mappings(self):
        """Создаём мапинг команд на звуковые файлы"""
        self.sound_map = {
            'greeting_morning': 'Доброе утро.wav',
            'greeting_sir': 'Всегда к вашим услугам сэр.wav',
            'at_service': 'К вашим услугам сэр.wav',
            'yes_sir': ['Да сэр.wav', 'Да сэр(второй).wav'],
            'as_you_wish': 'Как пожелаете .wav',
            'loading': 'Загружаю сэр.wav',
            'request_complete': 'Запрос выполнен сэр.wav',
            'diagnostics': ['Начинаю диагностику системы.wav', 'Начинаю диагностику системы (второй).wav'],
            'check_complete': 'Проверка завершена.wav',
            'power_off': 'Отключаю питание.wav',
            'rebooted': 'Я перезагрузился сэр.wav',
            'connected': 'Мы подключены и готовы.wav',
            'working_on_project': 'Мы работаем над проектом сэр 2.wav',
            'auto_assembly': 'Начинаю автоматическую сборку.wav',
            'calibrating': 'Импортирую установки, начинаю калибровку виртуальной среды.wav',
            'image_created': ['Образ создан.wav', 'Образ создан (второй).wav'],
            'battery': 'Заряд батареи, %.wav',
            'no_other_info': 'Другой информации нет.wav',
            'congratulations': 'Поздравляю сэр.wav',
            'oracle_grid': 'Выхожу на грид оракл.wav'
        }

        # Проверяем доступность файлов
        self.available_sounds = {}
        for key, value in self.sound_map.items():
            if isinstance(value, list):
                available = []
                for sound in value:
                    if (self.sounds_dir / sound).exists():
                        available.append(sound)
                if available:
                    self.available_sounds[key] = available
            else:
                if (self.sounds_dir / value).exists():
                    self.available_sounds[key] = value

        print(f"📂 Загружено {len(self.available_sounds)} звуковых категорий")

    def play_sound(self, sound_key=None, sound_file=None):
        """Воспроизвести звук по ключу или файлу"""
        try:
            if sound_key and sound_key in self.available_sounds:
                sounds = self.available_sounds[sound_key]
                if isinstance(sounds, list):
                    sound_file = random.choice(sounds)
                else:
                    sound_file = sounds

            if sound_file:
                file_path = self.sounds_dir / sound_file
                if file_path.exists():
                    print(f"🎵 Воспроизвожу: {sound_file}")
                    pygame.mixer.music.load(str(file_path))
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
                    return True
            return False
        except Exception as e:
            print(f"❌ Ошибка воспроизведения: {e}")
            return False

    def speak(self, text, sound_key=None):
        """Произнести текст (звук или синтез)"""
        print(f"🎙 JARVIS: {text}")
        if sound_key and self.play_sound(sound_key):
            return
        # Если нет подходящего звука - используем синтез
        self.engine.say(text)
        self.engine.runAndWait()

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

    def open_application(self, app_name):
        """Открыть приложение на macOS"""
        try:
            subprocess.run(['open', '-a', app_name], check=True)
            return True
        except subprocess.CalledProcessError:
            print(f"⚠️  Приложение '{app_name}' не найдено")
            return False

    def open_firefox(self, url=None):
        """Открыть Firefox с URL или без"""
        try:
            if url:
                # Открываем Firefox с конкретным URL
                subprocess.run(['open', '-a', 'Firefox', url], check=True)
            else:
                # Просто открываем Firefox
                subprocess.run(['open', '-a', 'Firefox'], check=True)
            return True
        except:
            print("⚠️  Firefox не найден, пробую открыть в браузере по умолчанию")
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
        elif engine == 'yandex':
            url = f'https://yandex.ru/search/?text={query_encoded}'
        else:
            url = f'https://www.google.com/search?q={query_encoded}'

        self.open_firefox(url)

    def execute_mode_command(self, mode):
        """Выполнить mode команду"""
        print(f"🔧 Выполняю команду: mode {mode}")

        env = os.environ.copy()
        env['PATH'] = f"/opt/homebrew/bin:/usr/local/bin:{env.get('PATH', '')}"

        try:
            cmd = f'mode {mode}'
            result = subprocess.run(
                ['/bin/zsh', '-i', '-c', cmd],
                capture_output=True,
                text=True,
                env=env,
                timeout=10
            )

            print(f"   Результат: код {result.returncode}")
            return result.returncode == 0

        except subprocess.TimeoutExpired:
            print("   ⚠️ Команда выполняется слишком долго")
            return True
        except Exception as e:
            print(f"   ❌ Ошибка выполнения: {e}")
            return False

    def process_command(self, command):
        """Обработать голосовую команду"""
        if not command:
            return

        print(f"\n📝 Обрабатываю команду: '{command}'")

        # === БРАУЗЕР И ПОИСК ===

        # Открыть сайт
        if 'открой сайт' in command or 'открыть сайт' in command:
            # Ищем URL в команде
            words = command.split()
            for word in words:
                if '.' in word and len(word) > 4:
                    if not word.startswith('http'):
                        url = f'https://{word}'
                    else:
                        url = word
                    self.speak(f"Открываю {word}", 'loading')
                    self.open_firefox(url)
                    self.speak("Сайт открыт", 'request_complete')
                    return
            self.speak("Не понял какой сайт открыть", 'no_other_info')
            return

        # Поиск в Google
        if 'найди' in command or 'поищи' in command or 'гугл' in command:
            # Извлекаем поисковый запрос
            search_terms = []
            if 'найди' in command:
                search_terms = command.split('найди', 1)[1].strip()
            elif 'поищи' in command:
                search_terms = command.split('поищи', 1)[1].strip()
            elif 'гугл' in command:
                search_terms = command.split('гугл', 1)[1].strip()

            if search_terms:
                self.speak(f"Ищу {search_terms}", 'oracle_grid')
                self.search_web(search_terms, 'google')
                self.speak("Результаты поиска на экране", 'request_complete')
            else:
                self.speak("Что искать?", 'no_other_info')
            return

        # YouTube
        if 'youtube' in command or 'ютуб' in command:
            if 'найди' in command or 'поищи' in command:
                # Поиск на YouTube
                search = command.replace('youtube', '').replace('ютуб', '')
                search = search.replace('найди', '').replace('поищи', '').strip()
                if search:
                    self.speak(f"Ищу на YouTube", 'loading')
                    self.search_web(search, 'youtube')
                else:
                    self.speak("Открываю YouTube", 'loading')
                    self.open_firefox('https://youtube.com')
            else:
                self.speak("Открываю YouTube", 'loading')
                self.open_firefox('https://youtube.com')
            self.speak("YouTube открыт", 'request_complete')
            return

        # Просто открыть браузер
        if 'браузер' in command or 'firefox' in command or 'фаерфокс' in command:
            self.speak("Открываю Firefox", 'loading')
            self.open_firefox()
            self.speak("Браузер открыт", 'request_complete')
            return

        # === ОТКРЫТИЕ ПРИЛОЖЕНИЙ ===

        if 'открой' in command or 'запусти' in command:
            # Ищем название приложения
            app_found = False
            for key, app_name in self.apps_map.items():
                if key in command:
                    self.speak(f"Открываю {app_name}", 'loading')
                    if self.open_application(app_name):
                        self.speak(f"{app_name} запущен", 'request_complete')
                    else:
                        self.speak(f"Не удалось открыть {app_name}", 'no_other_info')
                    app_found = True
                    break

            if not app_found:
                # Пробуем открыть как есть
                words = command.split()
                if len(words) > 1:
                    app = words[-1].capitalize()
                    self.speak(f"Пробую открыть {app}", 'loading')
                    if self.open_application(app):
                        self.speak(f"{app} открыт", 'request_complete')
                    else:
                        self.speak(f"Приложение {app} не найдено", 'no_other_info')
            return

        # === MODE КОМАНДЫ ===

        # ОТКЛЮЧИ ВСЁ - mode off
        if any(phrase in command for phrase in [
            'отключи всё', 'выключи всё', 'закрой всё',
            'конец работы', 'завершить всё', 'стоп всё'
        ]):
            self.speak("Закрываю все приложения", 'power_off')
            if self.execute_mode_command('off'):
                time.sleep(2)
                self.speak("Все приложения закрыты", 'check_complete')
            return

        # Личный режим - sm1le
        if any(phrase in command for phrase in [
            'личный', 'персональный', 'мой режим', 'смайл'
        ]):
            self.speak("Активирую личный режим", 'as_you_wish')
            if self.execute_mode_command('sm1le'):
                time.sleep(2)
                self.speak("Персональное окружение готово", 'request_complete')
            return

        # Рабочий режим
        if any(phrase in command for phrase in [
            'рабочий', 'работу', 'работа', 'work'
        ]):
            self.speak("Запускаю рабочий режим", 'loading')
            if self.execute_mode_command('work'):
                time.sleep(2)
                self.speak("Рабочее окружение готово", 'request_complete')
            return

        # Учебный режим
        if any(phrase in command for phrase in [
            'учебный', 'обучение', 'учёба', 'study'
        ]):
            self.speak("Активирую учебный режим", 'yes_sir')
            if self.execute_mode_command('study'):
                time.sleep(2)
                self.speak("Учебное окружение загружено", 'connected')
            return

        # SEO режим
        if 'seo' in command or 'сео' in command:
            self.speak("Запускаю SEO режим", 'working_on_project')
            if self.execute_mode_command('seo'):
                time.sleep(2)
                self.speak("SEO инструменты готовы", 'connected')
            return

        # Режим отдыха
        if any(phrase in command for phrase in [
            'отдых', 'отдохнуть', 'расслаб', 'чилл', 'chill'
        ]):
            self.speak("Включаю режим отдыха", 'yes_sir')
            if self.execute_mode_command('chill'):
                time.sleep(2)
                self.speak("Приятного отдыха", 'at_service')
            return

        # Фокус
        if any(phrase in command for phrase in [
            'фокус', 'концентрац', 'сосредоточ', 'focus'
        ]):
            self.speak("Режим концентрации", 'calibrating')
            if self.execute_mode_command('focus'):
                time.sleep(2)
                self.speak("Отвлекающие факторы отключены", 'check_complete')
            return

        # Встреча
        if any(phrase in command for phrase in [
            'встреча', 'созвон', 'конференц', 'zoom', 'meeting'
        ]):
            self.speak("Готовлю встречу", 'loading')
            if self.execute_mode_command('meeting'):
                time.sleep(2)
                self.speak("Готово к конференции", 'connected')
            return

        # === УТИЛИТЫ ===

        # Очистка
        if 'очист' in command or 'чист' in command:
            self.speak("Очищаю систему", 'diagnostics')
            if self.execute_mode_command('clean'):
                time.sleep(3)
                self.speak("Очистка завершена", 'check_complete')
            return

        # IP адрес
        if 'ip' in command or 'айпи' in command:
            self.speak("Проверяю IP", 'loading')
            self.execute_mode_command('ip')
            return

        # Создать проект
        if 'создай проект' in command or 'новый проект' in command:
            match = re.search(r'проект\s+(\w+)', command)
            if match:
                project_name = match.group(1)
                self.speak(f"Создаю проект {project_name}", 'auto_assembly')

                flags = []
                if 'фронт' in command:
                    flags.append('-front')
                if 'бэк' in command:
                    flags.append('-back')
                if 'мобил' in command:
                    flags.append('-mobile')
                if not flags:
                    flags = ['-front']

                if self.execute_mode_command(f'cp {project_name} {" ".join(flags)}'):
                    self.speak(f"Проект {project_name} создан", 'congratulations')
            return

        # Статус
        if 'статус' in command or 'диагностик' in command:
            self.speak("Диагностика системы", 'diagnostics')
            battery = subprocess.run(
                "pmset -g batt | grep -Eo '[0-9]+%' | head -1",
                shell=True, capture_output=True, text=True
            ).stdout.strip()
            if battery:
                self.play_sound('battery')
                time.sleep(0.5)
                self.speak(f"Заряд {battery}")
            self.speak("Диагностика завершена", 'check_complete')
            return

        # === СПЕЦИАЛЬНЫЕ ===

        # Приветствие
        if any(word in command for word in ['привет', 'здравствуй', 'добрый']):
            self.speak("Приветствую вас", 'greeting_sir')
            return

        # Помощь
        if 'помощь' in command or 'умеешь' in command:
            self.speak("Я могу:", 'at_service')
            time.sleep(0.5)
            self.speak("Открывать сайты и искать в интернете")
            self.speak("Запускать приложения")
            self.speak("Управлять режимами работы")
            self.speak("Скажите 'отключи всё' чтобы закрыть все приложения")
            return

        # Спасибо
        if 'спасибо' in command:
            self.speak("Всегда пожалуйста", 'at_service')
            return

        # Выход
        if any(word in command for word in ['выход', 'пока', 'до свидания']):
            self.speak("До встречи", 'greeting_sir')
            return 'exit'

        # Неизвестная команда
        self.speak("Не понял команду", 'no_other_info')

    def start(self):
        """Основной цикл работы"""
        print("\n" + "="*50)
        print("🤖 JARVIS ULTIMATE ЗАПУЩЕН")
        print("="*50)

        # Приветствие
        if (self.sounds_dir / 'Джарвис - приветствие.wav').exists():
            self.play_sound(sound_file='Джарвис - приветствие.wav')
        else:
            self.speak("Система JARVIS активирована", 'connected')

        print("\n💡 Команды:")
        print("   🌐 'Открой сайт google.com'")
        print("   🔍 'Найди рецепт пиццы'")
        print("   📺 'Открой YouTube'")
        print("   📱 'Открой Telegram'")
        print("   🛑 'Отключи всё'")
        print("   🏠 'Личный режим'\n")

        while True:
            print("\n⏳ Жду 'Джарвис'...")
            activation = self.listen(timeout=3)

            if activation and ('джарвис' in activation or 'jarvis' in activation):
                # Отклик
                responses = ['yes_sir', 'at_service', 'loading']
                self.speak("Слушаю", random.choice(responses))

                # Слушаем команду
                command = self.listen(timeout=10)
                if command:
                    result = self.process_command(command)
                    if result == 'exit':
                        break
                else:
                    self.speak("Повторите команду", 'no_other_info')

            elif activation and 'выход' in activation:
                self.speak("Выключаюсь", 'power_off')
                break

        print("\n👋 JARVIS завершил работу")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='JARVIS Ultimate')
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