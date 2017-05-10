from __future__ import print_function

import json
import os
import sys
import boto3

from pyicloud import PyiCloudService
from fuzzywuzzy import process
from base64 import b64decode

class EnvironmentVarNotSet(Exception):
    pass

# Environment variables
if 'APPLE_ID' in os.environ:
    APPLE_ID = os.environ['APPLE_ID']
else:
    raise EnvironmentVarNotSet('Env value of APPLE_ID must be defined for lambda function')

if 'DEVICE_NAME' in os.environ:
    DEVICE_NAME = os.environ['DEVICE_NAME']
else:
    raise EnvironmentVarNotSet('Env value of DEVICE_NAME must be defined for lambda function')

if 'APPLE_PASSWORD' in os.environ:
    ENCRYPTED = os.environ['APPLE_PASSWORD']
    APPLE_PASSWORD = boto3.client('kms').decrypt(CiphertextBlob=b64decode(ENCRYPTED))['Plaintext']
else:
    raise EnvironmentVarNotSet('Env value of APPLE_PASSWORD must be defined for lambda function')


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Login to apple account and play lost phone sound if a matching device is found
    """

    # We do the same action no matter which event type we get from the iot button
    print("iot event=" + json.dumps(event))

    # If you have bad credentials this will raise an exception
    iCloudApi = PyiCloudService(APPLE_ID, APPLE_PASSWORD)


    print("Looking for device \"" + DEVICE_NAME + "\" on apple id: \"" + APPLE_ID + "\"")

    # Put into a dict by device name
    deviceDict = {}
    for device in iCloudApi.devices:
        deviceDict[device["name"]] = device

    # We do a fuzzy match against the device name to make it easier
    # to deal with wierd unicode issues, etc.
    match = process.extractOne(DEVICE_NAME, deviceDict.keys())
    name = match[0]
    score = match[1]

    print("The following devices were found:")
    print('[%s]' % ', '.join(map(str, deviceDict.keys())))
    print("Match: \"" + name + "\" with score: " + str(score))

    # Play the sound on the device if we get a good enough match
    if score > 90
        print("Playing sound on \"" + name + "\"")
        deviceDict[name].play_sound()
    else
        print("The DEVICE_NAME \"" + DEVICE_NAME + "\" could not be found on account")

