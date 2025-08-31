#!/usr/bin/env python3
# Setup script for Lexy speech transcription application

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    # Read README.md if it exists, otherwise return basic description
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Lexy - Offline speech-to-text transcription application using Vosk"

# Read requirements.txt
def read_requirements():
    # Read requirements from requirements.txt
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="lexy",
    version="0.1.0",
    author="pwnderpants",
    author_email="pwnderpants@pwnderpants.com",
    description="Offline speech-to-text transcription application",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/pwnderpants/lexy",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "lexy=lexy.main:main",
        ],
    },
    keywords="speech recognition transcription vosk offline audio",
    project_urls={
        "Source": "https://github.com/pwnderpants/lexy",
        "Bug Reports": "https://github.com/pwnderpants/lexy/issues",
    },
    include_package_data=True,
    zip_safe=False,
)
