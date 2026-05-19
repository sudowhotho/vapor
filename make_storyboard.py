import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import VideoFileClip

# ==========================================
# 🛠️ CONFIGURATION (ADJUST QUALITY & SIZE HERE)
# ==========================================
THUMB_WIDTH = 480          # Width of each thumbnail in pixels (Increase for higher quality)
THUMB_HEIGHT = 270         # Height of each thumbnail (Keeps standard 16:9 widescreen ratio)
NUM_THUMBNAILS = 5         # How many pictures you want in your strip
JPEG_QUALITY = 95          # Image saving quality (1-100). 95 is crystal clear.
# ==========================================

def format_time(seconds):
    """Converts raw seconds (e.g., 75) into a clean timestamp string (e.g., 01:15)."""
    minutes = int(seconds) // 60
    secs = int(seconds) % 60
    return f"{minutes:02d}:{secs:02d}"

def create_video_storyboard(video_path):
    """Takes a video and creates a single high-quality image grid with timestamps."""
    print(f"Analyzing {video_path}...")
    
    with VideoFileClip(video_path) as clip:
        duration = clip.duration
        
        # Calculate perfectly spaced intervals across the clip
        times = np.linspace(1, duration - 1, NUM_THUMBNAILS)
        
        frames = []
        for t in times:
            # Grab the raw pixel frame
            frame = clip.get_frame(t)
            img = Image.fromarray(frame).resize((THUMB_WIDTH, THUMB_HEIGHT))
            
            # --- TIMESTAMP LOGIC ---
            # Create a drawing context on top of the thumbnail
            draw = ImageDraw.Draw(img)
            timestamp_text = format_time(t)
            
            # Try to use a clean system font, fallback to standard if missing
            try:
                font = ImageFont.truetype("arial.ttf", int(THUMB_HEIGHT * 0.12)) # Font scales with image size
            except IOError:
                font = ImageFont.load_default()
                
            # Draw a subtle dark background rectangle for the text so it's readable on bright video frames
            # Positions text in the bottom-right corner
            text_margin = 10
            text_box = draw.textbbox((0, 0), timestamp_text, font=font)
            text_w = text_box[2] - text_box[0]
            text_h = text_box[3] - text_box[1]
            
            x = THUMB_WIDTH - text_w - text_margin
            y = THUMB_HEIGHT - text_h - text_margin
            
            # Draw black background box, then white text over it
            draw.rectangle([x - 5, y - 5, THUMB_WIDTH - text_margin + 5, THUMB_HEIGHT - text_margin + 5], fill=(0, 0, 0, 180))
            draw.text((x, y), timestamp_text, fill=(255, 255, 255), font=font)
            
            frames.append(img)
        
        # Stitch the images horizontally into one long strip
        total_width = THUMB_WIDTH * NUM_THUMBNAILS
        storyboard = Image.new('RGB', (total_width, THUMB_HEIGHT))
        
        for i, frame_img in enumerate(frames):
            storyboard.paste(frame_img, (i * THUMB_WIDTH, 0))
            
        # Save next to the video file using our quality setting
        output_image_path = os.path.splitext(video_path)[0] + "_preview.jpg"
        storyboard.save(output_image_path, "JPEG", quality=JPEG_QUALITY)
        print(f"✅ Created preview sheet: {output_image_path}")

# --- ONLY RUNS IF YOU RUN THIS FILE DIRECTLY ---
if __name__ == "__main__":
    # Scan the folder for your PS5 clips
    valid_extensions = (".mp4", ".mkv", ".webm")

    for file in os.listdir("."):
        if file.lower().endswith(valid_extensions) and not file.startswith("final"):
            try:
                create_video_storyboard(file)
            except Exception as e:
                print(f"Could not process {file}: {e}")