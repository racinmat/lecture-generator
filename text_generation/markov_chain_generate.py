import markovify
import os
import os.path as osp

from utils import load_txt_data


class KeywordedText(markovify.Text):

    def word_join(self, words):

        return super().word_join(words)


def main():
    # loading data and training
    # sentences in texts should be delimited by .

    texts_dir = osp.join('..', 'pure_text_dataset_google')  # purely google stt generated dataset
    # texts_dir = osp.join('..', 'pure_text_dataset')   # hand-made dataset

    input_texts, input_rows = load_txt_data(texts_dir)

    model_2gram = markovify.NewlineText(input_texts, state_size=2)
    model_3gram = markovify.NewlineText(input_texts, state_size=3)
    # model_merged = markovify.combine([model_2gram, model_3gram])
    for i in range(10):
        # print(model_3gram.make_short_sentence(140))
        print(model_3gram.make_sentence(max_overlap_ratio=0.8, max_overlap_total=20))


if __name__ == '__main__':
    main()
