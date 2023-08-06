from setuptools import setup

setup(
    name="birdyaml",
    version="0.8.0",
    author="Anthony Casagrande",
    author_email="birdapi@gmail.com",
    description="Generic yaml to object parser for python",
    license="MIT",
    keywords="yaml birdapi",
    url="https://pypi.python.org/pypi/birdyaml",
    py_modules=['birdyaml'],
    install_requires=[
        "PyYAML",
        "birdjson"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
)