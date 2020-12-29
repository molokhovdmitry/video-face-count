import os

from flask.globals import current_app

from flask import (
    Blueprint, flash, g, redirect, render_template, request
)

import ffmpeg
import face_recognition, cv2
from werkzeug.utils import secure_filename

from VFR.db import get_db

bp = Blueprint('application', __name__)

@bp.route('/', methods=('GET', 'POST'))
def find():
    if request.method == 'POST':
        db = get_db()

        # Check if user selected a file
        file = request.files['file']
        if not file.filename:
            flash('No video file uploaded')
            return redirect(request.url)

        # Check if the filename is allowed
        if not allowed_file(file.filename):
            flash('Wrong file extension')
            return redirect(request.url)
        
        # Check if user entered "step"
        if not request.form.get('step'):
            flash('Enter "step"')
            return redirect(request.url)

        # Upload file
        filename = secure_filename(file.filename)
        tempPath = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(tempPath):
            os.makedirs(tempPath)
        path = os.path.join(tempPath, filename)
        file.save(path)
        
        # Video Face Recognition

        # Load the video (OpenCV)
        video = cv2.VideoCapture(path)

        # Get "step"
        step = int(request.form.get('step'))
        
        # Get metadata and check if the file is corrupted
        try:
            videoName = file.filename.rsplit(".")[0]
            videoExtension = file.filename.rsplit(".")[1]
            FPS = int(video.get(cv2.CAP_PROP_FPS))
            duration = str(round(float(ffmpeg.probe(path)['streams'][0]['duration'])))
            width = ffmpeg.probe(path)['streams'][0]['width']
            height = ffmpeg.probe(path)['streams'][0]['height']
            dimensions = str(width) + "×" + str(height)
        except:
            flash("Corrupted file")
            return redirect(request.url)

        # Delete video file
        os.remove(path)

        # Initialize a frame counter
        i = 0

        # Initialize arrays for a plot
        timeArray = []
        faceArray = []

        # Initialize frame array for database
        frameArray = []
        
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

            # Save frame
            frameArray.append(i)

            # Find faces
            face_locations = face_recognition.face_locations(frame[1])

            # Save face amount
            faceAmount = len(face_locations)
            faceArray.append(faceAmount)

        # Insert into database
        db.execute('INSERT INTO videos (name, extension, duration, FPS, dimensions, step) VALUES (?, ?, ?, ?, ?, ?)', (videoName, videoExtension, duration, FPS, dimensions, step))
        rowID = db.execute('SELECT last_insert_rowid()').fetchone()[0]
        for j in range (len(timeArray)):
            db.execute('INSERT INTO frames (video_id, second, frame, faces) VALUES (?, ?, ?, ?)', (rowID, timeArray[j], frameArray[j], faceArray[j]))
        db.commit()

        return render_template('plot.html', videoName=videoName, videoExtension=videoExtension, duration=duration, FPS=FPS, dimensions=dimensions, step=step, faceArray=faceArray, timeArray=timeArray)
    
    return render_template('index.html')

@bp.route("/about")
def about():
    return render_template("about.html")

# Function for file extension checking
ALLOWED_EXTENSIONS = {'mp4', 'avi'}
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS