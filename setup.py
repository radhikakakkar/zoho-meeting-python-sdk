from setuptools import setup, find_packages

setup(
    name="zoho-meeting-sdk",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",  # List any other dependencies
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python SDK for Zoho Meeting API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/zoho-meeting-python-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
