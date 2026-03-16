import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import queue
import cmath
import math
import time

live = False #True #False

ch = 2
bsz = 2048 #2048 #8 #16 #32 #64 #100 #2048
sr = 44100
dev = None
file = None
stream = None
evt = threading.Event()
q = queue.Queue()
qpos = 0
full = False
progress = 0
ready = 100.00 #0.50
skip = 0 #10000000
prev = None

hbsz = int(bsz / 2)
hann = np.hanning(bsz)
cola = np.append(np.linspace(0, 1, hbsz), np.linspace(1, 0, hbsz))

bands = 16
band = 16

eq = \
{
    "c": 5.0,
    "b": 2.0,
    "f": bsz * ((0.1 / bands) * band),
    "q": bsz,
    "g": 1.0,
    "l": 0.0,
}

def gauss(data, eq):
    n = len(data)
    for i in range(0, n):
        p = i
        if p > n / 2:
            p = n - p
        data[i] *= (pow(eq["c"], (-abs(pow(p - eq["f"], eq["b"])) / eq["q"])) * eq["g"]) + eq["l"]
    return data

def dsp(output, frames, time, status):
    global qpos
    data = [0]
    if qpos < len(q.queue):
        data = q.queue[qpos]
        print(qpos)
        if live:
            data = pre(data.copy())
        qpos += 1
    if len(data) < len(output):
        output[:len(data)] = data
        output[len(data):] = 0
        evt.set()
    else:
        output[:] = data

def pre(output):
    global prev, hann, cola, sss
    if len(output) == 0 \
    or len(output) != bsz:
        return output
    for k in range(0, len(output[0])):
        dat = []
        n = len(output)
        for i in range(0, n):
            dat.append(output[i][k])

        if prev == None:
            prev = [[0 for i in range(0, n)] for k in range(0, len(output[0]))]

        orig = dat.copy()
        hn = int(n / 2)

        sss_bac = prev[k].copy()
        sss_dat = np.append(prev[k][hn:], orig[:hn]).copy()
        sss_fwd = orig.copy()

        sss_bac *= cola #hann
        sss_dat *= cola #hann
        sss_fwd *= cola #hann
        
        sss_bac = np.fft.fft(sss_bac)
        sss_dat = np.fft.fft(sss_dat)
        sss_fwd = np.fft.fft(sss_fwd)

        sss_bac = gauss(sss_bac, eq)
        sss_dat = gauss(sss_dat, eq)
        sss_fwd = gauss(sss_fwd, eq)
        
        sss_bac = np.fft.ifft(sss_bac)
        sss_dat = np.fft.ifft(sss_dat)
        sss_fwd = np.fft.ifft(sss_fwd)

        dat = sss_dat + np.append(sss_bac[hn:], sss_fwd[:hn])

        for i in range(0, n):
            prev[k][i] = orig[i]
        
        for i in range(0, n):
            if math.isinf(dat[i].real) \
            or math.isnan(dat[i].real):
                output[i][k] = 0.0
            else:
                output[i][k] = dat[i].real

    return output

def main():
    global q, qpos, file, stream, progress, skip, full, evt, newdata
    try:
        if not full:
            file = sf.SoundFile("Ident.mp3")
            print(file)
            ch = file.channels
            sr = file.samplerate
            file.seek(skip, sf.SEEK_SET)
            data = [0] * bsz
            stream = sd.OutputStream(samplerate = sr,
                                     blocksize = bsz,
                                     device = dev,
                                     channels = ch,
                                     callback = dsp)
            stream.stop()
            progress = 0.0
            newdata = []
            while len(data):
                data = file.read(bsz)
                if not live:
                    data = pre(data.copy())
                q.put_nowait(data)
                newdata.extend(data)
                if not live:
                    progress += (bsz / file.frames) * 100
                    print("{:0.2f}%".format(progress))
                    if progress >= ready:
                        break
            print("done?")
            full = True
            print(newdata[0:100])
            #sf.write("EQ16.mp3", newdata, sr)
        stream.stop()
        stream.start()
        evt.wait()
        evt.clear()
        print("evt")
        qpos = 0
    except Exception as error:
        raise error

if __name__ == "__main__":
    while True:
        main()
