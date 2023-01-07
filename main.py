import speech_recognition as sr  # type: ignore
import pyautogui as gui
from vosk import Model, KaldiRecognizer, SetLogLevel  # type: ignore
from pyaudio import PyAudio, paInt16
from playsound import PlaysoundException, playsound as playsound_

# Speech Recognition
srrecognizer = sr.Recognizer()
mic = sr.Microphone()

# Vosk
SetLogLevel(-1)
model = Model('lite')
recognizer = KaldiRecognizer(model, 16000)  # Reconhecedor de Voz


def escrita():  # Speech Recognition
    while True:
        try:
            with mic as source:
                audio = srrecognizer.listen(source)
                fim = srrecognizer.recognize_google(audio, language='pt-BR')
                return fim

        except (sr.UnknownValueError, sr.RequestError):
            return detect_speak()


def detect_speak():  # Vosk
    capture = PyAudio()  # Capiturando o Mic

    stream = capture.open(
            format=paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8192
    )  # Configurando Captura

    stream.start_stream()  # Iniciar reconhecimento
    data = stream.read(16384)  # Lendo os dados do mic

    if recognizer.AcceptWaveform(data):  # Se identificar a voz ele retorna
        return eval(recognizer.Result())['text']


while True:
    speech = detect_speak()
    try:
        match speech:  # type: ignore
            case 'protocolo' | 'escreva':
                try:  # Corrigi o bug de execução de som
                    playsound_('sound.wav')
                except PlaysoundException:
                    playsound_('sound.wav')

                gui.typewrite(f'{escrita()}\n', interval=0.05)  # type: ignore

            case _:
                continue

    except (UnboundLocalError, NameError):
        continue
