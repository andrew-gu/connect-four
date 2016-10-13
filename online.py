import socket
import connectfour
import console

def input_host(): #RETURNS None IF EXCEPTION IS RAISED
    host = input('Host: ')
    port = int(input('Port: '))
    client = socket.socket()
    client.settimeout(0.5)
    try:
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
        return client

def input_username()->str:
    user = input('Username: ')
    if user.find(' ') != -1:
        print('ERROR: No spaces in usernames')
        input_username()
    else:
        return user

def ics_connect(c: socket, user: str):
    msg = 'I32CFSP_HELLO ' + user + '\r\n'
    c.send(msg.encode())
    serverMsg = c.recv(1024).decode()
    print(serverMsg)
    msg = 'AI_GAME\r\n'
    c.send(msg.encode())
    serverMsg = c.recv(1024).decode()
    print(serverMsg)

def send_move(c: socket.socket, col: int, move: int):
    msg = str()
    if move == 0:
        msg = 'POP ' + str(col)
    elif move == 1:
        msg = 'DROP ' + str(col)
    _send_msg(c, msg)

def recv_move(c: socket.socket)-> int:
    '''
    returns and parses server response into integers
    <10 is pop
    >= 10 is drop
    ones place represents col number
    -1 is invalid move, -2 is game over
    '''
    msgs = _recv_msgs(c)
    result = int()
    if msgs[0] == 'OKAY':
        if msgs[1].find('POP') != -1:
            col = int(msgs[1][4]) - 1
            result += col #add column #
        elif msgs[1].find('DROP') != -1:
            result += 10 #result is from 10 to 16
            col = int(msgs[1][5]) - 1
            result += col
        return result
    elif msgs[0] == 'INVALID':
        return -1
    elif msgs[0].find('WINNER') != -1:
        return -2

def main():
    user = input_username()
    c = input_host()
    if c == None:
        print('FATAL ERROR: Failed to connect')
        return
    ics_connect(c,user)
    _send_msg(c, 'DROP 4')
    l = _recv_msgs(c)
    print(l)

def _send_msg(c: socket.socket, msg: str):
    msg = msg + '\r\n'
    c.send(msg.encode())

def _recv_msg(c: socket.socket)->str:
    msg = c.recv(2048).decode()
    return msg

def _recv_msgs(c: socket.socket)->list:
    msgs = list()
    while True:
        try:
            removed = _remove_end_line(_recv_msg(c))
            for i in removed:
                msgs.append(i)
                print(i)
        except socket.timeout:
            #print('*****TIMED OUT*****')
            break
    return msgs

def _remove_end_line(s: str)-> list:
    result = list()
    while True:
        result.append(s[0:s.index('\r\n')])
        s = s[s.index('\r\n')+2:]
        if len(s) == 0:
            break
    return result


if __name__ == '__main__':
    main()
