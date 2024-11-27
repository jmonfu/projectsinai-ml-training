from setuptools import setup, find_packages

setup(
    name="smartsynch",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "tensorflow",
        "torch",
        "transformers",
        "sentence-transformers",
        "numpy",
        "pandas",
        "scikit-learn",
        "nltk",
        "spacy",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A smart task categorization system using ML",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
