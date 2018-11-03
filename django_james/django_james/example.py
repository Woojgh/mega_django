API_ENDPOINT = 'https://discordapp.com/api/v6'
CLIENT_ID = '507528707519545348'
CLIENT_SECRET = '-IdZfWDS9mi7r4MTURA_hBL_zzn8CbTe'
REDIRECT_URI = 'http://localhost:8000'

def exchange_code(code):
  data = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': REDIRECT_URI,
    'scope': 'identify email connections'
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  import pdb; pdb.set_trace()
  r = requests.post('%s/oauth2/token' % API_ENDPOINT, data, headers)
  r.raise_for_status()
  print(r.json())
  return r.json()