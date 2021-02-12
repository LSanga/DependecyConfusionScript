#this script will check which packages exists on official Pypi repository
#it is useful for check which one could be subject to dependency confusion attack

import requests
from lxml import html

file = "pip-packages.txt"
with open (file,"r") as f:
	for package in f:
		package = package.replace("\n","")
		print (package)

		response = requests.get("https://pypi.org/project/"+package+"/")
		if (response.status_code == 200):
			print (package)
		else:
			#print ("%s do not exist" %(package))
			pass

