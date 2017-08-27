from setuptools import setup

setup(name='mredu',
      version='0.4.1',
      description='A simple simulator of a system which implements map/reduce paradigm.',
      url='http://github.com/ramonpin/mredu',
      author='ramonpin',
      author_email='ramon.pin@gmail.com',
      license='Apache-2',
      packages=['mredu'],
      install_requires=[
        'toolz',
      ],
      zip_safe=False)
