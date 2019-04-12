import requests, json, io, subprocess, argparse
from string import punctuation


newPackagesJson = {}

def remove_special_chars(package_name):
    package_name = package_name.replace('/', '-')
    package_name = package_name.replace('@', '')
    for special_char in list(punctuation):
        if package_name.find(special_char) != -1 and special_char != ('-' and '_'):
            package_name.replace(special_char, '')
    return package_name

def getRequests(param, compare_value, carrot):
    try:
        print("Checking '{}' for updates".format(param))
        correctPackage = None
        req = requests.get('https://www.npmjs.com/search/suggestions?q={}'.format(param))
        reqJson = req.json()
        correctPackage = [package if package['name'] == param else None for package in reqJson][0]
        if correctPackage is None: raise AttributeError
        if correctPackage['version'] > compare_value:
            toList = correctPackage['version'].replace('.', ' ').split()
            carrotComprehension = [carrot] + toList if carrot is not None else correctPackage['version']
            return carrotComprehension
        else:
            toList = compare_value.replace('.', ' ').split()
            carrotComprehension = [carrot] + toList if carrot is not None else compare_value
            return carrotComprehension
    except AttributeError:
        print('{} package not found. Package could be deprecated.'.format(param))

def write_new_json(data, original_packagejson, filePath):
    if args['dnr'] == False:
        os.remove('{}/package.json'.format(filePath))
    original_packagejson['dependencies'] = data
    with open('package.json' if args['dnr'] else 'package_dependency_plus.json', 'w') as outfile:
        json.dump(original_packagejson, outfile)

def checkDependencyVersions(filePath):
    with open(filePath) as fileObj:
        packagesJson = json.load(fileObj)
        for packageName, versionNumber in packagesJson['dependencies'].items():
            if 'git' not in versionNumber:
                carrot = '^' if '^' in versionNumber else None
                val = getRequests(remove_special_chars(packageName), versionNumber, carrot)
                newPackagesJson[packageName] = val
    write_new_json(newPackagesJson, packagesJson, filePath)


def npm_install():
    print('Running npm install...')
    proc = subprocess.Popen(['npm', 'install'], stdout=subprocess.PIPE)
    for line in io.TextIOWrapper((proc.stdout), proc):
        print(line)
    print('Operation complete.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Dependency+', description='Check for latest version and upgrade npm package.json dependencies')
    parser.add_argument('-f', '--file', type=str, required=True, help='package.json file path; absolute or relative.')
    parser.add_argument('-n', '--npm', type=bool, default=False, required=False, help='npm install new package.json')
    parser.add_argument('--dnr', type=bool, default=False, required=False, help='do not remove existing project package.json')
    args = vars(parser.parse_args())

    if args['npm']:
        print('npm install enabled.')
        checkDependencyVersions(args['file'])
        npm_install()
    else:
        checkDependencyVersions(args['file'])
