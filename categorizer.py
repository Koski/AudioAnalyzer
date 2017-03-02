import glob
import os
import subprocess
import time
import librosa
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import urllib2
import datetime

radio_rock_url = "http://icelive0.80692-icelive0.cdn.qbrick.com/10565/80692_RadioRock.mp3"
music_folder = "static/music/"
class_mappings = {
    0 : "Music",
    1 : "Speech",
    2 : "Ads"
}

model_1_shape = 187
model_2_shape = 640

def extract_feature(file_name):
    X, sample_rate = librosa.load(file_name)
    stft = np.abs(librosa.stft(X))
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
    mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)
    return mfccs,chroma,mel,contrast

# def extract_feature(file_name):
#     X, sample_rate = librosa.load(file_name)
#     mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
#     log_amp = np.mean(librosa.logamplitude(librosa.feature.melspectrogram(X, sr=sample_rate)).T, axis = 0)
#     onset_env = librosa.onset.onset_strength(y=X, sr=sample_rate)
#     hop_length = 512
#     tg = np.mean(librosa.feature.tempogram(onset_envelope=onset_env, sr=sample_rate, hop_length=hop_length).T, axis=0)
#     return log_amp, tg, mel

def extract_features_from_file(file_name):
    features = np.empty(model_1_shape)
    mfccs, chroma, mel, contrast = extract_feature(file_name)
    ext_features = np.hstack([mfccs,chroma,mel,contrast])
    features = np.vstack([features,ext_features])
    return features

# def extract_features_from_file(file_name):
#     features = np.empty(model_2_shape)
#     amplitude, tempo_gram, mel = extract_feature(file_name)
#     ext_features = np.hstack([amplitude, tempo_gram, mel])
#     features = np.vstack([features,ext_features])
#     return features

def stream_to_file( ):
    url = urllib2.urlopen(radio_rock_url)
    date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = ''.join([music_folder,"radio_stream_", date_time, ".mp3"])
    f = file(file_name, "w")
    f.write(url.read(70*1024))
    return file_name

def convert_to_wav(file_name):
    wav_file= ''.join([file_name.split('.')[0], ".wav"])
    try:
        subprocess.check_call(['mpg123', '-w', wav_file, file_name])
    except subprocess.CalledProcessError as e:
        print e
        sys.exit(1)
    return wav_file

def normalize(variable, probabilities):
    return '{0:.2f}'.format((variable / np.sum(probabilities)) * 100)

def normalize_all_classes(probabilities):
    normalized_probabilities = {}
    for category in class_mappings.keys():
        # string_catecory = str(class_mappings[category])
        # print string_catecory
        # print type(string_catecory).__name__
        normalized_probabilities[class_mappings[category]] =  normalize(probabilities[category], probabilities)
    return normalized_probabilities

def get_class(features):
    n_dim = features.shape[1]
    n_classes = 3
    n_hidden_units_one = 280
    n_hidden_units_two = 300
    sd = 1 / np.sqrt(n_dim)

    with tf.Session() as sess:

        saver = tf.train.import_meta_graph("/Users/anttikari/school/ml_project/rock_tensor_amp_tempo_mel.chk.meta")
        checkpoint = tf.train.get_checkpoint_state("/Users/anttikari/school/ml_project/")
        print "================"
        print checkpoint.model_checkpoint_path
        saver.restore(sess, checkpoint.model_checkpoint_path)

        W_1 = [ v for v in tf.global_variables() if v.name == "w_1:0" ][0]
        b_1 = [ v for v in tf.global_variables() if v.name == "b_1:0" ][0]
        W_2 = [ v for v in tf.global_variables() if v.name == "w_2:0" ][0]
        b_2 = [ v for v in tf.global_variables() if v.name == "b_2:0" ][0]
        b = [ v for v in tf.global_variables() if v.name == "b:0" ][0]
        W = [ v for v in tf.global_variables() if v.name == "w:0" ][0]

        X = tf.placeholder(tf.float32,[None,n_dim])
        Y = tf.placeholder(tf.float32,[None,n_classes])
        h_1 = tf.nn.tanh(tf.matmul(X,W_1) + b_1)
        h_2 = tf.nn.sigmoid(tf.matmul(h_1,W_2) + b_2)
        y_ = tf.nn.softmax(tf.matmul(h_2,W) + b)

        probabilities = sess.run(y_, feed_dict={X: features})[1]
        y_pred = sess.run(tf.argmax(y_,1), feed_dict={X: features})

    sess.close()
    # Start using if want to show prediction probability
    # prediction_probability = format(probabilities[y_pred[1]] / np.sum(probabilities) * 100, '.4f')
    # print prediction_probability
    return y_pred[1], normalize_all_classes(probabilities)

def extract_class(file_name):
    fn = ''.join([music_folder, file_name])
    features = extract_features_from_file(fn)
    predicted_class, probabilities = get_class(features)
    return {'prediction' : class_mappings[predicted_class], 'probabilities' : probabilities}

def extract_current_class():
    streamed_mp3 = stream_to_file()
    wave_file = convert_to_wav(streamed_mp3)
    os.remove(streamed_mp3)
    features = extract_features_from_file(wave_file)
    os.remove(wave_file)
    predicted_class, probabilities = get_class(features)
    return {'prediction' : class_mappings[predicted_class], 'probabilities' : probabilities}

