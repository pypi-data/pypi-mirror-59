from distutils.core import setup
from setuptools import find_packages

setup(
    name='coraline-eda',
    packages=find_packages(exclude=["coraline_eda_app"]),
    version='1.1',
    description='Coraline Expolatory Data Analysis Tool',
    long_description="""
    Coraline Expolatory Data Analysis Tool - Pandas Profiling
    """,
    author='Jiranun J., Wichanon U.',
    author_email='jiranun@coraline.co.th, wichanon.u@coraline.co.th',
    url='https://www.coraline.co.th',
    keywords=['eda', 'pandas', 'profiling', 'pyqt', 'coraline'],
    python_requires='>=3.6',
    classifiers=['Programming Language :: Python',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: MIT License',
                 'Natural Language :: English',
                 ],
    install_requires=['pandas',
                      'pandas-profiling',
                      'numpy',
                      'matplotlib',
                      'pyqt5',
                      'scipy',
                      'xlrd'
                      ],
    entry_points={
        'console_scripts': [
            'coraline-eda=coraline_eda.eda_app:run',
        ],
    },
)
