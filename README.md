create env 

```bash
conda create -n wineq python=3.7 -y
```

activate env
```bash
conda activate wineq
```

created a req file

install the req
```bash
pip install -r requirements.txt
```

```bash
git init
```
```bash
dvc init 
```
```bash
dvc add data_given/mushrooms.csv

dvc repro -> to run the pipeline
dvc metrics show -> to see params.json and metrics.json
dvc metrics diff -> to see difference old and new metrics 
```
```bash
git add .
```
```bash
git commit -m "first commit"
```

oneliner updates  for readme

```bash
git add . && git commit -m "update Readme.md"
```
```bash
git remote add origin https://github.com/pranav-c01/Ineuron_internhip_proj.git
git branch -M main
git push origin main
```

tox command -
```bash
tox
```
for rebuilding -
```bash
tox -r 
```
pytest command
```bash
pytest -v
```

setup commands -
```bash
pip install -e .  # installs local packages present in dir (setup.py file)
```

build your own package commands- 
```bash
python setup.py sdist bdist_wheel
```

create an artifcats folder
```bash
mkdir artifacts
```

mlflow server command -
```bash
mlflow server
--backend-store-uri sqlite:///mlflow.db
--default-artifact-root ./artifacts
--host 0.0.0.0 -p 1234
```

mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts --host 0.0.0.0 -p 1234