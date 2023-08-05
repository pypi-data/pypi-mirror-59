import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    require_packages = [line[:-1] if line[-1] == '\n' else line for line in f]

setuptools.setup(
    name="embedding_as_service_client",
    version="1.0.0",
    author="Aman Srivastava",
    author_email="amans.rlx@gmail.com",
    description="embedding-as-service: one-stop solution to encode sentence to vectors using various embedding methods",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amansrivastava17/embedding-as-service",
    packages=setuptools.find_packages(),
    install_requires=require_packages,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords='bert nlp tensorflow machine learning sentence encoding embedding serving albert glove word2vec'
)
