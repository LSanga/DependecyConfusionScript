Python 2
require jq and npm

This script will search all the package.json file throught the github of an organization and will check all the dependencies found inside. If they are not found on the public npm repository, it means they could be vulnerable to the dependency confusion attack.

Usage:
python check-github-npm.py -t [organization]
python check-github-npm.py -t netflix

By default it will only print not found dependencies, enable verbose output with -v (is it recommended to redirect to a file)

TODO:
-convert to python3
-add option to supply a list of organization from a file
-add native option to write output to file(s)

