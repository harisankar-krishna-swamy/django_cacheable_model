import setuptools

import django_cacheable_model

with open('../README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='django_cacheable_model',
    version=django_cacheable_model.version,
    author='Harisankar Krishna Swamy',
    license='Apache2',
    author_email='harisankar.krishna@outlook.com',
    description='A cacheable Django model',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harisankar-krishna-swamy/django_cacheable_model.git",
    packages=setuptools.find_packages(exclude=["tests*"]),
    install_requires=["django>=2.0"],
    python_requires='>=3.7.4, <4',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    keywords='django cacheable model',
    project_urls={
        "GitHub": "https://github.com/harisankar-krishna-swamy/django_cacheable_model.git"
    },
)
