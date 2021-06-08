import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sql2py",
    version="0.0.1",
    author="Jacob Merizian",
    author_email="jmerizia@vt.edu",
    description="A package for statically type checked SQL queries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jmerizia/sql2py",
    project_urls={
        "Bug Tracker": "https://github.com/jmerizia/sql2py/issues",
    },
    entry_points = {
        'console_scripts': [
            'sql2py=sql2py.generate:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [],
    test_suite='tests',
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    package_data = {
        'sql2py': ['py.typed']
    },
    python_requires=">=3.6",
)

