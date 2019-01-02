import mp3tagger
import glob
import json

#PATH = "Z:\\mp3\\_Magyar\\Valami Amerika"
# PATH="/mnt/backupdsk/mp3/_Magyar""
#PATH="/mnt/backupdsk/mp3/_Rock/ACDC Best of"
PATH="/mnt/backupdsk/mp3/_Rock/Jethro_Tull"


directories = glob.glob(PATH + '/**/*/', recursive=True)

# Add current directory
directories.append(dir)

number_of_directories_found = len(directories)
print("Found {} directories to scan".format(number_of_directories_found))

for current_directory in directories:
    song_list = mp3tagger.collect_mp3info(current_directory)
    ret_song_list = mp3tagger.remove_bad_chars(song_list)
    print( json.dumps(ret_song_list, indent=4, ensure_ascii=False))
    mp3tagger.rewrite_songs_with_bad_chars(ret_song_list)
    number_of_directories_found = number_of_directories_found - 1;
    print("Number of directories to go {}".format(number_of_directories_found))
print("Walk complete. Remeber to check logfile for errors, like folders with v1 tags only.")
