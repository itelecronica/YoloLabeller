#We build virtualenvironment to download libraries only for this project
virtualenv venv_py3 -p python3
source venv_py3/bin/activate
pip install -r requirements.txt
