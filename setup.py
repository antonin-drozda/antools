"""
This is the setup file for the antools package. It uses setuptools for packaging
and includes metadata about the project such as name, version, dependencies, etc.
"""

from setuptools import find_packages, setup

import antools as ant

# %% pypi package setup

with open("README.txt", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

with open("CHANGELOG.txt", "r", encoding="utf-8") as changelog_file:
    long_description += "\n\n" + changelog_file.read()

setup(
    name=ant.__name__,
    author=ant.__author__,
    author_email=ant.__author_email__,
    version=ant.__version__,
    description=ant.__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=ant.__url__,
    license=ant.__license__,
    classifiers=ant.CLASSIFIERS,
    keywords=ant.KEYWORDS,
    packages=find_packages(include=["antools", "antools.*"]),
    include_package_data=True,
    package_data={"antools": ["automation_template/**/*"]},
    python_requires=">=3.13",
    install_requires=ant.PACKAGE_DEPENDENCY,
    zip_safe=False,
)
