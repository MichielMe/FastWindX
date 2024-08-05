from setuptools import find_packages, setup

setup(
    name="fastwindx",
    version="0.1.0",
    packages=find_packages(exclude=["template*"]),
    include_package_data=True,
    package_data={
        "fastwindx": ["template/**/*"],
    },
    install_requires=[
        "fastapi>=0.95.0,<0.96.0",
        "uvicorn>=0.20.0,<0.21.0",
        "sqlmodel>=0.0.8,<0.1.0",
        "alembic>=1.9.0,<2.0.0",
        "pydantic>=2.0.0,<3.0.0",
        "jinja2>=3.1.2,<3.2.0",
        "python-dotenv>=0.19.0,<0.20.0",
        "click>=8.0.0,<9.0.0",
    ],
    entry_points={
        "console_scripts": [
            "fastwindx=fastwindx.cli:main",
        ],
    },
)
