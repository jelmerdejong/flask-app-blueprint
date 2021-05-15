from typing import List
from rtlsdr import RtlSdr
import argparse
import numpy as np
import pyaudio
import scipy.signal as signal

SampleStream = List[float]
AudioStream = List[int]

stream_buf = bytes()
stream_counter = 0

audio_rate = 48000
audio_output = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=audio_rate, output=True)

def process(samples: SampleStream, sdr: RtlSdr) -> None:
    sample_rate_fm = 240000
    iq_comercial = signal.decimate(samples, int(sdr.get_sample_rate()) // sample_rate_fm)

    angle_comercial = np.unwrap(np.angle(iq_comercial))
    demodulated_comercial = np.diff(angle_comercial)

    audio_signal = signal.decimate(demodulated_comercial, sample_rate_fm // audio_rate, zero_phase=True)
    audio_signal = np.int16(14000 * audio_signal)

    audio_output.write(audio_signal.astype("int16").tobytes())

def read_callback(samples, rtl_sdr_obj):
    process(samples, rtl_sdr_obj)

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--ppm', type=int, default=0,
                    help='ppm error correction')
parser.add_argument('--gain', type=int, default=20,
                    help='RF gain level')
parser.add_argument('--freq', type=int, default=92900000,
                    help='frequency to listen to, in Hertz')
parser.add_argument('--verbose', action='store_true',
                    help='mute audio output')

args = parser.parse_args()

sdr = RtlSdr()
sdr.rs = 1024000
sdr.fc = args.freq
sdr.gain = args.gain
sdr.err_ppm = args.ppm

sdr.read_samples_async(read_callback, int(sdr.get_sample_rate()) // 16)
