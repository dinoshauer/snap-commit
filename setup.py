from setuptools import setup
import snapcommit

setup(
    name=snapcommit.name,
    version=snapcommit.version,
    author='Kasper Jacobsen',
    author_email='k@mackwerk.dk',
    description=snapcommit.__doc__,
    url=snapcommit.project_url,
    license='MIT',
    keywords='',
    packages=[
        'snapcommit'
    ],
    entry_points={
        'console_scripts': [
            'snapcommit = snapcommit.cli:cli',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
    install_requires=[
        'Pillow',
        'click',
        'pygit2',
        'requests',
        'v4l2',
        'v4l2capture',
    ],
)
