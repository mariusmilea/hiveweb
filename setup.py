from setuptools import find_packages, setup

setup(
    name='HiveWeb',
    version='0.1',
    url='https://github.com/spil-marius/hiveweb',
    author='Marius Milea',
    description=("Simple Hive UI written in Flask."),
    packages=find_packages(),
    include_package_data=True,
    scripts=[
        'scripts/run_gunicorn.sh',
        'run.py',
    ],
    install_requires=['flask', 'gunicorn']
)
