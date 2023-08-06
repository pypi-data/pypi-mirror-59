# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 19:51:40 2020

@author: Jasmanpreet
"""


from distutils.core import setup

setup(

  name = 'topsis_ucs633_jasman_101703259',         # How you named your package folder (MyLib)

  packages = ['topsis_ucs633_jasman_101703259'],   # Chose the same as "name"

  version = '0.1',      # Start with a small number and increase it with every change you make

  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository

  description = 'An implementation of topsis approach in python',   # Give a short description about your library

  author = 'Jasman',                   # Type in your name

  author_email = 'jkaur1_be17@thapar.edu',      # Type in your E-Mail

  url = 'https://github.com/jasmanpreet/topsis-in-python',   # Provide either the link to your github or to your website

  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on

  keywords = ['python', 'topsis', 'ucs633'],   # Keywords that define your package best

  install_requires=[            # I get to this in a second

          'validators',

          'beautifulsoup4',

      ],

  classifiers=[

    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package

    'Intended Audience :: Developers',      # Define that your audience are developers

    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License',   # Again, pick a license

    'Programming Language :: Python :: 3.4',      #Specify which pyhton versions that you want to support

    'Programming Language :: Python :: 3.7',

    'Programming Language :: Python :: 3.5',

    'Programming Language :: Python :: 3.6',

  ],

)