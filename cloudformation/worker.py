#!/usr/bin/python
QUEUE_NAME = "testakshay"
#START
import json,time,os,sys
from boto3.session import Session
s = Session(region_name="us-east-1")
sqs = s.resource("sqs")
s3 = s.client("s3")
queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)
cached = set()
while True:
    for message in queue.receive_messages():
        print "Starting"
        print message.body
        payload = json.loads(message.body)
        if not (payload['bucket'],payload['key']) in cached:
            s3.download_file(payload['bucket'], payload['key'], payload['key'])
            os.system('chmod a+x {}'.format(payload['key']))
            cached.add((payload['bucket'],payload['key']))
        sys.argv = [payload['key'],payload]
        execfile(payload['key'])
        message.delete()
    print "Queue empty going to sleep for a minute"
    time.sleep(60)

