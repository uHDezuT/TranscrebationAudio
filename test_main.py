import json
import os
import tkinter as tk
import wave
from datetime import datetime
from tkinter import filedialog

import vosk

# Инициализация модели распознавания речи
model = vosk.Model("vosk-model-small-ru-0.22")


def open_file():
    global audio_file_path
    audio_file_path = filedialog.askopenfilename(
        filetypes=[("WAV Files", "*.wav")])


# Функция для транскрибирования аудиофайла
def transcribe_audio():
    # Открытие аудиофайла и чтение данных
    audio_file = wave.open(audio_file_path, "rb")
    audio_data = audio_file.readframes(audio_file.getnframes())
    audio_file.close()

    # Инициализация распознавателя
    rec = vosk.KaldiRecognizer(model, audio_file.getframerate())

    # Распознавание речи
    rec.AcceptWaveform(audio_data)
    result = json.loads(rec.FinalResult())["text"]

    return result


def save_text():
    # Транскрибирование аудиофайла
    text = transcribe_audio()

    # Получение имени аудиофайла без расширения
    audio_file_name = os.path.splitext(os.path.basename(audio_file_path))[0]

    # Форматирование имени файла для текстового файла
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    text_file_name = f"{audio_file_name}_{now}.txt"

    # Сохранение текста в файл
    with open(text_file_name, "w") as f:
        f.write(text)


# Основная функция программы
def main():
    # Создание графического интерфейса
    root = tk.Tk()
    root.title("Аудио транскрибация")
    root.geometry("300x150")

    # Кнопка выбора файла
    select_file_button = tk.Button(root, text="Выбрать файл",
                                   command=open_file)
    select_file_button.pack(pady=10)

    # Кнопка транскрибации
    transcribe_button = tk.Button(root, text="Транскрибировать",
                                  command=save_text)
    transcribe_button.pack(pady=10)

    # Запуск графического интерфейса
    root.mainloop()


if __name__ == "__main__":
    main()
