# video-face-count
## Installation
Clone the repository and install requirements:
```
git clone https://github.com/molokhovdmitry/video-face-amount-recognition-web
cd video-face-amount-recognition-web
pip install -r requirements.txt
```
Install ffmpeg:
```
sudo apt-get ffmpeg
```
Install the project if you want so you can call it from anywhere.
```
pip install -e .
```
Launch:
```
export FLASK_APP=VFC
flask run
```

Buildpacks:
heroku/python
https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
