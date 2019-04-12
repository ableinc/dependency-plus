# Dependency+: npm dependency updater
Dependency+ is a dependency free, python package that allows you to update your npm packages
to their latest releases. Using your current project's packages.json file, you can use 
Dependency+ to check for updates and even be aware of deprecated libraries. Replacements 
for deprecated libraries will not be installed, please refer to author's repo.

# Requirements
* Python 2/3

# Install
<code>git clone https://github.com/ableinc/dependency-plus.git</code><br />
<code>cd dependency-plus</code><br />
<code>pip install -r requirements.txt</code>

# Commands
Get help:
<code>python dependency-plus.py -h</code>

Basic: 
<code>python dependency-plus.py -f [file_path]<sup>1</sup></code>

Do not delete existing package.json:
<code>python dependency-plus.py -f [file_path]<sup>1</sup> --dnr</code>

Update and run npm install after:
<code>python dependency-plus.py -f [file_path]<sup>1</sup> --npm</code>


<sub>1: Absolute or relative file path. Move file into node project to use 
relative file path or npm install feature</sub>
