from setuptools import setup, find_packages

setup(name='fangraphs_webscraper',
      version='0.1',
      description='Scrape Player Game Logs',
      url='https://github.com/conorkcorbin/fangraphs-webscraper',
      author='Conor Corbin',
      author_email='ccorbin@stanford.edu',
      license='MIT',
      install_requires=[
        'numpy>=1.13.3',
        'pandas>=0.20.3',
        'beautifulsoup4',
        ],
      scripts=['bin/get_player_ids.py',
               'bin/get_player_log.py'],
      packages=find_packages(),
      zip_safe=False)