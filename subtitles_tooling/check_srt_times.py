from sys import argv
from utils import load_srt_file, srt_files_in_dir


def check_dir(directory):
    for file_path in srt_files_in_dir(directory):
        print(file_path)
        check_srt_file_length(file_path)


def check_srt_file_length(filename, max_seconds=4.5):
    print('analyzing file', filename)
    records = load_srt_file(filename)

    for record in records:
        diff = record.seconds_diff()
        if diff > max_seconds:
            print('too long record', 'length: ', diff)
            print(record.start_timedelta(), record.end_timedelta(), record.text)


if __name__ == '__main__':
    directory = argv[1]
    check_dir(directory)
