"""
Setup for baguette-olite.
"""
from setuptools import setup, find_packages

setup(name="baguette-olite",
      version="1.0.0",
      platforms='any',
      packages=find_packages(),
      include_package_data=True,
      author="Vlad Temian",
      url="https://github.com/baguette-io/pyolite",
      description="Python wrapper for gitolite",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: BSD License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Topic :: System :: Networking',
          'Programming Language :: Python :: 2.7',
      ],
      install_requires=[
          'sh==1.09',
          'Unipath==1.0',
          'argparse==1.2.1',
          'async==0.6.1',
          'coverage==3.7.1',
          'gitdb==0.5.4',
          'smmap==0.8.2',
      ],
      extras_require={
          'testing':[
              'pytest==3.1.3',
              'mock==1.0.1',
              'spec==0.11.1',
          ],
      },
     )
