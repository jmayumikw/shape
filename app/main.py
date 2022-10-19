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
def encode(num: int = Path(title="The number that will be encoded", ge = 0, le=99999999)):
  s = []
  while True:
    num, r = divmod(num, BASE)
    s.append(find_key(r))
    if num == 0: break
  s = ''.join(reversed(s))
  return s.rjust(6, '-')

@app.get("/decode/{code}")
async def decode(code: str = Query(min_length=6, max_length=6, regex=char_list)):
  if len(code) != 6:
    raise HTTPException(status_code=422, detail="Invalid size")
  n = 0
  for c in code:
    if c == "-":
      n = 0
    else:
      n = n * BASE + dict_char[c]
  return n