import spacy
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

nlp = spacy.load('en_core_web_sm')

text = "The food we had yesterday was delicious. But the food next day was very boring"

kalimat =[]
kalimat = text.split('.')
print (kalimat)

sentences = [
  'The food we had yesterday was delicious',
  'My time in Italy was very enjoyable',
  'I found the meal to be tasty',
  'The internet was slow.',
  'Our experience was suboptimal'
]
print(sentences)

aspects = []

for sentence in kalimat:
    doc = nlp(sentence)
    target = ''
    desc_term = ''

    for token in doc:
        if token.dep_ == 'nsubj' and token.pos_ == 'NOUN':
            target = token.text
        if token.pos_ == 'ADJ':
            prepend = ''
            for child in token.children:
                if child.pos_ != 'ADV':
                    continue
                prepend += child.text + ' '
            desc_term = prepend + token.text

    aspects.append(
        {'aspects' : target,
         'desc': desc_term}
    )

    for aspect in aspects:
        aspect['sentiment'] = TextBlob(aspect['desc']).sentiment

print(aspects)