#!/bin/bash
set -e 

SCRIPT_ROOT_DIR=$(dirname $0)
pylint ${SCRIPT_ROOT_DIR}/../data_collection.py ${SCRIPT_ROOT_DIR}/../data_sources/* ${SCRIPT_ROOT_DIR}/../utils/*