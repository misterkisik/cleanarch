from setuptools import setup, find_packages

setup(
    name="cleanarch",
    version="1.0.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        "console_scripts": [
            "cleanarch = cleanarch.app:main",
        ],
    },
)
