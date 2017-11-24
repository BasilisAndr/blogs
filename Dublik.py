with open('D:\bare-guessed-bmr.txt') as f:
    res = f.readlines()
print(*set(filter(lambda x: res.count(x) > 1, res)))
