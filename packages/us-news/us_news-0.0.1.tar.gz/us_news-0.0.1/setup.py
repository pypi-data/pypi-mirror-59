from setuptools import setup, find_packages

# with open("README.md", "r") as f:
#     readme = f.read()

with open("requirements.txt", "r") as f:
    reqs = [lib.strip() for lib in f if lib]

setup(
    name="us_news",
    version="0.0.1",
    description="A web crawler to crawl Best Global University Ranking on usnews website",
    #long_description=readme,
    author='Low Wei Hong',
    author_email='M140042@e.ntu.edu.sg',
    url="https://github.com/M140042/us_news",
    packages=['us_news'],
    keywords="us_news",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        'console_scripts': [
            'dinner=dinner:main',
        ]
    },
    install_requires=reqs
)
