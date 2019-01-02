# Requires Python 3.5+
# Requires mp3-tagger library ("pip3 install mp3-tagger" or download from here: https://pypi.org/project/mp3-tagger/)
# nem kell -*- coding:Utf-8 -*-

import os
import glob
import json
import sys
import getopt
from mp3_tagger import MP3File
from mp3_tagger.id3 import VERSION_2, VERSION_BOTH, VERSION_1


#PATH = "/home/apulai/mp3"
#PATH = "Z:\\"
#PATH = "c:\\test"
#PATH="Z:\\juca"
#PATH="Z:\\mp3\\shrek"
#PATH="Z:\\mp3\\_Magyar"
#PATH="D:\\temp"
#PATH="Z:\\mp3\\_Latin"
#PATH="Z:\\mp3\\_Country"
#PATH="Z:\\mp3\\_Disco"
#PATH="Z:\\mp3\\_Folk"
#PATH="Z:\\mp3\\_Gyerek"
#PATH="Z:\\mp3\\_Hangoskonyv"
#PATH="Z:\\mp3\\_Jazz\\Take Five"
PATH="Z:\\mp3\\_Magyar\\Valami Amerika"
#PATH="Z:\\mp3\\_Pop\\Boney M - The Magic Of Boney M"
#PATH="Z:\mp3\_Magyar\István a király"
#PATH="Z:\\mp3\\_Vegyes"
#PATH="Z:\\mp3\\_Jazz\\Smooth Africa"
#PATH="Z:\\mp3\\_Rock"
#PATH="Z:\\mp3\\_Country"
#PATH="/mnt/backupdsk/mp3/_Magyar"

# We will look for these extensions
LIST_OF_EXTENSIONS = ".mp3", ".MP3"

# In some of the tags there were very strange chars
# We want them to be removed
BAD_CHARS = " \n\x00\r\ufeff"

# Pseudo done: TODO: Skip only those directories which were marked as consistent in the processed.log file (likely load proccessed log before run
# We log error message and then the directory name

# Pseudo done: TODO: Log somehow if mp3 file had only v1 tags
# Folder is logged


#LOGFILE_NAME = "uxprocessed.log"
LOGFILE_NAME = "processed.log"
#PROCESSED_DIR_FILE = PATH + "/uxprocessed.log"
PROCESSED_DIR_FILE = PATH + "/" + LOGFILE_NAME

rootDir = PATH
report_inconsistent_directories = 1
update_mp3data = 1

def collect_mp3info(directory):
    """
    function:	collect-mp3info
    input:	    foldername
    output:	    list of dictionaries containing mp3 tags per song
    operation:	opens each mp3 files, and extracts mp3 info into a list of dictionaries.
                might return an empty list

    """
    print("Function: collect_mp3info Directory {}".format(directory))
    songs_list = list()
    file_list = list()
    for extension in LIST_OF_EXTENSIONS:
            temp_list = glob.glob(directory + "/*" + extension, recursive=False)
            # Do not append a list to a list...
            file_list = file_list + temp_list

    #Since on windows .mp3 and .MP3 is not different
    #Make this list uniq again

    temp_list = file_list

    file_list = list()
    for x in temp_list:
        if x not in file_list:
            file_list.append(x)

    #extension = ".mp3"
    #file_list = glob.glob(directory + "/*" + extension, recursive=False)

    # print(directory),
    #print(file_list),

    for file in file_list:
        # print("file:", file)
        # print("file: " + file)
        # print("file: {} directory:{}".format(file,directory))
        # print("file: {0} directory:{1}".format(file,directory))
        # print("file: {0} directory:{1} file: {0}".format(file,directory))

        print(".", end="")
        d = dict()
        try:
            d["hasbadchars"] = False

            mp3 = MP3File(file)
            mp3.set_version(VERSION_2)  # we just want to get the v2 tags
            d["tagversion"]="v1"        # We hope tags will be v2, but let's set the worst case for us which is v1, if no v2 tags we will assume all was v1 and will not write

            if isinstance(mp3.artist, str):     # If it's a string we are good...
                if len(mp3.artist) == 0:        # But if v2 tag is empty, let's try v1 tag instead
                    mp3.set_version(VERSION_1)  # So there was a non-zero v2 tag
                else:
                    d["tagversion"] = "v2"
                d["artist"] = mp3.artist.rstrip()
            else:
                d["artist"] = ""

            mp3.set_version(VERSION_2)          # we just want to get the v2 tags
            if isinstance(mp3.album, str):      # If it's a string we are good...
                if len(mp3.album) == 0:         # But if v2 tag is empty, let's try v1 tag instead
                    mp3.set_version(VERSION_1)
                else:
                    d["tagversion"] = "v2"      # So there was a non-zero v2 tag
                d["album"] = mp3.album.rstrip()
            else:
                d["album"] = ""

            mp3.set_version(VERSION_2)          # we just want to get the v2 tags
            if isinstance(mp3.song, str):       # If it's a string we are good...
                if len(mp3.song) == 0:          # But if v2 tag is empty, let's try v1 tag instead
                    mp3.set_version(VERSION_1)
                else:
                    d["tagversion"] = "v2"      # So there was a non-zero v2 tag
                d["song"] = mp3.song.rstrip()
            else:
                d["song"] = ""

            mp3.set_version(VERSION_2)          # we just want to get the v2 tags
            if isinstance(mp3.band, str):       # If it's a string we are good...
                if len(mp3.band) == 0:          # But if v2 tag is empty, let's try v1 tag instead
                    mp3.set_version(VERSION_1)
                else:
                    d["tagversion"] = "v2"      # So there was a non-zero v2 tag
                d["band"] = mp3.band.rstrip()
            else:
                d["band"] = ""

            d["filename"] = file

            songs_list.append(d)
        except Exception as e:
            print("Warning: MP3 tag cannot be read from file: {}. Exception: {}".format(file, e))
            writelogfile("ERR MP3:" + format(file) + "\n")
    print("")
    print(json.dumps(songs_list, indent=4, ensure_ascii=False))

    return songs_list

