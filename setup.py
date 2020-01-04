from setuptools import setup

setup(name='helloshopper',
      version='1.0',
      description='Python Distribution Utilities',
      author='Greg Ward',
      author_email='gward@python.net',
      url='https://www.python.org/sigs/distutils-sig/',
      packages=['helloshopper'],
      install_requires=['pandas', 'scrape_schema_recipe', 'openpyxl', 'unidecode'],
      entry_points={
          'console_scripts': [
              'helloshopper = helloshopper.__main__:main',
            ]
      }
     )
