import markovify
import os
import os.path as osp
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
import re

from utils import load_txt_data


def main():
    # loading data and training
    # sentences in texts should be delimited by .

    texts_dir = osp.join('..', 'pure_text_dataset_google')   # purely google stt generated dataset
    # texts_dir = osp.join('..', 'pure_text_dataset')   # hand-made dataset

    input_texts, input_rows = load_txt_data(texts_dir)

    model_2gram = markovify.NewlineText(input_texts, state_size=2)
    model_3gram = markovify.NewlineText(input_texts, state_size=3)

    model = model_3gram
    chain = model.chain

    print('# sentence beginnings: ', len(chain.begin_choices))

    begin_freqs = np.diff([0] + chain.begin_cumdist)
    sorted_indices = np.argsort(begin_freqs)
    num_words = 30
    most_frequent_indices = sorted_indices[-num_words:][::-1]

    freq_words = np.array(chain.begin_choices)[most_frequent_indices]
    freqs = begin_freqs[most_frequent_indices] / sum(begin_freqs)

    plt.figure(figsize=(20, 12))
    plt.bar(freq_words, freqs)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
    plt.xticks(rotation=60)
    plt.savefig('sentence_start_freqs.png')


    number_regex = '(\D?)\d+(\D?)'
    numbers = re.search(number_regex, input_texts)
    numbers_2 = re.findall(number_regex, input_texts)
    input_texts_replaced = re.sub(number_regex, '\g<1>NUMBER\g<2>', input_texts)  # replace numbers by regex
    print(numbers)


if __name__ == '__main__':
    main()
