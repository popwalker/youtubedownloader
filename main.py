"""Module docstring
This script help you download youtube video and convert subtitle from vvt to srt
"""
import sys, getopt, os, subprocess
import convert

def usage():
    usagehelp = """ \

    Usage:

      main.py [options]

      -u    -- The url you want to download from.

      -h    -- Show help.

      -d    -- The directory which you want to put your video file to.

    Examples:

      python main.py -u "https://www.youtube.com/watch?v=_Nh0osOwuSk" -d "/tmp"

    """
    print(usagehelp)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    try:
        opts, args = getopt.getopt(argv[1:], "h:u:d:", ["help", "url", "dir"])
    except getopt.GetoptError as err:
        usage()
        sys.exit(2)

    url = None
    save_path = None
    verbose = False

    for o, v in opts:
        if o == "-v":
            verbose = True
        elif o in ["-h", "--help"]:
            usage()
            sys.exit()
        elif o in ["-u", "--url"]:
            url = v
        elif o in ["-d", "--dir"]:
            save_path = v
        else:
            assert False, "unhandled option"

    start_download(url, save_path)


def start_download(url=None, directory=None):
    # file name format
    fileformat = "%(upload_date)s-[%(title)s].%(ext)s"
    if directory != None:
        fileformat = directory + "/" + fileformat


    command = ["youtube-dl", "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
               "--write-auto-sub",
               "-o", fileformat,
               url
               ]
    # execute command
    popen = subprocess.Popen(command, stdout=subprocess.PIPE)

    # synchronize output
    while True:
        next_line = popen.stdout.readline()
        if next_line == b'' and popen.poll() != None:
            break
        print(next_line)

    # convert subtitle
    print("start convert subtitle")
    convert_subtitle_file(directory)


def convert_subtitle_file(top_path=None):
    if top_path is None:
        top_path = "."
    convert.walktree(top_path, convert.convert_vtt_to_srt)

if __name__ == "__main__":
    main()
