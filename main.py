import logging
import os.path
import sqlite3
import hashlib

from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
 
# [logging config
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
# logging config]
 
app = Flask(__name__, 
            static_url_path='',
            static_folder='web/static', 
            template_folder='web/templates'
)
app.secret_key = os.environ.get('SECRET_KEY', 'secret')

allowed_extensions = os.environ.get('ALLOWED_EXT', 'all') 
app.config['ALLOWED_EXTENSIONS'] = allowed_extensions.split('|') if '|' in allowed_extensions else 'all'

MAX_SIZE = os.environ.get('MAX_CONTENT_LENGTH', None)
app.config['MAX_CONTENT_LENGTH'] =  (int(MAX_SIZE) * 1000 * 1000) if MAX_SIZE else None
 
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

app.config['DB_NAME'] = os.path.join(os.getcwd(), 'data', 'records.db')

app.config['HEADER_LOGO'] = os.environ.get('HEADER_LOGO', '/img/header.jpg')
app.config['TITLE'] = os.environ.get('TITLE', 'Imaginator')
app.config['CALL_TO_ACTION'] = os.environ.get('CALL_TO_ACTION', 'A simple multi-image uploader')
 
 
@app.route('/', methods=['GET'])
def index():
    logging.info('Showing index page')
    return render_template('upload.html')
 
 
@app.route('/', methods=['POST'])
def upload_files():
    logging.info('Starting file upload')
 
    if 'files' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.url)
 
    files = request.files.getlist('files')
    author = request.form.get('author')
    if not author:
        flash('Missing Author', 'danger')
        return redirect(request.url)

    success_messages = ''
    warning_messages = '<b>Following files were not uploaded:</b><br><ul>'
    uploaded_files = []
    not_uploaded_files = []
    db_data_to_insert = []

    for file in files:
        # obtaining the name of the destination file
        filename = file.filename
        if filename == '':
            logging.info('Invalid file')
            flash('No file selected for uploading', 'danger')
            #return redirect(request.url)
        else:
            logging.info('Selected file is= [%s]', filename)
            # get filename w/o extension and extension
            filename_wo_ext,file_ext = os.path.splitext(filename)

            if file_ext in app.config['ALLOWED_EXTENSIONS'] or app.config['ALLOWED_EXTENSIONS']=='all':
                secure_fname = "{}_{}{}".format( secure_filename(filename_wo_ext), get_file_hash(file), file_ext )
                logging.info('Secure filename is= [%s]', secure_fname)

                file.save(os.path.join(UPLOAD_FOLDER, secure_fname))
                logging.info('Upload is successful')

                uploaded_files.append( filename )
                db_data_to_insert.append(
                    (author, secure_fname)
                )
            else:
                logging.info(f"Invalid file extension for {filename}")
                not_uploaded_files.append( filename )
                warning_messages += f"<li><i>{filename}</i> has invalid extension</li>"

    if len(files) == len(uploaded_files):
        flash('All files correctly uploaded!', 'success')
    elif not_uploaded_files:
        message = "<b>{} files out {}</b> were correctly uploaded.<br>".format(len(uploaded_files), len(files))
        flash(message + warning_messages, 'warning')
    warning_messages += '</ul>'

    # save data to db
    insert_data_into_db(db_data_to_insert)

    return redirect('/')
 

def get_file_hash(file):
    md5 = hashlib.md5(file.read()).hexdigest()
    file.seek(0)
    return md5


# @data: list of tuple
def insert_data_into_db(data):
    con = sqlite3.connect(app.config['DB_NAME'])
    cur = con.cursor()
    cur.executemany("INSERT INTO images (author, filename) VALUES(?, ?)", data)
    con.commit()

def create_db_if_not_exists():
    con = sqlite3.connect(app.config['DB_NAME'])
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS images(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT not null,
            filename TEXT not null,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    con.commit()
 
def check_upload_dir():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
 
 
if __name__ == '__main__':
    check_upload_dir()

    create_db_if_not_exists()
 
    server_port = os.environ.get('PORT', '5000')
    app.run(debug=False, port=server_port, host='0.0.0.0')