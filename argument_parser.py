from uploader import VALID_PRIVACY_STATUSES
from oauth2client.tools import argparser


def parse_args():
    argparser.add_argument("--file", help="This parameter is set automatically")
    argparser.add_argument("title", nargs='?', help="Video title")
    argparser.add_argument("--description", help="Video description", default="")
    argparser.add_argument("--category", default="22",
                           help="Numeric video category. " +
                                "See https://developers.google.com/youtube/v3/docs/videoCategories/list")
    argparser.add_argument("--keywords", help="Video keywords, comma separated",
                           default="")
    argparser.add_argument("--privacyStatus", choices=VALID_PRIVACY_STATUSES,
                           default=VALID_PRIVACY_STATUSES[0], help="Video privacy status.")
    argparser.add_argument("--retry", help="Skip video creation and attempt to upload latest video",
                           action="store_true")

    return argparser.parse_args()
