# Reddit-Shorts-Bot
Very simple program to upload auto generated videos from Reddit threads to YouTube via the YouTube Data API v3

This is an improved version of a prior project where I had slightly modified the RedditVideoMakerBot to enable automatic uploading. The major improvement is that no alterations have to be made to the source code of the RedditVideoMakerBot, so this program can still be used even as that repository is updated further, provided the current directory structure is kept.

# Requirements

A clone of the RedditVideoMakerBot [repository](https://github.com/elebumm/RedditVideoMakerBot) is required as it will be doing the video generation

Furthermore needed are following packages:
 - oauth2client
 - google-api-python-client
 - httplib2
 - python-dotenv

These are also listed in requirements.txt and can be installed with `pip install -r requirements.txt`

# Usage

Navigate to your clone of the repository and in the command line execute
```
$ python main.py
```

# Setup

1. Clone the RedditVideoMakerBot [repository](https://github.com/elebumm/RedditVideoMakerBot)
2. Follow the installation guide for the RedditVideoMakerBot
3. Test the RedditVideoMakerBot to make sure it works
4. Rename `.envTEMPLATE` to `.env` and specify the path to your clone of RedditVideoMakerBot within
5.	-  Create a project in the Google Cloud using the YouTube Data API v3 [^1]
	-  Rename `client_secretsTEMPLATE.json` to `client_secrets.json` and configure the marked fields with the information from your Google Cloud project
6. Run the program, on first usage, you will be asked to authorize the project by Google for a Google (YouTube) account

[^1]: The individual steps for 5. haven't been explained in detail as that would be complicated to follow.
For a good explanation of the individual steps I recommend [this](https://www.youtube.com/watch?v=aFwZgth790Q) video from 4:17 to 11:05. 
Once you have your client ID and client secret, you can configure your `client_secrets.json` like in the next substep.
