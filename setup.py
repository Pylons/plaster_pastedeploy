from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, 'README.rst')) as f:
        readme = f.read()
    with open(os.path.join(here, 'CHANGES.txt')) as f:
        CHANGES = f.read()
except IOError:
    readme = changes = ''


install_requires = [
    'PasteDeploy >= 1.5.0',  # py3 compat
    'plaster',
]

docs_require = [
    'Sphinx',
    'pylons-sphinx-themes',
]

tests_require = [
    'nose',
    'nose-exclude',
    'coverage',
    'mock',
]

setup(
    name='plaster_pastedeploy',
    version='0.1.0',
    description=(
        'A loader implementing the PasteDeploy loading syntax to be used '
        'by plaster.'
    ),
    long_description=readme + '\n\n' + changes,
    author='Hunter Senft-Grupp',
    author_email='huntcsg@gmail.com',
    url='https://github.com/mmerickel/plaster_pastedeploy',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        'docs': docs_require,
        'testing': tests_require,
    },
    test_suite='tests',
    zip_safe=False,
    keywords='plaster pastedeploy plaster_pastedeploy ini config',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    entry_points={
        'plaster.loader': [
            'ini+pastedeploy=plaster_pastedeploy:Loader',
            'config+pastedeploy=plaster_pastedeploy:Loader',
            'call+pastedeploy=plaster_pastedeploy:Loader',
            'egg+pastedeploy=plaster_pastedeploy:Loader',
        ],
    },
)
