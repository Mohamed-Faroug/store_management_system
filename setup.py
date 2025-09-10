#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="inventory-management-system",
    version="1.0.0",
    author="محمد فاروق",
    author_email="mfarouk@example.com",
    description="نظام شامل لإدارة المخزون والمبيعات",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mfarouk/inventory-management-system",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.2",
            "pytest-flask>=1.2.0",
            "pytest-cov>=4.1.0",
            "flake8>=6.0.0",
            "black>=23.7.0",
            "isort>=5.12.0",
        ],
        "docs": [
            "Sphinx>=7.1.2",
            "sphinx-rtd-theme>=1.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "inventory=run:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
