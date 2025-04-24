import subprocess

import spacy 

try:
    nlp = spacy.load("pt_core_news_lg")
except OSError:
    subprocess.run(["python3", "-m", "spacy", "download", "pt_core_news_lg"])
    nlp = spacy.load("pt_core_news_lg")


def get_pos_tags(text) -> list[dict[str, str]]:
    """
    Process the text and return a list of tuples with the word and its part of speech tag.
    """
    doc = nlp(text)
    pos_tags = [{'word': token.text, 'tag':token.pos_} for token in doc]
    return pos_tags