def remove_bad_chars(song_list):
    """
        function:	remove_bad_chars
        input:	    song_list
        output:	    corrected song list
        operation:	Walks so a song_list collected by collect_mp3info
                    Tries to remove bad chars we have seen mostly on windows
        """
    ret_list = list()
    for song in song_list:
        ret_song = dict()

        ret_song["hasbadchars"]=False

        ret_song["artist"] = song["artist"].rstrip(BAD_CHARS)
        if (ret_song["artist"] != song["artist"]):
            ret_song["hasbadchars"] = True

        ret_song["album"] = song["album"].rstrip(BAD_CHARS)
        if (ret_song["album"] != song["album"]):
            ret_song["hasbadchars"] = True

        ret_song["song"] = song["song"].rstrip(BAD_CHARS)
        if (ret_song["song"] != song["song"]):
            ret_song["hasbadchars"] = True

        ret_song["band"] = song["band"].rstrip(BAD_CHARS)
        if (ret_song["band"] != song["band"]):
            ret_song["hasbadchars"] = True

        ret_song["tagversion"]=song["tagversion"]
        ret_song["filename"] = song["filename"]
        ret_list.append(ret_song)

    return ret_list

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

    for song in songs_list:
        # We don't need to compare the first song to first_song one as well [1:] We can use 1: like operators on lists
        # But this is wrong what if we have only 1 song?!
        if song["album"] != "":
            first_nonempty_album = True
        if song["band"] != "":
            first_nonempty_band = True
        if song["artist"] != "":
            first_nonempty_artist = True

        if first_song["artist"] != song["artist"]:
            artist_consistent = False
            print("Suspect: Artist inconsistent")
            break
        if first_song["album"] != song["album"]:
            album_consistent = False
            print("Err: Album inconsistent")
            break
        if first_song["band"] != song["band"]:
            band_consistent = False
            print("Err: Band inconsistent")
            break

    # Not all artist was the same
    # We can correct it if band is consistent and album is consistent
    # And all artist is different then we are still OK

    if( artist_consistent == False):
        print("Double check artist consistency, if album and band is consitent, and no empty artists are then OK")
        if ( band_consistent == True and album_consistent == True):
            totalnumberofsongs = len(songs_list)
            artistlist = list()
            for song in songs_list:  # We need to generate the list of artists
                artistlist.append(song["artist"])
            track = {}
            for value in artistlist:
                if (value == [] or (value is None)):
                    value = "empty"
                if value not in track:
                    track[value] = 1
                else:
                    track[value] += 1
            numberofdifferentartists = len(track)
            #if ( float(numberofdifferentartists)/float(totalnumberofsongs)==1.0):
            if( "empty" not in artistlist):
                artist_consistent = True
                print("Doublecheck: artist is OK, since no empty artist while band and album is consistent")

            else:
                print("Double check: artist is really not OK")

    if not first_nonempty_band:
        print("Band is empty for all songs!")
    if not first_nonempty_album:
        print("Album is empty for all songs!")
    if not first_nonempty_artist:
        print("Artist is empty for all songs!")
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

    # If we get no data let's return
    totalnumberofsongs = len(songlist)
    if totalnumberofsongs == 0:
        return "empty", "empty", "empty"

    albumlist = list()
    bandlist = list()
    artistlist = list()
    for song in songlist:                   # Create 3 separate list of attributes so we can work with them easier
        albumlist.append(song["album"])
        bandlist.append(song["band"])
        artistlist.append(song["artist"])

    # Start work on list of albums, calculate most ferquent album name
    track = {}
    for value in albumlist:
        if( value == [] or (value is None) ): # sometimes we got NoneVaule, likely this won't happen anymore, but we still check
            value = "empty"
        if value not in track:
            track[value] = 1
        else:
            track[value] += 1
    retvalalbum=max(track, key=track.get)     # sometimes we got NoneVaule, likely this won't happen anymore, but we still check
    retvalalbumqty=track[retvalalbum]
    calculatedalbum=retvalalbum
    calculatedalbumqty=retvalalbumqty

    # Start work on list of artits, calculate most ferquent artist name
    track = {}
    for value in artistlist:
        if (value == [] or(value is None)):
            value = "empty"
        if value not in track:
            track[value] = 1
        else:
            track[value] += 1

    # We will select here the most frequent artist
    calculatedartist = max(track, key=track.get)
    retvalartist = calculatedartist
    calculatedartistqty = track[calculatedartist]
    retvalartistqty = calculatedartistqty
    totalnumberofdifferentartist=len(track)


    # But If all song has an artist we will propose keep instead
    if ("" not in artistlist):
        retvalartist = "keep"

    # Start work on list of band, calculate most ferquent band name
    track = {}
    for value in bandlist:
        if (value == "" or (value is None)):
            value = "empty"
        if value not in track:
            track[value] = 1
        else:
            track[value] += 1
    retvalband = max(track, key=track.get)
    retvalbandqty = track[retvalband]
    calculatedband=retvalband
    calculatedbandqty=retvalbandqty

