import pickle
import speech_recognition as sr
import pyttsx3
import datetime
import os
import threading
import tkinter as tk
import sys
from tkinter import ttk
from comandos import finish_day,start_day,buscar_temperatura,escreva,speak,tocar,horas,pesquisar,aumentar_volume,diminuir_volume,definir_volume,abrir,verificar_internet,get_system_info
import pywhatkit
import time

# Inicialização do reconhecedor de voz e do sintetizador de fala
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Função para ouvir o usuário
def listen():
    r = sr.Recognizer()
    command = "" # Initialize command as empty string

    # Option to type command
    print("Digite seu comando ou aguarde para falar:")
    typed_command = input()
    if typed_command:
        return typed_command.lower()

    # Option to listen to voice
    with sr.Microphone() as source:
        try:
            print("Ouvindo!")
            #recognizer.adjust_for_ambient_noise(source,duration=1)
            audio = recognizer.listen(source,timeout=5) # Increased timeout slightly
        except sr.exceptions.WaitTimeoutError:
            print("Tempo de espera esgotado para entrada de voz.")
            return "" # Return empty if voice input times out
        except Exception as e:
            print(f"Erro ao acessar o microfone: {e}")
            return ""


    try:
        command = recognizer.recognize_google(audio, language='pt-BR')
        print(f"Você disse: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Não foi possível entender o áudio.")
        return ""
    except sr.RequestError as e:
        print(f"Erro na requisição ao serviço de reconhecimento de fala; {e}")
        return ""
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante o reconhecimento de fala: {e}")
        return ""
    
    


# Função para responder a perguntas e executar comandos
def execute_command(command):
    if 'horas' in command:
        horas()
    elif 'tocar' in command:
        tocar(command) 
        window.withdraw()   
    elif 'aumentar volume' in command:
        aumentar_volume()
        window.withdraw()  
    elif 'diminuir volume' in command:
        diminuir_volume()
        window.withdraw()  
    elif 'definir' in command and 'volume' in command:
        definir_volume(command)
        window.withdraw()  
    elif 'pesquisar' in command:
        pesquisar(command)
        window.withdraw()  
    elif 'abrir' in command:
        abrir(command)
        window.withdraw()  
    elif 'verificar' in command and 'internet' in command:
        verificar_internet()
        window.withdraw()  
    elif 'verificar' in command and 'sistema' in command:
            system_info = get_system_info()
            for key, value in system_info.items():
                print(f'{key}: {value}')
                speak(f'{key}: {value}')
                window.withdraw()  
    elif 'ligar as luzes' in command:
        speak("Ligando as luzes.")
    elif 'temperatura' in command :
        buscar_temperatura()
        window.withdraw()  
    elif 'escreva' in command:
        escreva(command)
    elif 'iniciar dia' in command:
        start_day()
    elif 'finalizar dia' in command:
        finish_day()
    elif 'sair' in command:
        speak("Até logo!")
        exit()
    
is_listening = False

def start_listening():
    speak("Inicializando o sistema!")
    time.sleep(2)
    speak("Verificando integrações!")
    time.sleep(2)
    speak("Verificando hardware!")
    time.sleep(2)
    speak("Ligando motores!")
    time.sleep(5)
    speak("Motores ligados!")
    time.sleep(10)
    speak("Sistema Online!")
    time.sleep(1)
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
            window.withdraw()
            hour = int(datetime.datetime.now().hour)

            if hour>=0 and hour<12:
                
                speak("Bom dia senhor!")
            
            elif hour>=12 and hour<18:
                engine.say("Boa tarde senhor!")
            
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