import socket, _thread, pickle
from game import Game

server = socket.gethostbyname(socket.gethostname())  # '127.0.0.1'
port = 5500

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen()
print("Waiting for connection, Server started")

connected = set()  # stores IP addresses of the connected clients
games = {}  # stores the Game object
id_count = 0  # keeps track of no. of players joined; to run multiple games


def threaded_client(conn, player, game_id):
    global id_count

    conn.send(str.encode(str(player)))  # send the client whether they are player0 or player1; this will be stored in self.p in Network class
    reply = ''
    while True:
        try:
            data = conn.recv(4096).decode()
            if game_id in games:
                game = games[game_id]
                if not data:
                    break
                else:
                    if data == 'reset':
                        game.reset()
                    elif data != 'get':
                        game.play(player, data)

                    reply = game
                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break

    print('Lost connection')
    try:
        del games[game_id]  # deleting the Game object from games list
        print('Closing game', game_id)
    except:
        pass

    id_count -= 1
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    id_count += 1
    player = 0
    game_id = (id_count - 1) // 2  # keeps track of the game number to be created; when player1 joins it will be 0 and when player2 joins it will be 0, so player1&player2 are in game0; similarly player3&player4 will be in game1;...
    if id_count % 2 == 1:  # if there are odd no. of players, a new Game object is created
        games[game_id] = Game(game_id)  # in this case they become player0
        print('Creating a new game...')
    else:
        games[game_id].ready = True  # suppose a player has joined he will be created new Game in the above if condition; now if another player joins, he will join that game and the game will be ready
        player = 1  # in this case they become player1

    _thread.start_new_thread(threaded_client, (conn, player, game_id))  # when we create a thread, the first player gets current_player = 0 and second player gets current_player = 1

