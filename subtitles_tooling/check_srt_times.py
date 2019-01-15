import os
from sys import argv
import re
from datetime import timedelta

# Runs transcription for each file inside the specified directory
def check_dir(directory):
    for file in os.listdir(directory):
        if not file.endswith('.srt'):
            continue
        file_path = os.path.join(directory, file)
        check_srt_file_length(file_path)

        print(file_path)


def check_srt_file_length(filename, max_seconds=4.5):
    print('analyzing file', filename)
    with open(filename, encoding='utf-8', mode='r') as fp:
        lines = iter(fp)
        records = []
        while True:
            try:
                line = next(lines).replace('\n', '')
                line_number = int(line)
                line = next(lines).replace('\n', '')
                time_range = line
                m = re.match('(\d{1,2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{1,2}):(\d{2}):(\d{2}),(\d{3})', time_range)
                vals = [int(i) for i in m.groups()]
                seconds_start = vals[0] * 3600 + vals[1] * 60 + vals[2] + vals[3] / 1000
                seconds_end = vals[4] * 3600 + vals[5] * 60 + vals[6] + vals[7] / 1000
                line = next(lines).replace('\n', '')
                text = line
                next(lines)
                records.append({
                    's_start': seconds_start,
                    's_end': seconds_end,
                    'text': text
                })
            except StopIteration as e:
                print(e)
                break

    for record in records:
        diff = record['s_end'] - record['s_start']
        if diff > max_seconds:
            print('too long record', 'length: ', diff)
            print(timedelta(seconds=record['s_start']), timedelta(seconds=record['s_end']), record['text'])


if __name__ == '__main__':
    directory = argv[1]
    check_dir(directory)
