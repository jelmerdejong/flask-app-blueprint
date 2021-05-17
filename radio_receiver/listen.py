from typing import List
from rtlsdr import RtlSdr
import argparse
import datetime
import numpy as np
import pyaudio
import scipy.signal as signal
import speech_recognition as sr
import threading
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()


SampleStream = List[float]
AudioStream = List[int]

stream_buf = bytes()
stream_counter = 0

audio_rate = 48000

recognizer = sr.Recognizer()
audio_output = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=audio_rate, output=True)
ip_addr = os.getenv("ip_addr")
secret = os.getenv("secret")


endpoint_url = os.getenv("URL") or "http://{}/textapi/add?secret={}".format(ip_addr, secret)


def recognize(stream_text):
    global args

    def logger(s):
        f = open('radio_log.txt', 'a+', encoding='utf-8')
        f.write(datetime.datetime.now().strftime("[ %d-%b-%Y %H:%M:%S ] "))
        f.write(s)
        f.write("\x0A")
        f.close()

    # print('sync')
    audio_data = sr.AudioData(stream_text, audio_rate, 2)
    try:
        # result = recognizer.recognize_sphinx(audio_data)
        result = recognizer.recognize_google(audio_data, language=args.lang)
        print(result) # data -> send to server..
        res = requests.get("http://{}/textapi/add?data={}&secret=sec123".format(ip_addr, result))

        print(endpoint_url, res.status_code)
        logger(result)
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print("Could not request results from GSR service; {0}".format(e))
    # print('done')


def stream_audio(data: AudioStream):
    global args
    global stream_buf
    global stream_counter

    if not args.verbose:
        audio_output.write(data)

    if stream_counter < args.buf:
        stream_buf += data
        stream_counter += 1
    else:
        threading.Thread(target=recognize, args=(stream_buf,)).start()
        stream_buf = bytes()
        stream_counter = 0


def process(samples: SampleStream, sdr: RtlSdr) -> None:
    sample_rate_fm = 240000
    iq_comercial = signal.decimate(samples, int(sdr.get_sample_rate()) // sample_rate_fm)

    angle_comercial = np.unwrap(np.angle(iq_comercial))
    demodulated_comercial = np.diff(angle_comercial)

    audio_signal = signal.decimate(demodulated_comercial, sample_rate_fm // audio_rate, zero_phase=True)
    audio_signal = np.int16(14000 * audio_signal)

    stream_audio(audio_signal.astype("int16").tobytes())


def read_callback(samples, rtl_sdr_obj):
    process(samples, rtl_sdr_obj)


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--ppm', type=int, default=0,
                    help='ppm error correction')
parser.add_argument('--gain', type=int, default=20,
                    help='RF gain level')
parser.add_argument('--freq', type=int, default=92900000,
                    help='frequency to listen to, in Hertz')
parser.add_argument('--lang', type=str, default='en-US',
                    help='language to recognize, en-US, ru-RU, fi-FI or any other supported')
parser.add_argument('--buf', type=int, default=100,
                    help='buffer size to recognize, 100 = 6.25 seconds')
parser.add_argument('--verbose', action='store_true',
                    help='mute audio output')

args = parser.parse_args()

sdr = RtlSdr()
sdr.rs = 2400000
sdr.fc = args.freq
sdr.gain = args.gain
sdr.err_ppm = args.ppm

sdr.read_samples_async(read_callback, int(sdr.get_sample_rate()) // 16)