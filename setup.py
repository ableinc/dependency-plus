import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dependency-plus",
    version="0.0.1",
    author="AbleInc - Jaylen Douglas",
    author_email="douglas.jaylen@gmail.com",
    description="Dependency+ is a dependency free, python package that allows you to update your npm "
                "packages to their latest releases.",
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
