#! /anaconda3/envs/maga/bin/python

# from pymystem3 import Mystem
import fileinput
import pickle
from leventype import edit_distance
from leventype import c1_close_to_c2

# метод со списокм слов; работает только на леммах, зато сильно быстрее
# with open('pldf-win.txt') as f:
#     allwds = set(map(lambda x: x.strip(), f.readlines()))
# with open('allwds.pickle', 'wb') as f:
#     pickle.dump(allwds, f)
# with open('allwds.pickle', 'rb') as f:
#     allwds = pickle.load(f)
#
#
# closest = {
# 'й': set('цфы'),
# 'ц': set('йфыву'),
# 'у': set('цывак'),
# 'к': set('увапе'),
# 'е': set('капрн'),
# 'н': set('епрог'),
# 'г': set('нролш'),
# 'ш': set('голдщ'),
# 'щ': set('шлджз'),
# 'з': set('щджэх'),
# 'х': set('зжэ\ъ'),
# 'ъ': set('хэ\\'),
# 'ф': set('йцычя]'),
# 'ы': set('йцувсчяф'),
# 'в': set('цукамсчы'),
# 'а': set('укепимсв'),
# 'п': set('акенртим'),
# 'р': set('енгоьтип'),
# 'о': set('нгшлбьтр'),
# 'л': set('гшщдюбьо'),
# 'д': set('шщзж.юбл'),
# 'ж': set('щзхэ.юд'),
# 'э': set('зхъ\.ж'),
# ']': set('фя'),
# 'я': set('фыч'),
# 'ч': set('яфывс'),
# 'с': set('чывам'),
# 'м': set('свапи'),
# 'и': set('мапрт'),
# 'т': set('ипроь'),
# 'ь': set('тролб'),
# 'б': set('ьолдю'),
# 'ю': set('блдж.'),
# '.': set('юджэ')
# }
#
#
# def get_neighbours(word):
#     "All edits that are one edit away from `word`."
#     word = word.strip()
#     letters    = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
#     splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
#     deletes    = [L + R[1:]               for L, R in splits if R]
#     transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
#     replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
#     inserts    = [L + c + R               for L, R in splits for c in letters]
#     # с_replaces = [L + c + R[1:]           for L, R in splits if R for c in closest[R[0]]]
#     # с_inserts  = [L + c + R               for L, R in splits for c in closest[R[0]]]
#     # except:
#     #     print('ERROR in {}'.format(word))
#     #     print(splits)
#     return set(deletes + transposes + replaces + inserts)
#     # return set(deletes + transposes + replaces + inserts + с_replaces + с_inserts)
#
#
# def find_real(candidates):
#     real = []
#     for wd in candidates:
#         # print(wd)
#         # метод со списком слов
#         if wd in allwds:
#             real.append(wd)
#         # метод с майстемом
#         # a = m.analyze(wd)
#         # if len(a[0]['analysis'])>0:
#         #     if not 'qual' in a[0]['analysis'][0]:
#         #         real.append(wd)
#     return real

for line in fileinput.input():
    if 'none' not in line:
        try: # this is to work with both echo "wd" and real input
            wd = line.strip().split()[1]
        except:
            wd = line.strip()
        edist = [(0,)]
        error = 3
        candidates = []
        with open('lyashar.txt') as f:
            for llline in f:
                normwd, freq  = llline.split('\t')
                # if float(freq) <= 1000:
                now = edit_distance(wd, normwd)
                if edist[0][0] == 0 or edist[0][0] > now[0]:
                    edist = [now]
                    candidates = [(normwd, freq)]
                elif edist[0][0] == now[0]:
                    candidates.append((normwd, freq))
                    edist.append(now)
        print(candidates)
        print(edist)
        winner = sorted(candidates, key=lambda x: float(x[1]))[-1]
        print(line.strip(), '\t', winner[0], '\t', edist[candidates.index(winner)])





# print(edit_distance('роно', 'шлюз'))
# print(c1_close_to_c2(']', 'я'))
