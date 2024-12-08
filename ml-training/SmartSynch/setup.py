from setuptools import setup, find_packages

setup(
    name="smartsynch",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.115.5",
        "uvicorn==0.32.1",
        "python-dotenv",
        "pydantic==2.10.2",
        "scikit-learn>=1.0.2",
        "joblib>=1.1.0",
        "numpy>=1.21.0"
    ]
)
