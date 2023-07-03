import socket, os
from threading import Thread
from dotenv import load_dotenv
from datetime import datetime


load_dotenv() # Carrega as variáveis de ambiente

HOST = ''                                      # Endereco IP do Servidor
PORT = int(os.getenv('PORT', "1234"))            # Porta do Servidor

def writer(msg, file_name, client):
    file = open(file_name, "ab")

    # Verifica se o espaço restante do arquivo atualmente aberto, considerando o tamanho máximo por arquivo, é suficiente para receber o novo dado
    remain_space = int(os.getenv("MAX_FILE_LENGTH", "10")) - os.stat(file_name).st_size

    if remain_space >= len(msg):
        file.write(msg)
    else:
        # Caso não tenha espaço suficiente, então parte do arquivo é gravado no espaço 
        # restante do arquivo atual e logo depois novo(s) arquivo(s) é/são gerado(s) 
        # para armazenar o restante dos dados
        file.write(msg[:remain_space])
        
        date_time = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"logs/{client[0]}:{client[1]}_{date_time}"

        file = open(file_name, "ab")
        
        # Para mensagens que precisam ser armazenadas em mais de um arquivo o count_file
        # é utilizado para diferenciar os vários arquivos que compõem a mesma mensagem
        remain_msg_to_be_stored = len(msg) - remain_space
        head = remain_space
        count_file = 1

        # Esse laço avalia o quanto da mensagem falta ser armazenada e se deve ser em
        # um único arquivo ou em vários.
        while remain_msg_to_be_stored > 0:       
            if remain_msg_to_be_stored <= int(os.getenv("MAX_FILE_LENGTH", "10")):
                file.write(msg[head:])
                remain_msg_to_be_stored = 0
            else:
                file.write(msg[head:(head + int(os.getenv("MAX_FILE_LENGTH", "10")))])
                head += int(os.getenv("MAX_FILE_LENGTH", "10"))
                remain_msg_to_be_stored -= int(os.getenv("MAX_FILE_LENGTH", "10"))

                if remain_msg_to_be_stored > 0:
                    file_name = f"logs/{client[0]}:{client[1]}_{count_file}_{date_time}"
                    count_file += 1
                    file = open(file_name, "ab")
            
        file.close()

    return file_name

def listener(con, client):
    print(f"Recebido a conexão {client[0]}:{client[1]}")
    # Cancela a conexão caso o cliente não envie dados no timeout especificado
    con.settimeout(int(os.getenv("TIMEOUT", "10"))) 
    print("Conexão estabelecida de ", client)

    try:
        date_time = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"logs/{client[0]}:{client[1]}_{date_time}"
        
        while True:
            msg = con.recv(1024)

            # Encerra a conexão caso o programa cliente seja encerrado
            if not msg:
                con.close()

            file_name = writer(msg, file_name, client)

    except Exception as e:
        print(f"Cliente {client[0]}:{client[1]} desconectado")

if __name__ == "__main__":
    # Os argumentos indicam que o socket irá operar com IPv4 e utilizando o protocolo TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    
    #O uso de threads permite múltiplas conexões simultaneamente
    while True:
        conn, client = server.accept()
        conn_listener = Thread(target=listener, args=(conn, client,))
        conn_listener.start()
        # Não foi necessário finalizar as threads com o join(), pois o timeout do socket 
        # encerra a thread quando o cliente estoura o tempo limite para envio de mensagens
        # levantando uma exceção, já o client.close() encerra a conexão com o cliente
        # quando ele é encerrado antes de estourar o timeout também levantando uma
        # exceção o que encerra a thread para aquele cliente.