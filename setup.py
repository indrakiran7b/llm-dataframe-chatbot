from setuptools import setup, find_packages
from pathlib import Path

def load_requirements(filename: str = "requirements.txt"):
    """Load dependencies from a requirements file."""
    path = Path(__file__).parent / filename
    if not path.exists():
        return []
    with open(path) as f:
        return [
            line.strip() for line in f
            if line.strip() and not line.startswith("#") and line.strip() != "-e ."
        ]

setup(
    name="datachat",
    version="0.1.0",
    description="An interactive Streamlit + LLM powered data exploration chatbot.",
    packages=find_packages(exclude=("tests", "docs")),
    install_requires=load_requirements(),
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Streamlit",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    zip_safe=False,
)
