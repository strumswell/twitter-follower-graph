#  %% 
from wordcloud import WordCloud
from mpl_toolkits.mplot3d import Axes3D
from spacy.lang.de.stop_words import STOP_WORDS as STOP_WORDS_DE
from spacy.lang.en.stop_words import STOP_WORDS as STOP_WORDS_EN
#from spacy.lang.pt.stop_words import STOP_WORDS as STOP_WORDS_PT
#from spacy.lang.fr.stop_words import STOP_WORDS as STOP_WORDS_FR
import pandas as pd
import numpy as np
import spacy
import csv
import json
nlp = spacy.load('de_core_news_sm')
#nlp = spacy.load('pt_core_news_sm')
#nlp = spacy.load('en_core_web_sm')
#nlp = spacy.load("fr_core_news_sm")
# Polish Spacy Model: https://github.com/ipipan/spacy-pl
#nlp = spacy.load('pl_spacy_model') # or spacy.load('pl_spacy_model_morfeusz')
# Polish Stop Words: https://github.com/Alir3z4/python-stop-words
#from stop_words import get_stop_words
#STOP_WORDS_PL = get_stop_words('pl')
base_path = '/Users/philippbolte/Documents/FollowerNetworkTwitter'

def get_dict_from_texts(texts, filter_words, min_word_length):
    text_dict = {}
    for text in texts:
        # Do all lower case
        text_lowercase = nlp(text.lower())
        # Lemmatization
        text_lemma = ''
        for word in text_lowercase:
            text_lemma += word.lemma_
            text_lemma += ' '
        text_lemma = nlp(text_lemma) #Fix type
        # Filter points
        word_list = list(map(lambda x: x.text, filter(lambda x: x.pos_ != 'PUNCT', text_lemma)))
        # Filter stop words
        word_list_cleaned = [tok for tok in word_list if tok not in STOP_WORDS_DE]
        word_list_cleaned = [tok for tok in word_list_cleaned if tok not in STOP_WORDS_EN]
        #word_list_cleaned = [tok for tok in word_list_cleaned if tok not in STOP_WORDS_DE]
        # Filter short words
        word_list_cleaned = [tok for tok in word_list_cleaned if len(tok) >= min_word_length]
        # Filter filter words
        word_list_cleaned = [tok for tok in word_list_cleaned if not any(fword in tok for fword in filter_words)]
        # Build dict
        for term in word_list_cleaned:
            if term not in text_dict.keys():
                text_dict[term] = 1
            else:
                text_dict[term] += 1
    return text_dict

def save_wordcloud(text_dict, max_words, path):
    wc = WordCloud(height=1080, width=1920, background_color="white", max_words=max_words)
    wc.generate_from_frequencies(text_dict)
    wc.to_file(path)
    #plt.figure()
    #plt.imshow(wc)
    #plt.axis("off")
    #plt.pause(1)

def load_csv(_filename):
    with open(base_path + '/data/tweets'+_filename, newline='') as f:       
        reader = csv.reader(f)
        data = list(reader)
        return data

def save_dict_as_json(_text_dict, _path):
    with open(_path, 'w', encoding='utf8') as fp:
        json.dump(_text_dict, fp, indent=4, ensure_ascii=False)

#  %% 
influential_users_by_party = [{'Die_Gruenen': load_csv('/Die_Gruenen_cluster/influential_users.csv')}]

# %%
# -*- coding: utf-8 -*-
for influential_user in influential_users_by_party:
    party = list(influential_user.keys())[0]
    users = list(influential_user.values())[0]
    for user in users:
        print('Do '+user[0])
        cluster = user[1]
        name = user[0]
        print('\_____ Get tweets')
        df_tweets = pd.read_csv(base_path + '/data/tweets/'+party+"_cluster/"+str(cluster)+"/"+name+"_tweets.csv")
        texts = df_tweets['text']
        filter_words = ['https', 'http', '@', 'amp', 'all', 'jed', 'link', 'mal','prof', 'welch', 'ander', '-PRON-']
        print('\_____ Build Dict')
        text_dict = get_dict_from_texts(texts, filter_words, 3)
        print('\_____ Save Dict')
        save_dict_as_json(text_dict, base_path + '/data/tweets/'+party+'_cluster/'+str(cluster)+'/'+name+'_text_dict.json')
        print('\_____ Generate WC')
        save_wordcloud(text_dict, 50, base_path + '/data/tweets/'+party+'_cluster/'+str(cluster)+'/'+name+'_wordcloud.png')

# %%
