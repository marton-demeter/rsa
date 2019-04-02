import sys
import random
import math
import os
import time
import base64

def save_key(key, filename, type):
  file = open(filename, 'w')
  file.write('-----BEGIN RSA '+type+' KEY-----')
  for idx,char in enumerate(key):
    if idx % 64 == 0:
      file.write('\n')
    file.write(char)
  file.write('\n-----END RSA '+type+' KEY-----')
  file.close()

def power(a, n, p):
  res = 1
  while n > 0:
    if n & 1:
      res = (res * a) % p
    a = (a * a) % p
    n = n >> 1
  return res

def prime_fermat(n, k = 11):
  if n % 2 == 0 or n < 2:
    return False
  for i in range(0, k):
    a = random.randint(1, n-1)
    if power(a, n-1, n) != 1:
      return False
  return True

def is_prime(n):
  return prime_fermat(n)

def random_number_generator(bits = 2048):
  return int(os.urandom(int(bits/8)).hex(), 16)

def prime_candidate_generator(bits = 2048):
  p = random_number_generator(bits)
  while p % 2 == 0:
    p = random_number_generator(bits)
  return p

def egcd(a, b):
  if a == 0:
    return (b, 0, 1)
  else:
    g, y, x = egcd(b % a, a)
  return (g, x - (b // a) * y, y)

def modinv(a, m):
  g, x, y = egcd(a, m)
  return x % m

def generate_key(length = 4096):
  p = prime_candidate_generator(length / 2)
  q = prime_candidate_generator(length / 2)
  while not is_prime(p):
    p = p + 2
  while not is_prime(q):
    q = q + 2
  n = p * q
  phi = (p - 1) * (q - 1)
  e = 65537
  d = modinv(e, phi)
  return (e,d,n)

def main(username):
  st = time.time()
  ksize = 4096
  if len(sys.argv) == 3:
    ksize = int(sys.argv[2])
  e, d, n = generate_key(ksize)
  e = base64.b64encode(str(e).encode('utf-8')).decode('utf-8')
  d = base64.b64encode(str(d).encode('utf-8')).decode('utf-8')
  n = base64.b64encode(str(n).encode('utf-8')).decode('utf-8')
  save_key(str(d)+'+'+str(n), (username + '.prv'), 'PRIVATE')
  save_key(str(e)+'+'+str(n), (username + '.pub'), 'PUBLIC')
  sys.stdout.write('Generated '+str(ksize)+' bit keys in ')
  sys.stdout.write(str(round(time.time() - st, 2)) + ' seconds\n')

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print('Usage: python gensys.py <username> [<keysize>]')
    exit(1)
  main(sys.argv[1])