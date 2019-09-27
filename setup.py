from setuptools import find_packages, setup

setup(
    name='andromeda-frontend',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-login',
        'flask-bcrypt',
        'flask-cors',
        'flask-paranoid',
        'sqlite3',
        'peewee',
        'python-slugify',
    ],
)
