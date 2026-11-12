import socket

if __name__ == '__main__':
    server_soc = socket.socket()
    server_soc.bind(("0.0.0.0",1234))
    server_soc.listen(1)
    print("listening for client")
    client_soc, client_addr = server_soc.accept()
    print(client_addr[0])
    try:
        a = client_soc.recv(1024)
        print(a.decode())
        client_soc.send(b"order is being deliverd right now! pizza ready!!")
    except Exception as e:
        print(e)
    print("end")

