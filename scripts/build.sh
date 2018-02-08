#!/bin/bash
set -e 

SCRIPT_ROOT_DIR=$(dirname $0)
python -m py_compile ${SCRIPT_ROOT_DIR}/../data_collection.py