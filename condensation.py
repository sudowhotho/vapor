import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# 🔄 UPDATED: Point this to your new file name
from extraction import download_and_split_asset

# ==========================================
# 📂 CONFIGURATION (Dynamically targets the active Windows user's Desktop)
# ==========================================
WATCH_DIR = os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop')
# 🔄 UPDATED: Tracking atmosphere.txt instead of links.txt
TRACKED_FILE = os.path.join(WATCH_DIR, "atmosphere.txt") 
# ==========================================

class LinkFileHandler(FileSystemEventHandler):
    """Watches a text file for new YouTube/Meme links and processes them."""
    
    def on_modified(self, event):
        # We only care if our specific links.txt file was modified
        if os.path.abspath(event.src_path) != os.path.abspath(TRACKED_FILE):
            return
            
        # Give Windows a split second to release the file lock after saving
        time.sleep(0.5)
        
        # Read the links from the file
        if os.path.exists(TRACKED_FILE) and os.path.getsize(TRACKED_FILE) > 0:
            with open(TRACKED_FILE, "r") as f:
                lines = f.readlines()
                
            valid_links = [line.strip() for line in lines if line.strip().startswith(("http://", "https://"))]
            
            if valid_links:
                print(f"\n⚡ Detected {len(valid_links)} new link(s) to harvest!")
                
                # Clear the file immediately so it doesn't loop or double-process
                with open(TRACKED_FILE, "w") as f:
                    f.write("")
                    
                # Process each link found
                for url in valid_links:
                    try:
                        # Downloads it, splits it, and auto-names the folder using the video title
                        download_and_split_asset(url, custom_name=None)
                    except Exception as e:
                        print(f"Error processing link {url}: {e}")
                
                print("\n👀 Standing by for more links... (Save links inside links.txt)")

if __name__ == "__main__":
    # Automatically create the blank tracking file on your desktop if it's missing
    if not os.path.exists(TRACKED_FILE):
        with open(TRACKED_FILE, "w") as f:
            f.write("# Paste YouTube/Meme links here (one per line) and hit Save!\n")
        print(f"Created tracking file at: {TRACKED_FILE}")
        
    event_handler = LinkFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_DIR, recursive=False)
    
    observer.start()
    print(f"🎬💨 V.A.P.O.R. Condensation Loop is LIVE!")
    print(f"Drop assets into your desktop 'atmosphere.txt' and save. Press Ctrl+C to stop.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()