# video-face-count
This is my cs50x final project.
https://video-face-count.herokuapp.com/about

## Installation

### Clone the repository and install the requirements:
```
git clone https://github.com/molokhovdmitry/video-face-count
cd video-face-count
pip install -r requirements.txt
```
### Install ffmpeg:
```
sudo apt-get install ffmpeg
```
If you want you can install the application so it is possible to call it from anywhere.
```
pip install -e .
```
### Launch:
```
export FLASK_APP=VFC
flask run
```
Go to http://127.0.0.1:5000/

### Buildpacks for heroku deployment:
```
heroku/python
https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
```
