from setuptools import setup, find_namespace_packages

setup(
    name="smartsynch",
    version="1.0.0",
    packages=find_namespace_packages(include=["smartsynch*"]),
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
