import socket
import multiprocessing
import hashlib
import time

TARGET_MD5 = "EC9C0F7EDCC18A98B1F31853B1813301"

def worker_task(start, end, result_queue):
    """
    enter: start worker task to brute force a specific number range
    exit: worker finishes range or puts found solution into result queue
    """
    for num in range(start, end):
        num_str = str(num).zfill(10)  # Ensure 10 digits length
        if hashlib.md5(num_str.encode()).hexdigest().upper() == TARGET_MD5.upper():
            result_queue.put(num_str)
            return

def brute_force_chunk(start, end, num_cores):
    """
    enter: split chunk across multiple CPU cores using processes
    exit: return found solution if any, otherwise finish chunk
    """
    chunk_size = (end - start) // num_cores
    result_queue = multiprocessing.Queue()
    processes = []

    for i in range(num_cores):
        p_start = start + (i * chunk_size)
        p_end = start + ((i + 1) * chunk_size) if i < num_cores - 1 else end
        
        p = multiprocessing.Process(target=worker_task, args=(p_start, p_end, result_queue))
        processes.append(p)
        p.start()

    found = None
    while any(p.is_alive() for p in processes):
        if not result_queue.empty():
            found = result_queue.get()
            break
        time.sleep(0.05)

    for p in processes:
        if p.is_alive():
            p.terminate()
        p.join()

    return found

def start_client(server_ip='127.0.0.1'):
    """
    enter: start client connection to server and handle work loop
    exit: client socket closed and process ends
    """
    num_cores = multiprocessing.cpu_count()
    print(f"[*] Detected {num_cores} CPU cores. Connecting to server...")
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, 5000))
    except Exception as e:
        print("Error connecting to server:", e)
        return

    while True:
        try:
            data = client.recv(1024).decode()
        except Exception as e:
            print("Error receiving data from server:", e)
            break

        if not data:
            break

        if data.startswith("GET_WORK:"):
            _, start_str, end_str = data.split(":")
            start, end = int(start_str), int(end_str)
            
            print(f"[*] Received work range from server: {start} to {end}")
            
            found = brute_force_chunk(start, end, num_cores)

            try:
                if found:
                    print("Found solution:", found)
                    client.sendall(f"FOUND:{found}".encode())
                    break
                else:
                    client.sendall(b"DONE_CHUNK")
            except Exception as e:
                print("Error sending data to server:", e)
                break

    client.close()
    print("[*] Connection closed.")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    start_client('127.0.0.1')