import subprocess

import spacy 

try:
    nlp = spacy.load("pt_core_news_lg")
except OSError:
    subprocess.run(["python3", "-m", "spacy", "download", "pt_core_news_lg"])
    nlp = spacy.load("pt_core_news_lg")

upos_translation = {
    "ADJ"  : "Adjetivo",
    "ADP"  : "Preposição",
    "ADV"  : "Advérbio",
    "AUX"  : "Verbo Auxiliar",
    "CCONJ": "Conjunção Coordenativa",
    "DET"  : "Determinante (art ou pron não nominal)",
    "INTJ" : "Interjeição",
    "NOUN" : "Substantivo",
    "NUM"  : "Numeral",
    "PART" : "Partícula",
    "PRON" : "Pronome",
    "PROPN": "Nome Próprio",
    "PUNCT": "Pontuação",
    "SCONJ": "Conjunção Subordinativa",
    "SYM"  : "Símbolo",
    "VERB" : "Verbo",
    "X"    : "Outro"
}

def get_pos_tags(text) -> list[dict[str, str]]:
    """
    Processa o texto e retorna uma lista de dicionários com a palavra e sua classe gramatical em português.
    """
    doc = nlp(text)
    pos_tags = []
    for token in doc:
        tag = token.pos_
        translated_tag = upos_translation.get(tag, tag)  # Se não achar, usa a própria tag original
        pos_tags.append({'word': token.text, 'tag': translated_tag})
    return pos_tags
