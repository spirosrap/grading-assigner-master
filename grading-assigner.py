from __future__ import print_function
#!/usr/bin/env python
import argparse
import itertools
import logging
import os
import requests
import time
from pydub import AudioSegment
from pydub.playback import play
from pushbullet.pushbullet import PushBullet
import os
import sys


# Script config
CERTS_URL = 'https://review-api.udacity.com/api/v1/me/certifications.json'
ASSIGN_URL = 'https://review-api.udacity.com/api/v1/projects/{pid}/submissions/assign.json'
REVIEW_URL = 'https://review.udacity.com/#!/submissions/{sid}'
REQUESTS_PER_SECOND = 1 # Please leave this alone.

apiKey = "ENTER YOUR PUSHBULLET API KEY"
p = PushBullet(apiKey)
# Get a list of devices
devices = p.getDevices()

# Get a list of contacts
contacts = p.getContacts()


logging.basicConfig(format = '|%(asctime)s| %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

project = {19:"Pitch Perfect: 15$", 20:"MemeMe 2.0: $33",21:"On the Map: $28",22:"Virtual Tourist:$28",23:"You Decide!: 50$",78:"MemeMe 1.0: $28",95:"Pirate Fleet 1: $15",96:"Robot Maze 2: $15",97:"Alien Adventure 1: $12",98:"Alien Adventure 2: $12",99:"Dry-Run: 35$",101:"Pirate Fleet2: $12",102:"Alien 3: $25",110:"Alien 4: $25",111:"Silly Song: $25",155:"GeoQuiz: $15",168:"Common Interoperability Challenges"}
def request_reviews(token):
    song = AudioSegment.from_mp3("doorbell.mp3")
    headers = {'Authorization': token, 'Content-Length': '0'}

    logger.info("Requesting certifications...")
    certs_resp = requests.get(CERTS_URL, headers=headers)
    certs_resp.raise_for_status()

    certs = certs_resp.json()
    project_ids = [cert['project']['id'] for cert in certs if cert['status'] == 'certified']

    logger.info("Found certifications for project IDs: {}".format(str(project_ids)))
    logger.info("Polling for new submissions...")

    for pid in itertools.cycle(project_ids):
        try:
            resp = requests.post(ASSIGN_URL.format(pid = pid), headers=headers)
        except requests.exceptions.ConnectionError as e:
            logger.info("Failure to connect, Retrying")

        if resp.status_code == 201:
            submission = resp.json()
            play(song)
            logger.info("")
            logger.info("=================================================")
            logger.info("You have been assigned to grade a new submission!")
            logger.info("Project:" + str(project[pid]))            
            logger.info("View it here: " + REVIEW_URL.format(sid = submission['id']))
            logger.info("=================================================")
            logger.info("Continuing to poll...")
            p.pushNote(devices[0]["iden"], str(project[pid]),'Project to Review') #Push to iPhone/apple Watch
            
        elif resp.status_code == 404:
            logger.debug("{} returned {}: No submissions available."
                .format(resp.url, resp.status_code))
        elif resp.status_code in [400, 422]:
            logger.debug("{} returned {}: Assigned submission limit reached."
                .format(resp.url, resp.status_code))

        else:
            print("FAILURE!!: ",resp.status_code)
            time.sleep(5.0)
            #resp.raise_for_status()

        time.sleep(1.0 / REQUESTS_PER_SECOND)
        
if __name__=="__main__":
    parser = argparse.ArgumentParser(description =
	"Poll the Udacity reviews API to claim projects to review."
    )
    parser.add_argument('--auth-token', '-T', dest='token',
	metavar='TOKEN', type=str,
	action='store', default=os.environ.get('UDACITY_AUTH_TOKEN'),
	help="""
	    Your Udacity auth token. To obtain, login to review.udacity.com, open the Javascript console, and copy the output of `JSON.parse(localStorage.currentUser).token`.  This can also be stored in the environment variable UDACITY_AUTH_TOKEN.
	"""
    )
    parser.add_argument('--debug', '-d', action='store_true', help='Turn on debug statements.')
    args = parser.parse_args()

    if not args.token:
	parser.print_help()
	parser.exit()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    request_reviews(args.token)

