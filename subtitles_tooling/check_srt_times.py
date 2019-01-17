import os
from sys import argv
from datetime import timedelta
from utils import load_srt_file, srt_files_in_dir


def check_dir(directory):
    for file_path in srt_files_in_dir(directory):
        check_srt_file_length(file_path)

        print(file_path)


def check_srt_file_length(filename, max_seconds=4.5):
    print('analyzing file', filename)
    records = load_srt_file(filename)

    for record in records:
        diff = record['s_end'] - record['s_start']
        if diff > max_seconds:
            print('too long record', 'length: ', diff)
            print(timedelta(seconds=record['s_start']), timedelta(seconds=record['s_end']), record['text'])


if __name__ == '__main__':
    directory = argv[1]
    check_dir(directory)
