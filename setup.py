import subprocess
import sys
from pathlib import Path

from setuptools import setup

import uplift

cwd = Path(__file__).resolve().parent


def generate_cython():
    print("Cythonizing sources")
    p = subprocess.call([sys.executable, cwd / 'cythonize.py', 'uplift'], cwd=cwd)
    if p != 0:
        raise RuntimeError("Running cythonize failed!")


def setup_package():
    metadata = dict(name='uplift',
                    maintainer='Paulius Sarka',
                    maintainer_email='paulius.sarka@gmail.com',
                    description='uplift models',
                    license='new BSD',
                    url='',
                    version=uplift.__version__,
                    long_description='',
                    classifiers=['Intended Audience :: Science/Research',
                                 'Intended Audience :: Developers',
                                 'License :: OSI Approved',
                                 'Programming Language :: C',
                                 'Programming Language :: Python',
                                 'Topic :: Software Development',
                                 'Topic :: Scientific/Engineering',
                                 'Operating System :: Microsoft :: Windows',
                                 'Operating System :: POSIX',
                                 'Operating System :: Unix',
                                 'Operating System :: MacOS',
                                 'Programming Language :: Python :: 3.6'],
                    zip_safe=False,
                    include_package_data=True,
                    install_requires=['numpy >= 1.6.1',
                                      'scipy >= 0.9',
                                      'joblib',
                                      'Cython'])

    if len(sys.argv) >= 2 and sys.argv[1] not in 'config':

        print('Generating cython files')
        if not (cwd / 'PKG-INFO').exists():
            generate_cython()

        # Clean left-over .so .pyd and .dll files
        for path in (cwd / 'uplift').glob('**/*'):
            if path.suffix in {'.so', '.pyd', '.dll'}:
                pyx_path = path.with_suffix('.pyx')
                print(pyx_path)
                if not pyx_path.exists():
                    path.unlink()

    setup(**metadata)


if __name__ == "__main__":
    setup_package()
