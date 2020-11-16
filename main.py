#  Квадрат Полібія:
#
#  		+  1  2  3  4  5  6
#  		1  a  b  c  d  e  f
#  		2  g  h  i  j  k  l
#  		3  m  n  o  p  q  r
#  		4  s  t  u  v  w  x
#  		5  y  z  0  1  2  3
#  		6  4  5  6  7  8  9

text = input("Введіть текст:")

keys = {
    'a': 'c', 'b': 'i', 'c': 'p', 'd': 'h',
    'e': 'e', 'f': 'r', 'g': 'a', 'h': 'b',
    'i': 'd', 'j': 'f', 'k': 'g', 'l': 'k',
    'm': 'l', 'n': 'm', 'o': 'n', 'p': 'o',
    'q': 's', 'r': 'q', 's': 't', 't': 'u',
    'u': 'x', 'v': 'w', 'w': 'y', 'x': 'v',
    'y': 'z', 'z': 'u'
}

crypt = ""
for i in text:
    if i in keys:
        crypt += keys[i]
        crypt += " "
print("Зашифрований текст: " + crypt)

temp = ""
decrypt = ""
for i in crypt:
    if i != " ":
        temp += i
    else:
        for j in keys:
            if keys[j] == temp:
                decrypt += j
        temp = ""
print("Розшифрований текст: " + decrypt)
