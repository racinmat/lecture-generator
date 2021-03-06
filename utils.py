import re
import os
import os.path as osp
from datetime import timedelta


def srt_files_in_dir(directory):
    for file in os.listdir(directory):
        if not file.endswith('.srt'):
            continue
        file_path = osp.join(directory, file)
        yield file_path


class Record(object):
    def __init__(self, line_number: int, seconds_start: float, seconds_end: float, text: str):
        self.line_number = line_number
        self.seconds_start = seconds_start
        self.seconds_end = seconds_end
        self.text = text

    def start_timedelta(self):
        return timedelta(seconds=self.seconds_start)

    def end_timedelta(self):
        return timedelta(seconds=self.seconds_end)

    def seconds_diff(self):
        return self.seconds_end - self.seconds_start


def load_srt_file(filename):
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
                if text == '':
                    continue  # skipping empty subtitle
                records.append(Record(line_number, seconds_start, seconds_end, text))
            except StopIteration as e:
                break
    return records


def replace_special_words_to_keywords(text):
    number_regex = '(\D?)\d+(\D?)'
    text_numbers_replaced = re.sub(number_regex, '\g<1>NUMBER\g<2>', text)  # replace numbers by regex
    text = text_numbers_replaced
    return text


def replace_special_words_from_keywords(text):
    # todo: implement me, some smart number generator
    return text


def load_txt_data(input_dir):
    input_rows = []

    for input_file in os.listdir(input_dir):
        with open(osp.join(input_dir, input_file), mode='r', encoding='utf-8') as f:
            input_rows += f.readlines()

    input_texts = ''.join(input_rows)
    return input_texts, input_rows
