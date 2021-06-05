#!/bin/bash

set -euo pipefail

mkdir models
cd models
wget 'https://kna-public-models.s3.ap-south-1.amazonaws.com/spacy_model_v2.tar';
tar xvf ./spacy_model_v2.tar
cd ..
/usr/sbin/uwsgi --ini ./conf/uwsgi.ini
