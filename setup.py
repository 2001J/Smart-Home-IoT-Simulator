from setuptools import setup, find_packages

setup(
    name="smart_home_iot",
    version="1.0.0",
    description="A Python-based application that simulates a smart home environment with various IoT devices",
    author="ELTE Python",
    packages=find_packages(),
    install_requires=[
        "pillow>=9.0.0",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "smart-home-iot=main:main",
        ],
    },
) 