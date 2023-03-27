#!/bin/sh

pip3 install --upgrade build
python3 -m build
pip3 install dist/data_engineering_job_market-1.0.0-py3-none-any.whl --force-reinstall
python3 -m twine upload dist/*