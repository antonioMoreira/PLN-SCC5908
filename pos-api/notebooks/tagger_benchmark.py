import stanza
from stanza import Document
from tqdm import tqdm

stanza.download('pt')

nlp = stanza.Pipeline('pt')

sentences_ground_truth = []
current_sentence = []

# LENDO DATASET GROUND_TRUTH PARA COMPARAÇÃO (PORTTINARI)
DATASET_PATH = "Porttinari-base_train.conllu"

with open(DATASET_PATH, 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        if not line:
            if current_sentence:
                sentences_ground_truth.append(current_sentence)
                current_sentence = []
        elif line.startswith('#'):
            continue  # Skip comment lines
        else:
            fields = line.split('\t')
            token = {
                'id': fields[0],
                'form': fields[1],
                'lemma': fields[2],
                'upos': fields[3],
                'xpos': fields[4],
                'feats': fields[5],
                'head': fields[6],
                'deprel': fields[7],
                'deps': fields[8],
                'misc': fields[9],
            }
            current_sentence.append(token)

    if current_sentence:  # catch any leftover sentence
        sentences_ground_truth.append(current_sentence)

# Now 'sentences' is a list of sentences, each sentence is a list of token dicts.
print(sentences_ground_truth[0])  # Show the first sentence

# PROCESSANDO UM SAMPLE DE 500 FRASES DO DATASET COM O STANZA PARA TESTE

sentences_stanza = []
for sentence_info in tqdm(sentences_ground_truth[:500]):
    sentence = []
    for word in sentence_info:
        sentence.append(word['form'])
    sentence = ' '.join(sentence)
    doc:Document = nlp(sentence)
    sentences_stanza.append(doc)

number_of_hits = 0
number_of_mistakes = 0

# COMPARANDO OS TAGS
# MECANISMO PARA EVITAR PROBLEMAS DE DIFERENÇA DE TAGS (DAS vs DE + AS) FEITO PELO GEPETO
# CONFUSO - NÃO SEI SE FUNCIONA MAS EVITA ERROS DE IndexOutOfBounds

for i, doc in enumerate(sentences_stanza):
    for sentence_stanza in doc.sentences:
        j = 0  # índice para stanza
        k = 0  # índice para ground truth

        while j < len(sentence_stanza.words) and k < len(sentences_ground_truth[i]):
            word_stanza = sentence_stanza.words[j]
            word_ground = sentences_ground_truth[i][k]

            print("===========================================")
            print(f"i = {i}, j = {j}, k = {k}")
            print("Stanza:", word_stanza.text, word_stanza.upos)
            print("Ground Truth:", word_ground['form'], word_ground['upos'])

            if word_stanza.text == word_ground['form']:
                # Palavras iguais -> comparar as classes gramaticais (upos)
                if word_stanza.upos == word_ground['upos']:
                    number_of_hits += 1
                else:
                    number_of_mistakes += 1
                j += 1
                k += 1
            else:
                # Palavras diferentes: tentar lidar com contrações
                # (ex: Stanza tem 'das', Ground Truth tem 'de' + 'as')
                combined = word_ground['form']
                next_k = k + 1
                while next_k < len(sentences_ground_truth[i]) and len(combined) < len(word_stanza.text):
                    combined += sentences_ground_truth[i][next_k]['form']
                    next_k += 1

                if combined == word_stanza.text:
                    # Encontramos a combinação!
                    print(f"Encontramos a combinação: {combined} - {word_stanza.text}")
                    if word_stanza.upos == word_ground['upos']:
                        number_of_hits += 1
                    else:
                        number_of_mistakes += 1
                    j += 1
                    k = next_k  # pula para depois da combinação
                else:
                    print(f"Não foi possível alinhar: {word_stanza.text} vs {word_ground['form']}")
                    j += 1
                    k += 1  # avança ambos para tentar continuar

print(f"Acurácia final do sample: {1.0 - (number_of_mistakes / number_of_hits)}")
# Resultado: 0.91 = 91% de acertos
# Tenho a impressão de que alguns desses erros se devem à forma como o porttinari foi 
# etiquetado e não a erros de fato.
