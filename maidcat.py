import argparse
from pytube import YouTube
import os
import ffmpeg

def download_video(url, dl_folder, download_audio=False):
    try:
        yt = YouTube(url)
        print(f'Downloading {yt.title}...')
        
        if download_audio:
            stream = yt.streams.filter(only_audio=True).first()
            stream.download(dl_folder)
            
            # Convert to MP3 using ffmpeg-python
            mp4_file = os.path.join(dl_folder, stream.default_filename)
            mp3_file = os.path.join(dl_folder, f"{yt.title}.mp3")
            
            # Input and output file paths for ffmpeg
            input_file = ffmpeg.input(mp4_file)
            output_file = ffmpeg.output(input_file, mp3_file)
            
            # Run the ffmpeg command
            ffmpeg.run(output_file, overwrite_output=True)
            
            # Optionally, delete the original MP4 file
            os.remove(mp4_file)
        else:
            yt.streams.get_highest_resolution().download(dl_folder)
        
        print(f'Finished downloading {yt.title}.\n')
    except Exception as e:
        print(f'Error downloading {url}: {e}')

def download_videos_from_file(file_path, dl_folder, download_audio=False):
    with open(file_path, 'r') as file:
        for line in file:
            url = line.strip()
            if url:
                download_video(url, dl_folder, download_audio)

def main():
    parser = argparse.ArgumentParser(description="Download YouTube videos or audio.")
    parser.add_argument('urls', nargs='*', help='YouTube URLs', metavar='URL')
    parser.add_argument('-m', '--multiple', help='File containing multiple YouTube URLs')
    parser.add_argument('-p', '--path', default='./', help='Download folder path')
    parser.add_argument('-a', '--audio', action='store_true', help='Download audio only')

    args = parser.parse_args()

    if args.urls:
        for url in args.urls:
            download_video(url, args.path, args.audio)
    elif args.multiple:
        download_videos_from_file(args.multiple, args.path, args.audio)
    else:
        print("Please provide at least one YouTube URL or a file containing URLs.")

if __name__ == "__main__":
    main()
