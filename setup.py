from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="mosukas_google_drive_autosave",
    version="1.0.0",
    author="Lucas Lima",
    description="A script that automatically saves your projects on google drive after pressing ctrl+s or after a specific time range.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MosukaSan/Mosukas-Google-Drive-Autosave",
    packages=find_packages(),
    install_requires=requirements,
    package_data={
        '': ['*.json']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0 License",
        "Operating System :: OS Independent"
    ],
)