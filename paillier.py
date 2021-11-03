import time, prime, random, reader_writer
from math_tools import inverse_modulo, mod_power, fpb
from math import floor, log10

def key_generator():
    while True:
        prim = prime.Prime()
        p = prim.generate_prime()
        q = prim.generate_prime()
        if(fpb(p*q, (p-1)*(q-1))) == 1: break

    n = p*q
    lamda = (p - 1) * (q - 1) // fpb(p-1, q-1) 

    g = random.randint(1, n ** 2 - 1)
    mu = inverse_modulo(((mod_power(g, lamda, n ** 2)) - 1)//n, n)

    reader_writer.key_write('g=' + str(g) + '\n' + 'n=' + str(n), 'paillier_pubkey.pub')
    reader_writer.key_write('l=' + str(lamda) + '\n' + 'm=' + str(mu), 'paillier_prikey.pri')

def encrypt_paillier(plaintext):
    key_generator()
    text = reader_writer.key_read('paillier_pubkey.pub')
    keys = text.split('\n')
    g = int(keys[0][2:])
    n = int(keys[1][2:])

    block_length = floor(log10(n) + 1)

    plaintext = reader_writer.text_to_num(plaintext)

    plains = [plaintext[i:min(i+block_length, len(plaintext))] for i in range(0, len(plaintext), block_length)]

    ciphers = []
    while True:
        r = random.randint(0, n - 1)
        if fpb(r, n) == 1: break

    for plain in plains:
        c = str((mod_power(g, int(plain), (n ** 2))*mod_power(r, n, (n ** 2))) % (n ** 2))
        padded_c = (block_length - len(c)) * '0' + c
        ciphers.append(padded_c)
    return ciphers

def decrypt_paillier(ciphertext):
    text = reader_writer.key_read('paillier_prikey.pri')
    keys = text.split('\n')
    lamda = int(keys[0][2:])
    mu = int(keys[1][2:])

    text = reader_writer.key_read('paillier_pubkey.pub')
    keys = text.split('\n')
    g = int(keys[0][2:])
    n = int(keys[1][2:])

    block_length = floor(log10(n) + 1)

    ciphers = [ciphertext[i:min(i+block_length, len(ciphertext))] for i in range(0, len(ciphertext), block_length)]

    plains = []
    for c in ciphers:
        a = (mod_power(int(c), lamda, (n **2)) - 1) // n
        b = mu % n
        plain = str((a * b) % n)
        padded_plain = (block_length - len(plain)) * '0' + plain
        plains.append(reader_writer.num_to_text(padded_plain))

    return plains

print('Masukkan plainteks:')
hasil = encrypt_paillier(input())
print('Berikut adalah hasil enkripsi:', hasil)
hasil = ''.join([str(i) for i in hasil])
print('Berikut adalah hasil dekripsi dari enkripsi sebelumnya:', decrypt_paillier(hasil))