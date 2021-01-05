# video-face-count

## Installation
### Clone the repository and install the requirements:
```
git clone https://github.com/molokhovdmitry/video-face-amount-recognition-web
cd video-face-amount-recognition-web
pip install -r requirements.txt
```
### Install ffmpeg:
```
sudo apt-get ffmpeg
```
If you want you can install the project so it is possible to call it from anywhere.
```
pip install -e .
```
### Launch:
```
export FLASK_APP=VFC
flask run
```
Go to `http://127.0.0.1:5000/`

### Buildpacks for heroku deployment:
```
heroku/python
https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
```
