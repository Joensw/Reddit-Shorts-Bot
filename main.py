import os
import subprocess
import argument_parser
from uploader import get_authenticated_service, initialize_upload
from oauth2client.tools import argparser
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

load_dotenv()
RVBM_DIR = os.getenv('REDDIT_VIDEO_MAKER_BOT_DIR')
RVBM_RESULTS_DIR_NAME = "results"


def get_run_times():
    config_path = Path(RVBM_DIR + '/' + 'config.toml')
    with open(config_path, mode="rb") as fp:
        config = tomllib.load(fp)

    times_to_run = 1

    try:
        times_to_run = config["settings"]["times_to_run"]
    except KeyError:
        print(f"times_to_run not found, using default value: {times_to_run}")

    return times_to_run


def create_videos():
    cmd = Path('python ' + RVBM_DIR + '/' + 'main.py')

    original_dir = os.getcwd()
    os.chdir(RVBM_DIR)
    proc = subprocess.run(cmd.as_posix())
    proc.check_returncode()
    os.chdir(original_dir)


def get_list_of_newest_files(path, length: int = 1):
    list_of_paths = path.glob('**/*.mp4')
    latest_videos = sorted(list_of_paths, key=lambda x: x.stat().st_ctime, reverse=True)[:length]
    return [Path(x) for x in latest_videos]


def set_video_options(args, file_path):
    if args.title is None:
        full_title = "r/" + file_path.parent.stem + ":" + " " + file_path.stem
        truncated_title = (full_title[:97] + '..') if len(full_title) > 100 else full_title
        args.title = truncated_title
    return args


def upload_from_path(args, file_path):
    args = set_video_options(args, file_path)
    args.file = file_path
    if not args.file.exists():
        exit("Couldn't find video to upload!")
    youtube = get_authenticated_service(args)
    try:
        initialize_upload(youtube, args)
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))


def main():
    args = argument_parser.parse_args()

    # verify before attempting to upload to discover missing / expired o-auth key early

    times_to_run = get_run_times()
    results_path = Path(RVBM_DIR + '/' + RVBM_RESULTS_DIR_NAME)

    if args.retry:
        upload_from_path(args, get_list_of_newest_files(results_path)[0])
        return

    try:
        create_videos()
    except subprocess.CalledProcessError:
        print("Video Creation Process failed!")
        return

    for x in range(times_to_run):
        file_path = get_list_of_newest_files(results_path, times_to_run)[x]
        upload_from_path(args, file_path)


if __name__ == '__main__':
    main()
