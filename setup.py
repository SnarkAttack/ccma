import setuptools

with open("README.md", "r" encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="ccma",
    version="0.0.1",
    author="SnarkAttack",
    author_email="snarkattack0622@gmail.com",
    description="CryptoCurrency Market Analyzer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
