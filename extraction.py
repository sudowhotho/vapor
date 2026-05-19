import os
import subprocess
import yt_dlp

# ==========================================
# 📂 CONFIGURATION (Dynamically targets the active Windows user's Desktop)
# ==========================================
DESKTOP_PATH = os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop')
BASE_ASSETS_FOLDER = os.path.join(DESKTOP_PATH, 'Meme_Library')
# ==========================================

def clean_filename(name):
    """Cleans up a string to ensure it's safe for Windows folder/file names."""
    return "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).rstrip()

def process_single_video(video_info, custom_name=None):
    """Takes a single video's downloaded data and extracts the 3 target files."""
    video_title = video_info.get('title', 'video')
    
    # 1. Determine folder name specifically for THIS video
    if custom_name:
        base_filename = clean_filename(custom_name)
    else:
        base_filename = clean_filename(video_title)

    # Each video gets its own isolated target directory
    target_dir = os.path.join(BASE_ASSETS_FOLDER, base_filename)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Expected location of the file yt-dlp just completed downloading
    downloaded_file = video_info.get('requested_downloads', [{}])[0].get('filepath')
    
    if not downloaded_file or not os.path.exists(downloaded_file):
        print(f"❌ Error: Could not locate downloaded master file for {video_title}")
        return

    # Definitive paths for our targeted 3 outputs
    final_full = os.path.join(target_dir, f"{base_filename}_FULL.mp4")
    final_video = os.path.join(target_dir, f"{base_filename}_VIDEO_ONLY.mp4")
    final_audio = os.path.join(target_dir, f"{base_filename}_AUDIO_ONLY.mp3")

    print(f"⚡ Splitting channels into exactly 3 clean assets for: {base_filename}...")

    # File 1: Move and rename the master file to our target folder as the _FULL version
    if os.path.exists(final_full):
        os.remove(final_full)
    os.rename(downloaded_file, final_full)

    # File 2: Extract PURE VIDEO (Silent) using FFmpeg
    subprocess.run([
        'ffmpeg', '-y', '-i', final_full, 
        '-an', '-c:v', 'copy', final_video
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # File 3: Extract PURE AUDIO using FFmpeg
    subprocess.run([
        'ffmpeg', '-y', '-i', final_full, 
        '-q:a', '2', final_audio
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"✅ Success! Created 3 assets inside: {target_dir}")

def download_and_split_asset(video_url, custom_name=None):
    """
    Downloads a video or an entire playlist, ensuring every single video
    gets its own isolated folder with exactly 3 clean files.
    """
    if not os.path.exists(BASE_ASSETS_FOLDER):
        os.makedirs(BASE_ASSETS_FOLDER)

    # Configuration options for yt-dlp
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'merge_output_format': 'mp4',
        # Download files into the base asset directory temporarily
        'outtmpl': os.path.join(BASE_ASSETS_FOLDER, '%(title)s_temp_master.%(ext)s'),
        'quiet': True,
    }

    print(f"\n🎬 Fetching asset from: {video_url}")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info and download at the same time
            info = ydl.extract_info(video_url, download=True)
            
            # Check if the URL was a playlist
            if 'entries' in info:
                print(f"📂 Detected playlist! Processing individual videos...")
                for entry in info['entries']:
                    if entry:  # Ensure entry isn't broken/none
                        process_single_video(entry, custom_name=None)
            else:
                # Single video process
                process_single_video(info, custom_name=custom_name)

    except Exception as e:
        print(f"❌ Error packaging files: {e}")

if __name__ == "__main__":
    print("--- 📦 TRIPLE-THREAT VIDEO/AUDIO PLAYLIST PACKAGER ---")
    url = input("Paste the YouTube/Meme URL or Playlist: ").strip()
    name = input("Give this folder a name (Leave blank for automatic naming): ").strip()
    
    if url:
        download_and_split_asset(url, custom_name=name if name else None)
    else:
        print("No URL provided.")