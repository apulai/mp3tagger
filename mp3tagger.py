# Requires Python 3.5+
# Requires mp3-tagger library ("pip3 install mp3-tagger" or download from here: https://pypi.org/project/mp3-tagger/)

import os
import glob

from mp3_tagger import MP3File
from mp3_tagger.id3 import VERSION_2, VERSION_BOTH

#PATH = "/home/apulai/mp3"
#PATH = "Z:\\"
#PATH = "Z:\\Greatest Hits of the 80's 8CD 320KB 2Lions-Team\\Greatest Hits Of The 80's CD6"
#PATH = "c:\\test"
PATH="Z:\\juca"

EXTENSION = ".mp3"
PROCESSED_DIR_FILE = PATH + "/processed.log"


rootDir = PATH

def collect_mp3info(dir):
    """
    function:	collect-mp3info
    input:	    foldername
    output:	    list of dictionaries containing mp3 tags per song
    operation:	opens each mp3 files, and extracts mp3 info into a list of dictionaries.
                might retrun an empty list

    """
    retval = list();
    fileList = glob.glob(dir+"/*"+EXTENSION, recursive=False)
    print("collect_mp3info")
    #print(dir),
    #print(fileList),
    for file in fileList:
        print('file %s' % file)
        print(".",end=""),
        d = dict()
        mp3 = MP3File(file)
        mp3.set_version(VERSION_2)  # we just want to get the v2 tags
        d["artist"]=mp3.artist
        d["album"]=mp3.album
        d["song"]=mp3.song
        d["band"]=mp3.band
        d["folder"]=dir
        d["filename"]=file
        retval.append(d)
    print ("")
    print (retval)
    return retval

def is_mp3info_consistent(mp3taglist):
    """
    function:	is_mp3info_consistent
    input:	    list of dictionaries with mp3 tags
    output:	    True if album and band is the same
                True if list is empty
                False in other cases
    operation:	takes the list's first element and compares subsequent entries
                if there is a difference returns False
    """
    # if we got an empty list as input, we will return
    if( len(mp3taglist) == 0):
        return True
    #artist_consistent=True
    album_consistent=True
    band_consistent=True
    # we will compare each song to the first song
    firstsong=mp3taglist[0]

    for song in mp3taglist:
        #if( firstsong["artist"] != song["artist"]):
        #    artist_consistent=False
        #    print("Err: Artist inconsistent")
        #    break
        if( firstsong["album"] != song["album"]):
            album_consistent=False
            print("Err: Album inconsistent")
            break
        if (firstsong["band"] != song["band"]):
            band_consistent = False
            print("Err: Band inconsistent")
            break

    return ( album_consistent & band_consistent )

def suggest_mostfrequent_mp3info(songlist):
    """
    function:	suggest_mostfrequent_mp3info
    input:	    list of mp3 objects - songlist
    output:	    band and album tuple
    operation:	looks into the mp3 objects, and calculates the
                most frequent band and album string
                returns band, album
    """
    albumlist = list()
    bandlist = list()
    for song in songlist:
        albumlist.append(song["album"])
        bandlist.append(song["band"])

    track = {}
    for value in albumlist:
        if( value == [] ):
            value = "empty"
        if value not in track:
            track[value] = 0
        else:
            track[value] += 1
    retvalalbum=max(track, key=track.get)

    track = {}
    for value in bandlist:
        if (value == []):
            value = "empty"
        if value not in track:
            track[value] = 0
        else:
            track[value] += 1

    retvalband = max(track, key=track.get)
    print("Most frequent band: ", end="")
    print(retvalband, end="")
    print("\tMost frequent album: ", end="")
    print(retvalalbum)
    return retvalband,retvalalbum

def update_mp3info(songlist, requiredtag):
    """
    function:	update_mp3info
    input:	    songlist a directory of mp3 tags, dictionary of required mp3
    output:
    operation:	writes mp3tags into each song
    future:     updates processed dir logfile
    """
    print("update_mp3info")
    #print(dir),
    #print(fileList),
    for song in songlist:
        needtosave=False;
        if( song["album"] != requiredtag["album"]):
            needtosave=True
        if( song["band"] != requiredtag["band"]):
            needtosave=True
        if (song["song"] == ""):
            needtosave=True
        if (needtosave==True):
            mp3 = MP3File(song["filename"])
            mp3.set_version(VERSION_BOTH)
            mp3.band=requiredtag["band"]
            mp3.album=requiredtag["album"]
            if (song["song"] == ""):
                mp3.song = file
            print('Writing tags to %s' % song["filename"] )
            mp3.save()


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
                suggestedband,suggestedalbum=suggest_mostfrequent_mp3info(songlist)
                print("Suggested band: " + suggestedband + "\tSuggested album: " + suggestedalbum)
                accept = input("Accept suggested (Y/n/q)?")
                if accept.lower() == 'n':
                    suggestedband = input("Enter new band: %s " % suggestedband) or suggestedband
                    suggestedalbum = input("Enter new album: %s " % suggestedalbum) or suggestedalbum
                    print("New values: Suggested band: " + suggestedband + "\tSuggested album: " + suggestedalbum)
                if accept.lower() == 'q':
                    exit(2)
                d = dict ()
                d["band"] = suggestedband
                d["album"] = suggestedalbum
                update_mp3info(songlist,d)
            else:
                print("Album seems to be OK")
        if( len(subdirList) == 0):
            print("No subdirs")
        else:
            for dname in subdirList:
                print("Going to: %s" % dname)
                walkdir(dname)
        print("Directroy processed: " + dirName)


walkdir(PATH)



