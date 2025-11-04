from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="STUDY-BUDDY-AI",
    version="0.1",
    author="Kashi Revanna",
    packages=find_packages(),
    install_requires = requirements,
)