import requests, json, io, subprocess, argparse, os, sys
from string import punctuation


class DependencyPlus:
    def __init__(self, file_path):
        self.file_path = file_path
        self.package_json = {}
        self.newDependencies = {}
        self.newDevDependencies = {}
        self.packagesNotFound = []
        self.HOTWORDS = ['react-dom', 'electron']
        # self.specialCharDict = {}
        self.check_dependency_versions()

    @staticmethod
    def remove_special_chars(package_name):
        _package_name = package_name.replace('/', '-')
        # if _package_name != package_name: specialCharDict[_package_name] = package_name
        _package_name = package_name.replace('@', '')
        # if _package_name != package_name: specialCharDict[_package_name] = package_name
        for special_char in list(punctuation):
            if _package_name.find(special_char) != -1 and special_char != ('-' and '_'):
                _package_name.replace(special_char, '')
        return _package_name

    @staticmethod
    def get_correct_package(packages, pkg_name):
        for package in packages:
            if package['name'] == pkg_name or package['links']['npm'] == 'https://www.npmjs.com/package/{}'.format(pkg_name):
                return package
        return None

    def get_requests(self, package_name, old_version):
        try:
            print("Checking {} for updates".format(package_name))
            correct_package = None
            req = requests.get('https://www.npmjs.com/search/suggestions?q={}'.format(package_name))
            req_json = req.json()
            correct_package = self.get_correct_package(req_json, package_name)
            if correct_package is None: raise AttributeError
            if correct_package['version'] > old_version:
                print('FOUND! New version of {}'.format(package_name))
            return correct_package['version']
        except AttributeError:
            if package_name in self.HOTWORDS:
                print("- '{}' could not be found, traditionally. Existing version kept in place.".format(package_name))
                return old_version
            self.packagesNotFound.append(package_name)

    def write_new_json(self):
        try:
            if str(args['dnr']) == 'False':
                os.remove(self.file_path)
            self.package_json['dependencies'] = self.newDependencies
            self.package_json['devDependencies'] = self.newDevDependencies
            with open(self.file_path if str(args['dnr']) == 'False' else self.file_path.replace('/package.json', '/package_dependency_plus.json'), 'w') as outfile:
                json.dump(self.package_json, outfile, indent=2, sort_keys=True, ensure_ascii=False)
            if str(args['npm']) == 'True':
                self.npm_install()
        except FileNotFoundError as fnfe:
            self.restore_backup_copy()
            self.print_error_messages('FileNotFoundError', fnfe)
        except PermissionError as pe:
            self.restore_backup_copy()
            self.print_error_messages('PermissionError', pe)
        finally:
            self.cleanup()

    def play_maker(self, field, obj):
        for packageName, versionNumber in self.package_json[field].items():
            if 'git' not in versionNumber:
                val = self.get_requests(self.remove_special_chars(packageName), versionNumber)
                obj[packageName] = val

    def check_dependency_versions(self):
        try:
            with open(self.file_path) as fileObj:
                self.package_json = json.load(fileObj)
            self.play_maker('dependencies', self.newDependencies)
            self.play_maker('devDependencies', self.newDevDependencies)
            self.write_new_json()
        except TypeError as te:
            self.print_error_messages(te, self.file_path + ' is not a valid package.json')
        except KeyError:
            pass

    def npm_install(self):
        try:
            print('Running npm install...')
            proc = subprocess.Popen(['npm', 'install'], stdout=subprocess.PIPE, cwd=self.file_path.replace('package.json', ''))
            for line in io.TextIOWrapper(proc.stdout):
                print(line)
            print('Install complete.')
        except KeyboardInterrupt:
            print('Stopping npm install...')

    def cleanup(self):
        try:
            if len(self.packagesNotFound) > 0:
                print('\nPackages Not Found or Deprecated:')
                for index, item in enumerate(self.packagesNotFound):
                    print(index + 1, ': ', item)
            else:
                print('\nAll packages searched.')
        except UnboundLocalError as ule:
            self.print_error_messages('UnboundLocalError', ule)
        finally:
            print('Dependency+ Complete.')

    @staticmethod
    def print_error_messages(error_type, msg=None):
        print('An error has occured. Please refer below for messages.\n')
        print(error_type, ':', msg if msg is not None else 'No Details.')
        sys.exit()

    def restore_backup_copy(self):
        if not os.path.isfile(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as backup_copy:
                backup_copy.write(json.loads(self.package_json))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Dependency+', description="Check for latest versions of your project's dependencies and upgrade them and your npm package.json, in relation to the updates.")
    parser.add_argument('-f', '--file', type=str, required=True, help='package.json file path; absolute or relative.')
    parser.add_argument('-n', '--npm', type=str, required=False, default='False', help='npm install new package.json')
    parser.add_argument('--dnr', type=str, required=False, default='True', help='do not remove existing project package.json')
    args = vars(parser.parse_args())
    DependencyPlus(args['file'])
