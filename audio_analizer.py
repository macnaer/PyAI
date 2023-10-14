import wave
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.playback import play

import threading


def play_audio():
    audio = AudioSegment.from_wav("output.wav")
    play(audio)


def print_audio():
    audio_file = wave.open("output.wav", "rb")

    # Отримати параметри аудіо
    # sample_width = audio_file.getsampwidth()
    frame_rate = audio_file.getframerate()

    # Прочитати всі фрейми з аудіофайлу
    audio_data = audio_file.readframes(-1)

    # Конвертувати байти в числові дані
    audio_data = np.frombuffer(audio_data, dtype=np.int16)

    # Створити часову шкалу для діаграми
    time = np.linspace(0, len(audio_data) / frame_rate, num=len(audio_data))

    # Побудувати діаграму звуку
    plt.figure(figsize=(12, 6))
    plt.plot(time, audio_data, color='b')
    plt.title("Звукова діаграма")
    plt.xlabel("Час (секунди)")
    plt.ylabel("Амплітуда")
    plt.grid()
    plt.show()


# Потоки
# audio_thread = threading.Thread(target=play_audio)
plot_thread = threading.Thread(target=print_audio)


# audio_thread.start()
plot_thread.start()


# audio_thread.join()
plot_thread.join()
