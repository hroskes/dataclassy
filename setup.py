from setuptools import setup

setup(
    name='dataclassy',
    version='0.1',
    author='biqqles',
    author_email='biqqles@protonmail.com',
    description="An alternative to Python's dataclasses",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/biqqles/deconstruct',
    packages=['dataclassy'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
    ],
    python_requires='>=3.6',
)