from setuptools import setup

setup(
    name='available',
    version='0.1',
    py_modules=['available'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        available=available:show_available_sites
    ''',
)
