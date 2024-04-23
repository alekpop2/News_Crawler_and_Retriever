from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Dict, Tuple
import bisect
import pandas as pd
from doc_cleaner import clean_text, normalize_text
import os
import pickle
import nltk

def get_cleaned_df() -> pd.DataFrame:
    
    csv_file_path = os.path.join('web_crawler', 'docs.csv')

    if not os.path.exists(csv_file_path):
        raise Exception('docs.csv file does not exist')

    text_df = pd.read_csv(csv_file_path)
    text_df['title'] = text_df['title'].apply(clean_text)
    text_df['text'] = text_df['text'].apply(clean_text)

    text_df = text_df.drop_duplicates(subset='title', keep='first')
    return text_df

def get_normalized_docs() -> List[str]:

    text_df = get_cleaned_df()
    
    text_df['title'] = text_df['title'].apply(normalize_text)
    text_df['text'] = text_df['text'].apply(normalize_text)

    docs = list(text_df['text'])
    return docs

def create_tf_idf_index(docs: List[str]) -> Dict[str, List[Tuple[int, float]]]:

    vectorizer = TfidfVectorizer(token_pattern='(?u)\\b\\w+\\b')
    doc_term_matrix = vectorizer.fit_transform(docs)
    terms = vectorizer.get_feature_names_out()

    index = {}
    coords = doc_term_matrix.tocoo()
    
    for doc_id, term_id, tf_idf in zip(coords.row, coords.col, coords.data):
        term = terms[term_id]
        if term in index:
            bisect.insort(index[term], (doc_id, tf_idf))
        else:
            index[term] = [(doc_id, tf_idf)]
    
    return index

def create_pickled_index_from_docs() -> None:
    
    nltk.download('punkt')
    
    csv_file_path = os.path.join('web_crawler', 'docs.csv')

    if not os.path.exists(csv_file_path):
        raise Exception('docs.csv file does not exist')

    if os.path.exists('inverted_index.pkl'):
        os.remove('inverted_index.pkl')
    
    text_df = pd.read_csv(csv_file_path)
    text_df['title'] = text_df['title'].apply(clean_text)
    text_df['text'] = text_df['text'].apply(clean_text)
    text_df['title'] = text_df['title'].apply(normalize_text)
    text_df['text'] = text_df['text'].apply(normalize_text)

    docs = list(text_df['text'])
    index = create_tf_idf_index(docs)

    with open('inverted_index.pkl', 'wb') as file:
        pickle.dump(index, file)

def get_pickled_index() -> Dict[str, List[Tuple[int, float]]]:
    
    if os.path.exists('inverted_index.pkl'):
        with open('inverted_index.pkl', 'rb') as f:
            index = pickle.load(f)
            return index
    else:
        raise Exception('pickled index file does not exist')

