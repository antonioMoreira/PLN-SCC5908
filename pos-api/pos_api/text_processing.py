import spacy 

nlp = spacy.load("pt_core_news_sm")

def get_pos_tags(text) -> list[tuple[str, str]]:
    """
    Process the text and return a list of tuples with the word and its part of speech tag.
    """
    doc = nlp(text)
    pos_tags = [(token.text, token.pos_) for token in doc]
    return pos_tags

