import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sqlgood",
    version="0.0.1",
    author="Jacob Merizian",
    author_email="jmerizia@vt.edu",
    description="A package for statically type checked SQL queries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jmerizia/sqlgood",
    project_urls={
        "Bug Tracker": "https://github.com/jmerizia/sqlgood/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'fire==0.4.0'
    ],
    test_suite='tests',
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    package_data = {
        'sqlgood': ['py.typed']
    },
    python_requires=">=3.6",
)

