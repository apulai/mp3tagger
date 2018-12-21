# Requires Python 3.5+
# Requires mp3-tagger library ("pip3 install mp3-tagger" or download from here: https://pypi.org/project/mp3-tagger/)
# nem kell -*- coding:Utf-8 -*-

import os
import glob
import json
from mp3_tagger import MP3File
from mp3_tagger.id3 import VERSION_2, VERSION_BOTH, VERSION_1


#PATH = "/home/apulai/mp3"
#PATH = "Z:\\"
#PATH = "Z:\\Greatest Hits of the 80's 8CD 320KB 2Lions-Team\\Greatest Hits Of The 80's CD6"
#PATH = "c:\\test"
#PATH="Z:\\juca"
#PATH="Z:\\mp3\\shrek"
PATH="Z:\\mp3\\_Magyar"
#PATH="Z:\\mp3\\_Latin"
#PATH="Z:\\mp3\\_Gyerek"
#PATH="Z:\\mp3\\_Country"
#PATH="Z:\\mp3\\_Disco"
#PATH="/mnt/backupdsk/mp3/_Magyar"

EXTENSION = ".mp3"

# TODO: Skip directories marked as consistent in the processed.log file (likely load proccessed log before run
PROCESSED_DIR_FILE = PATH + "/processed.log"


rootDir = PATH
report_inconsistent_directories = 1
update_mp3data = 1

# TODO: sync v1 and v2 tags


def collect_mp3info(directory):
    """
    function:	collect-mp3info
    input:	    foldername
    output:	    list of dictionaries containing mp3 tags per song
    operation:	opens each mp3 files, and extracts mp3 info into a list of dictionaries.
                might return an empty list

    """
    print("Function: collect_mp3info")
    songs_list = list()
    file_list = glob.glob(directory + "/*" + EXTENSION, recursive=False)
    # print(directory),
    # print(file_list),
    for file in file_list:
        # print("file:", file)
        # print("file: " + file)
        # print("file: {} directory:{}".format(file,directory))
        # print("file: {0} directory:{1}".format(file,directory))
        # print("file: {0} directory:{1} file: {0}".format(file,directory))

        print(".", end="")
        d = dict()
        try:
            mp3 = MP3File(file)
        except Exception as e:
            print("Warning: MP3 tag cannot be read from file: {}. Exception: {}".format(file, e))

        mp3.set_version(VERSION_2)  # we just want to get the v2 tags
        if len(mp3.artist) == 0:      # But if v2 tag is empty, let's try v1 tag instead
            mp3.set_version(VERSION_1)
        if isinstance(mp3.artist, str):   # If it's a string we are good...
            d["artist"] = mp3.artist.rstrip()
        else:
            d["artist"] = ""

        mp3.set_version(VERSION_2)  # we just want to get the v2 tags
        if len(mp3.album) == 0:       # But if v2 tag is empty, let's try v1 tag instead
            mp3.set_version(VERSION_1)
        if isinstance(mp3.album, str):   # If it's a string we are good...
            d["album"] = mp3.album.rstrip()
        else:
            d["album"] = ""

        mp3.set_version(VERSION_2)  # we just want to get the v2 tags
        if len(mp3.song) == 0:        # But if v2 tag is empty, let's try v1 tag instead
            mp3.set_version(VERSION_1)
        if isinstance(mp3.song, str):   # If it's a string we are good...
            d["song"] = mp3.song.rstrip()
        else:
            d["song"] = ""

        mp3.set_version(VERSION_2)  # we just want to get the v2 tags
        if len(mp3.band) == 0:        # But if v2 tag is empty, let's try v1 tag instead
            mp3.set_version(VERSION_1)
        if isinstance(mp3.band, str):   # If it's a string we are good...
            d["band"] = mp3.band.rstrip()
        else:
            d["band"] = ""

        # TODO: doublecheck if "folder" is needed at all
        # d["folder"] = directory   # Patrik: It's not required as os.path.basedir(d["filename]) can generate it
        d["filename"] = file

        # TODO: on my raspberry pi there was a problem with UTF-8 coding, but this did not help
        #d2=dict()
        #for key,item in d.items():
        #   d2[key]=item.encode("utf-8")

        songs_list.append(d)
    print("")
    print(json.dumps(songs_list, indent=4, ensure_ascii=False))

    return songs_list