#If band is empty propose artist as band
    if retvalband == "empty" :
            # If the most frequent artist is present in more than 15% of the songs
            # and the band is empty let's propose artist as the band
            if float(calculatedartistqty)/float(totalnumberofsongs) >= 0.15:
                retvalband = calculatedartist



    print("Total number of songs in this folder:\t{}".format(totalnumberofsongs))

    print("Most frequent band:\t{} \tnumber of occurances: {} .".format(calculatedband, calculatedbandqty))
    print("Most frequent album:\t{} \tnumber of occurances: {} .".format(calculatedalbum, calculatedalbumqty))
    print("Most frequent artist:\t{} \tnumber of occurances: {} . ".format(calculatedartist, calculatedartistqty))

    print("Returning proposal for band:\t{} \tnumber of occurances: {} .".format(retvalband,retvalbandqty))
    print("Returning proposal for album:\t{} \tnumber of occurances: {} .".format(retvalalbum,retvalalbumqty))
    print("Returning proposal for artist:\t{} \tnumber of occurances: {} . ".format(retvalartist, retvalartistqty))

    return retvalband,retvalalbum,retvalartist


def update_mp3info(songlist, requiredtag, write_v1_tags=False):
    """
    function:	update_mp3info
    input:	    songlist a directory of mp3 tags, dictionary of required mp3, write_v1_tags by default false
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

        if( song["tagversion"]=="v1" and write_v1_tags == False):
            # ISSUE: mp3tagger seems not to handle corrctly if there is no tag or only v1 tags
            needtosave = False
            print("WARNING: Song with V1 tags only: {}".format(song["filename"]))
            #writelogfile("Log: only V1 tag excpetion: {}".format(song["filename"]))

        if needtosave==True :
            try:
                mp3 = MP3File(song["filename"])
                mp3.set_version(VERSION_BOTH)
                mp3.band = requiredtag["band"].rstrip(BAD_CHARS)
                mp3.album = requiredtag["album"].rstrip(BAD_CHARS)
                if song["song"] == "":
                    # My TC friend is totally bored sometimes somewhere so he learns stuff like [:-4]
                    mp3.song = os.path.basename(song["filename"])[:-4]
                    mp3.song = mp3.song.rstrip(BAD_CHARS)
                if (requiredtag["artist"] != "keep"):
                    mp3.artist = requiredtag["artist"].rstrip(BAD_CHARS)
                #print('Writing tags to %s' % song["filename"] )
                mp3.save()
            except Exception as e:
                print("Warning: MP3 tag cannot be saved for file: {}. Exception: {}".format(song["filename"], e))
                writelogfile("Log: Warning: MP3 tag cannot be saved for file:" + format(song["filename"])+ format(e))
            else:
                print("Info: MP3 tag updated for file: {}".format(song["filename"]))

def rewrite_songs_with_bad_chars(songlist):
    """
        function:	rewrite_songs_with_bad_chars
        input:	    songlist a directory of mp3 tags
        output:
        operation:	writes mp3tags and rstrips again
        """
    for song in songlist:
        try:
                if song["hasbadchars"] == True and song["tagversion"] == "v2":
                    try:
                        mp3 = MP3File(song["filename"])
                        mp3.set_version(VERSION_BOTH)
                        del mp3.band
                        mp3.band = song["band"].rstrip(BAD_CHARS)

                        del mp3.album
                        mp3.album = song["album"].rstrip(BAD_CHARS)

                        del mp3.song
                        mp3.song = song["song"].rstrip(BAD_CHARS)

                        del mp3.artist
                        mp3.artist = song["artist"].rstrip(BAD_CHARS)

                        mp3.save()
                    except Exception as e:
                        print(
                            "Warning: MP3 tag cannot be saved for file: {}. Exception: {}".format(song["filename"], e))
                        writelogfile(
                            "Log: Warning: MP3 tag cannot be saved for file:" + format(song["filename"]) + format(e))
                    else:
                        print("Info: MP3 badchars removed for file: {}".format(song["filename"]))
                elif song["tagversion"] == "v1":
                    writelogfile(
                        "ERR V1 BADCHAR: MP3 tag cannot be saved for file:" + format(song["filename"]) + format(e))
        except NameError:
            print("Info no bad chars, or not checked")
    return


def writelogfile(str):
    try:
        with open(PROCESSED_DIR_FILE, "a") as f:
            f.write(str)
    except IOError:
        print("Processed directories log file: {} cannot be opened.".format(PROCESSED_DIR_FILE))


def walkdir_OBSOLETE(dir):
    """
    function:	walkdir - OBSOLETE
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
                walkdir_OBSOLETE(dname)
        print("Directroy processed: {}".format(dirName))

