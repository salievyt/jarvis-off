#!/usr/bin/env python3
"""
J.A.R.V.I.S. - Just A Rather Very Intelligent System
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

class JARVIS:
    def __init__(self, sounds_dir=None):
        # Путь к папке со звуками
        if sounds_dir:
            self.sounds_dir = Path(sounds_dir)
        else:
            # По умолчанию ищем в ~/.jarvis/sounds/
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

            # Системные операции
            'diagnostics': ['Начинаю диагностику системы.wav', 'Начинаю диагностику системы (второй).wav'],
            'check_complete': 'Проверка завершена.wav',
            'power_off': 'Отключаю питание.wav',
            'rebooted': 'Я перезагрузился сэр.wav',
            'connected': 'Мы подключены и готовы.wav',

            # Работа с проектами
            'working_on_project': 'Мы работаем над проектом сэр 2.wav',
            'auto_assembly': 'Начинаю автоматическую сборку.wav',
            'calibrating': 'Импортирую установки, начинаю калибровку виртуальной среды.wav',
            'scan_complete': 'Сканирование макета завершено.wav',
            'image_created': ['Образ создан.wav', 'Образ создан (второй).wav'],

            # Статус и информация
            'battery': 'Заряд батареи, %.wav',
            'no_other_info': 'Другой информации нет.wav',
            'very_clever': 'Очень тонкое замечание сэр.wav',
            'congratulations': 'Поздравляю сэр.wav',

            # Юмор и персональность
            'miss_potts': 'Приближается мисс поттс =).wav',
            'thinking': 'О чем я думал, обычно у нас все веселенькое.wav',
            'what_trying': 'Чего вы пытаетесь добиться сэр.wav',

            # Технические фразы
            'new_element': 'Вы создали новый элемент.wav',
            'simulations': 'Я провел симуляции со всеми известными элементами.wav',
            'emergency_power': 'Включилось аварийное резервное питание.wav',
            'reactor_modified': 'Реактор принял модифицированное ядро.wav'
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

    def process_command(self, command):
        """Обработать голосовую команду"""
        if not command:
            return

        # Приветствия
        if any(word in command for word in ['привет', 'здравствуй', 'добрый день', 'доброе утро']):
            sound_key, text = self.get_greeting()
            self.speak(text, sound_key)
            return

        # Режимы работы
        if 'рабочий режим' in command or 'включи работу' in command:
            self.speak("Запускаю рабочий режим", 'loading')
            if self.execute_mode_command('work'):
                self.speak("Рабочее окружение готово", 'request_complete')
            return

        if 'режим обучения' in command or 'учебный режим' in command:
            self.speak("Активирую учебный режим", 'yes_sir')
            if self.execute_mode_command('study'):
                self.speak("Учебное окружение загружено", 'image_created')
            return

        if 'seo режим' in command or 'режим seo' in command:
            self.speak("Запускаю SEO окружение", 'working_on_project')
            if self.execute_mode_command('seo'):
                self.speak("SEO инструменты готовы к работе", 'connected')
            return

        if 'персональный режим' in command or 'мой режим' in command or 'смайл' in command:
            self.speak(f"Активирую ваш персональный режим", 'as_you_wish')
            if self.execute_mode_command('sm1le'):
                self.speak("Персональное окружение настроено", 'check_complete')
            return

        if 'режим отдыха' in command or 'отдохнуть' in command:
            self.speak("Включаю режим отдыха", 'yes_sir')
            if self.execute_mode_command('chill'):
                self.speak("Приятного отдыха", 'at_service')
            return

        if 'режим концентрации' in command or 'сосредоточиться' in command or 'фокус' in command:
            self.speak("Активирую режим глубокой концентрации", 'calibrating')
            if self.execute_mode_command('focus'):
                self.speak("Режим концентрации активен", 'request_complete')
            return

        if 'встреча' in command or 'созвон' in command:
            self.speak("Подготавливаю окружение для встречи", 'loading')
            if self.execute_mode_command('meeting'):
                self.speak("Всё готово для конференции", 'connected')
            return

        if 'закрой всё' in command or 'выключи всё' in command or 'конец работы' in command:
            self.speak("Закрываю все рабочие приложения", 'power_off')
            if self.execute_mode_command('off'):
                self.speak("Рабочий день завершён", 'greeting_sir')
            return

        # Утилиты
        if 'очистить' in command or 'почистить' in command:
            self.speak("Начинаю очистку системы", 'diagnostics')
            if self.execute_mode_command('clean'):
                self.speak("Очистка завершена", 'check_complete')
            return

        if 'мой ip' in command or 'айпи адрес' in command:
            self.speak("Проверяю ваш IP адрес", 'loading')
            self.execute_mode_command('ip')
            return

        if 'создать проект' in command or 'новый проект' in command:
            match = re.search(r'проект\s+(\w+)', command)
            if match:
                project_name = match.group(1)
                self.speak(f"Создаю проект {project_name}", 'auto_assembly')

                flags = []
                if 'фронт' in command:
                    flags.append('-front')
                if 'бэк' in command:
                    flags.append('-back')
                if 'мобильн' in command:
                    flags.append('-mobile')
                if not flags:
                    flags = ['-front']

                if self.execute_mode_command(f'cp {project_name} {" ".join(flags)}'):
                    self.speak(f"Проект {project_name} создан", 'congratulations')
            return

        # Системная информация
        if 'статус' in command or 'как дела' in command or 'диагностика' in command:
            self.speak("Анализирую систему", 'diagnostics')

            battery = subprocess.run(
                "pmset -g batt | grep -Eo '[0-9]+%' | head -1",
                shell=True, capture_output=True, text=True
            ).stdout.strip()

            if battery:
                # Пытаемся воспроизвести звук батареи
                self.play_sound('battery')
                time.sleep(0.5)
                self.speak(f"Заряд {battery}")

            self.speak("Диагностика завершена", 'check_complete')
            return

        # Выход
        if any(word in command for word in ['выход', 'пока', 'до свидания']):
            self.speak("Всегда к вашим услугам", 'greeting_sir')
            return 'exit'

        # Специальные фразы
        if 'спасибо' in command:
            self.speak("Всегда пожалуйста", 'at_service')
            return

        if 'ты здесь' in command or 'ты тут' in command:
            self.speak("Да, я здесь", 'yes_sir')
            return

        if 'перезагрузись' in command or 'рестарт' in command:
            self.speak("Перезагружаюсь", 'rebooted')
            time.sleep(2)
            self.speak("Система перезагружена", 'connected')
            return

        # Неизвестная команда
        self.speak("Не понял команду", 'no_other_info')

    def start(self):
        """Основной цикл работы"""
        # Начальное приветствие
        self.play_sound(sound_file='Джарвис - приветствие.wav')
        time.sleep(0.5)
        self.speak("Система JARVIS активирована", 'connected')

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
                    self.speak("Не услышал команду", 'no_other_info')

            elif activation and 'выход' in activation:
                self.speak("Завершаю работу", 'power_off')
                break

        print("\n👋 JARVIS завершил работу")

def main():
    """Главная функция"""
    import argparse

    parser = argparse.ArgumentParser(description='JARVIS - голосовой ассистент')
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
        print("Запустите установщик: bash install-jarvis.sh")
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