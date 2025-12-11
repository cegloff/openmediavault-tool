from setuptools import setup

setup(
    name='omv-tool',
    version='0.1.0',
    description='CLI tool for OpenMediaVault',
    author='Your Name',
    packages=['.'],
    install_requires=[
        'requests>=2.25.1',
        'click>=8.0.0',
    ],
    entry_points={
        'console_scripts': [
            'omv-tool = omv_tool:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
    ],
)
