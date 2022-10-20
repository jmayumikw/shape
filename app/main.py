
import string
from unittest import result
from fastapi import FastAPI, Path, HTTPException
app = FastAPI()

CHAR_LIST = string.ascii_uppercase + string.ascii_lowercase + string.digits + '!@#$%*()|_=+^/?'
BASE = len(CHAR_LIST)
DICT_CHAR = { CHAR_LIST[i]: i for i in range(len(CHAR_LIST))}

def find_key(value):
  for key, val in DICT_CHAR.items():
    if val == value:
      return key

@app.get("/encode/{num}")
def encode(num: int = Path(title = "The number that will be encoded", ge = 0, le=99999999)):
  res_list = []
  while True:
    num, rest = divmod(num, BASE)
    res_list.append(find_key(rest))
    if num == 0: break
  result = ''.join(reversed(res_list))
  return {"encode": result.rjust(6, '-')}

@app.get("/decode/{code}")
def decode(code: str):
  if len(code) != 6:
    raise HTTPException(status_code = 422, detail = "Invalid length")
  result = 0
  for char in code:
    if char == "-":
      result = 0
    else:
      try:
        result = result * BASE + DICT_CHAR[char]
      except:
        raise HTTPException(status_code = 422, detail = "Invalid input")
  return {"decode": result}
