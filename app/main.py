
import string
from fastapi import FastAPI, Path, HTTPException

tags_metadata = [
    {
        "name": "encode",
        "description": "This endpoint encode a number and return a string",
    },
    {
        "name": "decode",
        "description": "This endpoint decode a string and return a number",
    },
]


app = FastAPI(openapi_tags=tags_metadata)

CHAR_LIST = string.ascii_uppercase + string.ascii_lowercase + string.digits + '!@#$%*()|_=+^/?'
BASE = len(CHAR_LIST)
DICT_CHAR = { CHAR_LIST[i]: i for i in range(len(CHAR_LIST))}

def find_key(value):
  """
    This function find the key of value from a dictionary and returns a key
  """
  for key, val in DICT_CHAR.items():
    if val == value:
      return key
  raise TypeError("Only integers are allowed")

@app.get("/encode/{num}")
def encode(num: int = Path(title = "The number that will be encoded", ge = 0, le=99999999)):
  """
    This endpoint encode a number and return a string
  """
  res_list = []
  # use the same logic from binary encoding, but uses the DICT_CHAR
  while True:
    num, rest = divmod(num, BASE)
    res_list.append(find_key(rest))
    if num == 0: break
  result = ''.join(reversed(res_list))
  return {"encode": result.rjust(6, '-')}

@app.get("/decode/{code}")
def decode(code: str):
  """
    This endpoint decode a string and return a number
  """
  if len(code) != 6:
    raise HTTPException(status_code = 422, detail = "Invalid length")
  result = 0
  # use the same logic for binary decoding to a number, but uses de DICT_CHAR
  for char in code:
    if char == "-":
      result = 0
    else:
      try:
        result = result * BASE + DICT_CHAR[char]
      except:
        raise HTTPException(status_code = 422, detail = "Invalid input")
  return {"decode": result}
