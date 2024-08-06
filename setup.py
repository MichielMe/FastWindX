from setuptools import setup

setup(
    name="fastwindx",
    version="0.1.0",
    packages=[
        "fastwindx",
        "fastwindx.app",
        "fastwindx.app.api",
        "fastwindx.app.api.v1",
        "fastwindx.app.api.v1.endpoints",
        "fastwindx.app.core",
        "fastwindx.app.db",
        "fastwindx.app.db.models",
        "fastwindx.app.schemas",
        "fastwindx.app.services",
        "fastwindx.app.static",
        "fastwindx.app.templates",
        "fastwindx.app.tests",
        "fastwindx.app.tests.test_api",
        "fastwindx.app.utils",
        "fastwindx.app.views",
    ],
    include_package_data=True,
    package_data={
        "fastwindx": ["**/*"],
    },
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlmodel",
        "alembic",
        "pydantic",
        "pydantic-settings",
        "jinja2",
        "python-dotenv",
        "click",
    ],
    entry_points={
        "console_scripts": [
            "fastwindx=fastwindx.app.cli:main",
        ],
    },
)
