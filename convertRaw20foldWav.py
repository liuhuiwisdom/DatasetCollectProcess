# coding: utf-8
# rename the chinese singers name to numbers and record the name to number
from matplotlib import pylab
import numpy
import os
import wave
from pydub import AudioSegment

__author__ = 'zhangxulong'
wavs_dir = '107singersMp3'


def generate_singer_label(wavs_dir):
    dict_singer_label = {}
    singers = []
    for parent, dirnames, filenames in os.walk(wavs_dir):
        for filename in filenames:
            file = os.path.join(parent, filename)
            # singer_name = filename.split('_')[0]
            singer_name = file.split('/')[1]
            print 'singer name:', singer_name
            if singer_name != '.DS_Store':
                singers.append(singer_name)
    only_singers = sorted(list(set(singers)))
    print len(only_singers)
    for item, singer in enumerate(only_singers):
        dict_singer_label[singer] = item + 10001
    # print dict_singer_label
    return dict_singer_label


def key_value_reverse(dicts):
    new_dicts = {}
    for key in dicts:
        print key
        # new_dicts.setdefault(dicts[key], []).append(key)
        new_dicts.setdefault(dicts[key], key)
    return new_dicts


#
# dicts = {"aerosmith": '10001', "beatles": "10002", 'creedence_clearwater_revival': '10003', 'cure': '10004',
#          'dave_matthews_band': '10005', 'depeche_mode': "10006",
#          "fleetwood_mac": '10007', 'garth_brooks': '10008', "green_day": '10009', "led_zeppelin": "10010",
#          'madonna': '10011',
#          'metallica': '10012', 'prince': '10013', 'queen': '10014', 'radiohead': '10015', "roxette": "10016",
#          'steely_dan': '10017', 'suzanne_vega': '10018', 'tori_amos': '10019', 'u2': '10020'}

dicts = generate_singer_label(wavs_dir)


def rename_artist_folds(dir='107singersMp3'):
    for parent, dirname, filename in os.walk(dir):
        for file in filename:
            src = os.path.join(parent, file)
            print src
            artist = src.split('/')[1]
            if len(src.split('/')) == 3:
                title = src.split('/')[2]
                label = dicts[artist]
                dest = "out/" + str(label) + "/" + title
            else:
                title = 'null'
                label = 'null'
                dest = 'null'

            if dest != 'null':
                if not os.path.exists("out/" + str(label) + "/"):
                    os.makedirs("out/" + str(label) + "/")
                print dest
                f = open('107singersMp3_file_list.txt', 'a')
                f.write(src + '\n')
                f.close()

                os.rename(src, dest)
                print src

    return 0


# combine the same singers songs to one long pieces song

def conmbine(singer_item='zhangxulong', dir='album'):
    combine_songs = []
    for parent, dirname, filename in os.walk(dir):
        for file in filename:
            path = os.path.join(parent, file)

            singer_name = path.split('/')[1]
            if singer_name == singer_item:
                combine_songs.append(path)
                # print singer_name
    all_sound = AudioSegment.empty()
    for sound in combine_songs:
        all_sound += AudioSegment.from_mp3(sound)

    output_dir = "combined/" + singer_item + ".wav"
    if not os.path.exists("combined/"):
        os.makedirs("combined/")
    single_sound = all_sound.set_channels(1)
    single_sound.export(output_dir, format="wav")
    return 0


def combine_same_singer(dir="107singersMp3"):
    singers = []
    for parent, dirname, filename in os.walk(dir):
        for file in filename:
            path = os.path.join(parent, file)

            singer_name = path.split('/')[1]
            print singer_name
            singers.append(singer_name)
    singers_set = set(singers)

    for singer_item in singers_set:
        conmbine(singer_item, dir)
        # print singer_item

    print singers_set
    return 0


# split the long song into 20 equal folds
def split_20_folds(wav='example.wav', fold=20):
    out_dir = "20_fold/"
    seconds = 1000
    file_name = os.path.basename(wav)
    files = file_name.split('.')[0]
    file_name = out_dir + files + "/"
    if not os.path.exists(out_dir + files):
        os.makedirs(out_dir + files)
    print"debug===", wav
    if wav != 'combined/.DS_Store':
        sound = AudioSegment.from_wav(wav)
        durations = sound.duration_seconds
        print durations
        print fold
        part_durations = int(durations / fold)
        print part_durations
        for part in range(fold - 1):
            print part
            part_sound = sound[(part_durations * part * seconds):(part_durations * seconds * (part + 1))]
            part_sound.export(file_name + str(part) + ".wav", format='wav')
        last_part_sound = sound[(fold - 1) * seconds * part_durations:]
        last_part_sound.export(file_name + str(fold - 1) + ".wav", format='wav')
    return 0


def batch_split_20_folds(dir='combined'):
    for parent, dirname, filename in os.walk(dir):
        for file in filename:
            path = os.path.join(parent, file)
            if path != 'combined/.DS_Store':
                split_20_folds(path)
    return 0


# split to 17 train & 3 test files

def split_train_test(dir='20_fold'):
    # test = ['0', '1', '2', '3', '4']
    test = ['0', '1', '2']
    for parent, dirname, filename in os.walk(dir):
        for file in filename:
            print file
            if file != '.DS_Store':
                src = os.path.join(parent, file)
                one_dir = src.split('/')[0] + '/'
                two_dir = src.split('/')[1] + '/'
                title = src.split('/')[2]
                test_dir = 'test/'
                train_dir = 'train/'
                title_no = title.split('.')[0]
                if title_no in test:
                    dest = one_dir + two_dir + test_dir + title
                    if not os.path.exists(one_dir + two_dir + test_dir):
                        os.makedirs(one_dir + two_dir + test_dir)
                    os.rename(src, dest)
                else:
                    dest = one_dir + two_dir + train_dir + title
                    if not os.path.exists(one_dir + two_dir + train_dir):
                        os.makedirs(one_dir + two_dir + train_dir)
                    os.rename(src, dest)

    return 0


# 查看单声道波形
def draw_wav(wav_dir):
    print "begin draw_wav ==feature_extraction.py=="
    song = wave.open(wav_dir, "rb")
    params = song.getparams()
    nchannels, samplewidth, framerate, nframes = params[:4]  # format info
    song_data = song.readframes(nframes)
    song.close()
    wave_data = numpy.fromstring(song_data, dtype=numpy.short)
    wave_data.shape = -1, 1
    wave_data = wave_data.T
    time = numpy.arange(0, nframes) * (1.0 / framerate)
    len_time = len(time)
    time = time[0:len_time]
    pylab.plot(time, wave_data[0])
    pylab.xlabel("time")
    pylab.ylabel("wav_data")
    pylab.show()
    return 0

#######################################
# main steps
#######################################
# step 1
# rename_artist_folds()
# step 2 manually change the out to 107singersMp3 and delete the old one
# step 3
# combine_same_singer()
# step 4
# batch_split_20_folds()
# step 5
# split_train_test()
# step 6 finally change the 20_fold to 107singersMp3_20_fold and we get the needed dataset
