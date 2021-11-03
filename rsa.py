import time
from math import floor, log10
import prime
import reader_writer
from math_tools import inverse_modulo, mod_power, fpb

def key_generator(enc_key):
    while True:
        enc_key = int(enc_key)
        prim = prime.Prime()
        p = prim.generate_prime()
        q = prim.generate_prime()
        totient_n = (p-1)*(q-1)
        if fpb(enc_key, totient_n) == 1: break

    n = p*q
    
    dec_key = inverse_modulo(enc_key, totient_n)

    reader_writer.key_write('e=' + str(enc_key) + '\n' + 'n=' + str(n), 'rsa_pubkey.pub')
    reader_writer.key_write('d=' + str(dec_key) + '\n' + 'n=' + str(n), 'rsa_prikey.pri')

def encrypt_rsa(plaintext, enc_key):
    key_generator(enc_key)
    text = reader_writer.key_read('rsa_pubkey.pub')
    keys = text.split('\n')
    n = int(keys[1][2:])

    block_length = floor(log10(n) + 1)

    plaintext = reader_writer.text_to_num(plaintext)

    plains = [plaintext[i:min(i+block_length, len(plaintext))] for i in range(0, len(plaintext), block_length)]

    ciphers = []
    for plain in plains:
        cipher = str(mod_power(int(plain), int(enc_key), n))
        padded_cipher = (block_length - len(cipher)) * '0' + cipher
        ciphers.append(padded_cipher)

    return ''.join(ciphers)

def decrypt_rsa(ciphertext):
    text = reader_writer.key_read('rsa_prikey.pri')
    keys = text.split('\n')
    dec_key = int(keys[0][2:])
    n = int(keys[1][2:])

    block_length = floor(log10(n) + 1)

    ciphers = [ciphertext[i:min(i+block_length, len(ciphertext))] for i in range(0, len(ciphertext), block_length)]

    plains = []
    for cipher in ciphers:
        plain = str(mod_power(int(cipher), dec_key, n))
        padded_plain = (block_length - len(plain)) * '0' + plain
        plains.append(reader_writer.num_to_text(padded_plain))

    return ''.join(plains)
    

print('Masukkan kunci enkripsi:')
enc_key = int(input())
print('Masukkan plainteks:')
plaintext = input()
hasil = encrypt_rsa(plaintext, enc_key)
print('Berikut adalah hasil enkripsi:', hasil)
hasil = ''.join([str(i) for i in hasil])
print('Berikut adalah hasil dekripsi dari enkripsi sebelumnya:', decrypt_rsa(hasil))
