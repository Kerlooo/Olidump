from setuptools import setup

setup(
    name='olidump',
    version='1.0',
    py_modules=['olidump'],
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'olidump=olidump:main',
        ],
    },
)