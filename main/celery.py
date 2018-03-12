import os
from celery import Celery
import tempfile
import gzip
import json
from ohapi import api
import requests
# from .views import raise_http_error
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oh_data_uploader.settings')

OH_BASE_URL = settings.OPENHUMANS_OH_BASE_URL
OH_API_BASE = OH_BASE_URL + '/api/direct-sharing'
OH_DIRECT_UPLOAD = OH_API_BASE + '/project/files/upload/direct/'
OH_DIRECT_UPLOAD_COMPLETE = OH_API_BASE + '/project/files/upload/complete/'


app = Celery('proj')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(CELERY_BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


def check_integer(string):
    try:
        int(string.replace('"', ''))
        return True
    except ValueError:
        return False


def valid_line(line):
    lsplit = line.rstrip().split(",")
    if check_integer(lsplit[1]) and \
       check_integer(lsplit[2]) and \
       lsplit[0].startswith('"rs') and \
       len(lsplit) == 4:
        return True
    elif line.rstrip() == 'RSID,CHROMOSOME,POSITION,RESULT':
        return True
    else:
        return False


def upload_new_file(cleaned_file,
                    access_token,
                    project_member_id,
                    metadata):
    upload_url = '{}?access_token={}'.format(
        OH_DIRECT_UPLOAD, access_token)
    req1 = requests.post(upload_url,
                         data={'project_member_id': project_member_id,
                               'filename': cleaned_file.name,
                               'metadata': json.dumps(metadata)})
    if req1.status_code != 201:
        raise Exception('Bad response when starting file upload.')

    # Upload to S3 target.
    req2 = requests.put(url=req1.json()['url'], data=cleaned_file)
    if req2.status_code != 200:
        raise Exception('Bad response when uploading file.')

    # Report completed upload to Open Humans.
    complete_url = ('{}?access_token={}'.format(
        OH_DIRECT_UPLOAD_COMPLETE, access_token))
    req3 = requests.post(complete_url,
                         data={'project_member_id': project_member_id,
                               'file_id': req1.json()['id']})
    if req3.status_code != 200:
        raise Exception('Bad response when completing file upload.')


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


def process_target(data_file, access_token, member, metadata):
    tf = tempfile.NamedTemporaryFile(suffix=".gz")
    tf_out = tempfile.NamedTemporaryFile(prefix="ftdna-",
                                         suffix=".csv",
                                         mode="w+b")
    print("downloading ftdna file from oh")
    tf.write(requests.get(data_file['download_url']).content)
    tf.flush()
    print('read ftdna file')
    with gzip.open(tf.name, "rt", newline="\n") as ftdna_file:
        for line in ftdna_file:
            if valid_line(line):
                tf_out.write(line.encode('ascii'))
    tf_out.flush()
    tf_out.seek(0)
    print('cleaned file')
    api.delete_file(access_token,
                    str(member['project_member_id']),
                    file_id=str(data_file['id']))
    print('deleted old')
    upload_new_file(tf_out,
                    access_token,
                    str(member['project_member_id']),
                    data_file['metadata'])


@app.task(bind=True)
def clean_uploaded_file(self, access_token, file_id):
    member = api.exchange_oauth2_member(access_token)
    for dfile in member['data']:
        if dfile['id'] == file_id:
            print(dfile)
            process_target(dfile, access_token, member, dfile['metadata'])
    pass
