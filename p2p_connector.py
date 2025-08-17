import socket
import threading
import time

# --- Configuration ---
# You may need to adjust these values based on your network.
# 255.255.255.255 is the standard broadcast address for a local network.
BROADCAST_IP = '255.255.255.255'
BROADCAST_PORT = 12345
TRANSFER_PORT = 12346

# A dictionary to store discovered peers
# The key is a tuple (ip_address, transfer_port) and the value is the last seen timestamp.
discovered_peers = {} 

def get_my_ip():
    """
    Finds the local IP address of the machine.
    This is necessary for the broadcast to work correctly.
    """
    try:
        # We connect to a remote server to get our local IP.
        # It's just a trick, the connection is never made.
        temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_sock.connect(("8.8.8.8", 80))
        local_ip = temp_sock.getsockname()[0]
        temp_sock.close()
        return local_ip
    except socket.error as e:
        print(f"Error getting local IP: {e}")
        return None
    

def broadcast_presence(my_ip):
    """
    Continuously broadcasts this machine's presence to the network.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    message = f"{my_ip}:{TRANSFER_PORT}"
    
    while True:
        try:
            sock.sendto(message.encode('utf-8'), (BROADCAST_IP, BROADCAST_PORT))
            print('broadcast ip: '+BROADCAST_IP)
            print('broadcast port: '+str(BROADCAST_PORT))
            time.sleep(5)
        except Exception as e:
            print(f"Broadcast error: {e}")
            break


def show_discovered_peers():
    """
    Displays the list of discovered peers and their files.
    """
    if not discovered_peers:
        print("\nNo peers discovered yet. Waiting for others to broadcast...")
        return
    
    print("\n--- Discovered Peers ---")
    for i, (ip, _) in enumerate(discovered_peers.keys()):
        print(f"  {i+1}. Peer at IP: {ip}")


def listen_for_broadcasts():
    """
    Continuously listens for broadcast messages from other peers.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(('', BROADCAST_PORT))
    sock.settimeout(1) # Small timeout so the thread can be killed

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            ip, port = data.decode('utf-8').split(':')
            
            # Ignore broadcasts from this machine itself
            if ip != get_my_ip():
                discovered_peers[(ip, int(port))] = time.time()
                # print(f"Discovered new peer: {ip}")
        except socket.timeout:
            continue
        except Exception as e:
            # This can happen when the socket is closed on shutdown.
            # No need to print this.
            pass