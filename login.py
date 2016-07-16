# -*- coding: utf-8 -*-
import config
import json
import re
from collections import OrderedDict

def login_pokemon(user,passw):
	print '[!] doing login for:',user
	try:
		head={'User-Agent':'niantic'}
		r=config.s.get(config.login_url,headers=head)
		jdata=json.loads(r.content)
		data={'lt':jdata['lt'],
			'execution':jdata['execution'],
			'_eventId':'submit',
			'username':user,
			'password':passw}
		r1=config.s.post(config.login_url,data=data,headers=head)
		if 'errors' in r1.content:
			print json.loads(r1.content)['errors'][0].replace('&#039;','\'')
			return None
		ticket=re.sub('.*ticket=','',r1.history[0].headers['Location'])
		data1={'client_id':'mobile-app_pokemon-go',
				'redirect_uri':'https://www.nianticlabconfig.s.com/pokemongo/error',
				'client_secret':'w8ScCUXJQc6kXKw8FiOhd8Fixzht18Dq3PEVkUCP5ZPxtgyWsbTvWHFLm2wNY0JR',
				'grant_type':'refresh_token',
				'code':ticket}
		r2=config.s.post(config.login_oauth,data=data1)
		if 'error=' in r2.content:
			print '[-] pokemon attacking the login server'
			return None
		access_token=re.sub('&expireconfig.s.*','',r2.content)
		access_token=re.sub('.*access_token=','',access_token)
		return access_token
	except:
		print '[-] pokemon attacking the login server'
		return None
	
def login_google(email,passw):
	try:
		config.s.headers.update({'User-Agent':'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H143'})
		first='https://accounts.google.com/o/oauth2/auth?client_id=848232511240-73ri3t7plvk96pj4f85uj8otdat2alem.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&response_type=code&scope=openid%20email%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email'
		second='https://accounts.google.com/AccountLoginInfo'
		third='https://accounts.google.com/signin/challenge/sl/password'
		last='https://accounts.google.com/o/oauth2/token'
		r=config.s.get(first)
		
		GALX= re.search('<input type="hidden" name="GALX" value=".*">',r.content)
		gxf= re.search('<input type="hidden" name="gxf" value=".*:.*">',r.content)
		cont = re.search('<input type="hidden" name="continue" value=".*">',r.content)
		
		GALX=re.sub('.*value="','',GALX.group(0))
		GALX=re.sub('".*','',GALX)
		
		gxf=re.sub('.*value="','',gxf.group(0))
		gxf=re.sub('".*','',gxf)
		
		cont=re.sub('.*value="','',cont.group(0))
		cont=re.sub('".*','',cont)
		
		data1={'Page':'PasswordSeparationSignIn',
				'GALX':GALX,
				'gxf':gxf,
				'continue':cont,
				'ltmpl':'embedded',
				'scc':'1',
				'sarp':'1',
				'oauth':'1',
				'ProfileInformation':'',
				'_utf8':'?',
				'bgresponse':'js_disabled',
				'Email':email,
				'signIn':'Next'}
		r1=config.s.post(second,data=data1)
		
		profile= re.search('<input id="profile-information" name="ProfileInformation" type="hidden" value=".*">',r1.content)
		gxf= re.search('<input type="hidden" name="gxf" value=".*:.*">',r1.content)

		gxf=re.sub('.*value="','',gxf.group(0))
		gxf=re.sub('".*','',gxf)
		
		profile=re.sub('.*value="','',profile.group(0))
		profile=re.sub('".*','',profile)

		data2={'Page':'PasswordSeparationSignIn',
				'GALX':GALX,
				'gxf':gxf,
				'continue':cont,
				'ltmpl':'embedded',
				'scc':'1',
				'sarp':'1',
				'oauth':'1',
				'ProfileInformation':profile,
				'_utf8':'?',
				'bgresponse':'js_disabled',
				'Email':email,
				'Passwd':passw,
				'signIn':'Sign in',
				'PersistentCookie':'yes'}
		r2=config.s.post(third,data=data2)
		#thanks Nostrademous
		try:
			fourth= r2.history[1].headers['Location'].replace('amp%3B','')
		except:
			fourth= r2.history[0].headers['Location'].replace('amp%3B','')
		r3=config.s.get(fourth)
		
		client_id=re.search('client_id=.*&from_login',fourth)
		client_id= re.sub('.*_id=','',client_id.group(0))
		client_id= re.sub('&from.*','',client_id)
		
		state_wrapper= re.search('<input id="state_wrapper" type="hidden" name="state_wrapper" value=".*">',r3.content)
		state_wrapper=re.sub('.*state_wrapper" value="','',state_wrapper.group(0))
		state_wrapper=re.sub('"><input type="hidden" .*','',state_wrapper)

		connect_approve=re.search('<form id="connect-approve" action=".*" method="POST" style="display: inline;">',r3.content)
		connect_approve=re.sub('.*action="','',connect_approve.group(0))
		connect_approve=re.sub('" me.*','',connect_approve)

		data3 = OrderedDict([('bgresponse', 'js_disabled'), ('_utf8', '☃'), ('state_wrapper', state_wrapper), ('submit_access', 'true')])
		r4=config.s.post(connect_approve.replace('amp;',''),data=data3)

		code= re.search('<input id="code" type="text" readonly="readonly" value=".*" style=".*" onclick=".*;" />',r4.content)
		code=re.sub('.*value="','',code.group(0))
		code=re.sub('" style.*','',code)

		data4={'client_id':client_id,
			'client_secret':'NCjF1TLi2CcY6t5mt0ZveuL7',
			'code':code,
			'grant_type':'authorization_code',
			'redirect_uri':'urn:ietf:wg:oauth:2.0:oob',
			'scope':'openid email https://www.googleapis.com/auth/userinfo.email'}
		r5=config.s.post(last,data=data4)
		return json.loads(r5.content)
	except:
		print '[-] problem in google login..'
		return None