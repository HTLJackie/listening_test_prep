from subprocess import Popen, PIPE
from string import Template

from numpy import NaN
import util
import os
import pandas
import shutil
from xlwt import Workbook
import numbers


# Paths and variables
bpm_fn = "bpm_info.xls"
song_path = "./songs"
empty_beatmap_path = "./empty_beatmaps"
packaged_beatmap_path = "./packaged_beatmaps"
generated_beatmap_path = "./generated_beatmaps"
zip_path = "./empty_beatmaps"
generated_zip = "./generated_beatmaps.zip"
empty_zip = "./empty_beatmaps.zip"



def get_bpm():
    bpm_info = []
    directory = './Songs'

    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet_1')
    
    for song in os.listdir(directory):
        song_info = []
        song_name = str(song).replace(".mp3",'')
        song_info.append(song_name)
        s = os.path.join(directory, song)
        if os.path.isfile(s):
            ps = Popen(["../osu!/TimingAnlyz 0.32.4.exe", s.encode(), ""], stdin=PIPE, stdout=PIPE, shell=True)
            text = str(ps.communicate()[0])

            if text.find("Approximate") > 0:
                bpm = text[text.find("BPM:")+len("BPM:"):text.rfind("Offset")].replace("\\r\\n",'').strip()
                ps.kill()
                ps = Popen(["../osu!/TimingAnlyz 0.32.4.exe", s.encode(), bpm], stdin=PIPE, stdout=PIPE, shell=True)
                text2 = str(ps.communicate()[0])
                bpm = text2[text2.find("BPM:")+len("BPM:"):text2.rfind("Offset")].replace("\\r\\n",'').strip()
                offset = text2[text2.find("Offset:")+len("Offset:"):].replace("\\r\\n\'",'').strip()
                song_info.append(bpm_to_ms(float(bpm)))
                song_info.append(float(offset))
            elif text.find("BPM:") > 0:
                bpm = text[text.find("BPM:")+len("BPM:"):text.rfind("Offset")].replace("\\r\\n",'').strip()
                offset = text[text.find("Offset:")+len("Offset:"):].replace("\\r\\n\'",'').strip()
                song_info.append(bpm_to_ms(float(bpm)))
                song_info.append(float(offset))
            ps.kill()
        bpm_info.append(song_info)

    for song_i in range(0, len(bpm_info)):
        for info_j in range(0, len(bpm_info[song_i])):
            sheet1.write(song_i, info_j,bpm_info[song_i][info_j])

    wb.save(bpm_fn)


def bpm_to_ms(bpm):
    return round(float(60000 / bpm), 12)


def gen_empty_beatmap(mode, beatmap_no, bpm, offset):
    beatmap_template = ""
    with open('beatmap_template.txt', 'r') as file:
        beatmap_template = file.read()

    if not pandas.isna(bpm):
        tm = Template(beatmap_template)
        return tm.substitute(
            mode = mode,
            beatmap_no = beatmap_no,
            bpm = bpm,
            offset = offset
        )

def init_beatmaps():
    beatmap_path = empty_beatmap_path
    if not os.path.exists(beatmap_path):
        os.makedirs(beatmap_path)

    col_name = ['no','bpm','offset']
    df = pandas.read_excel(bpm_fn, header=None,names=col_name)

    creator = "_"
    artist = "_"
    version = "Easy"
    # 0 = All; 1 = taiko; 2 = catch; 3 = mania; 4 = osu
    mode = 0

    for _, row in df.iterrows():
        song_no = int(row['no'])
        fn = "{creator} - {song_no} ({artist}) [{version}].osu".format(
            creator = creator,
            song_no = song_no,
            artist = artist,
            version = version
        )
        new_beatmap = gen_empty_beatmap(mode, song_no, row['bpm'], row['offset'])
        if new_beatmap != None:
            complete_path = os.path.join(beatmap_path, fn)
            with open(complete_path, 'w') as f:
                f.write(new_beatmap)
    
def clear():
    if os.path.exists(empty_beatmap_path):
        shutil.rmtree(empty_beatmap_path)

    if os.path.exists(packaged_beatmap_path):
        shutil.rmtree(packaged_beatmap_path)

    if os.path.exists(generated_beatmap_path):  
        shutil.rmtree(generated_beatmap_path)

    if os.path.exists(zip_path):
        shutil.rmtree(zip_path)

    if os.path.exists(generated_zip):
        os.remove(generated_zip)
    if os.path.exists(empty_zip):
        os.remove(empty_zip)
    

if __name__ == "__main__":
    get_bpm()
    clear()
    init_beatmaps()
    util.package(song_path, empty_beatmap_path, packaged_beatmap_path)
    util.zip(zip_path, packaged_beatmap_path)
