import argparse
from uploader import VALID_PRIVACY_STATUSES


def parse_args():
    parser = argparse.ArgumentParser(description="Upload auto generated content to YouTube shorts")
    parser.add_argument("--file", help="This parameter is set automatically")
    parser.add_argument("title", nargs='?', help="Video title")
    parser.add_argument("--description", help="Video description", default="")
    parser.add_argument("--category", default="22",
                        help="Numeric video category. " +
                             "See https://developers.google.com/youtube/v3/docs/videoCategories/list")
    parser.add_argument("--keywords", help="Video keywords, comma separated",
                        default="")
    parser.add_argument("--privacyStatus", choices=VALID_PRIVACY_STATUSES,
                        default=VALID_PRIVACY_STATUSES[0], help="Video privacy status.")
    parser.add_argument("--retry", help="Skip video creation and attempt to upload latest video",
                        action="store_true")
    return parser.parse_args()
