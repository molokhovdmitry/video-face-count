import os
import functools

from flask.globals import current_app

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import ffmpeg
import face_recognition, cv2
from werkzeug.utils import secure_filename

from VFR.db import get_db
from VFR.upload import allowed_file

bp = Blueprint('application', __name__)

@bp.route('/', methods=('GET', 'POST'))
def find():
    if request.method == 'POST':
        db = get_db()
        
        # Check if user entered "step"
        #if not 

        # Check if user selected a file
        file = request.files['file']
        if not file.filename:
            flash('No video file uploaded')
            return redirect(request.url)

        # Check if the filename is allowed
        if not allowed_file(file.filename):
            flash('Wrong file extension')
            return redirect(request.url)

        # Upload file
        filename = secure_filename(file.filename)
        tempPath = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(tempPath):
            os.makedirs(tempPath)
        path = os.path.join(tempPath, filename)
        file.save(path)
        
        # Video Face Recognition
        # Check if the file is actually a video file

        # Load the video (OpenCV)
        video = cv2.VideoCapture(path)

        # Get "step"
        step = int(request.form.get('step'))
        
        # Get metadata
        videoName = file.filename
        FPS = int(video.get(cv2.CAP_PROP_FPS))
        duration = str(round(float(ffmpeg.probe(path)['streams'][0]['duration'])))
        width = ffmpeg.probe(path)['streams'][0]['width']
        height = ffmpeg.probe(path)['streams'][0]['height']
        dimensions = str(width) + "×" + str(height)
        
        # Delete video file
        os.remove(path)

        # Initialize a frame counter
        i = 0

        # Initialize arrays for a plot
        timeArray = []
        faceArray = []
        
        # Iterate over frames
        while True:
            # Skip "FPS * step" frames
            if (i % (FPS * step) != 0) or i != 0:
                for k in range(int((FPS * step) - 1)):
                    i += 1
                    if not video.grab():
                        break
                    continue
            # Get frame
            frame = video.read()
            
            # Count frames
            i += 1

            # Stop when no frames left
            if not frame[0]:
                break

            # Save second
            second = int(i / FPS)
            timeArray.append(second)

            # Find faces
            face_locations = face_recognition.face_locations(frame[1])

            # Save faces
            faceAmount = len(face_locations)

            # Save faces
            faceArray.append(faceAmount)

        return render_template('plot.html', videoName=videoName, duration=duration, FPS=FPS, dimensions=dimensions, step=step, faceArray=faceArray, timeArray=timeArray)
    
    return render_template('index.html')