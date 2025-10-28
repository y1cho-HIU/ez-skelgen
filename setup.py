from setuptools import setup, find_packages

setup(
    name="ez-skelgen",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ez-skelgen=ez-skelgen.main:main',
        ],
    },
    python_requires='>=3.7',
    author="y1cho-HIU",
    description="Generate Directory",
    url="https://github.com/y1cho-HIU/ez-skelgen",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)