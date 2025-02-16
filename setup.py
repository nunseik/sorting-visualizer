from setuptools import setup, find_packages

setup(
    name="sorting_visualizer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'PyQt6',
        'matplotlib',
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A sorting algorithm visualization tool",
    keywords="sorting, algorithms, visualization",
    python_requires='>=3.6',
)