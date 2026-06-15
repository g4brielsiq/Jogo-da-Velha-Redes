import socket
import threading

HOST = '0.0.0.0'
PORT = 5050

board = [' '] * 9
players = []       # lista de (conn, addr, simbolo)
lock = threading.Lock()
current_turn = 0   # índice em players de quem deve jogar


def reset_board():
    global board, current_turn
    board = [' '] * 9
    current_turn = 0


def render_board():
    b = board
    return (
        f"\n {b[0]} | {b[1]} | {b[2]} \n"
        f"---+---+---\n"
        f" {b[3]} | {b[4]} | {b[5]} \n"
        f"---+---+---\n"
        f" {b[6]} | {b[7]} | {b[8]} \n"
    )


def check_winner():
    wins = [
        (0,1,2),(3,4,5),(6,7,8),  # linhas
        (0,3,6),(1,4,7),(2,5,8),  # colunas
        (0,4,8),(2,4,6)           # diagonais
    ]
    for a,b_,c in wins:
        if board[a] == board[b_] == board[c] != ' ':
            return board[a]
    if ' ' not in board:
        return 'empate'
    return None


def broadcast(msg, exclude=None):
    for conn, addr, sym in players:
        if conn != exclude:
            try:
                conn.sendall(msg.encode())
            except:
                pass


def send_to(conn, msg):
    try:
        conn.sendall(msg.encode())
    except:
        pass


def handle_client(conn, addr, player_index):
    global current_turn

    sym = players[player_index][2]
    print(f"[CONEXÃO] {addr} conectado como {sym}")

    # Espera o segundo jogador
    send_to(conn, f"Você é o jogador {sym}. Aguardando oponente...\n")

    while len(players) < 2:
        pass  # espera ativa simples

    send_to(conn, "Jogo iniciado!\n")
    send_to(conn, render_board())

    if player_index == 0:
        send_to(conn, "Sua vez! Digite a posição (1-9): ")
    else:
        send_to(conn, "Aguarde o oponente jogar...\n")

    while True:
        try:
            data = conn.recv(1024).decode().strip()
        except:
            break

        if not data:
            break

        with lock:
            # Verifica se é a vez deste jogador
            if current_turn != player_index:
                send_to(conn, "Não é sua vez! Aguarde.\n")
                continue

            # Valida entrada
            if not data.isdigit() or not (1 <= int(data) <= 9):
                send_to(conn, "Posição inválida! Digite um número de 1 a 9: ")
                continue

            pos = int(data) - 1
            if board[pos] != ' ':
                send_to(conn, "Posição ocupada! Escolha outra: ")
                continue

            # Faz a jogada
            board[pos] = sym

            # Envia tabuleiro atualizado para todos
            board_str = render_board()
            broadcast(board_str)

            winner = check_winner()
            if winner:
                if winner == 'empate':
                    broadcast("Empate! Nenhum vencedor.\n")
                else:
                    broadcast(f"Jogador {winner} venceu!\n")
                broadcast("Encerrando conexão. Obrigado por jogar!\n")
                # Fecha conexões após pequeno delay
                for c, a, s in players:
                    try:
                        c.close()
                    except:
                        pass
                reset_board()
                players.clear()
                return

            # Passa a vez
            current_turn = 1 - current_turn
            next_conn = players[current_turn][0]
            send_to(next_conn, "Sua vez! Digite a posição (1-9): ")
            other = players[1 - current_turn][0]
            send_to(other, "Aguarde o oponente jogar...\n")

    print(f"[DESCONEXÃO] {addr}")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(2)
    print(f"[SERVIDOR] Aguardando jogadores em {HOST}:{PORT}...")

    while True:
        conn, addr = server.accept()
        if len(players) >= 2:
            conn.sendall("Partida em andamento. Tente mais tarde.\n".encode())
            conn.close()
            continue

        sym = 'X' if len(players) == 0 else 'O'
        players.append((conn, addr, sym))
        idx = len(players) - 1

        t = threading.Thread(target=handle_client, args=(conn, addr, idx))
        t.daemon = True
        t.start()


if __name__ == '__main__':
    start_server()
