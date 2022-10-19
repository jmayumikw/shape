from fastapi import FastAPI, Path, Query, HTTPException
import string
app = FastAPI()

char_list = string.ascii_uppercase + string.ascii_lowercase + string.digits + '!@#$%*()|_=+^/?'
BASE = len(char_list)
dict_char = { char_list[i]: i for i in range(len(char_list))}

def find_key(value):
  for k, v in dict_char.items():
    if v == value:
      return k

@app.get('/')
def root():
  return { "message": "HEllo" }

@app.get("/encode/{num}")
def encode(num: int = Path(title="The ID of the item to get", ge = 0, le=99999999)):
  if num < 0:
    raise HTTPException(status_code=404, detail="Invalid number")
  s = []
  while True:
    num, r = divmod(num, BASE)
    print(num, r)
    s.append(find_key(r))
    print(s)
    if num == 0: break
  s = ''.join(reversed(s))
  return s.rjust(6, '-')

@app.get("/decode/{code}")
def decode(code: str):
  n = 0
  for c in code:
    if c == "-":
      n = 0
    else:
      n = n * BASE + dict_char[c]
      print(n)
  return n