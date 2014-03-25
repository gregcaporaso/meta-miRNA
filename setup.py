#!/usr/bin/env python

from distutils.core import setup
from distutils.command.build_py import build_py
from glob import glob
from sys import platform, argv
from urllib import urlopen
from StringIO import StringIO
import tarfile


# if egg_info is passed as an argument do not build any of the dependencies
if 'egg_info' not in argv:
    url = None
    prefix = ""
    if platform == 'darwin':
        url = urlopen("ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.3.5/sratoolkit.2.3.5-mac64.tar.gz")
        prefix = "sratoolkit.2.3.5-mac64"
    elif platform == 'linux2':
        url = urlopen("http://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.3.5/sratoolkit.2.3.5-ubuntu64.tar.gz")
        prefix = "sratoolkit.2.3.5-ubuntu64"
    else:
        raise SystemError(platform + " platform not supported by miMAP")

    url_f = StringIO(url.read())
    tar_f = tarfile.open(fileobj=url_f, mode='r:gz')
    fastq_dump = tar_f.extractfile(prefix+'/bin/fastq-dump.2.3.5')
    with open('scripts/fastq-dump.2.3.5', 'w') as f:
        f.write(fastq_dump.read())
        f.close()
        fastq_dump.close()
        tar_f.close()
        url_f.close()
        url.close()


setup(name='miMAP',
      cmdclass = {'build_py':build_py},
      version='1.0',
      description='Python Distribution Utilities',
      author='Giorgio Casaburi',
      author_email='casaburi@ceinge.unina.it',
      url='https://github.com/casaburi/miMAP?source=cc',
      packages=['mimap',
                'mimap/commands',
                'mimap/interfaces',
                'mimap/interfaces/html',
                'mimap/interfaces/html/config'],
      install_requires=["pyqi == 0.3.1-dev",
                        "qiime == 1.8.0"],
      dependency_links=[
          'https://github.com/bipy/pyqi/archive/master.zip#egg=pyqi-0.3.1-dev'
      ],
      scripts=glob('scripts/*')
     )