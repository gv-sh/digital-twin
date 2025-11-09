"""
Setup script for digital-twin package.

For modern installation, pyproject.toml is the primary configuration.
This setup.py is provided for backward compatibility.
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements from requirements.txt
def read_requirements():
    """Read requirements from requirements.txt"""
    req_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    with open(req_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="digital-twin",
    version="0.1.0",
    author="Digital Twin Team",
    description="Fleet Decarbonization Analysis - Digital Twin for heavy transport fleet optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/digital-twin",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "plotly>=5.0.0",
        "scipy>=1.7.0",
    ],
    extras_require={
        "notebook": [
            "jupyter>=1.0.0",
            "ipywidgets>=7.6.0",
            "kaleido>=0.2.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
    },
    keywords="fleet decarbonization monte-carlo risk-analysis digital-twin optimization",
    project_urls={
        "Documentation": "https://github.com/yourusername/digital-twin/blob/main/README.md",
        "Source": "https://github.com/yourusername/digital-twin",
        "Issues": "https://github.com/yourusername/digital-twin/issues",
    },
)
