import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dna_designer",
    version="0.3.2",
    author="Keoni Gandall",
    author_email="koeng101@gmail.com",
    description="A package that assists in designing DNA",
    package_data={'': ['./dna_designer/data/*']},
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
