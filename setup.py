from setuptools import setup, find_packages

setup(
    name='CAW',
    version='0.1',
    url='https://github.com/mypackage.git',
    author='Author Name',
    author_email='viniciustonon@gmail.com',
    description='CAW WoW addon manager',
    packages=find_packages(),
    install_requires=['urllib', 'BeautifulSoup'],
    scripts=['bin/caw'],
)
