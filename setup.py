from setuptools import setup

setup(name='tbdb',
      version='0.0.8',
      description='Python API to TalkBankDB.',
      url='https://github.com/TalkBank/TBDBpy',
      author='John Kowalski',
      license='LICENSE',
      packages=['tbdb'],
      install_requires=[
        "requests >= 2.24.0"
    ]
)
