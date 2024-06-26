from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mccapicli",
    version="0.1.0",
    author="Panagiotis Kouzaris",
    author_email="panas@panas.cy",
    description="A command-line interface for MCC API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/veryredpp/mccapicli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license="MIT",
    entry_points={
        'console_scripts': [
            'mccapicli=mccapicli.__main__:run',
        ],
    },
)
