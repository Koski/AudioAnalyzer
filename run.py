import urllib2
import numpy as np
import os
import random
import json
import librosa
import StringIO

from plotter import get_matplot_wave_plot, get_spec_plot, get_log_amp_spec_matplot, get_matplot_chroma
from categorizer import extract_current_class, extract_class
from flask import Flask, request, render_template, send_file, make_response

music_dir = 'static/music/'

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/audio/get_category/<filename>', methods=['GET'])
def category(filename):
    print "=================="
    filename = request.path.split('/')
    category = extract_class(filename[-1])
    print category
    return json.dumps(category)

@app.route('/wave_plot/<filename>')
def wave_plot(filename):
    fn = ''.join(["static/music/", filename])
    fig = get_matplot_wave_plot(fn)
    img = StringIO.StringIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route('/spec_plot/<filename>')
def spec_plot(filename):
    fn = ''.join(["static/music/", filename])
    fig = get_spec_plot(fn)
    img = StringIO.StringIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route('/log_amp_plot/<filename>')
def log_amp_plot(filename):
    fn = ''.join(["static/music/", filename])
    fig = get_log_amp_spec_matplot(fn)
    img = StringIO.StringIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route('/chroma_plot/<filename>')
def chroma_plot(filename):
    fn = ''.join(["static/music/", filename])
    fig = get_matplot_chroma(fn)
    img = StringIO.StringIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route('/get_current_category')
def current_category():
    cat_and_prob= extract_current_class()
    return json.dumps(cat_and_prob)

@app.route('/audio/')
def songs():
    music_files = [f for f in os.listdir(music_dir) if f.endswith('wav')]
    return render_template('songs.html',
                                                music_files = music_files)

@app.route('/audio/<filename>')
def sample_page(filename):
    return render_template('sample_page.html',
                                                music_sample = filename)

@app.route('/stream')
def stream():
    return render_template('stream.html')

if __name__ == '__main__':
    app.run()
