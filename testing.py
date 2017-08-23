

d1 = dict()
d1.update({'55.71':[1, 2, 3]})
d1.update({'55.72':[4, 5, 6]})

d2 = dict()
d2.update({'55.73':[7, 8, 9]})
d2.update({'55.72':[10, 11, 12]})

dm = d1.copy()
dm = dm.update(d2)

print dm




