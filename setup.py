from setuptools import setup, find_packages


from pkg_resources import parse_requirements
with open("Requirements.txt", encoding="utf-8") as fp:
    install_requires = [str(requirement) for requirement in parse_requirements(fp)]

setup(
    name="PyLucas",
    version="1.0.1",
    description="Personal utility library for Nuhil Lucas.",
    long_description="Personal utility library for Nuhil Lucas.",
    author="Nuhil Lucas",
    author_email="XFramilRainX@163.com",
    maintainer="Nuhil Lucas",
    maintainer_email="XFramilRainX@163.com",
    url="https://None",
    license="Apache License, Version 2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    packages=find_packages(),
    install_requires=install_requires
)