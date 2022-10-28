import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='cirmesh',
    packages=find_packages(),
    version='0.0.3',
    description='basic',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/thomle295/cirmesh",
    author='ThomLe',
    author_email="thomlestudy295@gmail.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    license='MIT',
    install_requires=[
        'numpy',
        'trimesh',
        'alphashape',
        'pymeshfix'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests'
)
