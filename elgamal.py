import time, random, prime
from math import log10, floor
from math_tools import mod_power
import prime
import reader_writer

def key_generator():
    prim = prime.Prime()    
    p = prim.generate_prime()
    g = random.randint(2, p-1)
    x = random.randint(1, p-2)
    y = mod_power(g, x, p)

    reader_writer.key_write('y=' + str(y) + '\n' + 'g=' + str(g) + '\n' + 'p=' + str(p), 'elgamal_pubkey.pub')
    reader_writer.key_write('x=' + str(x) + '\n' + 'p=' + str(p), 'elgamal_prikey.pri')

def encrypt_elgamal(plaintext):
    key_generator()
    text = reader_writer.key_read('elgamal_pubkey.pub')
    keys = text.split('\n')
    y = int(keys[0][2:])
    g = int(keys[1][2:])
    p = int(keys[2][2:])

    block_length = floor(log10(p - 1) + 1)

    plaintext = reader_writer.text_to_num(plaintext)

    plains = [plaintext[i:min(i+block_length, len(plaintext))] for i in range(0, len(plaintext), block_length)]

    ciphers = []
    
    k = random.randint(1, p-2)
    for plain in plains:
        a = str(mod_power(g, k, p))
        padded_a = (block_length - len(a)) * '0' + a
        pre_b = int(plain) * mod_power(y, k, p) % p
        b = str(pre_b)
        padded_b = (block_length - len(b)) * '0' + b        
        ciphers.append(padded_a)
        ciphers.append(padded_b)
    return ''.join(ciphers)

def decrypt_elgamal(ciphertext):
    text = reader_writer.key_read('elgamal_prikey.pri')
    keys = text.split('\n')
    x = int(keys[0][2:])
    p = int(keys[1][2:])

    block_length = floor(log10(p - 1) + 1)

    ciphers = [ciphertext[i:min(i+2*block_length, len(ciphertext))] for i in range(0, len(ciphertext), 2*block_length)]

    plains = []
    for cipher in ciphers:
        a, b = cipher[:block_length], cipher[block_length:]
        plain = str((int(b) * (mod_power(int(a), p - 1 - x, p))) % p)
        padded_plain = (block_length - len(plain)) * '0' + plain
        plains.append(reader_writer.num_to_text(padded_plain))
    return ''.join(plains)

print('Masukkan plainteks:')
hasil = encrypt_elgamal(input())
print('Berikut adalah hasil enkripsi:', hasil)
hasil = ''.join([str(i) for i in hasil])
print('Berikut adalah hasil dekripsi dari enkripsi sebelumnya:', decrypt_elgamal(hasil))
