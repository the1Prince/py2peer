# --- Main Application Logic ---
import server_node
import client_node
import threading






def main():
    """
    Main entry point for the application.
    """
    print("Welcome to Simple P2P File Sharer!")
    
    while True:
        print("\nWhat would you like to do?")
        print("  [1] Start sharing files (Server)")
        print("  [2] Download files (Client)")
        print("  [q] Quit")
        
        choice = input("> ").strip().lower()
        
        if choice == '1':
            server_node.start_server()
            break
        elif choice == '2':
            client_node.start_client()
            break
        elif choice == 'q':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter '1', '2', or 'q'.")


if __name__ == "__main__":
  
    main()
    # Start the tray icon application
    