from __future__ import print_function

import json
import os
import boto3

from pyicloud import PyiCloudService
#from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from base64 import b64decode

# Environment variables
ENCRYPTED = os.environ['APPLE_PASSWORD']
APPLE_PASSWORD = boto3.client('kms').decrypt(CiphertextBlob=b64decode(ENCRYPTED))['Plaintext']

APPLE_ID = os.environ['APPLE_ID']
DEVICE_NAME = os.environ['DEVICE_NAME']


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("iot event=" + json.dumps(event))

    iCloudApi = PyiCloudService(APPLE_ID, APPLE_PASSWORD)
    # TODO: check for login failure

    # TODO: checdk for env not set - but maybe need to do above?
    print("Looking for device \"" + DEVICE_NAME + "\" on apple id: \"" + APPLE_ID + "\"")

    # Put into a dict by device name
    deviceDict = {}
    for device in iCloudApi.devices: 
        print(device["name"])
        deviceDict[device["name"]] = device

    # We do a fuzzy match against the device name to make it easier
    # to deal with wierd unicode issues, etc.
    matchName = process.extractOne(DEVICE_NAME, deviceDict.keys())
    # TODO: check for no match - how high should match probablity be?
    print("match:" + matchName[0])
    print(deviceDict[matchName[0]]['name'])

    # Actually play the find iPhone sound
    deviceDict[matchName[0]].play_sound()

    # find_phone()
    print("find phone finished")

