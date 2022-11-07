import util, os, shutil, re

root_dir = "./"
unzip_path = "./generated_beatmaps"
downloaded_zip_path = "./generated_beatmaps.zip"
song_path = "./songs"
complete_beatmap_path = "./complete_beatmaps"
all_beatmap_path = "./all_beatmaps"

def clear():
    if os.path.exists(unzip_path):  
        shutil.rmtree(unzip_path)

    if os.path.exists(complete_beatmap_path):
        shutil.rmtree(complete_beatmap_path)

if __name__ == "__main__":
    clear()
    util.unzip(downloaded_zip_path, root_dir)
    util.package(song_path, unzip_path, complete_beatmap_path)
    storage = util.connectFirebase()
    for root, dirs, _ in os.walk(complete_beatmap_path):
        for d in dirs:
            startIdx = [h.start() for h in re.finditer(r"-",d)][0]
            endIdx = [h.start() for h in re.finditer(r"\(",d)][0]
            beatmap_no = d[startIdx + 1: endIdx - 1]
            for element in os.listdir(os.path.join(root, d)):
                util.upload(storage, os.path.join(beatmap_no, element).replace("\\","/").lstrip(), os.path.join(root, d, element))
    
    # storage = util.connectFirebase()
    # util.listAll(storage)