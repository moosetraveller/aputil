import setuptools

if __name__ == "__main__":

    with open("README.md", "r") as fh:
        long_description = fh.read()

    setuptools.setup(
        name="ArcPyUtil",
        version="0.3",
        author="Thomas Zuberbuehler",
        author_email="thomas.zuberbuehler@gmail.com",
        description="Collection of arcpy helper classes and functions.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/moosetraveller/arcpy-util",
        packages=setuptools.find_packages(where="src"),
        package_dir={"": "src"},
        classifiers=[
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Intended Audience :: Developers",
            "License :: MIT",
            "Operating System :: OS Independent",
        ],
        install_requires=[
            # "arcpy",
            "deprecated",
        ],
    )
