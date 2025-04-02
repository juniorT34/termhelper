from setuptools import find_packages, setup

setup(
    name="cmdhelper",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "cmdhelper": ["data/*.yaml", "web/templates/*", "web/static/*"],
    },
    description="A command-line helper tool with AI-powered explanations",
    author="Your Name",
    author_email="your.email@example.com",
    license="MIT",
    url="https://github.com/yourusername/cmdhelper",
    install_requires=[
        "requests",
        "rich",
        "argcomplete",
        "tqdm",
        "pyyaml",
        "rapidfuzz",
        "flask",
        "openai",
        "python-dotenv",
        "markdown",
    ],
    entry_points={
        "console_scripts": [
            "cmdhelper=cmdhelper.cmdhelper:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
