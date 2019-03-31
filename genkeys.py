import sys
import random
import math
import os
from itertools import compress

def save_key(key, filename):
  file = open(filename, 'w')
  file.write(key)
  file.close()

def power(a, n, p):
  res = 1
  a = a % p
  while n > 0:
    if n & 1:
      res = (res * a) % p
    n = n >> 1
    a = (a * a) % p
  return res

def prime_simple(n):
  if n <= 3:
    return n > 1
  elif n % 2 == 0 or n % 3 == 0:
    return False
  else:
    i = 5
    while i * i <= n:
      if n % i == 0 or n % (i + 2) == 0:
        return False
      i = i + 6
    return True

def prime_fermat(n, k = 3):
  if n % 2 == 0 or n < 2:
    return False
  for i in range(0, k):
    a = random.randint(1, n-1)
    res = power(a, n-1, n)
    if res != 1:
      return False
  return True

def is_prime(n):
  return prime_fermat(n)

def random_number_generator(bytes = 256):
  return int(os.urandom(bytes).hex(), 16)

def generate_key():
  e = d = 0
  while e == d:
    p = q = 0
    while p == q:
      while not is_prime(p):
        p = random_number_generator(2)
      while not is_prime(q):
        q = random_number_generator(2)
    n = p * q
    phi = (p - 1) * (q - 1)
    while True:
        e = random_number_generator(2)
        if (math.gcd(e, phi) == 1) and (e < phi):
          break
    for i in range(1, phi):
      if i * e % phi == 1:
        d = i
        break
  return (e,d,n)


def main(username):
  e, d, n = generate_key()
  print(e,d,n)
  # save_key(str(d)+','+str(n), (username + '.prv'))
  # save_key(str(e)+','+str(n), (username + '.pub'))

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print('Usage: python gensys.py <username> || ./gensys.py <username>')
    exit(1)
  main(sys.argv[1])