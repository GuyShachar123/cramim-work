import socket
import threading
import hashlib
import time

TARGET_MD5 = "EC9C0F7EDCC18A98B1F31853B1813301"
CHUNK_SIZE = 25000000  
current_number = 0
found_solution = None
winning_client = None
start_time = None
lock = threading.Lock()
clients_connected = set()

retry_chunks = []

def verify_md5(num_str):
    return hashlib.md5(num_str.encode()).hexdigest().upper() == TARGET_MD5.upper()

def handle_client(client_socket, client_address):
    global current_number, found_solution, winning_client
    print(f"[+] Client connected: {client_address}")

    with lock:
        clients_connected.add(client_address)
    
    current_chunk = None 

    while not found_solution:
        with lock:
            if retry_chunks:
                current_chunk = retry_chunks.pop(0)
                start, end = current_chunk
            else:
                # Otherwise, take the next sequential chunk
                start = current_number
                end = current_number + CHUNK_SIZE
                current_number = end
                current_chunk = (start, end)

        request = f"GET_WORK:{start}:{end}"
        try:
            client_socket.sendall(request.encode())
        except Exception as e:
            print(f"Error sending data to client {client_address}:", e)
            with lock:
                retry_chunks.append(current_chunk)
            break

        try:
            response = client_socket.recv(1024).decode()
        except Exception as e:
            print(f"Error receiving data from client {client_address}:", e)
            with lock:
                retry_chunks.append(current_chunk)
            break

        if not response:
            with lock:
                retry_chunks.append(current_chunk)
            break

        if response.startswith("FOUND:"):
            candidate = response.split(":")[1]
            if verify_md5(candidate):
                with lock:
                    if not found_solution:
                        found_solution = candidate
                        winning_client = client_address
                print(f"Success! Client {client_address} found the solution: {candidate}")
                break
            else:
                print(f"[-] Client {client_address} sent an incorrect solution: {candidate}")
        elif response == "DONE_CHUNK":
            current_chunk = None
                
    client_socket.close()
    print(f"Finished connection with {client_address}")

def start_server():
    global start_time
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5000))
    server.listen(5)
    server.settimeout(1.0)
    print("[*] Server is listening on port 5000...")
    
    start_time = time.time()  

    while not found_solution:
        try:
            client_sock, addr = server.accept()
            if found_solution:
                client_sock.close()
                break
            t = threading.Thread(target=handle_client, args=(client_sock, addr))
            t.start()
        except socket.timeout:
            continue
        except Exception as e:
            break

    elapsed_time = time.time() - start_time
    print("\n" + "="*40)
    print("[!] Process finished - Final Statistics:")
    print(f"[*] 1. Original String (Solution): {found_solution}")
    print(f"[*] 2. Total computers/clients that participated: {len(clients_connected)}")
    print(f"[*]    Winning client address: {winning_client}")
    print(f"[*] 3. Time elapsed until solution found: {elapsed_time:.2f} seconds")
    print("="*40)

if __name__ == "__main__":
    start_server()
