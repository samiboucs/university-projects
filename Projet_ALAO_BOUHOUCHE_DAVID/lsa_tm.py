#! /usr/bin/env python3
# -*- coding:utf8 -*-

'''
***Latent Semantic Analysis using Python***
:author: Avinash Navlani <https://www.datacamp.com/profile/avinashnvln8>
:script_url: https://www.datacamp.com/community/tutorials/discovering-hidden-topics-python
'''

#import modules
import os.path
from gensim import corpora
from gensim.models import LsiModel
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim.models.coherencemodel import CoherenceModel

def load_data(path,file_name):
    """
    Input  : path and file_name
    Purpose: loading text file
    Output : list of paragraphs/documents and
             title(initial 10 words considred as title of document)
    """
    documents_list = []
    titles = []
    with open( os.path.join(path, file_name) ,"r", encoding = 'utf8') as fin:
        for line in fin.readlines():
            text = line.strip()
            documents_list.append(text)
    print("Total Number of Documents:",len(documents_list))
    titles.append( text[0:min(len(text),10)] )
    return documents_list,titles
	
def preprocess_data(doc_set):
    """
    Input  : docuemnt list
    Purpose: preprocess text (tokenize, removing stopwords, and stemming)
    Output : preprocessed text
    """
    # initialize regex tokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    # create French stop words list
    fr_stop = set(stopwords.words('french'))
    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()
    # list for tokenized documents in loop
    texts = []
    # loop through document list
    for i in doc_set:
        # clean and tokenize document string
        raw = i.lower()
        tokens = tokenizer.tokenize(raw)
        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if not i in fr_stop]
        # stem tokens
        stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
        # add tokens to list
        texts.append(stemmed_tokens)
    return texts
	
def prepare_corpus(doc_clean):
    """
    Input  : clean document
    Purpose: create term dictionary of our courpus and Converting list of documents (corpus) into Document Term Matrix
    Output : term dictionary and Document Term Matrix
    """
    # Creating the term dictionary of our courpus, where every unique term is assigned an index. dictionary = corpora.Dictionary(doc_clean)
    dictionary = corpora.Dictionary(doc_clean)
    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    # generate LDA model
    return dictionary,doc_term_matrix

#LSA - Topic Modelling
##Application du modèle sur le corpus LONGIT
number_of_topics = 1

words = 100

document_list,titles = load_data("",'./corpus_files/prod_all_txt/corpus_longit.csv')

clean_text = preprocess_data(document_list)

dictionary,doc_term_matrix = prepare_corpus(clean_text)

lsamodel = LsiModel(doc_term_matrix, num_topics = number_of_topics, id2word = dictionary)  # train model

print(lsamodel.print_topics(num_topics = number_of_topics, num_words = words))

output_file = open('./corpus_files/tm_csv/topic_modelling.csv', mode = 'w', encoding = 'utf8')

output_file.write("Topic modelling du corpus LONGIT : "+str(lsamodel.print_topics(num_topics = number_of_topics, num_words = words)))

output_file.close()