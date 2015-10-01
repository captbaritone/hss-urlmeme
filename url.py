import glob
import re
import os

from flask import Flask, render_template, request, redirect

from ngram import NGram

APP_ROOT = os.path.dirname(__file__)

app = Flask(__name__, static_url_path='/static')

IMAGE_PATH = 'static/images/'

IMAGES = {
    "terra-run.gif": [
        'terra run',
        'terra race'
    ],
    "bromance.jpg": [
        'bromance',
        'tomo d cash'
    ],
    "garland-dance.gif": [
        "garland dance",
        "trice dance",
        "gtrice dance"
    ],
    "ofer-uggs.jpg": [
        "ofer uggs",
        "goldstein uggs",
        "tulioz uggs"
    ],
    "dcash.jpg": [
        "daniel cash",
        "d cash",
        "d cache",
        "d money",
        "d ram"
    ],
    "lia-dance.gif": [
        "lia dance",
        "lia",
        "Lia Zadoyan"
    ],
    "kerey-keytar.gif": [
        "kerey roper keytar",
        "kerey couch"
    ],
    "cooper.jpg": [
        "cooper",
        "mascot",
        "feed me",
    ]
}

LOCAL_IMAGE_PATH = os.path.join(APP_ROOT, IMAGE_PATH)


def replace_underscore(string):
    return re.sub(r'_', ' ', string)


def tokenize(string):
    string = re.sub(r' ', '', string)
    return replace_underscore(string.lower())


def fix_image_dict(folder, image_dict):
    """Add any images not in the hard-coded dictionary"""
    image_pattern = os.path.join(LOCAL_IMAGE_PATH, "*.*")
    for file_path in glob.glob(image_pattern):
        file_name = os.path.basename(file_path)
        if file_name not in image_dict:
            image_dict[file_name] = [replace_underscore(os.path.splitext(file_name)[0])]


def guess_image(name):
    '''
    Guess which meme image they mean by finding the alias with greatest ngram
    similarity
    '''
    name = tokenize(name)
    best = '404'
    best_score = None
    for guess_image, names in IMAGES.iteritems():
        for guess in names:
            guess = tokenize(guess)
            score = NGram.compare(guess, name)
            if best_score is None or score > best_score:
                best_score = score
                best = guess_image
    app.logger.info('Pick image %s for name "%s"' % (best, name))
    return best


@app.route("/")
def help():
    return render_template('help.html', base_url=request.base_url)


@app.route('/<name>')
def image(name):
    if name.endswith(('.png', '.jpg', '.gif')):
        name = name[:-4]

    image = guess_image(name)
    return redirect('/' + IMAGE_PATH + image, code=301)

if __name__ == "__main__":
    fix_image_dict(LOCAL_IMAGE_PATH, IMAGES)
    app.run(debug=False)
