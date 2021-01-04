git clone https://github.com/molokhovdmitry/video-face-amount-recognition-web
cd video-face-amount-recognition-web
pip install -r requirements.txt
sudo apt-get ffmpeg
pip install -e .
export FLASK_APP=VFC
flask run

Buildpacks:
heroku/python
https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