def v1_tags_present(song_list):
    # Walk through the tags and check if any of them is v1
    # if v1 we return true
    for song in song_list:
        if song["tagversion"] == "v1":
            return True
    return False


def process_dir(current_directory):
    """
    function:	process_dir
    input:	    foldername
    output:	    0 if directory is updated
                1 if directory is not updated
                2 if directory has v1 tags and it is not updated
    operation:	generates list of songs in current directory
                collects mp3info
                processes mp3info
    """

    song_list=collect_mp3info(current_directory)
    if (len(song_list) > 0):
        # If there are v1 tags present we will log only an error for this directory
        if (v1_tags_present(song_list) == True ):
            print("Album has songs with v1 tags only, not safe to process")
            return 2
        if (is_mp3info_consistent(song_list) == False):
            print(json.dumps(song_list, indent=4, ensure_ascii=False))
            print("Album is inconsistent")
            if (update_mp3data == 1):
                # Try to analyze the collected info, and come back with suggestions
                suggestedband, suggestedalbum, suggestedartist = suggest_mostfrequent_mp3info(song_list)
                # Ask for user input
                print("Suggested band: " + suggestedband + "\tSuggested album: " + suggestedalbum + "\tSuggested artist: " + suggestedartist)
                accept = input("Accept suggested (Y/n/q/(s)kip)?")
                if accept.lower() == 'n':
                    suggestedband = input("Enter new band: %s " % suggestedband) or suggestedband
                    suggestedalbum = input("Enter new album: %s " % suggestedalbum) or suggestedalbum
                    suggestedartist = input(
                        "Enter new artist (or keep to keep) %s" % suggestedartist) or suggestedartist
                    print(
                        "New values: Suggested band: " + suggestedband + "\tSuggested album: " + suggestedalbum + "\tSuggested artist: " + suggestedartist)
                if accept.lower() == 'q':
                    exit(2)
                if accept.lower() != 's':
                    d = dict()
                    d["band"] = suggestedband
                    d["album"] = suggestedalbum
                    d["artist"] = suggestedartist
                    update_mp3info(song_list, d)
                else:
                    print ("Skipping this directory")
                    return 1
        else:
            print("Album is consistent")


    return 0


