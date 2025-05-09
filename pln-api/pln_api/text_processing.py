import subprocess

from typing import cast

import stanza
from stanza import Document
from stanza.models.common.doc import Word

stanza.download('pt') # download Portuguese model
nlp = stanza.Pipeline('pt') # initialize Portuguese neural pipeline

upos_translation = {
    "ADJ"  : "Adjetivo",
    "ADP"  : "Preposição",
    "ADV"  : "Advérbio",
    "AUX"  : "Verbo Auxiliar",
    "CCONJ": "Conjunção Coordenativa",
    "DET"  : "Determinante",
    "INTJ" : "Interjeição",
    "NOUN" : "Substantivo",
    "NUM"  : "Numeral",
    "PART" : "Partícula",
    "PRON" : "Pronome",
    "PROPN": "Substantivo Próprio",
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
    doc:Document = nlp(text) # type: ignore
    pos_tags = []
    word:Word
    for word in doc.iter_words():
        tag = cast(str, word.upos)
        translated_tag = upos_translation.get(tag, tag)  # Se não achar, usa a própria tag original
        pos_tags.append({'word': word.text, 'tag': translated_tag})
    return pos_tags
