import socket
import collections

Client = collections.namedtuple('Client',['connection','instream','outstream'])

def input_host()-> Client:
    '''
    Connects to server, creates i/o stream, and returns in a Client object
    Terminates if connection fails
    '''
    valid_port = False
    host = input('Host: ')
    while not valid_port:
        try:
            port = int(input('Port: '))
            valid_port = True
        except (ValueError,TypeError):
            print('ERROR: Invalid Port')
    client = socket.socket()
    try:
        #client.connect((host,port))
        client.connect(('woodhouse.ics.uci.edu',4444))
    except socket.gaierror:
        print('ERROR: Failed to get address info')
    except socket.timeout:
        print('ERROR: Timed out')
    except InterruptedError:
        print('ERROR: Connection interrupted')
    except ConnectionRefusedError:
        print('ERROR: Connection Refused')
    else:
        client_io = _create_io(client)
        return client_io

def ics_connect(client: Client):
    '''
    connects to woodhouse ics server with connect four protocol
    closes connection if invalid server response
    '''
    user = _input_username()
    msg = 'I32CFSP_HELLO ' + user
    _send_msg(client, msg)
    response = _recv_msg(client)
    if response != 'WELCOME ' + user:
        close_client(client)
    print('SERVER: ' + response)
    msg = 'AI_GAME'
    _send_msg(client, msg)
    response = _recv_msg(client)
    if response != 'READY':
        close_client(client)
    print('SERVER: ' + response)

def send_move(client: Client, col: int, move: int):
    '''
    sends move with correct syntax to server
    '''
    if move == 0:
        _send_msg(client,'POP ' + str(col))
    elif move == 1:
        _send_msg(client,'DROP ' + str(col))

def parse_msg(client: Client)->list:
    '''
    returns list of len 2
    1st element: -1 if invalid user move, 0-6 if server pop, 10-16 if server drop
    2nd element: -1 if bad input, 0 if ready, 1 if red win, 2 if yellow win
    '''
    msg_list = [0]*2
    msg = _recv_msg(client)
    print('SERVER: ' + msg)

    if msg == 'OKAY':
        move = _recv_msg(client)
        result = _recv_msg(client)
        print('SERVER: ' + move)
        print('SERVER: ' + result)
        #parse move and check if valid syntax
        if move[0:4] == 'POP ':
            try:
                msg_list[0] = int(move[-1]) - 1
            except (TypeError, ValueError, NameError):
                msg_list[1] = -1
        elif move[0:5] == 'DROP ':
            try:
                msg_list[0] = int(move[-1]) + 9
            except (TypeError, ValueError, NameError):
                msg_list[1] = -1
        else:
            msg_list[1] = -1

        #parse result and check if valid syntax
        if result.find('WINNER') != -1:
            if result == 'WINNER_RED':
                msg_list[1] = 1
            elif result == 'WINNER_YELLOW':
                msg_list[1] = 2
        elif result == 'READY':
            msg_list[1] = 0
        else:
            msg_list[1] = -1


    elif msg == 'INVALID':
        msg_list[0] = -1
        result = _recv_msg(client)
        print('SERVER: ' + result)
        if result == 'READY':
            msg_list[1] = 0
        else:
            msg_list[1] = -1


    else:
        msg_list[0] = -1
        msg_list[1] = -1
    #close sockets if bad move
    if msg_list[1] == -1:
        close_client(client)
    return msg_list

def _input_username()->str:
    valid = False
    user = str()
    while not valid:
        user = input('Enter Username: ')
        if user.find(' ') != -1 or len(user) == 0:
            print('ERROR: Invalid userame')
        else:
            valid = True
    return user

def _create_io(client: socket.socket)->Client:
    return Client(client,client.makefile('r'),client.makefile('w'))

def _send_msg(client: Client, msg: str):
    client.outstream.write(msg + '\r\n')
    client.outstream.flush()

def _recv_msg(client: Client)->str:
    return client.instream.readline()[:-1]

def close_client(client: Client)->str:
    client.instream.close()
    client.outstream.close()
    client.connection.close()
