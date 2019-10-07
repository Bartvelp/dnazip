from setuptools import setup

setup(name='dnazip',
      version='0.1',
      description='Compression for Fasta files',
      url='http://github.com/Bartvelp/dnazip',
      author='Bart Grosman',
      author_email='',
      license='MIT',
      scripts=['bin/dnazip'],
      packages=['dnazip'],
      zip_safe=False)