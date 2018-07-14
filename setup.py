from setuptools import setup, find_packages

setup(
    name='jschema2py',
    version='0.1.0',
    description="jsonschema to python class converter",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jacopodl/jschema2py",
    author="Jacopo De Luca",
    author_email="jacopo.delu@gmail.com",
    license='MIT',
    keywords=["jschema2py", "json", "schema", "jsonschema", "library", "python3"],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ]
)
