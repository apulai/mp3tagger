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
report_inconsisent_directories = 1
update_mp3data = 1

# TODO: sync v1 and v2 tags


def collect_mp3info(dir):
    """
    function:	collect-mp3info
    input:	    foldername
    output:	    list of dictionaries containing mp3 tags per song
    operation:	opens each mp3 files, and extracts mp3 info into a list of dictionaries.
                might return an empty list

    """
    print("Function: collect_mp3info")
    return_value = list()
    file_list = glob.glob(dir+"/*"+EXTENSION, recursive=False)
    # print(dir),
    # print(file_list),
    for file in file_list:
        # print("file:", file)
        # print("file: " + file)
        # print("file: {} dir:{}".format(file,dir))
        # print("file: {0} dir:{1}".format(file,dir))
        # print("file: {0} dir:{1} file: {0}".format(file,dir))

        print(".", end="")
        d = dict()
        try:
            mp3 = MP3File(file)

            mp3.set_version(VERSION_2)  # we just want to get the v2 tags
            if(mp3.artist == []):      # But if v2 tag is empty, let's try v1 tag instead
                mp3.set_version(VERSION_1)

            # TODO: replace empty to ""
            if(mp3.artist is not None):#Sometimes valuetype was NoneType, this checks for it
                d["artist"] = mp3.artist.rstrip()
            else:
                d["artist"] = "empty"

            mp3.set_version(VERSION_2)  # we just want to get the v2 tags
            if (mp3.album == []):       # But if v2 tag is empty, let's try v1 tag instead
                mp3.set_version(VERSION_1)

            if (mp3.album is not None):#Sometimes valuetype was NoneType, this checks for it
                d["album"] = mp3.album.rstrip()
            else:
                d["album"] = "empty"

            mp3.set_version(VERSION_2)  # we just want to get the v2 tags
            if (mp3.song == []):        # But if v2 tag is empty, let's try v1 tag instead
                mp3.set_version(VERSION_1)

            if (mp3.song is not None): #Sometimes valuetype was NoneType, this checks for it
                d["song"] = mp3.song.rstrip()
            else:
                d["song"] = "empty"

            mp3.set_version(VERSION_2)  # we just want to get the v2 tags
            if (mp3.band == []):        # But if v2 tag is empty, let's try v1 tag instead
                mp3.set_version(VERSION_1)

            if (mp3.band is not None): #Sometimes valuetype was NoneType, this checks for it
                d["band"] = mp3.band.rstrip()
            else:
                d["band"] = "empty"

            #TODO: doublecheck if "folder" is needed at all
            d["folder"] = dir
            d["filename"] = file

            #TODO: on my raspberry pi there was a problem with UTF-8 coding, but this did not help
            #d2=dict()
            #for key,item in d.items():
            #   d2[key]=item.encode("utf-8")

            return_value.append(d)
        except Exception as e:
            print("Warning: MP3 tag cannot be read from file: {}. Exception: {}".format(file, e))
    print ("")

    for song in return_value:
        # TODO: Patrik to make it UTF-8 ready!!!
        print(json.dumps(song, indent=4))
        print (song)

    #print (return_value)
    return return_value

def is_mp3info_consistent(mp3taglist):
    """
    function:	is_mp3info_consistent
    input:	    list of dictionaries with mp3 tags
    output:	    True if album, band and artist is the same
                True if list is empty
                False if all band, artist and album tag is empty
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
    artist_consistent=True
    first_nonempty_album=False
    first_nonempty_band=False
    first_nonempty_artist=False
    # we will compare each song to the first song
    firstsong=mp3taglist[0]

    for song in mp3taglist:
        if ( song["album"] != ""):
            first_nonempty_album = True
        if ( song["band"] != []):
            first_nonempty_band = True
        if (song["artist"] != []):
            first_nonempty_artist = True

        if( firstsong["artist"] != song["artist"]):
            artist_consistent = False
            print("Err: Artist inconsistent")
            break
        if( firstsong["album"] != song["album"]):
            album_consistent = False
            print("Err: Album inconsistent")
            break
        if (firstsong["band"] != song["band"]):
            band_consistent = False
            print("Err: Band inconsistent")
            break
        if (firstsong["artist"] != song["artist"]):
            artist_consistent_consistent = False
            print("Err: Artist inconsistent")
            break

    #return ( album_consistent & band_consistent )
    if( first_nonempty_band == False ):
        print("Band is empty!")
    if (first_nonempty_album == False):
        print("Album is empty!")
    if (first_nonempty_artist == False):
        print("Artist is empty!")
    return ( album_consistent & band_consistent & artist_consistent & first_nonempty_album & first_nonempty_band & first_nonempty_artist)

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

    #TODO: add album cover!

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
                # TODO: do not insert the full filename if empty, only the part before the mp3 (Patrik)
                if (song["song"] == ""):
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
                if( report_inconsisent_directories == 1):
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
    walkdir(PATH)
    #collect_mp3info("D:\\temp\\mp3\\Alma Együttes - Bio (2006)")
