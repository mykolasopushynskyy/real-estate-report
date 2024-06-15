from setuptools import setup, find_packages

setup(
    name='Real estate parser',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'start=app.application:main',
        ]
    },
    install_requires=[
        "setuptools~=65.5.1",
        "requests~=2.32.3",
        "pandas~=2.2.2",
        "beautifulsoup4~=4.4.1",
        "plotly~=5.22.0",
        "packaging~=24.1",
        "progressbar~=2.5",
        "typing_extensions~=4.12.2"
    ]
)