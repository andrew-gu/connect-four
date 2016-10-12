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

def send_move(c: socket.socket, col: int):
    msg = 'DROP ' + str(col)
    _send_msg(c, msg)

def recv_move(c: socket.socket)-> int:
    msgs = _recv_msgs(c)
    if msgs[0] == 'OKAY':
        return msgs[1][-1]
    elif msgs[0] == 'INVALID':
        return -1

def main():
    user = input_username()
    c = input_host()
    if c == None:
        print('fatal error')
        return
    ics_connect(c,user)
    _send_msg(c, 'DROP 4')
    _recv_msgs(c)

def _send_msg(c: socket.socket, msg: str):
    msg = msg + '\r\n'
    c.send(msg.encode())

def _recv_msg(c: socket.socket)->str:
    msg = c.recv(2048).decode()
    msg = msg[:-1]
    print(msg)
    return msg

def _recv_msgs(c: socket.socket)->list:
    msgs = list()
    while True:
        try:
            msgs.append(_recv_msg(c))
        except socket.timeout:
            break
    return msgs

if __name__ == '__main__':
    main()
