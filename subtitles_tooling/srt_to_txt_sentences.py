import os.path as osp
from utils import load_srt_file, srt_files_in_dir
from absl import flags
from absl import app

FLAGS = flags.FLAGS

flags.DEFINE_string('srt_dir', '../text_out/corrected-final', 'Input directory with .srt files.')
flags.DEFINE_string('txt_dir', '../pure_text_dataset', 'Output directory with .txt files.')
flags.DEFINE_boolean('missing_punctuation', False, 'If true, punctuation will be added based on capitals from google stt.')


def extract_dir(in_directory, out_directory):
    for file_path in srt_files_in_dir(in_directory):
        print(file_path)
        srt_to_sentences(file_path, out_directory)


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


def add_punctuation_by_capitals(sentences):
    i = 0
    while i < len(sentences) - 1:
        sentence = sentences[i]
        next_sentence = sentences[i + 1]
        new_sentence = next_sentence[0].isupper()
        if new_sentence:
            sentence += '.'
            sentences[i] = sentence
        i += 1
    return sentences


def remove_quotation_marks(sentences):
    return map(lambda x: x.replace('"', ''), sentences)


def srt_to_sentences(filename, out_directory):
    print('parsing file', filename)
    records = load_srt_file(filename)

    sentences = []
    for record in records:
        if record.text.startswith('(') and record.text.endswith(')'):
            # note from audience
            continue
        sentences.append(record.text)

    missing_punctuation = FLAGS.missing_punctuation
    if missing_punctuation:
        sentences = list(add_punctuation_by_capitals(sentences))

    sentences = list(merge_sentences_together(sentences))
    sentences = list(remove_quotation_marks(sentences))
    # merging parts of sentences into sentences
    basename = osp.splitext(osp.basename(filename))[0]
    with open(osp.join(out_directory, basename + '.txt'), mode='w+', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(sentence + '\n')


def main(_):
    in_directory = FLAGS.srt_dir
    out_directory = FLAGS.txt_dir
    extract_dir(in_directory, out_directory)


if __name__ == '__main__':
    app.run(main)