def is_mp3info_consistent(songs_list):
    """
    function:	is_mp3info_consistent
    input:	    list of dictionaries with mp3 tags
    output:	    True if album, band and artist are the same for all songs
                True if list is empty
                False if all band, artist and album tags are empty
                False in other cases
    operation:	takes the list's first element and compares subsequent entries
                if there is a difference returns False
    """
    # if we got an empty list as input, we will return
    if len(songs_list) == 0:
        return True
    # artist_consistent = True
    album_consistent = True
    band_consistent = True
    artist_consistent = True
    first_nonempty_album = False
    first_nonempty_band = False
    first_nonempty_artist = False
    # we will compare each song to the first song
    first_song = songs_list[0]

    for song in songs_list[1:]:     # We don't need to compare the first song to first_song one as well [1:]
        if song["album"] != "":
            first_nonempty_album = True
        if song["band"] != "":
            first_nonempty_band = True
        if song["artist"] != "":
            first_nonempty_artist = True

        if first_song["artist"] != song["artist"]:
            artist_consistent = False
            print("Err: Artist inconsistent")
            break
        if first_song["album"] != song["album"]:
            album_consistent = False
            print("Err: Album inconsistent")
            break
        if first_song["band"] != song["band"]:
            band_consistent = False
            print("Err: Band inconsistent")
            break

    #return ( album_consistent & band_consistent )
    # TODO: not sure what this is below.... Do we need it?
    if not first_nonempty_band:
        print("Band is empty for all songs!")
    if not first_nonempty_album:
        print("Album is empty for all songs!")
    if not first_nonempty_artist:
        print("Artist is empty! for all songs")
    return album_consistent and band_consistent and artist_consistent and first_nonempty_album and \
        first_nonempty_band and first_nonempty_artist


def suggest_mostfrequent_mp3info(songlist):
    """
    function:	suggest_mostfrequent_mp3info
    input:	    list of mp3 objects - songlist
    output:	    band, album, artist tuple
    operation:	looks into the mp3 objects, and calculates the
                most frequent band and album string
                returns band, album
    """
    albumlist = list()
    bandlist = list()
    artistlist = list()
    for song in songlist:
        albumlist.append(song["album"])
        bandlist.append(song["band"])
        artistlist.append(song["artist"])

    track = {}
    for value in albumlist:
        if( value == [] or (value is None) ):
            value = "empty"
        if value not in track:
            track[value] = 0
        else:
            track[value] += 1
    retvalalbum=max(track, key=track.get)
    retvalalbumqty=track[retvalalbum]

    track = {}
    for value in bandlist:
        if (value == [] or (value is None)):
            value = "empty"
        if value not in track:
            track[value] = 0
        else:
            track[value] += 1
    retvalband = max(track, key=track.get)
    retvalbandqty = track[retvalband]

    track = {}
    for value in artistlist:
        if (value == [] or(value is None)):
            value = "empty"
        if value not in track:
            track[value] = 0
        else:
            track[value] += 1
    retvalartist = max(track, key=track.get)
    retvalartistqty = track[retvalartist]

#TODO: If band is empty propose artist as band
#TODO: If all_artist is only once: propose keep to keep them

    print("Most frequent band: ", end="")
    print(retvalband, retvalbandqty)
    print("Most frequent album: ", end="")
    print(retvalalbum,retvalalbumqty)
    print("Most frequent artist: ", end="")
    print(retvalartist, retvalartistqty)

    return retvalband,retvalalbum,retvalartist


