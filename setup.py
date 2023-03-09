from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="data-engineering-utokyo",
    version="0.1.0",
    description="Data Engineering for the EDM Search at the University of Tokyo",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="https://latent-ad-qml.readthedocs.io/en/latest/",
    author="Roman Wixinger, Shintaro Nagase, Naoya Ozawa",
    packages=find_packages(exclude=["scripts"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "matplotlib>=3.5",
        "numpy>=1.21",
        "pandas>=1.4.0",
        "scikit-learn==1.1.1",
        "scipy>=1.9",
    ],
    extras_require={
        "docs": [
            "sphinx>=3.0",
            "sphinx-autoapi",
            "numpy>=1.21",
            "pandas>=1.4.0"
        ]
    }
)
