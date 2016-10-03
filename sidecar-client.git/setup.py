try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='python-sidecarclient',
    version='2.0',
    description='Sidecar client is a helpper method tp connect to sidecar REST API',
    long_description = 'Sidecar client is a helpper method tp connect to sidecar REST API',
    author='Binoy MV, Dinesh Patra',
    author_email='binoy.mv@poornam.com, dineshpatra28@gmail.com',
    license='NephoScale',
    keywords='Nova evacuation',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    entry_points={
        'console_scripts': [
            'sidecar=sidecarclient.shell:main',
        ],
    },
)

