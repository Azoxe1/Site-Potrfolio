import requests

url = 'http://127.0.0.1:8000/api/v1/details/'

r = requests.get(url, headers={
  'Authorization': 'Token 7e1c16f1d4f076338b49b4bf3903c778df205c9a'
  }
)

print(r.text)