import subprocess
import re
import os
import sys

# --- CONFIGURATION ---
# Dynamically targets the active Windows user's Desktop
DESKTOP_PATH = os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop')
BASE_ASSETS_FOLDER = os.path.join(DESKTOP_PATH, 'Meme_Library')

SILENCE_THRESH = "-30dB"     # Sensitivity: lower (e.g., -35dB) = quieter, higher (-25dB) = louder
SILENCE_DURATION = "0.5"     # Minimum duration of silence to trigger a cut (seconds)
# ---------------------

def process_full_video(video_path, folder_path, folder_name):
    """Analyzes a specific _FULL.mp4 video and cuts it into sequenced clips."""
    print(f"\n🎧 Analyzing audio track for: {folder_name}_FULL.mp4...")

    # Step 1: Detect silences using FFmpeg's silencedetect filter
    cmd = f'ffmpeg -i "{video_path}" -af silencedetect=noise={SILENCE_THRESH}:d={SILENCE_DURATION} -f null -'
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    output, _ = process.communicate()

    # Step 2: Extract timestamps
    silence_starts = [float(x) for x in re.findall(r"silence_start: (\d+\.?\d*)", output)]
    silence_ends = [float(x) for x in re.findall(r"silence_end: (\d+\.?\d*)", output)]

    if not silence_starts:
        print(f" ⚠️  No silence thresholds detected for {folder_name}. Try adjusting SILENCE_THRESH.")
        return

    # Step 3: Calculate loud segments (the actual individual meme clips)
    segments = []
    current_start = 0.0

    for start, end in zip(silence_starts, silence_ends):
        # Only treat it as a clip if there's a gap longer than 0.2 seconds between silences
        if start > current_start + 0.2:  
            segments.append((current_start, start))
        current_start = end

    # Catch the final clip after the last silence drop
    segments.append((current_start, None))

    print(f" 🎯 Found {len(segments)} potential soundbites/clips. Slicing video...")

    # Step 4: Batch cut the video file into a nested "clips" directory
    clips_dir = os.path.join(folder_path, "split_clips")
    if not os.path.exists(clips_dir):
        os.makedirs(clips_dir)

    for i, (start, end) in enumerate(segments):
        clip_file = os.path.join(clips_dir, f"{folder_name}_clip_{i+1:03d}.mp4")
        
        if end:
            duration = end - start
            split_cmd = f'ffmpeg -y -ss {start} -i "{video_path}" -t {duration} -c copy "{clip_file}"'
        else:
            split_cmd = f'ffmpeg -y -ss {start} -i "{video_path}" -c copy "{clip_file}"'
            
        subprocess.run(split_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"    [+] Saved: split_clips/{os.path.basename(clip_file)} ({start:.2f}s)")

if __name__ == "__main__":
    if not os.path.exists(BASE_ASSETS_FOLDER):
        print(f"❌ Error: The directory '{BASE_ASSETS_FOLDER}' does not exist.")
        sys.exit()

    print("--- ✂️ AUTOMATED SILENCE-DETECTION VIDEO SPLITTER ---")
    
    # Track if we found anything to process
    processed_count = 0

    # Step 5: Walk through all directories in the Meme_Library
    for root, dirs, files in os.walk(BASE_ASSETS_FOLDER):
        for file in files:
            # We look exclusively for files ending with _FULL.mp4
            if file.endswith("_FULL.mp4"):
                full_video_path = os.path.join(root, file)
                folder_name = os.path.basename(root)
                
                # Check if we already processed this folder to save time
                if os.path.exists(os.path.join(root, "split_clips")):
                    print(f"\n⏩ Skipping '{folder_name}' - 'split_clips' folder already exists.")
                    continue
                
                process_full_video(full_video_path, root, folder_name)
                processed_count += 1
                
    if processed_count == 0:
        print("\n🤷 No new '_FULL.mp4' assets found needing processing.")
    else:
        print(f"\n✅ All done! Processed {processed_count} video folder(s).")