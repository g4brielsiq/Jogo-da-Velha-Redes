# Jogo da Velha — Redes de Computadores 2026.1

Aplicação cliente-servidor de Jogo da Velha implementada em Python
utilizando sockets TCP e threads.

## Requisitos

- Python 3.x instalado
- Dois terminais (ou dois computadores na mesma rede)

## Como rodar

### 1. Iniciar o servidor

Abra um terminal e execute:

```
python server.py
```

O servidor ficará aguardando dois jogadores na porta **5050**.

### 2. Conectar os clientes

Abra **dois terminais separados** (podem ser na mesma máquina ou em
máquinas diferentes na mesma rede) e execute em cada um:

```
python client.py
```

- Se estiver rodando tudo na mesma máquina, pressione **Enter** quando
  perguntar o IP (usará localhost automaticamente).
- Se o cliente estiver em outra máquina, informe o IP da máquina onde
  o servidor está rodando (ex: `192.168.1.10`).

### 3. Jogar

- O primeiro a conectar será **X**, o segundo será **O**.
- O tabuleiro usa posições de **1 a 9**, conforme o mapa abaixo:

```
 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9
```

- Quando for sua vez, digite o número da posição e pressione **Enter**.
- O jogo termina quando há um vencedor ou empate.

## Arquitetura

| Arquivo     | Descrição                                      |
|-------------|------------------------------------------------|
| `server.py` | Servidor TCP que gerencia o estado do jogo     |
| `client.py` | Cliente que se conecta ao servidor e interage  |

- **Protocolo**: TCP via sockets (`socket.AF_INET`, `socket.SOCK_STREAM`)
- **Threads**: o servidor cria uma thread por jogador; o cliente usa uma
  thread dedicada para receber mensagens do servidor sem bloquear a entrada.
