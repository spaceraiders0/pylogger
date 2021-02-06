from setuptools import setup

with open("README.md", "r") as readme:
    markdown_description = readme.read()

setup(
    name="spacelogger",
    version="1.0.0",
    description="A small, and lightweight logger.",
    py_modules=["spacelogger"],
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
        "Operating System :: OS IndependantA,"
    ],
    long_description=markdown_description,
    long_description_content_type="text/markdown",
    extras_require={
        "dev": {
            "pytest >= 3.7",
        },
    },
)


