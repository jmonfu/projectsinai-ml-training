from setuptools import setup, find_packages

setup(
    name="smartsynch",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "transformers",
        "torch",
        "sentence-transformers",
        "huggingface-hub"
    ]
)
