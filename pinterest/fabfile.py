import os
from fabric.api import task,local
import json
import boto3,requests,sys


@task
def populate_q(queue_name,output_bucket,code_bucket,code_key):
    """
    Example:   fab populate_q:testakshay,testakshay,aub3data,download.py
    :param queue_name:
    :param output_bucket:
    :param code_bucket:
    :param code_key:
    :return:
    """
    sqs = boto3.resource('sqs')
    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3')
    queue = sqs.get_queue_by_name(QueueName=queue_name)
    b = s3.create_bucket(Bucket=output_bucket)
    s3_client.upload_file(code_key, code_bucket, code_key)
    count = 1
    sitemap = requests.get('https://www.pinterest.com/v2_sitemaps/www_v2_board_sitemap.xml').content
    for line in sitemap.split():
        if line.startswith('<loc>'):
            entry = {'url':line.strip().replace('<loc>','').replace('</loc>',''),'output_bucket':output_bucket,'bucket':code_bucket,'key':code_key}
            response = queue.send_message(MessageBody=json.dumps(entry))
            count += 1
            if count % 1000 == 0:
                print "Added {} messages".format(count)
                break

@task
def test():
    pass
