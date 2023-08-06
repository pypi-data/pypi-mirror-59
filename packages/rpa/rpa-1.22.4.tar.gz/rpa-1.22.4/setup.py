from setuptools import setup

setup(
    name='rpa',
    version='1.22.4',
    py_modules=['rpa'], install_requires=['tagui>=1.22.4'],
    author='Ken Soh',
    author_email='opensource@tebel.org',
    license='Apache License 2.0',
    url='https://github.com/tebelorg/TagUI-Python',
    description='TagUI for Python is a Python package for RPA (robotic process automation)',
    long_description='TagUI for Python homepage - https://github.com/tebelorg/TagUI-Python',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
