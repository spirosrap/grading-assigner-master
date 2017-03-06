#Requirements

* [pyPushBullet](https://github.com/Azelphur/pyPushBullet)
* pip install pydub (If you want your computer to play a sound with a newly assigned project
* Add your devices to [Pushbullet](https://www.pushbullet.com) and get an API key
* Install ffmpeg (Mac: brew install ffmpeg)

# Usage
Requires the `requests` module, which you can either install globally or in a virtualenv.

```
usage: grading-assigner.py [-h] [--auth-token TOKEN]

Poll the Udacity reviews API to claim projects to review.

optional arguments:
  -h, --help            show this help message and exit
  --auth-token TOKEN, -T TOKEN
                        Your Udacity auth token. To obtain, login to
                        review.udacity.com, open the Javascript console, and
                        copy the output of
                        `JSON.parse(localStorage.currentUser).token`. This can
                        also be stored in the environment variable
                        UDACITY_AUTH_TOKEN.
  --debug, -d           Turn on debug statements.
```

# Example
```
$ export UDACITY_AUTH_TOKEN=...
$ ./grading-assigner.py
|2016-01-11 12:51:17,885| Requesting certifications...
|2016-01-11 12:51:17,972| Found certifications for project IDs: [2, 1]
|2016-01-11 12:51:17,972| Polling for new submissions...
|2016-01-11 12:51:57,285|
|2016-01-11 12:51:57,285| =================================================
|2016-01-11 12:51:57,285| You have been assigned to grade a new submission!
|2016-01-11 12:51:57,285| View it here: http://review.udacity.com/#!/submissions/13
|2016-01-11 12:51:57,285| =================================================
|2016-01-11 12:51:57,285| Continuing to poll...
|2016-01-11 12:52:02,471|
|2016-01-11 12:52:02,471| =================================================
|2016-01-11 12:52:02,471| You have been assigned to grade a new submission!
|2016-01-11 12:52:02,471| View it here: http://review.udacity.com/#!/submissions/14
|2016-01-11 12:52:02,471| =================================================
|2016-01-11 12:52:02,471| Continuing to poll...
```

Press ctrl-c to quit.

![img](img2.png)
![img](img.png)
