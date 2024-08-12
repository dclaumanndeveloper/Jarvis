import pickle
import speech_recognition as sr
import pyttsx3
import datetime
import os
import threading
import tkinter as tk
from tkinter import ttk
from comandos import speak,tocar,horas,pesquisar,aumentar_volume,diminuir_volume,definir_volume,abrir,verificar_internet,get_system_info
import pywhatkit

# Inicialização do reconhecedor de voz e do sintetizador de fala
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Função para ouvir o usuário
def listen():
    with sr.Microphone() as source:
        print("Ouvindo...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source,timeout=3)
    try:
        command = recognizer.recognize_google(audio, language='pt-BR')
        print(f"Você disse: {command}")
        return command.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        #speak("Erro ao se conectar ao serviço de reconhecimento de voz; {0}".format(e))
        return ""
    except sr.WaitTimeoutError:
        return ""
    except sr.exceptions.WaitTimeoutError:
        return ""

# Função para responder a perguntas e executar comandos
def execute_command(command):
    if 'horas' in command:
        horas()
    elif 'tocar' in command:
        tocar(command)    
    elif 'aumentar volume' in command:
        aumentar_volume()
    elif 'diminuir volume' in command:
        diminuir_volume()
    elif 'definir' in command and 'volume' in command:
        definir_volume(command)
    elif 'pesquisar' in command:
        pesquisar(command)
    elif 'abrir' in command:
        abrir(command)
    elif 'verificar' in command and 'internet' in command:
        verificar_internet()
    elif 'verificar' in command and 'sistema' in command:
            system_info = get_system_info()
            for key, value in system_info.items():
                print(f'{key}: {value}')
                speak(f'{key}: {value}')
    elif 'ligar as luzes' in command:
        speak("Ligando as luzes.")
    elif 'sair' in command:
        speak("Até logo!")
        exit()
    
# Interface gráfica
#window = tk.Tk()
#window.title("Jarvis")
#style = ttk.Style()
#style.theme_use('clam')

#label_status = ttk.Label(window, text="Jarvis ativado. Diga 'Jarvis' para me chamar.")
#label_status.pack()

#text_output = tk.Text(window, height=10, width=50)
#text_output.pack()


is_listening = False

def start_listening():
    global is_listening
    if not is_listening:
        is_listening = True
        # label_status.config(text="Ouvindo...")
        threading.Thread(target=listen_for_command).start()

def stop_listening():
    global is_listening
    is_listening = False
#    label_status.config(text="Jarvis ativado. Diga 'Jarvis' para me chamar.")

# Loop principal
def listen_for_command():
    while is_listening:
        activation_phrase = listen()
        if 'jarvis' in activation_phrase:
            hour = int(datetime.datetime.now().hour)

            if hour>=0 and hour<12:
                
                speak("Bom dia senhor!")
            
            elif hour>=12 and hour<18:
                
                speak("Boa tarde senhor!")
            
            else:
                speak("Boa noite senhor!")
                speak("Como posso ajudar?")
                command = listen()
                execute_command(command)

start_listening()
#window.mainloop()