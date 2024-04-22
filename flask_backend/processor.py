from typing import List, Dict, Tuple, Set
import math
import numpy as np
from doc_cleaner import clean_text, normalize_text, spell_correct_query
from indexer import get_pickled_index, get_cleaned_df, get_normalized_docs

def create_query_dict(query: Set[str], index: Dict[str, List[Tuple[int, float]]], docs: List[str]) -> Dict[str, float]:

    vector = {}
    N = len(docs)
    
    for term in query:
        df = len(index[term]) if term in index else 0
        idf = math.log10(N / df) if df > 0 else 0
        vector[term] = idf
    
    return vector

def create_doc_term_matrix(query: Set[str], index: Dict[str, List[Tuple[int, float]]], docs: List[str]) -> List[List[float]]:

    all_words = set.union(query, set(index.keys()))
    all_words_sorted = sorted(list(all_words))
    doc_term_matrix = [[0 for _ in range(len(all_words_sorted))] for _ in range(len(docs))]

    for word, postings in index.items():
        word_index = all_words_sorted.index(word)
        for doc_id, tf_idf in postings:
            doc_term_matrix[doc_id][word_index] = tf_idf
    
    return doc_term_matrix

def create_query_vector(query: Set[str], index: Dict[str, List[Tuple[int, float]]], docs: List[str]) -> List[float]:

    all_words = set.union(query, set(index.keys()))
    all_words_sorted = sorted(list(all_words))
    query_idfs = create_query_dict(query, index, docs)
    query_vector = [0 for _ in range(len(all_words_sorted))]
    
    for term, idf in query_idfs.items():
        term_index = all_words_sorted.index(term)
        query_vector[term_index] = idf
    
    return query_vector

def create_scores_list(doc_term_matrix: List[List[float]], query_vector: List[float]) -> List[Tuple[int, float]]:

    scores = []

    for doc_id, doc_vector in enumerate(doc_term_matrix):
        score = np.dot(np.array(query_vector), np.array(doc_vector))
        scores.append((doc_id, score))
    
    scores.sort(reverse=True, key = lambda tup: tup[1])
    return scores

def search_relevant_docs(query: Set[str], index: Dict[str, List[Tuple[int, float]]], docs: List[str]) -> List[int]:

    doc_term_matrix = create_doc_term_matrix(query, index, docs)
    query_vector = create_query_vector(query, index, docs)
    scores = create_scores_list(doc_term_matrix, query_vector)
    top_docs = [doc_id for doc_id, _ in scores][:10]
    
    return top_docs

def process_query(query: str) -> List[str]:

    index = get_pickled_index()
    
    cleaned_df = get_cleaned_df()
    cleaned_docs = list(cleaned_df['text'])
    normalized_docs = get_normalized_docs()
    
    processed_query = clean_text(query)
    processed_query = normalize_text(processed_query)
    processed_query = processed_query.split()
    processed_query = spell_correct_query(processed_query, index)
    processed_query = set(processed_query)
    
    top_doc_ids = search_relevant_docs(processed_query, index, normalized_docs)
    top_docs = [cleaned_docs[doc_id] for doc_id in top_doc_ids]
    return top_docs


