import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import specgram
import librosa
import librosa.display

# Only works locally
def get_wave_plot(sound_name):
    X, sr = librosa.load(sound_name)
    raw_sound = X
    fig = plt.figure(figsize=(15,2))
    fig.suptitle("Monophonic waveform", fontsize=12)
    librosa.display.waveplot(raw_sound, sr=22050)
    return fig

def get_spec_plot(sound_name):
    X, sr = librosa.load(sound_name)
    raw_sound = X
    fig = plt.figure(figsize=(15,2))
    fig.suptitle("Spectrogram", fontsize=12)
    plt.specgram(np.array(raw_sound), Fs=22050)
    return fig

# Only works locally
def get_log_amp(sound_name):
    X, sr = librosa.load(sound_name)
    raw_sound = X
    fig = plt.figure(figsize=(15,2))
    fig.suptitle("Log amplitude spectrogram", fontsize=12)
    D = librosa.logamplitude(np.abs(librosa.stft(raw_sound))**2, ref_power=np.max)
    librosa.display.specshow(D,x_axis='time' ,y_axis='log')
    return fig

def get_chroma(sound_name):
    y, sr = librosa.load(sound_name)
    fig = plt.figure(figsize=(15,2))
    fig.suptitle("Chromagram", fontsize=12)
    C = librosa.feature.chroma_cqt(y=y, sr=sr)
    librosa.display.specshow(C, y_axis='chroma')
    return fig

def get_matplot_chroma(sound_name):
    y, sr = librosa.load(sound_name)
    fig = plt.figure(figsize=(15,2))
    fig.suptitle("Chromagram", fontsize=12)
    C = librosa.feature.chroma_cqt(y=y, sr=sr)
    plt.imshow(C)
    return fig

def get_matplot_wave_plot(sound_name):
    X, sr = librosa.load(sound_name)
    raw_sound = X
    fig = plt.figure(figsize=(15,2))
    fig.suptitle("Waveform", fontsize=12)
    times = np.arange(len(raw_sound))/float(sr)
    plt.plot(times, raw_sound, 'b')
    return fig

def get_log_amp_spec_matplot(sound_name):
    X, sr = librosa.load(sound_name)
    raw_sound = X
    fig = plt.figure(figsize=(15,2))
    fig.suptitle("Log amplitude", fontsize=12)
    D = librosa.logamplitude(np.abs(librosa.stft(raw_sound))**2, ref_power=np.max)
    plt.imshow(D, aspect='auto', cmap='inferno')
    return fig
