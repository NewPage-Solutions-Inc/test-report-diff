#!/usr/bin/env python

"""The setup/install script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = ['Click>=8.1.3', ]

test_requirements = ['pytest>=6', ]

setup(
    author="NewPage Solutions",
    author_email='InnovationDesk@newpage.io',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Software Development :: Quality Assurance',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    description="A script to get the diff of 2 test reports. Helps with triaging/investigating large test reports",
    entry_points={
        'console_scripts': [
            'test_report_diff=test_report_diff.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='test report, diff, triage, compare reports',
    name='test_report_diff',
    packages=find_packages(include=['test_report_diff', 'test_report_diff.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/newpage-solutions-inc/test_report_diff',
    version='0.1.0',
    zip_safe=False,
)
