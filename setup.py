# %% lib import
from setuptools import setup, find_packages
import antools as ant

# %% pypi package setup

# classifiers for pypi package
CLASSIFIERS = [
    'Framework :: IDLE',
    'Topic :: Utilities',
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.13',
    'Operating System :: OS Independent',
    'Environment :: Plugins',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Natural Language :: English',
]

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
  classifiers=CLASSIFIERS,
  keywords=ant.KEYWORDS, 
  packages=find_packages(include=["antools", "antools.*"]),
  include_package_data=True,
  package_data={"antools": ["automation_template/**/*"]},
  python_requires='>=3.13',
  install_requires=ant.PACKAGE_DEPENDENCY,
  zip_safe=False
)