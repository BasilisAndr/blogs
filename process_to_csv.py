#! /anaconda3/envs/maga/bin/python

import fileinput
from pymystem3 import Mystem

m = Mystem()
print('word;lemma;gr')

for line in fileinput.input():
# 	a = m.analyze(line.strip())
# 	print(a)
	try:
		a = m.analyze(line.strip())[0]['analysis'] #[0]['qual']
		if len(a) == 0:
			print("{};{};{}".format(line.strip(), 'none', 'none'))
# 			print()
		else:
			if 'qual' in a[0]:
				print("{};{};{}".format(line.strip(), a[0]['lex'], a[0]['gr']))
# 				print()
	except:
		continue
