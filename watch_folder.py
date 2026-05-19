import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# Import the storyboard function we already perfected
from make_storyboard import create_video_storyboard

# ==========================================
# 📂 CONFIGURATION (Dynamically targets the active Windows user's Desktop)
# ==========================================
DESKTOP_PATH = os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop')
FOLDER_TO_WATCH = os.path.join(DESKTOP_PATH, 'PS5_Drop_Zone')
# ==========================================

class PS5FileHandler(FileSystemEventHandler):
    """Watches for new files and processes them once they finish copying."""
    
    def on_created(self, event):
        # Ignore folders, only look at files
        if event.is_directory:
            return
            
        file_path = event.src_path
        file_name = os.path.basename(file_path)
        valid_extensions = (".mp4", ".mkv", ".webm")
        
        if file_name.lower().endswith(valid_extensions) and not file_name.startswith("final"):
            print(f"\n✨ New video detected: {file_name}")
            
            # Defensive Check: Wait for the file to finish transferring/copying
            historical_size = -1
            while True:
                time.sleep(1) # Wait a second
                try:
                    current_size = os.path.getsize(file_path)
                    if current_size == historical_size:
                        # File size stopped growing, meaning the copy is finished!
                        break
                    historical_size = current_size
                except Exception:
                    # File is still locked by the system moving it
                    continue
            
            # Run our storyboard logic seamlessly
            try:
                create_video_storyboard(file_path)
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

if __name__ == "__main__":
    # Create the folder automatically if it doesn't exist yet
    if not os.path.exists(FOLDER_TO_WATCH):
        os.makedirs(FOLDER_TO_WATCH)
        print(f"Created watch folder at: {FOLDER_TO_WATCH}")
        
    event_handler = PS5FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=FOLDER_TO_WATCH, recursive=False)
    
    observer.start()
    print(f"👀 Live monitoring started on: {FOLDER_TO_WATCH}")
    print("You can drag and drop clips here. Press Ctrl+C in this terminal to stop.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()