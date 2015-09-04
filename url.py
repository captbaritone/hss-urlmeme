import re
import os

from flask import Flask, render_template, request, redirect

from ngram import NGram

APP_ROOT = os.path.dirname(__file__)

app = Flask(__name__, static_url_path='/static')

IMAGES = {
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
    "cooper.jpg": [
        "cooper",
        "mascot",
        "feed me",
    ]
}


def replace_underscore(string):
    return re.sub(r'_', ' ', string)


def tokenize(string):
    string = re.sub(r' ', '', string)
    return replace_underscore(string.lower())


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
    return redirect("/static/images/" + image, code=301)

if __name__ == "__main__":
    app.run(debug=False)
