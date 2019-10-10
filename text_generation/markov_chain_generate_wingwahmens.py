import markovify
import os
import os.path as osp

from utils import load_txt_data
import pandas as pd


class KeywordedText(markovify.Text):

    def word_join(self, words):
        return super().word_join(words)


def next_same_user(df): return df.shift(-1)['UserID'] == df['UserID']


def prev_same_user(df): return df.shift(1)['UserID'] == df['UserID']


def is_smiley(df): return (df['MessageBody'].str.len() == 2) & (df['MessageBody'].str.startswith(':'))


def is_next_withing_time(df, sec=60): return (df.shift(-1)['DateTime'] - df['DateTime']).dt.seconds <= sec


def is_prev_withing_time(df, sec=60): return (df['DateTime'] - df.shift(1)['DateTime']).dt.seconds <= sec


def select_name(x):
    if len(x) > 1:
        return x[~x.str.match('Removed user')]
    return x


def load_data():
    df = pd.read_csv(r'E:\Projects\fb-downloader-conversions\data\Wongwahmeni-total.csv', encoding='utf-8')
    # df = pd.read_csv('data/example.csv')
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    df['MessageBody'] = df['MessageBody'].str.replace('[\?#]utm_.*\(\)', '')
    df['MessageBody'] = df['MessageBody'].fillna('').str.replace('\\n', ' ', regex=False)
    df = df.set_index('DateTime', drop=False)

    # if user was missing for some time, he has Removed User XYZ instead of his name. This is fixed here.
    id_and_name = df.groupby(['UserID', 'UserName']).count().index.to_frame().reset_index(drop=True)
    id_to_name = id_and_name.groupby('UserID').agg(select_name)

    # I can not pair images to text, so I exclude empty messages
    df = df[df['MessageBody'] != '']
    df['UserName'] = df['UserID'].map(id_to_name['UserName'])

    # lots of messages is one char long, and they are after another message from same user, merging them
    one_char_suffix = (df.shift(-1)['MessageBody'].str.len() == 1) & next_same_user(df)
    one_char_suffix_next = (df['MessageBody'].str.len() == 1) & prev_same_user(df)
    df.loc[one_char_suffix, 'MessageBody'] += ' ' + df.shift(-1)[one_char_suffix]['MessageBody']
    df = df[~one_char_suffix_next]

    # also lots of 2char emoji faces appears as individual message, appending them
    smiley_suffix = is_smiley(df.shift(-1)) & next_same_user(df)
    smiley_suffix_next = is_smiley(df) & prev_same_user(df)
    df.loc[smiley_suffix, 'MessageBody'] += ' ' + df.shift(-1)[smiley_suffix]['MessageBody']
    df = df[~smiley_suffix_next]

    # also lots of messages by same user is split to multiple rows. Merge them
    df = df.groupby([pd.Grouper(freq='5min'), 'UserName'])['MessageBody'].agg(' '.join).reset_index()
    return df


def generate_grek():
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


def train_or_load(input_data, name):
    if osp.exists(name):
        with open(name, 'r') as f:
            model = markovify.Text.from_json(f.read())
    else:
        model = markovify.NewlineText(input_data, state_size=3)
        with open(name, 'w') as f:
            model_json = model.to_json()
            f.write(model_json)

    return model


def train_wingwahmen_models(df):
    all_input_texts = '\n'.join(df['MessageBody'])

    # model for all wingwahmens
    model_3gram = train_or_load(all_input_texts, 'model_wingwamens_all.json')

    # model per user
    models = {}
    for username in df['UserName'].unique():
        if username in ['Removed user 100001231147296']:    # some blacklist
            continue
        df_user = df[df['UserName'] == username]
        input_texts = '\n'.join(df_user['MessageBody'])
        models[username] = train_or_load(input_texts, f'model_wingwamens_{username}.json')

    return model_3gram, models

def generate_wingwahmeni():
    # loading data and training
    # sentences in texts should be delimited by .

    df = load_data()

    model_all, models = train_wingwahmen_models(df)
    # model_merged = markovify.combine([model_2gram, model_3gram])
    for i in range(5):
        print(model_all.make_sentence(max_overlap_ratio=0.8, max_overlap_total=20, tries=30))

    for username, model in models.items():
        print()
        print(username)
        for i in range(5):
            print(model.make_sentence(max_overlap_ratio=0.8, max_overlap_total=20, tries=30))


def main():
    # generate_grek()
    generate_wingwahmeni()


if __name__ == '__main__':
    main()
