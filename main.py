import os
import subprocess
from uploader import VALID_PRIVACY_STATUSES, get_authenticated_service, initialize_upload
from oauth2client.tools import argparser
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

load_dotenv()

REDDIT_VIDEO_MAKER_BOT_DIR = os.getenv('REDDIT_VIDEO_MAKER_BOT_DIR')


def get_run_times():
    config_path = Path(REDDIT_VIDEO_MAKER_BOT_DIR + '/' + 'config.toml')
    with open(config_path, mode="rb") as fp:
        config = tomllib.load(fp)

    times_to_run = 1

    try:
        times_to_run = config["settings"]["times_to_run"]
    except KeyError:
        print(f"times_to_run not found, using default value: {times_to_run}")

    return times_to_run


def create_videos():
    cmd = Path('python ' + REDDIT_VIDEO_MAKER_BOT_DIR + '/' + 'main.py')

    original_dir = os.getcwd()
    os.chdir(REDDIT_VIDEO_MAKER_BOT_DIR)
    subprocess.call(cmd.as_posix())
    os.chdir(original_dir)


def find_latest_list(path, length: int = 1):
    list_of_paths = path.glob('**/*.mp4')
    latest_videos = sorted(list_of_paths, key=lambda x: x.stat().st_ctime, reverse=True)[:length]
    return [Path(x) for x in latest_videos]


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
    argparser.add_argument("title", nargs='?', help="Video title", default="#shorts")
    argparser.add_argument("--description", help="Video description",
                           default="")
    argparser.add_argument("--category", default="22",
                           help="Numeric video category. " +
                                "See https://developers.google.com/youtube/v3/docs/videoCategories/list")
    argparser.add_argument("--keywords", help="Video keywords, comma separated",
                           default="")
    argparser.add_argument("--privacyStatus", choices=VALID_PRIVACY_STATUSES,
                           default=VALID_PRIVACY_STATUSES[0], help="Video privacy status.")
    argparser.add_argument("--retry", help="Skip video creation and attempt to upload latest video",
                           action="store_true")
    args = argparser.parse_args()

    # verify before attempting to upload to discover missing / expired o-auth key early
    verify(args)

    times_to_run = get_run_times()
    results_path = Path(REDDIT_VIDEO_MAKER_BOT_DIR + '/' + 'results')

    if args.retry:
        to_upload = find_latest_list(results_path)[0]
        args.file = to_upload
        upload(args)
        return

    create_videos()  # Will create as many videos as is specified in the RVMB config.toml
    for x in range(times_to_run):
        to_upload = find_latest_list(results_path, times_to_run)[x]
        args.file = to_upload
        upload(args)


if __name__ == '__main__':
    main()
