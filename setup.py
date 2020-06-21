from setuptools import setup, find_packages

setup(
    name='alana_dataset_utils',
    version='0.2',
    packages=find_packages(),
    url='',
    license='',
    author='Ioannis Papaioannou',
    author_email='i.papaioannou@hw.ac.uk',
    description='A set of tools for extracting segments from the Alana dataset',
    install_requires=["tqdm"]
)
