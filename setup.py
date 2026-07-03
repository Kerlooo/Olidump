from setuptools import setup

setup(
    name='olidump',
    version='1.1',
    description='Scarica challenge e allegati da OliCyber training.',
    author='Kerlo',
    url='https://github.com/Kerlooo/Olidump',
    license='CC-BY-4.0',
    py_modules=['olidump'],
    python_requires='>=3.8',
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'olidump=olidump:main',
        ],
    },
)
