from setuptools import setup, find_packages

setup(
    name='apirl',
    version='0.1.0',
    author='Sabyasachi',
    author_email='sabychakraborty08@gmail.com',
    description='A Python package to manage API rate limits by automatically queuing and pacing API requests.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mixter3011/aprl.git',
    packages=find_packages(),
    install_requires=[
        'certifi',
        'python-dotenv',
    ],
    extras_require={
        'dev': [
            'pytest',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