def update_mp3info(songlist, requiredtag):
    """
    function:	update_mp3info
    input:	    songlist a directory of mp3 tags, dictionary of required mp3
    output:
    operation:	writes mp3tags into each song, if tag == keep keeps tag (artist only)
    future:     updates processed dir logfile
    """

    # TODO: add album cover!

    print("Function: update_mp3info")
    #print(dir),
    #print(fileList),
    for song in songlist:
        needtosave=False
        if( song["album"] != requiredtag["album"]):
            needtosave=True
        if( song["band"] != requiredtag["band"]):
            needtosave=True
        if (song["song"] == ""):
            needtosave=True
        if( song["artist"] != requiredtag["artist"] and requiredtag["artist"] != "keep" ):
            needtosave=True
        if (needtosave==True):
            try:
                mp3 = MP3File(song["filename"])
                mp3.set_version(VERSION_BOTH)
                mp3.band=requiredtag["band"]
                mp3.album=requiredtag["album"]
                if song["song"] == "":
                    # My TC friend is totally bored sometimes somewhere so he learns stuff like [:-4]
                    mp3.song = os.path.basename(song["filename"])[:-4]
                if (requiredtag["artist"] != "keep"):
                    mp3.artist=requiredtag["artist"]
                #print('Writing tags to %s' % song["filename"] )
                mp3.save()
            except Exception as e:
                print("Warning: MP3 tag cannot be saved for file: {}. Exception: {}".format(song["filename"], e))
            else:
                #TODO: update processed.log as directory now consistent
                print("Info: MP3 tag updated for file: {}".format(song["filename"]))


def writelogfile(str):
    try:
        with open(PROCESSED_DIR_FILE, "a") as f:
            f.write(str)
    except IOError:
        print("Processed directories log file: {} cannot be opened.".format(PROCESSED_DIR_FILE))


def walkdir(dir):
    """
    function:	walkdir
    input:	    foldername
    output:	    none
    operation:	recureseivly walks through the directories
                tries to collect mp3 info in each dir
                checks mp3 info per directroy
    future changes:   make it non-recursive?
    """
    for dirName, subdirList, fileList in os.walk(dir):
        print('\nArrived in directory: %s' % dirName)
        songlist = collect_mp3info(dirName)

        # songlist maybe empty, in this case we skip info check
        if( len(songlist) > 0):
            if( is_mp3info_consistent(songlist)== False):
                print("Album is INCONSISTENT")
                if( update_mp3data == 1):
                    suggestedband,suggestedalbum,suggestedartist=suggest_mostfrequent_mp3info(songlist)
                    print("Suggested band: " + suggestedband + "\tSuggested album: " + suggestedalbum + "\tSuggested artist: " + suggestedartist)
                    accept = input("Accept suggested (Y/n/q)?")
                    if accept.lower() == 'n':
                        suggestedband = input("Enter new band: %s " % suggestedband) or suggestedband
                        suggestedalbum = input("Enter new album: %s " % suggestedalbum) or suggestedalbum
                        suggestedartist = input("Enter new artist (or keep or blank) %s" % suggestedartist) or suggestedartist
                        print("New values: Suggested band: " + suggestedband + "\tSuggested album: " + suggestedalbum + "\tSuggested artist: " + suggestedartist)
                    if accept.lower() == 'q':
                        exit(2)
                    d = dict ()
                    d["band"] = suggestedband
                    d["album"] = suggestedalbum
                    d["artist"] = suggestedartist
                    update_mp3info(songlist,d)
                if( report_inconsistent_directories == 1):
                    writelogfile("Inconsistent:" + dirName + "\n")

            else:
                print("Album seems to be OK")
                writelogfile("Consistent:" + dirName + "\n")
        if( len(subdirList) == 0):
            print("No subdirs")
        else:
            for dname in subdirList:
                print("Going to: {}".format(dname))
                walkdir(dname)
        print("Directroy processed: {}".format(dirName))


if __name__ == "__main__":
    # walkdir(PATH)
    song_list = collect_mp3info("C:\\tmp\\Music\\Parno Graszt\\Rávágok a zongorára")
    print(is_mp3info_consistent(song_list))
