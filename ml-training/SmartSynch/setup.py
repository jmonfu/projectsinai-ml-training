from setuptools import setup as setuptools_setup, find_packages
import nltk

def download_nltk_data():
    nltk.download('punkt')
    nltk.download('punkt_tab')

if __name__ == "__main__":
    download_nltk_data()

setuptools_setup(
    name="smartsynch",
    version="0.1.0",
    packages=find_packages(where="."),
    package_dir={"": "."},
    install_requires=[
        "fastapi",
        "uvicorn",
        "redis",
        "tensorflow>=2.18.0",
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
