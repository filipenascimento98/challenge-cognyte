import socket, os
from dotenv import load_dotenv

load_dotenv()
SERVER = "192.168.0.2"
PORT = int(os.getenv('PORT', "1234"))   

if __name__ == "__main__":
    # Os argumentos indicam que o socket irá operar com IPv4 e utilizando o protocolo TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((SERVER, PORT))
    
    while True:
        string = input("Digite uma mensagem: ")
        server.send(bytes(string, "utf-8"))