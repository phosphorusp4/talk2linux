from setuptools import setup, find_packages

setup(
    name='talk2linux',
    version='v0.1.0-beta0.1.2',
    description='A Command Line Interface for interacting with Linux systems using OpenAI',
    author='Phosphorus',
    author_email='bailinwp4@163.com',
    packages=find_packages(),
    install_requires=[
        'openai',
    ],
    entry_points={
        'console_scripts': [
            'talk2=talk2linux.__main__:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Development Status :: 3 - Alpha'
    ],
    python_requires='>=3.6',
)
