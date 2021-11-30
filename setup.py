from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('requirements.txt') as file:
    INSTALL_REQUIERES = file.read().splitlines()

setup(
    author="Paula Encinar",
    author_email='evolved5g@gmail.com',
    mainteiner='Paula Encinar',
    python_requires='>=3.8',
    description="Evolved5G NetApp Template ",
    entry_points={
        'console_scripts': []
    },
    install_requires=INSTALL_REQUIERES,
    license="OSI Approved :: Apache Software License",
    long_description=README,
    include_package_data=True,
    keywords='template',
    name='template',
    packages=find_packages(exclude=["tests"]),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/EVOLVED-5G/template',
    version='1.0.0',
    zip_safe=False,
)
