#We build virtualenvironment to download libraries only for this project
virtualenv venv_py3 -p python3
source venv_py3/bin/activate
pip install qtmodern==0.2.0
pip install PyQt5==5.15.4
pip install opencv-python==4.2.0.34
pip install scipy==1.7.0
pip install pynput==1.7.3
pip install psutil==5.8.0