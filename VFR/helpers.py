ALLOWED_EXTENSIONS = {'mp4', 'avi'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS