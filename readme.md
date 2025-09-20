## Use duckdb and the duckdb iceberg extension to read data from GCS
This repo provides a simple way to interact with the builder.love data warehouse from a local machine. 

*Architecture*
- duckdb iceberg extension
- duckdb https s3 library
- google cloud storage bucket
- apache iceberg data table

### Steps
- request a storage bucket read access key from trevor@builder.love
- clone this repo to your local machine
- create a .env file at the root of the project
- set key id and key value as environment variables in the .env file: gcs_access_key and gcs_secret_key
- confirm the .env file, with the appropriate path, is in your .gitignore
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

The data exposed using this repo is currently limited to the Ethereum project. Data for one time period has been exposed (August 2025). 

### Table Schema: `public_research.contributor_repo_commits_v2`

| column_name | column_type | null | key | default | extra |
| :--- | :--- | :--- | :--- | :--- | :--- |
| contributor_unique_id_builder_love | VARCHAR | YES | None | None | None |
| repo | VARCHAR | YES | None | None | None |
| project_title | VARCHAR | YES | None | None | None |
| contributor_contributions | BIGINT | YES | None | None | None |
| is_fork | BOOLEAN | YES | None | None | None |
| data_timestamp | TIMESTAMP WITH TIME ZONE | YES | None | None | None |


*column descriptions*
- contributor_unique_id_builder_love: a best-effort attempt to create unique ids for contributors. For logged-in github users, value is set as the concatenation of github login + id. For anon users, concatenate github name + email. Unfortunately, the id contains duplicates. Feedback welcome, but duplicates may be unavoidable.  
- repo: the code repo. The contributor dataset contains only github repos. 
- project_title: the name of the project that is associated with the repo. Note, repos can be associated with multiple projects. 
- contributor_contributions: number of commits. The endpoint is defined [here](https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-repository-contributors)
- is_fork: boolean flag indicating if the repo is a fork
- data_timestamp: date queried from github rest api