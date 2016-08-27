__author__ = 'aub3'
from fabric.api import task
import json

@task
def compile():
    template = json.load(file('template.json'))
    start = False
    content = []
    for line in file('worker.py'):
        if start:
            content.append(line)
        if line.startswith('#START'):
            start = True

    payload = [u'',
               [u'#!/usr/bin/python \n',
                u'QUEUE_NAME            = "',
                {u'Fn::GetAtt': [u'InputQueue', u'QueueName']},
                u'";\n',
                u"print 'Hello world!'\n" ] + content
               ]
    template['Resources']['LaunchConfig']['Metadata']["AWS::CloudFormation::Init"]['WorkerRole']['files']['/home/ec2-user/worker.py']['content']['Fn::Join'] = payload;
    with open('stack.json','w') as output:
        json.dump(template,output,indent=4, sort_keys=True)