import re
from nltk.tokenize import wordpunct_tokenize


def preprocess(text):
    """
    Basic NLP preprocessing:
    1. lowercase
    2. tokenize
    3. remove punctuation
    4. remove very short/noise tokens
    """

    text = text.lower()

    # Normalize common apostrophe/contraction forms
    text = text.replace("can't", "cannot")
    text = text.replace("i'm", "i am")
    text = text.replace("what's", "what is")
    text = text.replace("who's", "who is")
    text = text.replace("where's", "where is")

    tokens = wordpunct_tokenize(text)

    cleaned_tokens = []

    for token in tokens:

        if re.fullmatch(r"[a-z0-9]+", token):

            if len(token) > 1:
                cleaned_tokens.append(token)

    return " ".join(cleaned_tokens)