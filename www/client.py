import socket
import time


def client():
    try:
        # Connect to server
        s = socket.socket()
        host = '192.168.0.23'
        port = 8080
        s.connect((host, port))
        print('Connected...')
    except Exception as e:
        print(e)
        pass

    while True:
        try:
            # Recieve incoming data
            filename = 'data.json'
            file = open(filename, 'wb')
            file_data = s.recv(1024)
            file.write(file_data)
            file.close()
            print('Data recieved.')
            time.sleep(4)
        except Exception as e:
            print(e)
            pass


if __name__ == '__main__':
    client()
