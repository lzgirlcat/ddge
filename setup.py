import setuptools


def long_description():
    with open("README.md") as fp:
        return fp.read()

def parse_requirements_file(path):
    with open(path) as fp:
        dependencies = (d.strip() for d in fp.read().split("\n") if d.strip())
        return [d for d in dependencies if not d.startswith("#")]


setuptools.setup(
    name="ddge",
    version='0.2.137.3',
    description="DuckDuckGo Email Protection CLI",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    author="Zoey !",
    maintainer_email="cb98uzhd@duck.com",
    license='GNU General Public License v3.0',
    url="https://github.com/lzgirlcat/ddge",
    python_requires=">=3.7",
    entry_points={"console_scripts": ["ddge = ddge.cli:main"]},
    install_requires=parse_requirements_file("requirements.txt"),
    include_package_data=True,
    keywords=["email", "duckdcukgo", "protection", "ddg"],
    project_urls={
        "Source (GitHub)":"https://github.com/lzgirlcat/ddge",
        "Issue Tracker": "https://github.com/lzgirlcat/ddge/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
