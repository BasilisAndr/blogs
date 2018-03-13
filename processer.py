#! /Users/user/myproject/venv/anaconda3/envs/maga/bin/python

import fileinput
from pymystem3 import Mystem

m = Mystem()

for line in fileinput.input():
# 	a = m.analyze(line.strip())
# 	print(a)
	try:
		a = m.analyze(line.strip())[0]['analysis'] #[0]['qual']
		if len(a) == 0:
			print(line.strip())
# 			print()
		else:
			if 'qual' in a[0]:
				print(line.strip())
# 				print()
	except:
		continue

