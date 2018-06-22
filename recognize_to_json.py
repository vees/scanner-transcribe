#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 21:19:40 2018

@author: rob
"""

"""
type(f)
Out[38]: google.cloud.speech_v1.types.RecognizeResponse

type(f.results)
Out[44]: google.protobuf.pyext._message.RepeatedCompositeContainer

type(f.results[0])
Out[45]: google.cloud.speech_v1.types.SpeechRecognitionResult

type(f.results[0].alternatives)
Out[46]: google.protobuf.pyext._message.RepeatedCompositeContainer

type(f.results[0].alternatives[0])
Out[47]: google.cloud.speech_v1.types.SpeechRecognitionAlternative

type(f.results[0].alternatives[0].transcript)
Out[48]: str

"""

def to_json(g, speech_file):
    from google.cloud.speech_v1 import types
    import json
    import os
    from datetime import datetime
    if not isinstance(g,types.RecognizeResponse):
        return {}
    file=speech_file
    base=os.path.basename(file)
    begintime=datetime.strptime(base,"scanner-%Y-%m-%d-%H-%M-%S.wav").isoformat()
    a=[]
    i=0
    for result in g.results:
        i+=1
        if len(result.alternatives)>0:
            alt=result.alternatives[0]

            a.append({'recordtime': begintime,
                      'sequence': i,
                      'transcript': alt.transcript,
                      'confidence': alt.confidence})

    return json.dumps(a)

def postup(g, speech_file):
    import requests
    requests.post("https://vees.net/scanner/save",
        to_json(g, speech_file))
