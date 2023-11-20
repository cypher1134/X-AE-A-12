from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = ''
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

# Setting up
setup(
        name="src", 
        version=VERSION,
        author="Groupe1",
        author_email="<vianney.saintgeorges-chaumet@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        scripts=['main.py','scraper.py'],
        install_requires=['panda>=0.3.1',
                          'sqlite3',
                          'tqdm>=4.66.1',
                          'time'], 
        
        keywords=['python', 'src'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)