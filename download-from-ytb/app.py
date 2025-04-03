#author: mercierd575
#v0.1.0
#date: 2025-04-03
#brief: this web app program takes an URL as an imput and downloads a mp3 or mp4 file
#       depending on the user's choice regarding the format.
#       it has to be run on PowerShell using the command
#       streamlit run app.py
#       Make sure no other apps are running on port 8501,
#       otherwise streamlit won't be able to open.
#       A corrupted cache may cause issues.
#       To clear a corrupted cache in the shell, run
#       streamlit cache clear
#       And restart the app with
#       streamlit run app.py
#
#DISCLAIMER: Do not use this app for any illegal purposes. I may not be held
#            accountable for any legal troubles following the use of this app.

import streamlit as st          # Using streamlit for the WebApp
import subprocess               # Using subprocess to run yt-dlp (a command line tool)
                                # directly from python
import os                       # os is used to list downloaded files after using yt-dlp
                                # and remove the downloaded file after serving it to the user

st.title("YouTube Video Downloader 🎥")    # Title of the web app

# User inputs
url = st.text_input("Enter YouTube URL:")   # Asks for a YOUTUBE url specifically
# Format choice shows up as a bullet point list that can be checked
format_choice = st.radio("Select Format:", ("MP4 (Video)", "MP3 (Audio)"))

if st.button("Download"):
    if url:
        # Define output filename
        # Resulting filename will be: [video's title on Youtube].[format (mp3 or mp4)]
        output_format = "mp4" if format_choice == "MP4 (Video)" else "mp3"
        output_filename = f"%(title)s.%(ext)s"

        # Define the yt-dlp command
        command = [
            "yt-dlp",
            "-o", output_filename,
            "-f", "bestaudio/best" if output_format == "mp3" else "best",
            "--extract-audio" if output_format == "mp3" else "",
            "--audio-format" if output_format == "mp3" else "",
            output_format if output_format == "mp3" else "",
            url,
        ]

        command = [c for c in command if c]  # Remove empty strings

        # Run yt-dlp
        process = subprocess.run(command, capture_output=True, text=True)

        if process.returncode == 0:
            # Get downloaded file
            downloaded_file = None
            for file in os.listdir():
                if file.endswith(output_format):
                    downloaded_file = file
                    break

            if downloaded_file:
                with open(downloaded_file, "rb") as file:
                    st.download_button("Click to Download", file, downloaded_file)

                os.remove(downloaded_file)  # Clean up after download
            else:
                st.error("Download failed. Try again!")
        else:
            st.error("Error downloading video.")
    else:
        st.warning("Please enter a valid URL.")