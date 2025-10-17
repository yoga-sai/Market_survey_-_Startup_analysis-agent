from setuptools import setup, find_packages

setup(
    name="market-analyst-agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0.0",
        "openai>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "market-analyst=agent.runner:main",
        ],
    },
)
