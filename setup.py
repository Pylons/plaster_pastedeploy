from setuptools import setup, find_packages

def readfile(name):
    with open(name) as f:
        return f.read()

readme = readfile('README.rst')
changes = readfile('CHANGES.rst')

install_requires = [
    'PasteDeploy >= 1.5.0',  # py3 compat
    'plaster >= 0.5',  # file schemes
]

tests_require = [
    'pytest',
    'pytest-cov',
]

setup(
    name='plaster_pastedeploy',
    version='0.6',
    description=(
        'A loader implementing the PasteDeploy syntax to be used by plaster.'
    ),
    long_description=readme + '\n\n' + changes,
    author='Hunter Senft-Grupp',
    author_email='pylons-discuss@googlegroups.com',
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
        'Development Status :: 5 - Production/Stable',
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
            'file+ini=plaster_pastedeploy:Loader',
            'egg=plaster_pastedeploy:Loader',
            'pastedeploy=plaster_pastedeploy:Loader',
            'pastedeploy+ini=plaster_pastedeploy:Loader',
            'pastedeploy+egg=plaster_pastedeploy:Loader',
        ],
        'plaster.wsgi_loader_factory': [
            'file+ini=plaster_pastedeploy:Loader',
            'egg=plaster_pastedeploy:Loader',
            'pastedeploy=plaster_pastedeploy:Loader',
            'pastedeploy+ini=plaster_pastedeploy:Loader',
            'pastedeploy+egg=plaster_pastedeploy:Loader',
        ],
    },
)
