import pickle
import zlib

inp = open('hero.pkl' , 'rb')

mismatchedHeroes = pickle.load(inp)

print mismatchedHeroes['SPIDER-MAN/PETER PAR'][:10]
