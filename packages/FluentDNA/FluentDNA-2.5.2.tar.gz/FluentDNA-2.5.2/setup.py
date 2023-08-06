from FluentDNA import VERSION
from setuptools import setup, find_packages

utils_ver = '1.0.13'

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='FluentDNA',
    version=VERSION,
    description='Visualization tool for bare fasta files.  Supports whole genome alignment and multiple sequence alignment.',
    author='Josiah Seaman, Bryan Hurst',
    author_email='josiah@newline.us',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=('build', 'obj', 'results')),
    include_package_data=True,
    package_data={'FluentDNA': ['html_template/*', 'example_data/*',
                          'html_template/img/*', 'example_data/alignments/*',]},
    scripts=['FluentDNA/fluentdna.py'],
    install_requires=[
        'Pillow>=3.2.0',
        'psutil>=5.4.5',
        # 'blist>=1.3.6',
        'natsort>=5.1.1',
        'numpy>=1.13.3',
        'DNASkittleUtils>=' + utils_ver,
    ],
    extras_require = {'optimized_alignment': ['blist>=1.3.6']}, #for optional packages
    zip_safe=False,
    url='https://github.com/josiahseaman/FluentDNA',
    download_url='https://github.com/josiahseaman/FluentDNA',
    keywords=['bioinformatics', 'dna', 'fasta', 'chain', 'alignment', 'species diversity'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
)