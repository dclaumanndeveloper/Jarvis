import pickle
import speech_recognition as sr
import pyttsx3
import datetime
import os
import threading
import tkinter as tk
from tkinter import ttk
from comandos import speak,say,tocar,horas,pesquisar,aumentar_volume,diminuir_volume,definir_volume,abrir,verificar_internet,get_system_info
import pywhatkit

# Inicialização do reconhecedor de voz e do sintetizador de fala
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Função para ouvir o usuário
def listen():
    print("Chegou aqui 1")
    r = sr.Microphone()
    with r as source:
        print("Chegou aqui 2")
        print("Ouvindo...")
        recognizer.adjust_for_ambient_noise(source,duration=1)
        audio = recognizer.listen(source,timeout=5)
    try:
        command = recognizer.recognize_google(audio, language='pt-BR')
        print(f"Você disse: {command}")
        return command.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print(f"{e}")
        return " Deu Erro"
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

# Loop principal
def listen_for_command():
    while is_listening:
        activation_phrase = listen()
        if 'jarvis' in activation_phrase:
            hour = int(datetime.datetime.now().hour)

            if hour>=0 and hour<12:
                
                speak("Bom dia senhor!")
            
            elif hour>=12 and hour<18:
                engine.say("Boa tarde senhor!")
                #engine.runAndWait()
                #speak("Boa tarde senhor!")
            
            else:
                speak("Boa noite senhor!")
            speak("Qual sua ordem?")
            command = listen()
            execute_command(command)
# Criar a janela principal
window = tk.Tk()
window.title("Jarvis")

# Configurar o estilo (opcional)
style = ttk.Style()
style.theme_use('clam')  # Ou outro tema de sua preferência

# Adicionar elementos à interface (exemplos)
label_status = ttk.Label(window, text="Jarvis ativado. Diga 'Jarvis' para me chamar.")
label_status.pack()

text_output = tk.Text(window, height=10, width=50)
text_output.pack()

# Função para atualizar a interface com a saída da IA
def update_output(text):
    text_output.insert(tk.END, text + "\n")
    text_output.see(tk.END)  # Rolar para o final

start_listening()

# Iniciar o loop principal da interface gráfica
window.mainloop()