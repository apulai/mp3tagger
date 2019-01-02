import mp3tagger

PATH = "PATH="
Z:\\mp3\\_Magyar\\Valami
Amerika
"
# PATH="/mnt/backupdsk/mp3/_Magyar""


directories = glob.glob(PATH + '/**/*/', recursive=True)

# Add current directory
directories.append(dir)

number_of_directories_found = len(directories)
print("Found {} directories to scan".format(number_of_directories_found))

for current_directory in directories:
    song_list = mp3tagger.collect_mp3info(PATH)
    ret_song_list = mp3tagger.remove_bad_chars(song_list)
    mp3tagger.rewrite_songs_with_bad_chars(ret_song_list)
    number_of_directories_found = number_of_directories_found - 1;
    print("Number of directories to go {}".format(number_of_directories_found))
print("Walk complete. Remeber to check logfile for errors, like folders with v1 tags only.")
