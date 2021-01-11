import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="b2style-anselm-baur", # Replace with your own username
    version="0.0.1",
    author="Anselm Baur",
    author_email="anselm.baur@desy.de",
    description="style package for Belle II plots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anselm-baur/b2style",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
