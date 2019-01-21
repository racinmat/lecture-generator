import markovify
import os
import os.path as osp


def main():
    # loading data and training
    # sentences in texts should be delimited by .
    input_texts = ''
    texts_dir = osp.join('..', 'pure_text_dataset')
    for input_file in os.listdir(texts_dir):
        with open(osp.join(texts_dir, input_file), mode='r', encoding='utf-8') as f:
            input_texts += f.read()
    #   some sentences from dataset are not in models parsed sentences, debug it
    model_2gram = markovify.NewlineText(input_texts, state_size=2)
    model_3gram = markovify.NewlineText(input_texts, state_size=3)
    # model_merged = markovify.combine([model_2gram, model_3gram])
    for i in range(5):
        # print(model_3gram.make_short_sentence(140))
        print(model_3gram.make_sentence(max_overlap_ratio=0.8, max_overlap_total=20))

if __name__ == '__main__':
    main()
