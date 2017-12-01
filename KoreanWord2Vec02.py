#-*- coding: utf-8 -*-

import nltk
from nltk import word_tokenize, sent_tokenize
import gensim
from gensim.models.word2vec import Word2Vec

# MYSQL CONNECTION
from sqlalchemy import create_engine

# KoNLPy
from konlpy.tag import Twitter
twitter = Twitter()

engine = create_engine('mysql+mysqlconnector://safty:Cndqnreo!@#$@1.246.219.220/product_safty')


KoreanDocuments = []

with engine.connect() as con:

    #rs = con.execute('SELECT 5')

    #data = rs.fetchone()[0]

    #print(u"Data: %s" % data) 

    result = con.execute("SELECT ppom_cont_index, board_num, board_title as title, content FROM ppomppu_contents LIMIT 1000")

    for row in result:
        KoreanDocuments.append(row['title'] + row['content'])

#print(word_tokenize(KoreanDocuments[0]))

KoreanTokenizedDocuments = [twitter.pos(i, norm=True, stem=True) for i in KoreanDocuments]

print(KoreanTokenizedDocuments)

KoreanTokenizedTerms = []

for KoreanTokenizedDocument in KoreanTokenizedDocuments:
    KoreanTokenizedTerms.append([term[0] for term in KoreanTokenizedDocument if (term[1] in ('Noun','Adjective','Verb'))])

#print(KoreanTokenizedSentences[:5])


print(KoreanTokenizedTerms)


model = Word2Vec(sentences=KoreanTokenizedTerms, size=64, sg=1, window=10, min_count=1, seed=42, workers=8)

model.save('KoreanWord2Vec.w2v')

print(u"==================================")
print(u"삼성 Similarity Words:")
print(u"==================================")

for word in model.most_similar(positive=[u'삼성'], negative=[], topn=30):
    print("==> " + str(word))

print("\n")

print(u"==================================")
print(u"스마트폰 Similarity Words:")
print(u"==================================")

for word in model.most_similar(positive=[u'스마트폰'], negative=[], topn=30):
    print("==> " + str(word))
