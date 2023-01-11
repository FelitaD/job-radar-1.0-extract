# data-job-crawler

The purpose of building a package is to make it easily reusable. In my project [job-market-batch] the custom code used in Airflow's DAG is imported through packages.
The downside is that everytime I need to modify the code, I need to update the package. 
The other package used in [job-market-batch] project to process the scraped data is [data-job-etl].

# How to create a new release

1. Modify toml file : increase package's version
2. Upgrade build
`pip install --upgrade build`
3. Build the wheel : produces 2 files, a .whl and a .tar.gz
`python3 -m build`
4. Install from the wheel : select the last file version 
`pip3 install dist/data_job_crawler-0.X.0-py3-none-any.whl --force-reinstall`
5. Upload to pypi : username \_\_token\_\_ 
`python3 -m twine upload dist/data_job_crawler-0.X.0-py3-none-any.whl`
6. Reinstall package in Airflow

