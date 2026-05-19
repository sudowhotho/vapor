# V.A.P.O.R. 🎬💨
### **V**ideo & **A**udio **P**re-processing **O**rganization **R**outine

An automated, multi-step preprocessing asset pipeline built to optimize workflow management for content creators, video editors, and game clip archivers. This package automates the tedious chore of media digging, downloading, stream separation, silence-detecting cuts, and visual storyboarding.

🚀 Quick Start (Dependencies Installation)
This guide assumes you already have Python installed. To set up your environment, open your terminal (Windows PowerShell/CMD or Linux Bash) inside your project directory and run the following command:

Bash
pip install -r requirements.txt
This will automatically read your requirements file and install all necessary dependencies (yt-dlp, watchdog, pillow, moviepy, and numpy) in one go.

📁 Pipeline Architecture & Workflow
For the environment to function seamlessly, place all 5 scripts into a single workspace folder. The pipeline divides into two independent, hands-off automation workflows and one manual batch utility:

📁 Project Root/
├── extraction.py          (Helper: Core downloading & stream extraction engine)
├── condensation.py        (Workflow 1: Live background web scraper)
├── distillation.py        (Workflow 2: Manual chunk-splitter utility)
├── watch_folder.py       (Workflow 3: Local drop-zone monitor)
└── make_storyboard.py    (Helper: Continuous timeline image composite generator)
⚡ Workflow 1: The Automated Web Media Scraper
Run condensation.py to launch a persistent background monitoring loop.

A blank links.txt tracking file will automatically generate on your Windows Desktop if it isn't already there.

Find any YouTube URL or Playlist URL, paste it into links.txt, and save the text file.

The script instantly wakes up, clears the file to prevent accidental duplication cycles, and triggers extraction.py

It extracts your target media directly into an organized subfolder inside a desktop directory named Meme_Library, cleanly separating it into 3 master assets:

*_AUDIO_ONLY.mp3 — Clean audio track for quick soundbites and dialogue sampling.

*_VIDEO_ONLY.mp4 — High-quality video track without audio layout constraints.

*_FULL.mp4 — Master copy containing both perfectly synchronized streams.

✂️ Workflow 2: Automated Silence-Detection Splitting
When you are ready to curate your downloaded footage, run distillation.py manually.

The script automatically sweeps through your entire Meme_Library directory, filtering specifically for your master _FULL.mp4 tracks.

It evaluates the underlying audio frequencies using a silence-threshold filter and cuts the video tracks wherever natural breaks occur.

Every individual joke, sentence, or sketch is output as a sequentially numbered video chunk inside an isolated split_clips/ directory created right next to the master file.

Duplication Protection: If a split_clips/ folder already exists for a video, the script safely skips it instantly, saving valuable processing time on previously managed footage.

🎮 Workflow 3: Local Drop-Zone Monitor & Visual Storyboarding
Run watch_folder.py to activate the local console and capture tracker.

A folder named PS5_Drop_Zone will automatically generate on your desktop.

Drag and drop raw console captures, gameplay clips, or local recordings directly into the zone.

The watcher initializes a defensive sizing loop, monitoring the file size to wait until your computer finishes moving or copying the heavy media stream.

Once unlocked, it seamlessly calls make_storyboard.py to extract 5 mathematically spaced frame screenshots across the video's total runtime.

It bakes timeline positions directly onto the frames and stitches them into a horizontal composite sheet named *_preview.jpg.

This allows you to visually audit long, multi-hour streams to track action peaks and milestones without opening demanding video editing suites.

🛠️ Global System Prerequisite: No-Admin FFmpeg Setup
The backend splitting, audio processing, and video tracking mechanics rely entirely on FFmpeg running as a command-line tool. If your computer lacks administrative privileges, you can safely install it at the local user account level without needing system elevation.

Windows Non-Admin Step-by-Step Installation:
Download the latest compiled "essentials" release architecture package from a verified source like gyan.dev or Bagois.

Extract the archive and move the folder inside your own home user profile directory, for example:

Plaintext
C:\Users\<YOUR_ACCOUNT_NAME>\ffmpeg
Open the Windows Start Menu, type env, and choose Edit the system environment variables (or search for Environment Variables).

Look at the top section of the window labeled User Variables for .

Note: Editing user path metrics does not require computer administrator rights and isolates changes safely to your profile.

Find the variable named Path, select it, and click Edit.

Click New, paste the path pointing to the inner bin execution directory, and click OK to save:

Plaintext
C:\Users\<YOUR_ACCOUNT_NAME>\ffmpeg\bin
Launch a completely fresh terminal window or command prompt and type:

Bash
ffmpeg -version
If the version text prints out successfully, your system environment path resolution is active, and your content creation preprocessing package is fully ready to run!