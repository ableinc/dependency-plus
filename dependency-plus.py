
import requests, json, io, subprocess, argparse, os, sys
from string import punctuation


newDependencies = {}
packagesNotFound = []
# specialCharDict = {}


def remove_special_chars(package_name):
    _package_name = package_name.replace('/', '-')
    # if _package_name != package_name: specialCharDict[_package_name] = package_name
    _package_name = package_name.replace('@', '')
    # if _package_name != package_name: specialCharDict[_package_name] = package_name
    for special_char in list(punctuation):
        if _package_name.find(special_char) != -1 and special_char != ('-' and '_'):
            _package_name.replace(special_char, '')
    return _package_name


def get_requests(param, old_version, carrot):
    try:
        print("Checking '{}' for updates".format(param))
        correct_package = None
        req = requests.get('https://www.npmjs.com/search/suggestions?q={}'.format(param))
        req_json = req.json()
        correct_package = [package if package['name'] == param else None for package in req_json][0]
        if correct_package is None: raise AttributeError
        if correct_package['version'] > old_version:
            to_list = correct_package['version'].replace('.', ' ').split()
            carrot_comprehension = [carrot] + to_list if carrot is not None else correct_package['version']
            return carrot_comprehension
        else:
            to_list = old_version.replace('.', ' ').split()
            carrot_comprehension = [carrot] + to_list if carrot is not None else old_version
            return carrot_comprehension
    except AttributeError:
        packagesNotFound.append(param)


def write_new_json(new_dependencies, original_package_json, file_path):
    if args['dnr'] is False:
        os.remove(file_path)
    original_package_json['dependencies'] = new_dependencies
    with open('package.json' if args['dnr'] else 'package_dependency_plus.json', 'w') as outfile:
        json.dump(original_package_json, outfile)
    if args['npm']:
        npm_install()


def check_dependency_versions(file_path):
    try:
        with open(file_path) as fileObj:
            packages_json = json.load(fileObj)
            for packageName, versionNumber in packages_json['dependencies'].items():
                if 'git' not in versionNumber:
                    carrot = '^' if '^' in versionNumber else None
                    val = get_requests(remove_special_chars(packageName), versionNumber, carrot)
                    newDependencies[packageName] = val
        write_new_json(newDependencies, packages_json, file_path)
    except TypeError:
        print(args['file'], ' is not a valid package.json')
        sys.exit()


def npm_install():
    print('Running npm install...')
    proc = subprocess.Popen(['npm', 'install'], stdout=subprocess.PIPE, cwd=args['file'].replace('package.json', ''))
    for line in io.TextIOWrapper(proc.stdout):
        print(line)
    print('Install complete.')


def cleanup():
    if len(packagesNotFound) > 0:
        print('Packages Not Found or Deprecated:\n')
        for index, item in enumerate(packagesNotFound):
            print(index, ': ', item)
    del newDependencies, packagesNotFound


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Dependency+', description='Check for latest version and upgrade npm package.json dependencies')
    parser.add_argument('-f', '--file', type=str, required=True, help='package.json file path; absolute or relative.')
    parser.add_argument('-n', '--npm', type=bool, default=False, required=False, help='npm install new package.json')
    parser.add_argument('--dnr', type=bool, default=False, required=False, help='do not remove existing project package.json')
    args = vars(parser.parse_args())
    check_dependency_versions(args['file'])
