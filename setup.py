import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="composer",
    url='https://github.com/anr990/composer',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'pytest',
        'click',
        'pytz',
        'boto3',
        'mock',
        'lxml',
        'xmljson'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
    entry_points='''
    [console_scripts]
    compose=composer.cli:cli
    '''
)
