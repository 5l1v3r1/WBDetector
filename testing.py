

a = dict()
d1 = dict({3:[1, 2, 3]})
print d1
a.update({0:d1})
print a
d1.update({5:[5, 3, 2, 1, 4]})
print d1
a.update({0:d1})
print a
# print a
# a.update({0:d2})
# print a
