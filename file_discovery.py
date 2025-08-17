# file_discovery.py
import os

SHARED_FOLDER = 'shared_files'

def show_available_files():
    """
    Displays the list of files in the shared folder.
    """
    if not os.path.exists(SHARED_FOLDER):
        print(f"The '{SHARED_FOLDER}' directory does not exist.")
        return []
    
    files = [f for f in os.listdir(SHARED_FOLDER) if os.path.isfile(os.path.join(SHARED_FOLDER, f))]
    if not files:
        print("No files available for sharing.")
    else:
        print("\n--- Available Files to Share ---")
        for i, filename in enumerate(files):
            print(f"  {i+1}. {filename}")
    return files