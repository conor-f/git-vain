from setuptools import (
    find_packages,
    setup
)

INSTALL_REQUIRES = (
    "apprise",
    "pygithub<=1.58.2",
    "requests",
)

setup(
    name='git_vain',
    version='1.1.0',
    python_requires='>=3.6',
    description='',
    long_description='',
    author='Conor Flynn',
    url='https://github.com/conor-f/git-vain',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': [
            'git-vain = git_vain.bin.git_vain:main',
            'star-repo = git_vain.bin.star_repo:main'
        ]
    }
)
