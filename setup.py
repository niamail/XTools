from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Natural Language :: Chinese (Simplified)",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=["pyyaml>=6.0"],
    python_requires=">=3.8, <=3.11",
    name="XTools",
    version="0.1.1",
    author="Lee Zhang",
    author_email="xggsusers@gmail.com",
    description="A python package of tools by Lee Zhang",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://leezhang.space",
    packages=find_packages(),
)
