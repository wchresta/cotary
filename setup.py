import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cotary",
    version="0.1",

    author="Wanja Chresta",
    author_email="wanja.hs@chrummibei.ch",
    description="Prove a file currently exists without disclosing it's content.",
    entry_points={
        'console_scripts': [ 'cotary=cotary.cotary:main' ]
    },
    install_requires=['python-twitter>=3.0','pyyaml>=3.0'],
    license='LICENSE',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wchresta/cotary",
    project_urls={
        "Source Code": "https://github.com/wchresta/cotary",
        "Issues": "https://github.com/wchresta/cotary/issues",
    },
    packages=setuptools.find_packages(),
    python_requires='>=3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Legal Industry",
        "Intended Audience :: Science/Research",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Security :: Cryptography",
        "Topic :: Utilities",
    ],
)
