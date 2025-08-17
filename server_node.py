# --- Server Logic (for sharing files) ---
import os
import p2p_connector
import threading
import time
import socket
import file_discovery

SHARED_FOLDER = 'shared_files'

def start_server():
    """
    Starts the file sharing server and broadcast listener.
    """
    my_ip = p2p_connector.get_my_ip()
    if not my_ip:
        print("Could not determine local IP. Exiting.")
        return

    print(f"Starting server on {my_ip}...")
    
    # Ensure the shared directory exists
    if not os.path.exists(SHARED_FOLDER):
        os.makedirs(SHARED_FOLDER)
        print(f"Created shared directory: '{SHARED_FOLDER}'")

    # Start the broadcast listener in a separate thread
    listener_thread = threading.Thread(target=p2p_connector.listen_for_broadcasts)
    listener_thread.daemon = True # Kills thread when main program exits
    listener_thread.start()

    # Start the file transfer server in a separate thread
    transfer_thread = threading.Thread(target=handle_file_transfers)
    transfer_thread.daemon = True
    transfer_thread.start()

    # Start broadcasting our presence
    broadcast_thread = threading.Thread(target=p2p_connector.broadcast_presence(my_ip), args=(my_ip,))
    broadcast_thread.daemon = True 
    broadcast_thread.start()
    
    print("\nServer is running. Peers can now discover and download files from you.")
    print("Press Ctrl+C to stop.")
    file_discovery.show_available_files()
    
    try:
        # Keep the main thread alive to allow other threads to run
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nServer shutting down.")





def handle_file_transfers():
    """
    Listens for incoming file transfer requests from clients.
    """
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('', p2p_connector.TRANSFER_PORT))
    server_sock.listen(5)
    
    while True:
        try:
            client_conn, addr = server_sock.accept()
            print(f"\nIncoming connection from {addr[0]}...")
            threading.Thread(target=serve_file_request, args=(client_conn,)).start()
        except Exception as e:
            print(f"Transfer listener error: {e}")
            break


def serve_file_request(conn):
    """
    Handles a single file request from a client.
    """
    try:
        data = conn.recv(1024).decode('utf-8')
        filename = data.strip()
        filepath = os.path.join(SHARED_FOLDER, filename)
        
        if os.path.isfile(filepath):
            print(f"Sending file: {filename}")
            conn.sendall(b'OK') # Signal that the file exists
            time.sleep(0.1) # A small delay to ensure the client receives 'OK'
            with open(filepath, 'rb') as f:
                conn.sendfile(f)
            print(f"Successfully sent '{filename}'")
        else:
            print(f"File '{filename}' not found.")
            conn.sendall(b'NOT_FOUND')
    except Exception as e:
        print(f"Error handling file transfer: {e}")
    finally:
        conn.close()
