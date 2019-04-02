import sys
import base64
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def quit():
  print('Usage (encrypt): python crypt.py -e <pubkey> <plain> <cipher>')
  print('Usage (decrypt): python crypt.py -d <prvkey> <cipher> <plain>')
  exit(1)

def parse_args(args):
  method = 'e'
  plain = args[2]
  cipher = args[3]
  key = args[1]
  if '-d' in args:
    method = 'd'
    plain = args[3]
    cipher = args[2]
  for idx,arg in enumerate(args):
    if '.txt' in arg:
      plain = args[idx]
    if '.cip' in arg:
      cipher = args[idx]
    if ('.pub' in arg) or ('.prv' in arg):
      key = args[idx]
  return (method,key,plain,cipher)

def power(a, n, p):
  res = 1
  while n > 0:
    if n & 1:
      res = (res * a) % p
    a = (a * a) % p
    n = n >> 1
  return res

def parse_key(filename):
  f = open(filename, 'r')
  fline = f.readline()
  exp, mod = ((f.read())[:-(len(fline)-2)]).split('+')
  f.close()
  exp = int(base64.b64decode(exp.encode('utf-8')))
  mod = int(base64.b64decode(mod.encode('utf-8')))
  return (exp,mod)

def encrypt_aes(ifile, ofile, kfile):
  f = open(ifile, 'r')
  data = (f.read()).encode('utf-8')
  f.close()
  key = os.urandom(int(192/8))
  cipher = AES.new(key, AES.MODE_CBC)
  ct_bytes = cipher.encrypt(pad(data, AES.block_size))
  iv = base64.b64encode(cipher.iv).decode('utf-8')
  ct = base64.b64encode(ct_bytes).decode('utf-8')
  key = encrypt_rsa(int.from_bytes(key, 'big'), kfile)
  key = base64.b64encode(key.encode('utf-8')).decode('utf-8')
  f = open(ofile, 'w')
  f.write(ct+','+iv+','+key)
  f.close()

def decrypt_aes(ifile, ofile, kfile):
  f = open(ifile, 'r')
  ct, iv, key = f.read().split(',')
  f.close()
  key = base64.b64decode(key.encode('utf-8')).decode('utf-8')
  key = decrypt_rsa(key, kfile).to_bytes(int(192/8), 'big')
  c = AES.new(key, AES.MODE_CBC, base64.b64decode(iv))
  pt = unpad(c.decrypt(base64.b64decode(ct)), AES.block_size).decode('utf-8')
  f = open(ofile, 'w')
  f.write(pt)
  f.close()

def encrypt_rsa(data, kfile):
  exp, mod = parse_key(kfile)
  return str(power(data, exp, mod))

def decrypt_rsa(data, kfile):
  exp, mod = parse_key(kfile)
  return power(int(data), exp, mod)

def main(m, k, p, c):
  if m == 'e':
    encrypt_aes(p, c, k)
  if m == 'd':
    decrypt_aes(c, p, k)

if __name__ == '__main__':
  if sys.version_info[0] != 3:
    print('Use python 3.')
    exit(1)
  if len(sys.argv) != 5:
    quit()
  if not ('-e' in sys.argv or '-d' in sys.argv):
    quit()
  m, k, p, c = parse_args(sys.argv[1:])
  main(m, k, p, c)
