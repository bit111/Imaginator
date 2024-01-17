# Imaginator
Imaginator is a simply **dockerized** multi-image upload app wrote in Python, Flask and Bootstrap 5 to allow users to quickly handle images (but also any other file) upload.

![Screenshot of Imaginator](docs/img/screenshot.png?raw=true "Imaginator")

The idea was born from the need to create a platform to allow event guests to share their photos with the organizer by uploading them to a physical server, without going through third-party clouds and/or paid services.

Once you have configured the app on your server, simply generate a QR-code and print it on your event invitations!

## Requirements
To work properly the project requires:
- Python 3.10/3.11
- [Flask](https://pypi.org/project/Flask/)
- [Werkzeug](https://pypi.org/project/Werkzeug/)

## How it works

For each upload, the system add an entry in a `SQLite` database with:
- author's name;
- filename;
- timestamp.

With Imaginator you can choose what file extensions are allowed to upload (default: `all`).

## Installation
Imaginator run using [Docker](https://docker.com/) container to speed-up production process.

### Using Docker
Imaginator is fully customizable via `docker-compose.yml` file using these parameters:

| PARAMETER   |      DESCRIPTION      |  DEFAULT |
|----------|-------------|---------------|
| ALLOWED_EXT|  Allowed file extensions | `all` |
| TITLE |    Title shown in home-page header |   `Imaginator` |
| CALL_TO_ACTION | Subtitle shown in home-page header | `A simple multi-image uploader` |
| HEADER_LOGO | Header background | `web/static/img/header.jpg` |
| SECRET_KEY | Used by [Flask](https://explore-flask.readthedocs.io/en/latest/configuration.html) to sign cookies | `mysecretkey` (change it!) |

#### Run
```
git clone https://github.com/bit111/Imaginator.git
docker compose up -d --build
# go to http://<IP>:<PORT>
```

### Using virtual environment (only for test!)
```
git clone https://github.com/bit111/Imaginator.git
cd imaginator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```
## TO DO
- [ ] Using WSGI server insteaf of Flask for production environment.

## Credits
This work was inspired by https://examples.javacodegeeks.com/upload-a-file-with-python-flask/.

Default header logo by [Roman](https://pixabay.com/it/users/akitada31-172067/).

## License
Copyright (c) 2024. Available under the [GNU AFFERO GENERAL PUBLIC](https://www.gnu.org/licenses/agpl-3.0.en.html) LICENSE.

