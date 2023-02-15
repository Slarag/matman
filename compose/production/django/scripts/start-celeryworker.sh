#!/bin/bash

set -o errexit
set -o nounset

celery -A matman worker -l INFO