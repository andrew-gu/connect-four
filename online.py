import socket
import connectfour
import console
import collections

Client = collections.namedtuple('Client', ['conn','instream','outstream'])

def input_host()-> Client: #RETURNS None IF EXCEPTION IS RAISED
    host = input('Host: ')
    port = int(input('Port: '))
    client = socket.socket()
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
        cIn = client.makefile('r')
        cOut = client.makefile('w')
        return Client(conn=client, instream=cIn, outstream=cOut)

def ics_connect(c: Client, user: str): #fix later
    c.outstream.write('I32CFSP_HELLO ' + user + '\r\n')
    c.outstream.flush()
    serverMsg = c.instream.readline()[:-1]
    print(serverMsg)
    c.outstream.write('AI_GAME\r\n')
    serverMsg = c.instream.readline()[:-1]
    print(serverMsg)

def input_username()->str:
    user = input('Username: ')
    if user.find(' ') != -1:
        print('ERROR: No spaces in usernames')
        input_username()
    else:
        return user
def main():
    user = input_username()
    c = input_host()
    if c == None:
        print('fatal error')
        return

    while(True):
        msg = input() + '\r\n'
        c.outstream.write(msg)
        c.outstream.flush()
        serverMsg = c.instream.readline()[:-1]
        while serverMsg != None:
            print(serverMsg)
            serverMsg = c.instream.readline()[:-1]


if __name__ == '__main__':
    main()
