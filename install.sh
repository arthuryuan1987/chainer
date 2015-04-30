#!/bin/sh

mkdir .install-tmp
cd .install-tmp

pip install pycuda
pip install Mako
git clone https://github.com/lebedov/scikits.cuda
cd scikits.cuda
python setup.py install
cd ..

git clone https://github.com/hannes-brt/cudnn-python-wrappers
cd cudnn-python-wrappers
python setup.py install
cd ..

cd ..
python setup.py install

echo
echo 'Now you can use chainer by import chainer.'
echo 'If you want to run unittests, install nose (pip install nose) and'
echo 'run nosetests command at "tests" directory (not this directory).'
