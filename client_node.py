# --- Client Logic (for downloading files) ---
import threading
import os
import socket
import time
import p2p_connector

def start_client():
    """
    Starts the broadcast listener and interactive client interface.
    """
    my_ip = p2p_connector.get_my_ip()
    if not my_ip:
        print("Could not determine local IP. Exiting.")
        return

    print("Starting client...")
    
    # Ensure the downloads directory exists
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
        print("Created downloads directory: 'downloads'")

    # Start the broadcast listener
    listener_thread = threading.Thread(target=p2p_connector.listen_for_broadcasts)
    listener_thread.daemon = True
    listener_thread.start()
    
    print("\nClient is running. Waiting for peers to be discovered...")
    
    while True:
        try:
            p2p_connector.show_discovered_peers()
            
            # Simple command-line interface
            print("\nOptions:")
            print("  [d] to download a file from a peer")
            print("  [q] to quit")
            print("  [r] to refresh the peer list")
            
            choice = input("> ").strip().lower()

            if choice == 'd':
                download_file_interface()
            elif choice == 'q':
                break
            elif choice == 'r':
                print("Refreshing...")
            else:
                print("Invalid option. Please try again.")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
            
    print("\nClient shutting down.")





def download_file_interface():
    """
    Allows the user to select a peer and a file to download.
    """
    if not p2p_connector.discovered_peers:
        print("No peers available to download from. Please wait for discovery.")
        return
        
    p2p_connector.show_discovered_peers()
    
    try:
        peer_choice_str = input("Enter the number of the peer to connect to: ")
        peer_index = int(peer_choice_str) - 1
        
        peer_list = list(p2p_connector.discovered_peers.keys())
        if not (0 <= peer_index < len(peer_list)):
            print("Invalid peer number.")
            return

        target_ip, target_port = peer_list[peer_index]
        print(f"Connecting to {target_ip}...")
        
        # In a more advanced version, we'd list files first.
        # For simplicity, we ask for a filename directly.
        filename = input("Enter the filename you want to download: ").strip()

        download_file(target_ip, target_port, filename)
    except ValueError:
        print("Invalid input. Please enter a number.")
    except Exception as e:
        print(f"An error occurred during download: {e}")


def download_file(ip, port, filename):
    """
    Establishes a connection and requests a file from a peer.
    """
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_sock.connect((ip, port))
        client_sock.sendall(filename.encode('utf-8'))
        
        # Wait for the peer's response
        response = client_sock.recv(1024).decode('utf-8').strip()
        if response == 'OK':
            print(f"Downloading '{filename}'...")
            download_path = os.path.join('downloads', filename)
            
            with open(download_path, 'wb') as f:
                while True:
                    data = client_sock.recv(4096)
                    if not data:
                        break
                    f.write(data)
            print(f"Download complete! File saved to '{download_path}'")
        elif response == 'NOT_FOUND':
            print(f"Error: The file '{filename}' was not found on the peer.")
        else:
            print("Unexpected response from peer.")

    except socket.error as e:
        print(f"Connection error: {e}")
    finally:
        client_sock.close()