#!/usr/bin/env python3
"""
J.A.R.V.I.S. Advanced - Полная интеграция с mode системой
Голосовой ассистент с оригинальными звуками JARVIS из Iron Man
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
import json
from pathlib import Path
import threading

class JARVIS:
    def __init__(self, sounds_dir=None):
        print("Initializing JARVIS...")
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

        # Текущий контекст
        self.current_mode = None
        self.last_command_time = time.time()

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
            # Приветствия
            'greeting_morning': 'Доброе утро.wav',
            'greeting_main': 'Джарвис - приветствие.wav',
            'greeting_sir': 'Всегда к вашим услугам сэр.wav',
            'at_service': 'К вашим услугам сэр.wav',

            # Подтверждения
            'yes_sir': ['Да сэр.wav', 'Да сэр(второй).wav'],
            'as_you_wish': 'Как пожелаете .wav',
            'loading': 'Загружаю сэр.wav',
            'request_complete': 'Запрос выполнен сэр.wav',
            'есть': 'Есть.wav',

            # Системные операции
            'diagnostics': ['Начинаю диагностику системы.wav', 'Начинаю диагностику системы (второй).wav'],
            'check_complete': 'Проверка завершена.wav',
            'power_off': 'Отключаю питание.wav',
            'power_off_diagnostic': 'Отключаю питание, начинаю диагностику системы.wav',
            'rebooted': 'Я перезагрузился сэр.wav',
            'connected': 'Мы подключены и готовы.wav',
            'emergency_power': 'Включилось аварийное резервное питание.wav',

            # Работа с проектами
            'working_on_project': 'Мы работаем над проектом сэр 2.wav',
            'auto_assembly': 'Начинаю автоматическую сборку.wav',
            'calibrating': 'Импортирую установки, начинаю калибровку виртуальной среды.wav',
            'scan_complete': 'Сканирование макета завершено.wav',
            'image_created': ['Образ создан.wav', 'Образ создан (второй).wav'],
            'save_to_stark': 'Сохранить его в центральной базе данных Stark Industries.wav',
            'create_visual': 'Создать визуальный образ по новым спецификациям.wav',

            # Статус и информация
            'battery': 'Заряд батареи, %.wav',
            'no_other_info': 'Другой информации нет.wav',
            'very_clever': 'Очень тонкое замечание сэр.wav',
            'congratulations': 'Поздравляю сэр.wav',
            'charge_depleted': 'Еще один заряд израсходован.wav',

            # Технические фразы
            'new_element': 'Вы создали новый элемент.wav',
            'simulations': 'Я провел симуляции со всеми известными элементами.wav',
            'reactor_modified': 'Реактор принял модифицированное ядро.wav',
            'cant_synthesize': 'К сожалению его невозможно синтезировать.wav',
            'oracle_grid': 'Выхожу на грид оракл.wav',
            'stealth_mode': 'Да, это поможет вам оставаться незамеченным.wav',

            # Предупреждения
            'under_fire': 'Сэр, вы под прицелом, нужен обманный маневр.wav',
            'flight_not_ready': 'Сэр, для реальной попытки полета не просчитаны еще террабайты данных.wav',
            'reactor_warning': 'Реактор не предназначен для длительных полетов.wav',
            'health_warning': 'К сожалению устройство которое сохраняет вам жизнь в то же время убивает вас.wav',
            'time_running_out': 'У вас на исходе и время, и варианты решения проблемы.wav',

            # Юмор и персональность
            'miss_potts': 'Приближается мисс поттс =).wav',
            'thinking': 'О чем я думал, обычно у нас все веселенькое.wav',
            'what_trying': 'Чего вы пытаетесь добиться сэр.wav',
            'dont_move': 'Сэр, не будете дергаться больно не будет.wav',

            # Локации
            'east_coast': 'Восточное побережье.wav',
            'new_york': 'Район Нью-Йорка, Манхэттэн и окрестности.wav'
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

                    # Ждём окончания воспроизведения
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

        # Сначала пробуем воспроизвести звуковой файл
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

    def get_greeting(self):
        """Получить приветствие в зависимости от времени"""
        hour = datetime.now().hour
        if hour < 12:
            return ('greeting_morning', f"Доброе утро, {self.user_name}")
        else:
            return ('greeting_sir', f"К вашим услугам, {self.user_name}")

    def execute_mode_command(self, mode):
        """Выполнить mode команду"""
        try:
            self.current_mode = mode
            result = subprocess.run(
                f"source ~/.zshrc && mode {mode}",
                shell=True,
                executable="/bin/zsh",
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Ошибка выполнения: {e}")
            return False

    def get_system_status(self):
        """Получить подробный статус системы"""
        status = {}

        # Батарея
        battery = subprocess.run(
            "pmset -g batt | grep -Eo '[0-9]+%' | head -1",
            shell=True, capture_output=True, text=True
        ).stdout.strip()
        status['battery'] = battery

        # Время работы
        uptime = subprocess.run(
            "uptime | sed 's/.*up //' | sed 's/,.*//'",
            shell=True, capture_output=True, text=True
        ).stdout.strip()
        status['uptime'] = uptime

        # Свободное место
        disk = subprocess.run(
            "df -h / | awk 'NR==2 {print $4}'",
            shell=True, capture_output=True, text=True
        ).stdout.strip()
        status['disk'] = disk

        # Погода
        weather = subprocess.run(
            "curl -s 'wttr.in/Bishkek?format=%t' 2>/dev/null",
            shell=True, capture_output=True, text=True
        ).stdout.strip()
        status['weather'] = weather

        return status

    def process_command(self, command):
        """Обработать голосовую команду"""
        if not command:
            return

        # Обновляем время последней команды
        self.last_command_time = time.time()

        # === ПРИВЕТСТВИЯ ===
        if any(word in command for word in ['привет', 'здравствуй', 'добрый день', 'доброе утро']):
            sound_key, text = self.get_greeting()
            self.speak(text, sound_key)
            return

        # === РЕЖИМЫ РАБОТЫ (расширенные варианты) ===

        # Личный/персональный режим - sm1le
        if any(phrase in command for phrase in [
            'личный режим', 'персональный режим', 'мой режим',
            'смайл', 'режим смайл', 'перейди в личный'
        ]):
            self.speak("Активирую ваш персональный режим", 'as_you_wish')
            if self.execute_mode_command('sm1le'):
                self.speak("Персональное окружение настроено", 'image_created')
            return

        # Рабочий режим - work
        if any(phrase in command for phrase in [
            'рабочий режим', 'включи работу', 'режим работы',
            'начни работу', 'запусти работу', 'перейди в рабочий'
        ]):
            self.speak("Запускаю рабочий режим", 'loading')
            if self.execute_mode_command('work'):
                self.speak("Рабочее окружение готово", 'request_complete')
            return

        # Учебный режим - study
        if any(phrase in command for phrase in [
            'режим обучения', 'учебный режим', 'режим учебы',
            'включи учебу', 'начни обучение', 'перейди в учебный'
        ]):
            self.speak("Активирую учебный режим", 'yes_sir')
            if self.execute_mode_command('study'):
                self.speak("Учебное окружение загружено", 'connected')
            return

        # SEO режим - seo
        if any(phrase in command for phrase in [
            'seo режим', 'режим seo', 'включи seo',
            'оптимизация', 'перейди в seo'
        ]):
            self.speak("Запускаю SEO окружение", 'working_on_project')
            if self.execute_mode_command('seo'):
                self.speak("SEO инструменты готовы", 'connected')
            return

        # Режим отдыха - chill
        if any(phrase in command for phrase in [
            'режим отдыха', 'отдохнуть', 'расслабиться',
            'отдых', 'чилл', 'chill', 'перейди в отдых'
        ]):
            self.speak("Включаю режим отдыха", 'yes_sir')
            if self.execute_mode_command('chill'):
                self.speak("Приятного отдыха", 'at_service')
            return

        # Режим концентрации - focus
        if any(phrase in command for phrase in [
            'режим концентрации', 'сосредоточиться', 'фокус',
            'глубокая работа', 'не отвлекать', 'перейди в фокус'
        ]):
            self.speak("Активирую режим глубокой концентрации", 'calibrating')
            if self.execute_mode_command('focus'):
                self.speak("Режим концентрации активен. Все отвлекающие факторы отключены", 'stealth_mode')
            return

        # Встреча - meeting
        if any(phrase in command for phrase in [
            'встреча', 'созвон', 'конференция', 'звонок',
            'meeting', 'zoom', 'перейди во встречу'
        ]):
            self.speak("Подготавливаю окружение для встречи", 'loading')
            if self.execute_mode_command('meeting'):
                self.speak("Всё готово для конференции", 'connected')
            return

        # Закрыть всё - off
        if any(phrase in command for phrase in [
            'закрой всё', 'выключи всё', 'конец работы',
            'завершить работу', 'остановить всё', 'закончить день'
        ]):
            self.speak("Закрываю все рабочие приложения", 'power_off')
            if self.execute_mode_command('off'):
                self.speak("Рабочий день завершён", 'greeting_sir')
            return

        # === УТИЛИТЫ ===

        # Очистка системы - clean
        if any(phrase in command for phrase in [
            'очистить', 'почистить', 'освободи место',
            'очистка', 'удали кэш', 'почисти систему'
        ]):
            self.speak("Начинаю очистку системы", 'diagnostics')
            if self.execute_mode_command('clean'):
                self.speak("Очистка завершена. Система оптимизирована", 'check_complete')
            return

        # IP адрес - ip
        if any(phrase in command for phrase in [
            'мой ip', 'айпи адрес', 'ip адрес',
            'какой ip', 'покажи ip'
        ]):
            self.speak("Проверяю ваш IP адрес", 'loading')
            self.execute_mode_command('ip')
            self.speak("Информация выведена на экран", 'request_complete')
            return

        # Скорость сайта - seo-speed
        if 'скорость' in command and 'сайт' in command:
            # Извлекаем URL из команды
            words = command.split()
            for word in words:
                if '.' in word or 'ru' in word or 'com' in word:
                    self.speak(f"Анализирую скорость сайта {word}", 'scan_complete')
                    self.execute_mode_command(f'seo-speed {word}')
                    self.speak("Анализ завершён", 'check_complete')
                    return
            self.speak("Не удалось определить адрес сайта", 'no_other_info')
            return

        # === ПРОЕКТЫ ===

        # Создать проект - cp
        if 'создать проект' in command or 'новый проект' in command:
            match = re.search(r'проект\s+(\w+)', command)
            if match:
                project_name = match.group(1)
                self.speak(f"Создаю проект {project_name}", 'auto_assembly')

                flags = []
                if 'фронт' in command or 'frontend' in command:
                    flags.append('-front')
                if 'бэк' in command or 'backend' in command:
                    flags.append('-back')
                if 'мобильн' in command or 'mobile' in command:
                    flags.append('-mobile')
                if not flags:
                    flags = ['-front']

                if self.execute_mode_command(f'cp {project_name} {" ".join(flags)}'):
                    self.speak(f"Проект {project_name} создан и готов к работе", 'congratulations')
            return

        # Открыть проект - project
        if 'открыть проект' in command or 'открой проект' in command:
            match = re.search(r'проект\s+(\w+)', command)
            if match:
                project_name = match.group(1)
                self.speak(f"Открываю проект {project_name}", 'loading')
                if self.execute_mode_command(f'project {project_name}'):
                    self.speak(f"Проект {project_name} загружен", 'image_created')
                else:
                    self.speak(f"Проект {project_name} не найден", 'no_other_info')
            return

        # === СИСТЕМНАЯ ИНФОРМАЦИЯ ===

        # Подробный статус
        if any(phrase in command for phrase in [
            'статус', 'как дела', 'диагностика', 'состояние системы',
            'проверка системы', 'системная информация'
        ]):
            self.speak("Анализирую систему", 'diagnostics')
            status = self.get_system_status()

            # Батарея
            if status['battery']:
                self.play_sound('battery')
                time.sleep(0.5)
                self.speak(f"Заряд {status['battery']}")

            # Время работы
            if status['uptime']:
                self.speak(f"Система работает {status['uptime']}")

            # Свободное место
            if status['disk']:
                self.speak(f"Свободно {status['disk']} на диске")

            # Погода
            if status['weather']:
                self.speak(f"Температура в Бишкеке {status['weather']}")

            self.speak("Диагностика завершена", 'check_complete')
            return

        # Только батарея
        if 'батарея' in command or 'заряд' in command:
            battery = subprocess.run(
                "pmset -g batt | grep -Eo '[0-9]+%' | head -1",
                shell=True, capture_output=True, text=True
            ).stdout.strip()
            if battery:
                self.play_sound('battery')
                time.sleep(0.5)
                self.speak(f"Текущий заряд {battery}")

                # Предупреждение о низком заряде
                battery_int = int(battery.replace('%', ''))
                if battery_int < 20:
                    self.speak("Рекомендую подключить зарядку", 'charge_depleted')
            return

        # === СПЕЦИАЛЬНЫЕ КОМАНДЫ ===

        # Экстренный режим
        if 'экстренн' in command or 'срочн' in command or 'аварийн' in command:
            self.speak("Активирую экстренный режим", 'emergency_power')
            self.speak("Закрываю все лишние процессы", 'power_off_diagnostic')
            self.execute_mode_command('focus')
            return

        # Помощь
        if 'помощь' in command or 'что ты умеешь' in command or 'команды' in command:
            self.speak("Я могу управлять всеми вашими режимами работы", 'at_service')
            time.sleep(0.5)
            self.speak("Скажите 'перейди в личный режим' для активации вашего персонального окружения")
            self.speak("Или 'рабочий режим' для начала работы")
            self.speak("Также доступны: учебный, SEO, отдых, концентрация, встреча")
            self.speak("Могу создавать проекты, проверять систему, очищать кэш")
            return

        # === ЮМОР И ПЕРСОНАЛЬНОСТЬ ===

        if 'спасибо' in command:
            responses = ['at_service', 'greeting_sir', 'yes_sir']
            self.speak("Всегда пожалуйста", random.choice(responses))
            return

        if 'ты здесь' in command or 'ты тут' in command:
            self.speak("Да, я здесь", 'yes_sir')
            return

        if 'перезагрузись' in command or 'рестарт' in command:
            self.speak("Перезагружаюсь", 'rebooted')
            time.sleep(2)
            self.speak("Система перезагружена", 'connected')
            return

        if 'шутка' in command or 'пошути' in command:
            self.speak("Хм, дайте подумать", 'thinking')
            time.sleep(1)
            jokes = [
                "Почему программисты путают Хэллоуин и Рождество? Потому что Oct 31 = Dec 25",
                "В квантовой физике вы можете быть и живы, и мертвы одновременно. В программировании это называется undefined behavior",
                "Я бы рассказал вам шутку про UDP, но не уверен, что она дойдёт"
            ]
            self.speak(random.choice(jokes))
            return

        # === КОНТЕКСТНЫЕ ПОДСКАЗКИ ===

        # Если долго не было команд
        time_since_last = time.time() - self.last_command_time
        if time_since_last > 300:  # 5 минут
            if 9 <= datetime.now().hour <= 18:
                self.speak("Могу чем-то помочь?", 'at_service')
            return

        # === ВЫХОД ===

        if any(word in command for word in ['выход', 'пока', 'до свидания', 'завершить']):
            farewells = [
                ("Всегда к вашим услугам", 'greeting_sir'),
                ("До встречи, сэр", 'at_service'),
                ("Буду ждать вашего возвращения", 'yes_sir')
            ]
            text, sound = random.choice(farewells)
            self.speak(text, sound)
            return 'exit'

        # === НЕИЗВЕСТНАЯ КОМАНДА ===

        # Пытаемся понять намерение
        if 'включи' in command or 'запусти' in command or 'открой' in command:
            self.speak("Не понял, что именно запустить. Уточните команду", 'no_other_info')
        elif 'режим' in command:
            self.speak("Неизвестный режим. Доступны: личный, рабочий, учебный, SEO, отдых, концентрация, встреча", 'no_other_info')
        else:
            self.speak("Не понял команду. Скажите 'помощь' для списка возможностей", 'no_other_info')

    def start(self):
        """Основной цикл работы"""
        # Начальное приветствие
        self.play_sound(sound_file='Джарвис - приветствие.wav')
        time.sleep(0.5)
        self.speak("Система JARVIS активирована", 'connected')

        # Проверяем время и даём контекстную подсказку
        hour = datetime.now().hour
        if 9 <= hour < 12:
            self.speak("Рекомендую начать с персонального режима для просмотра дневной сводки", 'very_clever')
        elif 12 <= hour < 14:
            self.speak("Время обеда. Могу включить режим отдыха", 'at_service')
        elif 18 <= hour < 20:
            self.speak("Вечер. Готов завершить рабочий день или продолжить?", 'at_service')

        while True:
            print("\n⏳ Жду активационное слово 'Джарвис'...")
            activation = self.listen(timeout=3)

            if activation and ('джарвис' in activation or 'jarvis' in activation):
                # Активация - выбираем случайный ответ
                responses = ['yes_sir', 'at_service', 'loading']
                self.speak("Слушаю", random.choice(responses))

                # Слушаем команду
                command = self.listen(timeout=10)

                if command:
                    result = self.process_command(command)
                    if result == 'exit':
                        break
                else:
                    # Если не услышал, предлагаем повторить
                    self.speak("Не услышал команду. Повторите, пожалуйста", 'no_other_info')

            elif activation and 'выход' in activation:
                self.speak("Завершаю работу", 'power_off')
                break

        print("\n👋 JARVIS завершил работу")

def main():
    """Главная функция"""
    import argparse

    parser = argparse.ArgumentParser(description='JARVIS Advanced - голосовой ассистент')
    parser.add_argument('--sounds', '-s', type=str,
                        help='Путь к папке со звуками JARVIS')
    args = parser.parse_args()

    # Проверка зависимостей
    try:
        import pygame
        import speech_recognition
        import pyttsx3
    except ImportError as e:
        print(f"❌ Отсутствует библиотека: {e}")
        print("Запустите установщик: bash install-jarvis-voice.sh")
        sys.exit(1)

    try:
        jarvis = JARVIS(sounds_dir=args.sounds)
        jarvis.start()
    except KeyboardInterrupt:
        print("\n⛔ Прервано пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()