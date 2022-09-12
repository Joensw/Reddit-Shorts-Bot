import os
import subprocess
from uploader import VALID_PRIVACY_STATUSES, get_authenticated_service, initialize_upload
from oauth2client.tools import argparser
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

REDDIT_VIDEO_MAKER_BOT_DIR = os.getenv('REDDIT_VIDEO_MAKER_BOT_DIR')


def create_video():
    cmd = Path('python ' + REDDIT_VIDEO_MAKER_BOT_DIR + '/' + 'main.py')

    original_dir = os.getcwd()
    os.chdir(REDDIT_VIDEO_MAKER_BOT_DIR)
    subprocess.call(cmd.as_posix())
    os.chdir(original_dir)


def find_latest(path):
    list_of_paths = path.glob('**/*.mp4')
    latest_video = Path(max(list_of_paths, key=lambda x: x.stat().st_ctime))
    return latest_video


def upload(args):
    if not args.file.exists():
        exit("Couldn't find video to upload!")
    youtube = get_authenticated_service(args)
    try:
        initialize_upload(youtube, args)
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))


def verify(args):
    get_authenticated_service(args)


def main():
    argparser.add_argument("--file", help="This parameter doesnt do anything")
    argparser.add_argument("--title", help="Video title", default="#shorts #askreddit")
    argparser.add_argument("--description", help="Video description",
                           default="")
    argparser.add_argument("--category", default="22",
                           help="Numeric video category. " +
                                "See https://developers.google.com/youtube/v3/docs/videoCategories/list")
    argparser.add_argument("--keywords", help="Video keywords, comma separated",
                           default="")
    argparser.add_argument("--privacyStatus", choices=VALID_PRIVACY_STATUSES,
                           default=VALID_PRIVACY_STATUSES[0], help="Video privacy status.")
    args = argparser.parse_args()

    # verify before attempting to upload
    verify(args)

    # Make a new video
    create_video()

    # Find the latest created video
    results_path = Path(REDDIT_VIDEO_MAKER_BOT_DIR + '/' + 'results')
    to_upload = find_latest(results_path)

    # Upload it
    args.file = to_upload
    upload(args)


if __name__ == '__main__':
    main()
