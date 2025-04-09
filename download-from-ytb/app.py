#author: mercierd575
#v0.1.1
#date:
# v0.1.0 2025-04-03
# v0.1.1 2025-04-04
#brief: this web app program takes an URL as an input and downloads a mp3 or mp4 file
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
#       Do not forget to download ffmpeg and add it to PATH variables
#       to run this program
#
#DISCLAIMER: Do not use this app for any illegal purposes. I may not be held
#            accountable for any legal troubles following the use of this app.

import streamlit as st          # Using streamlit for the WebApp
import subprocess               # Using subprocess to run yt-dlp (a command line tool)
                                # directly from python
import os                       # os is used to list downloaded files after using yt-dlp
                                # and remove the downloaded file after serving it to the user
import ffmpeg as converter      # Using ffmpeg to convert m4a audio files to mp3

st.set_page_config(
    page_title="YouTube Downloader",  # Name displayed on tab
    page_icon=":rocket:",  # Use an emoji or a path to an image for the tab icon
    layout="centered",  # "centered" or "wide"
    initial_sidebar_state="auto"  # "auto", "expanded" or "collapsed"
)

st.title("YouTube Video Downloader 🎥")    # Title of the web app


# User inputs
url = st.text_input("Enter YouTube URL:")   # Asks for a YOUTUBE url specifically
# Format choice shows up as a bullet point list that can be checked
format_choice = st.radio("Select Format:", ("MP4 (Video)", "MP3 (Audio)", "M4A (Uncompressed audio)"))

if st.button("Download"):
    if url:
        # Define output filename
        # Resulting filename will be: [video's title on Youtube].[format (mp3 or mp4)]
        if format_choice == "MP4 (Video)":
            output_format = "mp4"
        elif format_choice == "MP3 (Audio)":
            output_format = "mp3"
        else:
            output_format = "m4a"

        output_filename = "%(title)s.%(ext)s"

        # Define the yt-dlp command
        if output_format == "mp4":
            command = [
                "yt-dlp",
                # Downloads mp4 format and merges with m4a for best quality if available
                # else, downloads best mp4 available quality.
                "-f", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
                "-o", output_filename,
                url
            ]

        elif output_format == "mp3":  # MP3 (Audio)
            command = [
                "yt-dlp",
                "-x", "--audio-format", output_format,
                "--audio-quality", "0",
                "-o", output_filename,
                url
            ]
        else:
            command = [
                "yt-dlp",
                "-f", "ba[ext=m4a]",
                "-o", output_filename,
                url
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
            if output_format == "mp4":
                st.error("Error downloading video.")
            elif output_format == "mp3" or output_format == "m4a":
                st.error("Error downloading audio.")
            else:
                st.error("Error downloading file.")
    else:
        st.warning("Please enter a valid URL.")