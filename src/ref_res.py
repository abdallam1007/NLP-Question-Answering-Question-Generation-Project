import spacy

import spacy
import neuralcoref

nlp = spacy.load("en_core_web_sm")
neuralcoref.add_to_pipe(nlp)

doc = nlp("John is a doctor. He loves his job.")

for token in doc:
    if token._.in_coref:
        print(token.text, "is a coreference of", token._.coref_clusters[0].main.text)
