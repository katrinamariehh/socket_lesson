import socket, sys, select

def open_connection(host, port):
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((host, port))
    return my_socket

def main():
    my_socket = open_connection("localhost", 5555)
    running = True
    while running:

        inputready, outputready, exceptready = select.select([my_socket, sys.stdin], [], [])

        for s in inputready:

            if s == sys.stdin:
                # Get data from the keyboard
                user_in = sys.stdin.readline()
                if user_in == "/quit\n":
                    print "(You have left the chat.)"
                    running = False
                my_socket.sendall(user_in)

            else:
                # Get data from the socket
                msg = s.recv(1024)
                if not msg:
                    print "Disconnected from server!"
                    running = False
                elif "/quit" in msg:
                    pass
                else:
                    print format_message(msg)


    my_socket.close()

def format_message(message):
    if "::" in message:
        message = message.split("::", 1)
        return '[' + message[0] + '] ' + message[1]
    elif "logged in" in message or "disconnected" in message:
        return "(" + message[:-1] + ")\n"
    else:
        return message

if __name__ == "__main__":
    main()
