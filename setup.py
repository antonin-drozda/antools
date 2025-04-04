# %% lib import
from setuptools import setup, find_packages
import antools as ant

# %% pypi package setup

setup(
  name=ant.__name__,
  author=ant.__author__,
  author_email=ant.__author_email__,  
  version=ant.__version__,  
  description=ant.__description__,  
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type='text/markdown',
  url=ant.__url__,  
  license=ant.__license__, 
  classifiers=ant.CLASSIFIERS,
  keywords=ant.KEYWORDS, 
  packages=find_packages(include=["antools", "antools.*"]),
  include_package_data=True,
  package_data={"antools": ["automation_template/**/*"]},
  python_requires='>=3.13',
  install_requires=ant.PACKAGE_DEPENDENCY,
  zip_safe=False
)