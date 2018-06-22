#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the REST API for batch
processing.

Example usage:
    python transcribe.py resources/audio.raw
    python transcribe.py gs://cloud-samples-tests/speech/brooklyn.flac
"""

# [START import_libraries]
import argparse
import io
# [END import_libraries]

phrases="""Ten two
Ten ninety six
precinct
ID
checking the area
suspicious activity
hours
Engine
Medic
hours
code violation
gas station
off of
bomb threat
Drumcastle
Joppa
ID number
MVA
NCIC
residential
requesting
requested
officers
CC number
in reference to
advise
damage
Ten Fifty
Ten Fifty PI
air bags
Maryland tags
911
telephone misuse
standing by
in service
possession
destruction of property
gunshot
I'm OK
inmate
Loch Raven
Parkville
message
your location
tri-district
is clear
have you clear
en route
transporting
wanted to verify
the Beltway
in the roadway
Towson
shots fired
disregard
first due
start up
log you on
log me on
log me off
logged on
direct
roll call
CAC
sally port
what's your twenty
units
all units
breathing
area hospitals are clear
area hospitals are on yellow
area hospitals are on red
area hostpitals
childbirth
response on west
response on east
emergency
alert
Ten seven
Ten twenty one
Overlea
White Marsh
Trooper
Maryland State Police
MSP
criss-cross
allie annie
medic unit
Northwest
fire box
medical box
white male
black male
white female
black female
sergeant
lieutennant
captain
prisoner
courthouse
mental health
weapons
your attention
my attention
i'll take it
i'll handle
truck
give me a call at
staging area
missing person
pounds
go ahead
Wilkens
he'll be at
in a wheelchair
intoxicated
holding
ten seven
send your message
domestic disturbance
requesting to cancel
your discretion
hold us clear
elevator
blood pressure
facial droop
upon arrival
nausea
heart rate
pulse ox
how do you copy
first name
middle name
last name
common spelling
switch back
switch up
another medic
wrapped up
BGE
Comcast
trouble breathing
patient
year old male
year old female
hit and run
alpha
bravo
charlie
delta
near
psychiatric
refusing
hold it for me
Ten eight
stand by
can you assist
Ten nine
pulse
finger stick
L and D
Baltimore County
Baltimore Unit
Air on the channel
give you a landline
ETA
how do you copy
trauma category
tenderness
sinus rhythm
vital signs
laceration
dizzyness
that's correct
homeless
cooperative
tresspassing
burglary
robbery
medication
make contact
walk-in
listed as
North Point
Mr. Tire
I'm direct
St. Joe's
GBMC
St. Agnes
Franklin Square
correcting
Kings Oak
Solar Circle
Anonymous caller
crowd
argument
you can ten twenty-two
you can cancel
Headquarters
at that location
pass it on
be on East
be on West
be on Central
traffic stop
touch base
assignment
keep me clear
make me primary
Saytr Hill
run a tag
found drugs
complaint
Ten forty three
dispatch to
twenty-nine
is negative
828
swung around
83 south
83 north
Leslie Avenue
Wicomico
ten four
conscious and breathing
changed over
Baltimore National Pike
description
that description
on foot
engine 101
hydrants
engine two
in station
available
identified
subject
out with him
out with her
description of subject
units in area of
number one male
tattoos
Soundex
date of birth
number two male
number one female
number two female
disgruntled
Harford Road
Northwest Hospital
be an issue
Incident Commander
EMS
another one for delay
sending you down the call
suspect
checked him over
checked her over
Sinai Hospital
Sinai
responding
chest pains
reference to
clothing
were you direct
the desk
pain
baseball diamond
on the fence
respond on
Quarry Lake Drive
audible burglar alarm
if anyone is there
direct on that
send that down
loop around
gonna be holding
no parking zone
send you codes
your facility
arthritis
stated
cancer
hypertension
lungs are clear
IV fluids
standing orders
clear
paramedic
clear on the channel
he's fine
be a dispatch to
commander
Dutch Village
come back around
ten twenty two
keying up
shopping center
Perring Manor
Harford County
complainant
out with subject
ten four for now
local box
involving a pedestrian
ambulance
ambo
female officer
Precinct Three
I'll take a copy
mobile crisis
detain him
good job
warrant
sent you down
Gwynn Oak Avenue
institute
radio check
radio shop
medical call
Falls Road
and the city line
Harford County Sheriff
circumstances
can you advise
abuse
standby for a second
caller
requesting medics
Park Haven
Aviation
mixed race
black hair
brown hair
blue eyes
brown eyes
green eyes
canine unit
advise you can
tag number
uncertain if
Upper Mills
en route to location
Precinct Twelve
gonna have
head up there
incident
County Ride
caller advises
in the station
incident number
KFC
anyone available""".split('\n')


# [START def_transcribe_file]
def transcribe_file_ret(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    # [START migration_sync_request]
    # [START migration_audio_config_file]
    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code='en-US',
        speech_contexts=[types.SpeechContext(
            phrases=phrases,
        )])
        #use_enhanced=True,
       # model='phone_call',)
    # [END migration_audio_config_file]

    # [START migration_sync_response]
    response = client.recognize(config, audio)
    # [END migration_sync_request]
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    return(response)

if __name__ == '__main__':
    import os
    import recognize_to_json
    import time
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'dir', help='Last file that has been scanned')
    parser.add_argument(
        'last', help='Last file that has been scanned')
    args = parser.parse_args()
    lastfile = args.last
    while 1:
        unprocessed = sorted([x for x in os.listdir(args.dir) if x>lastfile])
        for upwav in unprocessed:
            fullpath = os.path.join(args.dir,upwav)
            if os.path.getsize(fullpath)==944044:
                r = transcribe_file_ret(fullpath)
                recognize_to_json.postup(r, fullpath)
                print("Processed " + upwav)
                lastfile = upwav
            elif len(unprocessed)>1:
                continue
        time.sleep(45)
