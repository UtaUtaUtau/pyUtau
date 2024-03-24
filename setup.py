from setuptools import setup

with open('README.md', encoding='utf8') as f:
    long_description = f.read()

setup(
    name='pyutau',
    packages=['pyutau'],
    version='1.2.1',
    license='MIT',
    description='A python library/module for parsing UTAU plugin data',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='UtaUtaUtau',
    author_email='diamond.glacier16@gmail.com',
    url='https://github.com/UtaUtaUtau/pyUtau',
    keywords=['utau'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10'],
    download_url='https://github.com/UtaUtaUtau/pyUtau/archive/refs/tags/v1.2.1.tar.gz'
    )
