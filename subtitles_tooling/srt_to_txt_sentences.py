from sys import argv
from datetime import timedelta
from utils import load_srt_file, srt_files_in_dir


def extract_dir(directory):
    for file_path in srt_files_in_dir(directory):
        print(file_path)
        srt_to_sentences(file_path)


def srt_to_sentences(filename, max_seconds=4.5):
    print('parsing file', filename)
    records = load_srt_file(filename)

    sentences = []
    for record in records:
        if record.text.startswith('(') and record.text.endswith(')'):
            # note from audience
            continue
        sentences.append(record.text)

    prev_sentence = sentences[0]
    for i, sentence in list(enumerate(sentences))[1:]:
        if prev_sentence[-1] not in ['.', '!', '?'] and sentence[0].islower():
            # not end of sentence
            print('merging together', prev_sentence, sentence)
            sentence = f"{prev_sentence} {sentence}".replace('  ', ' ')  # merge with double space replace
            del sentences[i - 1]
            sentences[i] = sentence
        prev_sentence = sentence
    # merging parts of sentences into sentences
    print(sentences)


if __name__ == '__main__':
    # directory = argv[1]
    directory = '../text_out/corrected-final'
    extract_dir(directory)
