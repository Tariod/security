from vigenere_cipher import vigenere_cipher

encoded = 'Yx`7cen7v7ergrvc~yp:|rn7OXE7t~g.re97R9p97~c7d.xb{s7cv|r7v7dce~yp75.r{{x7`xe{' \
          's57vys;7p~ary7c.r7|rn7~d75|rn5;7oxe7c.r7q~edc7{rccre75.57`~c.75|5;7c.ry7oxe75r57`~c.75r5;7c.ry75{' \
          '57`~c.75n5;7vys7c.ry7oxe7yroc7t.ve75{' \
          r'57`~c.75|57vpv~y;7c.ry75x57`~c.75r57vys7dx7xy97Nxb7zvn7bdr7vy7~ysro7xq7tx~yt~srytr;7_vzz~yp7s~dcvytr;7\vd' \
          '~d|~7rovz~yvc~xy;7dcvc~dc~tv{7crdcd7xe7`.vcrare7zrc.xs7nxb7qrr{7`xb{s7d.x`7c.r7urdc7erdb{c9 '

ALPHABET_SIZE = 256
with open('part_02/decoded.txt', 'w') as file:
    for key in range(ALPHABET_SIZE):
        file.write(f'Key {key}: {vigenere_cipher(encoded.encode(), chr(key).encode())}\n')

# KEY := 23
