#!/bin/sh

pip3 install --upgrade build
python3 -m build
pip3 install dist/data_job_crawler-1.1.0-py3-none-any.whl --force-reinstall
python3 -m twine upload dist/data_job_crawler-1.1.0-py3-none-any.whl
