# setup.py

from setuptools import setup, find_packages

setup(
    name="ai_melt",
    version="0.1.0",
    description="AI-MELT: Metaphor Detection Pipeline (Step 1) of the MELT framework",
    author="María Isabel Marín",
    author_email="m.i.marin.morales@rug.nl",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv",
        "requests",
        "transformers",
        "spacy",
        "torch>=2.0.0",
        "fastapi>=0.95.0",    # si tu servicio usa FastAPI
        "uvicorn[standard]>=0.22.0",
        "pydantic>=1.10.0",   # para esquemas Pydantic
    ],
    entry_points={
    "console_scripts": [
        "ai-melt-step1=step_one_primary_metaphor.cli:main",
        ],
    },
)
