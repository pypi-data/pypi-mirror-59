from setuptools import setup

REPO_URL = 'http://github.com/okfn-brasil/serenata-toolbox'

with open('README.rst') as fobj:
    long_description = fobj.read()

setup(
    author='Serenata de Amor',
    author_email='contato@serenata.ai',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
    ],
    description='Toolbox for Serenata de Amor project',
    zip_safe=False,
    install_requires=[
        'aiofiles',
        'aiohttp',
        'beautifulsoup4>=4.4',
        'lxml>=3.6',
        'pandas>=0.18',
        'python-decouple>=3.1',
        'tqdm'
    ],
    keywords='serenata de amor, data science, brazil, corruption',
    license='MIT',
    long_description=long_description,
    name='serenata-toolbox',
    packages=[
        'serenata_toolbox',
        'serenata_toolbox.federal_senate',
        'serenata_toolbox.chamber_of_deputies',
        'serenata_toolbox.datasets'
    ],
    scripts=['serenata_toolbox/serenata-toolbox'],
    url=REPO_URL,
    python_requires='>=3.6',
    version='15.1.6',
)
