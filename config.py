import requests

api_url='https://pgorelease.nianticlabs.com/plfe/rpc'
login_url='https://sso.pokemon.com/sso/login?service=https%3A%2F%2Fsso.pokemon.com%2Fsso%2Foauth2.0%2FcallbackAuthorize'
login_oauth='https://sso.pokemon.com/sso/oauth2.0/accessToken'

proxies = {
  'http': 'http://127.0.0.1:8888',
  'https': 'http://127.0.0.1:8888',
}
use_proxy=False
debug=True
google=True

s=requests.session()
if use_proxy:
	s.proxies.update(proxies)
	s.verify=False
s.headers.update({'User-Agent':'Niantic App'})
