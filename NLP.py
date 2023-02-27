import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest
from textblob import TextBlob
from spacytextblob.spacytextblob import SpacyTextBlob


nlp = spacy.load('en_core_web_sm')


async def rangkum(text):
    stopwords = list(STOP_WORDS)+list(punctuation)+['\n']

    docx = nlp(text)

    #Tokenization
    for token in docx :
        print (token.text)

    word_freq = {}

    for word in docx:
        if word.text not in stopwords:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    #print(word_freq)

    max_freq = max(word_freq.values())

    #print(max_freq)

    for word in word_freq.keys():
        word_freq[word] = (word_freq[word]/max_freq)

    #print (word_freq)

    sentence_list = [ sentence for sentence in docx.sents]

    sentences_scores = {}

    for sent in sentence_list:
        for word in sent:
            if word.text.lower() in word_freq.keys():
                if len(sent.text.split(' ')) < 30:
                    if sent not in sentences_scores.keys():
                        sentences_scores[sent] = word_freq[word.text.lower()]
                    else:
                        sentences_scores[sent] += word_freq[word.text.lower()]

    #print (sentences_scores)

    summarized_sentences = nlargest(6,sentences_scores,key=sentences_scores.get)

    #print (summarized_sentences)
    final = [w.text for w in summarized_sentences]

    summary = ''.join(final)

    print (summary)

    print (len(text))
    print(len(summary))
    return summary

async def text_summary(text):
    extra_words = list(STOP_WORDS)+list(punctuation)+['\n']+['\n\n']
   

    
    docx = nlp(text)

    all_words=[word.text for word in docx]
    Freq_word={}
    for w in all_words:
        w1=w.lower()
        if w1 not in extra_words and w1.isalpha():
            if w1 in Freq_word.keys():
                Freq_word[w1]+=1
            else:
                Freq_word[w1]=1



    val=sorted(Freq_word.values())
    max_freq=val[-3:]
    

    for word in Freq_word.keys():
        Freq_word[word] = (Freq_word[word]/max_freq[-1])

    sent_strength={}
    for sent in docx.sents:
        for word in sent :
                if word.text.lower() in Freq_word.keys():
                    if sent in sent_strength.keys():
                        sent_strength[sent]+=Freq_word[word.text.lower()]
                    else:
                        sent_strength[sent]=Freq_word[word.text.lower()]
                else: 
                    continue   

    top_sentences=(sorted(sent_strength.values())[::-1])
    top30percent_sentence=int(0.3*len(top_sentences))
    top_sent=top_sentences[:top30percent_sentence]

    summary=[]
    for sent,strength in sent_strength.items():
        if strength in top_sent:
            summary.append(sent)
        else:
            continue

    for i in summary:
        print(i,end="")

    listtostr = ' '.join(map(str,summary))

    return listtostr

async def text_sentiment(text):
    
    kalimat =[]
    kalimat = text.split('.')
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
            aspect['subjectivity'] = TextBlob(aspect['desc']).subjectivity
            aspect['polarity'] = TextBlob(aspect['desc']).polarity
            

            if aspect['subjectivity'] > 0 and aspect['polarity'] > 0:
                aspect['sentiment'] = "Positive"
            else:
                aspect['sentiment'] = "Negative"

    return aspects
    
