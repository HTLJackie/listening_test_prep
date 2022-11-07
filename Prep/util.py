import os, shutil
import pyrebase

config = {
    "apiKey": "AIzaSyDhPZufXE3mxBU6wPTvU-GGgvz5JrVq3fk",
    "authDomain": "musicrhythmgame.firebaseapp.com",
    "projectId": "musicrhythmgame",
    "storageBucket": "musicrhythmgame.appspot.com",
    "messagingSenderId": "652450328369",
    "appId": "1:652450328369:web:87df1a0624d884012c8a10",
    "measurementId": "G-TF07MM5KNN",
    "databaseURL": "",
    "serviceAccount": "serviceAccountKey.json"
}

def connectFirebase():
    firebase_storage = pyrebase.initialize_app(config)
    storage = firebase_storage.storage()
    return storage

def upload(storage, dest, src):
    storage.child(dest).put(src)

def download(storage, src, path, filenme):
    dest = os.path.join("../osu!/Songs", src)
    storage.child(src).download(path, filenme)

def listAll(storage):
    count = 0
    files  = storage.list_files()
    for file in files:
        print(storage.child(file.name).get_url(None))
        count += 1

    print(count)

def package(song_path, beatmap_path, dest_path):
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    # put beatmaps into separate folders
    for beatmap in os.listdir(beatmap_path):
        new_path = os.path.join(dest_path, os.path.splitext(beatmap)[0])
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        full_path = os.path.join(beatmap_path, beatmap)
        new_full_path = os.path.join(new_path, beatmap)
        shutil.copyfile(full_path, new_full_path)

    # put songs into separate folders
    for song in os.listdir(song_path):
        folder = "_ - {song_no} (_) [Easy]".format(song_no = os.path.splitext(song)[0])
        new_path = os.path.join(dest_path, folder)
        # if not os.path.exists(new_path):
        #     os.makedirs(new_path)
        # full_path = os.path.join(song_path, song)
        # new_full_path = os.path.join(new_path, song)
        # shutil.copyfile(full_path, new_full_path)
        # new_name = os.path.join(new_path, "audio.mp3")
        # os.rename(new_full_path, new_name)

        if os.path.exists(new_path):
            full_path = os.path.join(song_path, song)
            new_full_path = os.path.join(new_path, song)
            shutil.copyfile(full_path, new_full_path)
            new_name = os.path.join(new_path, "audio.mp3")
            os.rename(new_full_path, new_name)
        
def zip(dest_dir, src_dir):
    shutil.make_archive(dest_dir, 'zip', src_dir)


def unzip(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    shutil.unpack_archive(src_dir, dest_dir, 'zip')