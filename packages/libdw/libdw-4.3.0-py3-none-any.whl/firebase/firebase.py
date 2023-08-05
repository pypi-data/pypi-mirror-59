import json, urllib.request, urllib.error, urllib.parse

class FirebaseApplication():
	def __init__(self, url, token):
		self.url=url
		self.firebaseToken=token

	def put(self, root,node, data):
		json_url=self.url+root+node
		opener = urllib.request.build_opener(urllib.request.HTTPHandler)
		request = urllib.request.Request(json_url+'.json?auth='+self.firebaseToken, 
			data=json.dumps(data).encode('utf-8'))

		request.add_header('Content-Type', 'your/contenttype')
		request.get_method = lambda: 'PUT'
		result = opener.open(request)
		if result.getcode()==200:
			return "OK"
		else:
			return "ERROR"

	def post(self, newnode, data):
		json_url=self.url+newnode		
		opener = urllib.request.build_opener(urllib.request.HTTPHandler)
		request = urllib.request.Request(json_url+'.json?auth='+self.firebaseToken, 
			data=json.dumps(data).encode('utf-8'))

		request.add_header('Content-Type', 'your/contenttype')
		request.get_method = lambda: 'POST'
		result = opener.open(request)
		if result.getcode()==200:
			return "OK"
		else:
			return "ERROR"

	def get(self, node):
		json_url=self.url+node
		opener = urllib.request.build_opener(urllib.request.HTTPHandler)
		request = urllib.request.Request(json_url+'.json?auth='+self.firebaseToken)
		request.get_method = lambda: 'GET'
		result = opener.open(request)
		return json.loads(result.read().decode('utf-8'))
