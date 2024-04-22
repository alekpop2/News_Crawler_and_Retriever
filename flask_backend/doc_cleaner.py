import re
from copy import deepcopy
import nltk
from nltk.corpus import stopwords
from typing import List, Dict, Tuple

def remove_emojis(text: str) -> str:

    # Unicode ranges for emojis
    emoji_pattern = re.compile(
        '['
        '\U0001F600-\U0001F64F'  # emoticons
        '\U0001F300-\U0001F5FF'  # symbols & pictographs
        '\U0001F680-\U0001F6FF'  # transport & map symbols
        '\U0001F700-\U0001F77F'  # alchemical symbols
        '\U0001F780-\U0001F7FF'  # Geometric Shapes Extended
        '\U0001F800-\U0001F8FF'  # Supplemental Arrows-C
        '\U0001F900-\U0001F9FF'  # Supplemental Symbols and Pictographs
        '\U0001FA00-\U0001FA6F'  # Chess Symbols
        '\U0001FA70-\U0001FAFF'  # Symbols and Pictographs Extended-A
        '\U00002702-\U000027B0'  # Dingbats
        '\U000024C2-\U0001F251' 
        ']+', flags=re.UNICODE
    )

    return emoji_pattern.sub(r'', text)

def clean_text(text: str) -> str:

    text = deepcopy(text)
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)  # Replace tabs or multiple spaces with a single space
    return text

def normalize_text(text: str) -> str:
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')
    
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

    try:
        nltk.data.find('corpora/wordnet.zip')
    except LookupError:
        nltk.download('wordnet')
    
    try:
        nltk.data.find('corpora/omw-1.4/')
    except LookupError:
        nltk.download('omw-1.4')
    
    text = deepcopy(text)
    text = remove_emojis(text)
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = text.lower()

    tokens = nltk.tokenize.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    lemmatizer = nltk.stem.WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word=word) for word in tokens]
    
    text = ' '.join(tokens)
    return text

def spell_correct_word(word: str, inverted_index: Dict[str, List[Tuple[int, float]]]) -> str:

    if word in inverted_index:
        return word
    else:
        words = list(set(inverted_index.keys()))
        word_dist_pairs = [(word, nltk.edit_distance(w, word)) for w in words]
        min_dist = min([dist for _, dist in word_dist_pairs])
        min_pairs = list(filter(lambda tup: tup[1] == min_dist, word_dist_pairs))
        suggestion = min_pairs[0][0]
        return suggestion

def spell_correct_query(query: List[str], inverted_index: Dict[str, List[Tuple[int, float]]]) -> List[str]:

    corrected_query = []
    for word in query:
        corrected_word = spell_correct_word(word, inverted_index)
        corrected_query.append(corrected_word)
    
    return corrected_query
