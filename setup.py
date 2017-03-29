from setuptools import setup, find_packages

def readfile(name):
    with open(name) as f:
        return f.read()

readme = readfile('README.rst')
changes = readfile('CHANGES.rst')

install_requires = [
    'PasteDeploy >= 1.5.0',  # py3 compat
    'plaster',
]

tests_require = [
    'pytest',
    'pytest-cov',
]

setup(
    name='plaster_pastedeploy',
    version='0.2',
    description=(
        'A loader implementing the PasteDeploy syntax to be used by plaster.'
    ),
    long_description=readme + '\n\n' + changes,
    author='Hunter Senft-Grupp',
    author_email='huntcsg@gmail.com',
    url='https://github.com/Pylons/plaster_pastedeploy',
    packages=find_packages('src', exclude=['tests']),
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    install_requires=install_requires,
    extras_require={
        'testing': tests_require,
    },
    zip_safe=False,
    keywords='plaster pastedeploy plaster_pastedeploy ini config egg',
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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    entry_points={
        'plaster.loader_factory': [
            'ini=plaster_pastedeploy:Loader',
            'ini+pastedeploy=plaster_pastedeploy:Loader',
            'egg=plaster_pastedeploy:Loader',
            'egg+pastedeploy=plaster_pastedeploy:Loader',
        ],
        'plaster.wsgi_loader_factory': [
            'ini=plaster_pastedeploy:Loader',
            'ini+pastedeploy=plaster_pastedeploy:Loader',
            'egg=plaster_pastedeploy:Loader',
            'egg+pastedeploy=plaster_pastedeploy:Loader',
        ],
    },
)
