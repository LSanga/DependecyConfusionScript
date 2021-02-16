#python 2

#this script will search all the package.json file from an organization on github, extract all the dependencies and check if they exist on public NPM repository
#the ones that doesn't exist could be vulnerable to a dependency confusion attack

#if launched with verbose, is it recommended to save the output to a file
#python check-github-npm.py > results.txt

#it require jq and npm

import subprocess
import argparse

parser=argparse.ArgumentParser(description='''Check NPM dependencies across organizations in GitHub''')
parser.add_argument('--verbose', '-v', default=False, required=False, action='store_true', help='show verbose output')
parser.add_argument('--target', '-t', default=True, required=False, help='single target organization')
args = parser.parse_args()

if args.target:
    organization = args.target
    

#extract all package.json file from an organization on Github
extract_packages = 'curl -s -H "Accept: application/vnd.github.v3+json" "https://api.github.com/search/code?q=JSON&q=org%3A'+organization+'+filename%3Apackage.json&type=Code" | jq -r ".items[].git_url"'
p = subprocess.Popen(extract_packages, stdout=subprocess.PIPE, shell=True)
(packages, err) = p.communicate()
packages = packages.split()

#for every package, find all dependecies
for package in packages:
    #print (package)
    package = package.decode()
    
    #extract all dependencies
    find_dependencies = "curl -s -H 'Accept: application/vnd.github.v3.raw' '"+str(package)+"' |  jq -r '.dependencies,.devDependencies | keys? | .[]'"
    
    p = subprocess.Popen(find_dependencies, stdout=subprocess.PIPE, shell=True)
    (dependencies, err) = p.communicate()
    dependencies = dependencies.split()
    
    for dependency in dependencies:
        #print (dependency)
        dependency = dependency.decode()
        check_dependency = "npm info "+dependency+" 2>&1 > /dev/null || echo 404 && echo 200"
        p = subprocess.Popen(check_dependency, stdout=subprocess.PIPE, shell=True)
        (result, err) = p.communicate()
        result = result.split()

        if not args.verbose:
            if int(result[0]) != 200:
                print("%s,%s" % (dependency,result[0]))
        else:
            print("%s,%s" % (dependency,result[0]))
