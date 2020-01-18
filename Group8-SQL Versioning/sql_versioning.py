"""

@author ozanselte

Todo:
    * integration for group plan: check below.
"""

import os
import json
import requests
from base64 import b64decode, b64encode

t_path = './temps/'
v_path = './versions/'

def send_to_plan(obj, status):
	"""
	@param obj: json object.
	@param status: true when pass, false when reject.
	"""
	pass

def save_file(path, cont):
	ff = open(path, 'w')
	ff.write(cont)
	ff.close()

def get_file(path):
	ff = open(path, 'r')
	cont = ff.read()
	ff.close()
	return cont

def version_file(filename):
	os.popen('cp ' + t_path + '/' + filename + ' ' + v_path + '/' + filename)
	os.popen('git -C ' + v_path + ' add ' + filename)
	os.popen('git -C ' + v_path + ' commit -m "' + filename + '"')
	os.popen('rm -f ' + t_path + '/' + filename)

def main(json_str):
	obj = json.loads(json_str)
	obj['destination'] = obj['origin']

	# get_script operasyonu iptal, README'yi kontrol edin.
	# kullanilmayacak ama kalsin.
	if 'get_script' == obj['op']: 
		is_exists = os.path.exists(v_path+obj['name'])
		if is_exists:
			decoded = get_file(v_path+obj['name'])
			obj['file'] = b64encode(bytes(decoded, 'utf-8')).decode('utf-8')
			obj['op'] = '?' #TODO: OPERATE
		else:
			#TODO: script yok hata gonder OPERATE
			print('Error, olmayan script istendi.')


	elif 'version' == obj['op']:
		decoded = b64decode(obj['file']).decode('utf-8')
		save_file(t_path+obj['name'], decoded)
		is_exists = os.path.exists(v_path+obj['name'])
		if is_exists:
			obj['destination'] = 9
			obj['new'] = obj['file']
			decoded = get_file(v_path+obj['name'])
			obj['old'] = b64encode(bytes(decoded, 'utf-8')).decode('utf-8')
			obj['reminder'] = obj['origin']
		else:
			version_file(obj['name'])
		del obj['file']
		print('x')
	elif 'check' == obj['op']:
		obj['origin'] = obj['reminder']
		if obj['result']:
			version_file(obj['name'])
			# TODO versiyonlandi:
			# Grup 2'ye -plan- result true olarak gonderilecek.
			# {"origin": 8, "destination": 2, "name": "b", "result": true}
		else:
			print('Error, versiyonlanamadi')
			# TODO versiyonlanmadi:
			# Grup 2'ye -plan- result false olarak gönderilecek.
			# {"origin": 8, "destination": 2, "name": "b", "result": false}
	obj['origin'] = 8
	del obj['op']
	body = json.dumps(obj)
	print(body)
	requests.post("http://localhost:8081/", json=obj)

json_str = """
{
	"origin": 9,
	"destination": 8,
	"op": "check",
	"name": "b",
	"result": false
}
"""

main(json_str)