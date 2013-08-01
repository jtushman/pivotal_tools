from setuptools import setup

setup(name='pivotal_tools',
      version='0.1',
      description='Collection of pivotal command line tools',
      url='http://github.com/jtushman/pivotal_readme',
      author='Jonathan Tushman',
      author_email='jonathan.tushman@zefr.com',
      license='MIT',
      packages=['pivotal_tools'],
      install_requires=[
          'docopt>=0.6'
      ],
      entry_points={
          'console_scripts': ['pivotal_tools = pivotal_tools:main']
      },
      zip_safe=False)
