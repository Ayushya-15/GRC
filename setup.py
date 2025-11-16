from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="grc-compliance-tool",
    version="1.0.0",
    author="GRC Compliance Team",
    description="A comprehensive GRC compliance tool for risk identification and elimination as per ISO 31000",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ayushya-15/GRC",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "tensorflow>=2.8.0",
        "scapy>=2.4.5",
        "python-nmap>=0.7.1",
        "requests>=2.27.0",
        "xgboost>=1.5.0",
        "lightgbm>=3.3.0",
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0",
        "reportlab>=3.6.0",
        "jinja2>=3.0.0",
        "sqlalchemy>=1.4.0",
        "pyyaml>=6.0",
        "colorama>=0.4.4",
        "tqdm>=4.62.0",
    ],
    entry_points={
        "console_scripts": [
            "grc-scan=grc_tool.main:main",
        ],
    },
)
