import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 5050


def receive_messages(conn):
    """Thread que fica escutando mensagens do servidor e imprime na tela."""
    while True:
        try:
            msg = conn.recv(1024).decode()
            if not msg:
                print("\n[INFO] Conexão encerrada pelo servidor.")
                break
            print(msg, end='', flush=True)
        except:
            print("\n[INFO] Conexão perdida.")
            break


def start_client():
    host = input("IP do servidor (Enter para localhost): ").strip()
    if not host:
        host = HOST

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((host, PORT))
    except Exception as e:
        print(f"Não foi possível conectar: {e}")
        sys.exit(1)

    print("Conectado ao servidor!\n")

    # Thread para receber mensagens do servidor
    t = threading.Thread(target=receive_messages, args=(conn,))
    t.daemon = True
    t.start()

    # Loop principal: lê entrada do usuário e envia ao servidor
    while True:
        try:
            entrada = input()
            conn.sendall(entrada.encode())
        except (EOFError, KeyboardInterrupt):
            print("\nSaindo...")
            conn.close()
            break
        except:
            break


if __name__ == '__main__':
    start_client()
