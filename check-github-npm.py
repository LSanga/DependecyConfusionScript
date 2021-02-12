#this script will search all the package.json file from an organization on github, extract all the dependencies and check if they exist on public NPM repository
#the ones that doesn't exist could be vulnerable to a dependency confusion attack

#is it reccomended to save the output on a file or print only the one that doesn't exist (http status 404)
#eg
#python check-github-npm.py > results.txt

import subprocess

organization = "test"

#extract all package.json file from an organization on Github
extract_packages = 'curl -H "Accept: application/vnd.github.v3+json" "https://api.github.com/search/code?q=JSON&q=org%3A'+organization+'+filename%3Apackage.json&type=Code" | jq ".items[].git_url"'
p = subprocess.Popen(extract_packages, stdout=subprocess.PIPE, shell=True)
(packages, err) = p.communicate()
packages = packages.split()

#for every package, find all dependecies
for package in packages:
	package = package.replace('"','')
	print (package)

	#extract all dependencies
	find_dependencies = "curl -H 'Accept: application/vnd.github.v3.raw' '"+package+"' |  jq '.dependencies,.devDependencies | keys? | .[]'"
	p = subprocess.Popen(find_dependencies, stdout=subprocess.PIPE, shell=True)
	(dependencies, err) = p.communicate()
	dependencies = dependencies.split()
	
	for dependency in dependencies:
		dependency = dependency.replace('"','')
		#print (dependency)
		
		check_dependency = "npm info "+dependency+" 2>&1 > /dev/null || echo 404 && echo 200"
		p = subprocess.Popen(check_dependency, stdout=subprocess.PIPE, shell=True)
		(result, err) = p.communicate()
		result = result.split()

		print("%s,%s" % (dependency,result))
