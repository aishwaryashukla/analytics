import nltk

nltk.download('vader_lexicon')
nltk.download('punkt')

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import sentiment
from nltk import word_tokenize


sid = SentimentIntensityAnalyzer()
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

f = open('file.txt')
fmwildfires1 = f.read()
sentences = tokenizer.tokenize(fmwildfires1)
print(sentences)

total_compound = 0
for sentence in sentences:
    #    print(sentence)
    scores = sid.polarity_scores(sentence)
    print(scores['compound'])
    total_compound = total_compound + scores['compound']
#    for key in sorted(scores):
#        print('{0}: {1}, '.format(key, scores[key]), end='')
#    print()
print('Total sentiment score= {0}'.format(total_compound))