def walkdir(dir):
    """
        function:	walk
        input:	    root folder name
        output:	    none
        operation:	generates list of directories
                    processes each unprocessed directory
                    logs processed directories
        """

    # List all directories
    directories = glob.glob(PATH + '/**/*/', recursive=True)

    #Debug if all directories are listed
    #i = 1
    #for p in directories:
    #    print("{} {}".format(i,p))
    #    i=i+1
    #exit(1)

    # Add current directory
    directories.append(dir)

    number_of_directories_found = len(directories)
    print("Found {} directories to scan".format(number_of_directories_found))

    # We will skip processed directories
    # Therefore we try to load the list of processed directories
    try:
        with open(PROCESSED_DIR_FILE) as f:
            processed_dirs = f.read().splitlines()
    except IOError:
        print("Processed directories log file: {} cannot be opened.".format(PROCESSED_DIR_FILE))
        processed_dirs = []
    # print(processed_dirs)
    # Logfile of processed directories are now loaded

    current_directory = ''
    first_file = True
    first_file_in_dir = True
    new = {}
    for current_directory in directories:
            # We will check in this list if our current directory was alread processed:
            if current_directory not in processed_dirs:
                # If our current directory was not already processed we will process it.
                # We will collect and update mp3 info in to following call:
                #print("Processing dir: {}".format(current_directory))
                retval = process_dir(current_directory)

                # Process_dir will return different error codes for different problems
                # Let's check them 1 by 1
                if retval == 0:
                    # If we managed to refresh this directory,
                    # we log it as updated
                    processed_dirs.append(current_directory)
                    writelogfile(current_directory + '\n')
                elif retval == 1:
                    print("Directory was skipped / not processed")
                    #We are adding some easy to grep error in the log
                    #This will also invalidate the directory when we will load the processed.log file
                    #next time we run this tool (there is likely no Skip: driectory when listing the contents)
                    writelogfile("Skip:" + current_directory + '\n')
                else:
                    # We are adding some easy to grep error in the log
                    # This will also invalidate the directory when we will load the processed.log file
                    # next time we run this tool (there is likely no Skip: driectory when listing the contents)
                    print("Directory had V1 only tags")
                    writelogfile("ERR V1:" + current_directory + '\n')
            else:
                print("Directory: {} was already processed.".format(current_directory))
            number_of_directories_found = number_of_directories_found - 1;
            print("Number of directories to go {}".format(number_of_directories_found))
    print("Walk complete. Remeber to check logfile for errors, like folders with v1 tags only.")

#TODO: if no arguments, then use current folder as path
def main(argv):
    global PATH
    global PROCESSED_DIR_FILE
    global LOGFILE_NAME

    try:
        PATH
    except NameError:
        print("PATH is not defined, we will use current directory")
        PATH = os.getcwd()
    else:
        print("PATH is defined in the script body")


    try:
        opts, args = getopt.getopt(argv, "hp:l:",["path=","log="])
    except getopt.GetoptError:
        print('mp3tagger.py -p <path> -l <logfiledir>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('mp3tagger.py -p <path> -l <logfiledir>')
            sys.exit()
        elif opt in ("-p", "--path"):
            PATH = arg
        elif opt in ("-l", "--logdir"):
            LOGFILE_NAME = arg

        PROCESSED_DIR_FILE = PATH + "/" + LOGFILE_NAME

    print("Path {} Logdir {} Concat {}".format(PATH,LOGFILE_NAME,PROCESSED_DIR_FILE))
    walkdir(PATH)

if __name__ == "__main__":
    main(sys.argv[1:])

    exit(0)
    #songlist = collect_mp3info("Z:\\mp3\\_Magyar\\István a király\\Cd1")
    songlist = collect_mp3info("D:\\temp\\mp3\\Valami Amerika")
    suggestedband, suggestedalbum, suggestedartist = suggest_mostfrequent_mp3info(songlist)
    print("Suggested band: " + suggestedband + "\tSuggested album: " + suggestedalbum + "\tSuggested artist: " + suggestedartist)
    requiredtag = dict()
    requiredtag["artist"]="ARTISTA"
    requiredtag["album"]="ALBUMM"
    requiredtag["band"]="Banda"
    update_mp3info(songlist, requiredtag)
    rewrite_songs_with_bad_chars(songlist)
