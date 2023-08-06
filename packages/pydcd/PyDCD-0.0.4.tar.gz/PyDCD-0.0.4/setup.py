import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyDCD", 
    version="0.0.4",
    author="Kunpeng Zhang & Shaokun Fan & Bruce Golden",
    author_email="shaokunfan@gmail.com",
    description="PyDCD: A Deep Learning-Based Community Detection Software in Python for Large-scale Networks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kpzhang/deepcommunitydetection",
    include_package_data=True,
    py_modules = ["PyDCD"],
    packages=setuptools.find_packages(),
    install_requires = ['numpy', 'networkx', 'torch', 'sklearn', 'scipy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.1',
)