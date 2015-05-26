import socket
from os import system
from getopt import getopt, GetoptError
from modules import *
from threading import Thread


def usage():
    if 'win' in sys.platform:
        system("cls")
    else:
        system("clear")
    print("""
888b    888          888     .d8888b.           888                      
8888b   888          888    d88P  Y88b          888                      
88888b  888          888    888    888          888                      
888Y88b 888  .d88b.  888888 888         .d88b.  88888b.  888d888 8888b.  
888 Y88b888 d8P  Y8b 888    888        d88""88b 888 "88b 888P"      "88b 
888  Y88888 88888888 888    888    888 888  888 888  888 888    .d888888 
888   Y8888 Y8b.     Y88b.  Y88b  d88P Y88..88P 888 d88P 888    888  888 
888    Y888  "Y8888   "Y888  "Y8888P"   "Y88P"  88888P"  888    "Y888888 
                                                             By Amir Saad
                                                           GitHub.com/0xAmir
Examples: ./nc.py -l -p port
          ./nc.py -c -a address -p port

-h, --help          Display this message.
-l, --listen        Server (Listener) mode.
-c, --client        Client mode.
-p, --port          Port to listen on.
-a, --address       Address to listen at/connect to.
-s, --shell         Shell mode (Bind/Reverse).
-d, --download      File recieval mode.
-u, --upload        File upload mode.
""")
    sys.exit(0)



def main():

    mode                 = ""
    action               = ""
    port                 = 0
    address              = '0.0.0.0'
    path                 = ""


    if not sys.argv[1:]:
        usage()
    try:
        opts, args = getopt(sys.argv[1:], "hlcp:a:sdu:", ["help", "listen", "client", "port", "address", "shell", "download", "upload"])

        for o, a in opts:
            if o in ("-h", "--help"):
                usage()
            elif o in ("-l", "--listen"):
                mode = "listen"
            elif o in ("-c", "--client"):
                mode = "client"
            elif o in ("-p", "--port"):
                port = int(a)
            elif o in ("-a", "--address"):
                address = a
            elif o in ("-s", "--shell"):
                action = "shell"
            elif o in ("-d", "--download"):
                action = "download"
            elif o in ('-u', "--upload"):
                action = "upload"
                path = a

    except GetoptError as e:
        print("[-]Error: " + str(e))
        sys.exit(-1)


    if mode == "listen":

        try:

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((address, port))
            sock.listen(1)

            if(address  == "0.0.0.0"):
                print("\nListener started on ALL INTERFACES on port " + str(port))
            else:
                print("\nListener start on " + address + " on port " + str(port))
            if action == "download":
                print("\n[!]Download Mode")
            while (True):
                client, address = sock.accept()
                print("Received connection from " + str(address[0]) + " on port " + str(address[1]))
                if action == "shell":
                    shell(client)
                elif action == "download":
                    download(client)
                w1 = Thread(target=send, args=(client,))
                w2 = Thread(target=recv, args=(client,))
                w1.start()
                w2.start()

        except Exception as e:
            print("[-]Connection couldn't be established, lost or terminated\nError: " + str(e))
            sock.close()
            sys.exit(1)


    elif mode == "client":
        try:
            if action == "upload":
                print("\n[!]Upload Mode")
            print("\n[+]Establishing connection to " + address + " on port " + str(port))
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_errorno = sock.connect((socket.gethostbyname(address), int(port)))

            if not sock_errorno:
                print("[+]Connection Established !\n")

            if "upload" == action:
                upload(path, sock)
            if "shell" == action:
                shell(sock)

            w1 = Thread(target=send, args=(sock,))
            w2 = Thread(target=recv, args=(sock,))
            w1.start()
            w2.start()
        except Exception as e:
            print("[-]FATAL: " + str(e))
            sock.close()
            sys.exit(1)

if __name__ == "__main__":
    main()
