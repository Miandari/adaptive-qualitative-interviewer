"""
Setup file to make the ESM Chatbot importable
"""
from setuptools import setup, find_packages

setup(
    name="esm_chatbot",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        line.strip()
        for line in open("requirements.txt").readlines()
        if line.strip() and not line.startswith("#")
    ],
)
