from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(name='ndocker',
      version='1.0.0',
      description='docker network configration',
      long_description=long_description,
      url='http://github.com/codlin/ndocker',
      author='Sean Z',
      author_email='sean.z.ealous@gmail.com',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Testers',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'License :: OSI Approved :: Apache License',
          'Programming Language :: Python :: 2.7', ],
       install_requires=['Click==6.7', ],
       entry_points={
           'console_scripts': [
           'ndocker=ndocker.command_line:cli'],},
       packages=find_packages(exclude=['ndocker_test']),
       include_package_data=True,
       zip_safe=False)