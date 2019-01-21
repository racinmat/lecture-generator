from sys import argv
import os.path as osp
from utils import load_srt_file, srt_files_in_dir


def extract_dir(directory):
    for file_path in srt_files_in_dir(directory):
        print(file_path)
        srt_to_sentences(file_path)


def merge_sentences_together(sentences):
    i = 0
    while i < len(sentences) - 1:
        sentence = sentences[i]
        next_sentence = sentences[i + 1]
        sentence_continues = sentence[-1] not in ['.', '!', '?'] and not sentence.endswith('tzv.')
        sentence_is_continued = next_sentence[0].islower() or next_sentence[0] in ['"']
        if sentence_continues and sentence_is_continued:
            # not end of sentence
            print('merging together', sentence, next_sentence)
            sentence = f"{sentence} {next_sentence}".replace('  ', ' ')  # merge with double space replace
            sentences[i] = sentence
            del sentences[i + 1]
        else:
            i += 1
    return sentences

def srt_to_sentences(filename):
    print('parsing file', filename)
    records = load_srt_file(filename)

    sentences = []
    for record in records:
        if record.text.startswith('(') and record.text.endswith(')'):
            # note from audience
            continue
        sentences.append(record.text)

    merged_sentences = list(merge_sentences_together(sentences))
    # merging parts of sentences into sentences
    basename = osp.splitext(osp.basename(filename))[0]
    with open(osp.join('..', 'pure_text_dataset', basename+'.txt'), mode='w+', encoding='utf-8') as f:
        for sentence in merged_sentences:
            f.write(sentence+'\n')


if __name__ == '__main__':
    directory = argv[1]
    # directory = '../text_out/corrected-final'
    extract_dir(directory)
