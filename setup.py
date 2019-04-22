import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="npm-updater",
    version="1.0.0",
    author="AbleInc - Jaylen Douglas",
    author_email="douglas.jaylen@gmail.com",
    entry_points={'console_scripts': ['npm-updater=dependency-plus:main']},
    description="Dependency+ automatically checks and updates your npm packages to their latest releases, while"
                "also updating your project's existing package.json.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ableinc/dependency-plus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
