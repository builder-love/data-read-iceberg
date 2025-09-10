## Use duckdb and the duckdb iceberg extension to read data from GCS
This repo provides a simple way to interact with the builder.love data warehouse from a local machine. 

*Architecture*
- duckdb iceberg extension
- duckdb https s3 library
- google cloud storage bucket
- apache iceberg data table

### Steps
- request a storage bucket read access key from trevor@builder.love
- set key id and key value as environment variables: gcs_access_key and gcs_secret_key
- recommended to create a virtual environment using pyenv and install requirements using uv
``` 
pyenv virtualenv 3.13.5 my_venv
pyenv local my_venv
uv pip install -r requirements.txt
```
- run the python script
```
python query_iceberg_gcs.py
```

### Data dictionary

The data exposed using this repo is currently limited to project repo contributors and contributor commit counts

Table Schema: public_research.contributor_repo_commits_v2
column_name

column_type

null

key

default

extra

contributor_unique_id_builder_love

VARCHAR

YES

None

None

None

repo

VARCHAR

YES

None

None

None

contributor_contributions

BIGINT

YES

None

None

None

data_timestamp

TIMESTAMP WITH TIME ZONE

YES

None

None

None

*column descriptions*
- contributor_unique_id_builder_love: a best-effort attempt to create unique ids for contributors. For logged-in github users, value is set as concatenate github login + id. For anon users, concatenate github name + email. Unfortunately, the id contains duplicates. Feedback welcome, but may be unavoidable.  
- repo: the code repo. The contributor dataset contains only github repos. 
- contributor_contributions: number of commits. The endpoint is defined [here](https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-repository-contributors)
- data_timestamp: date queried from github rest api