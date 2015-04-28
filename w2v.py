import codecs
import word2vec
from translate import Translator

# print word2vec.word2vec("1.txt", "1.bin")
translator = Translator(to_lang='ru')
model = word2vec.load("vectors.bin")
while True:
    try:
        idx, metrics = model.cosine(raw_input())
        words = model.generate_response(idx, metrics).tolist()
        for word, prob in words:
            print word, prob, translator.translate(word)
    except KeyError:
        print "not found"