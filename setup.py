# %% lib import
from setuptools import setup, find_packages
import antools as ant

# %% pypi package setup

# classifiers for pypi package
CLASSIFIERS = [
    'Framework :: IDLE',
    'Topic :: Utilities',
    'Development Status :: 1 - Planning',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Operating System :: OS Independent',
    'Environment :: Plugins',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Natural Language :: English',
]

setup(
  name=ant.__name__,
  author=ant.__author__,
  author_email=ant.__contact__,  
  version=ant.__version__,  
  description=ant.DESCRIPTION,  
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url=ant.URL,  
  license=ant.__license__, 
  classifiers=CLASSIFIERS,
  keywords=ant.KEYWORDS, 
  py_module=['antools'],
  packages=find_packages(exclude=('docs', 'docs.*', 'tests', 'venv')),
  python_requires='>=3.6',
  install_requires=ant.PACKAGE_DEPENDENCY,
  zip_safe=False
)
