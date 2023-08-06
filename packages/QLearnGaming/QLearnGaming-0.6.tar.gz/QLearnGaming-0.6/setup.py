from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()






from distutils.core import setup
setup(
  name = 'QLearnGaming',         # How you named your package folder (MyLib)
  packages = ['QLearnGaming'],   # Chose the same as "name"
  version = '0.6',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A library which makes it simple to build Deep Learning on games',   # Give a short description about your library
  author = 'Azfar Mohamed',                   # Type in your name
  author_email = 'azfarmah@outlook.com',      # Type in your E-Mail
  url = 'https://github.com/user/azfar154',   # Provide either the link to your github or to your website,    # I explain this later on
  keywords = ['KERAS', 'GYM', 'GAMING'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'keras',
          'gym',
          'numpy',
          'tensorflow'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.6',
  ],
  long_description=long_description,
    long_description_content_type='text/markdown'
)
