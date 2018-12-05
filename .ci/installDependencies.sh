#/usr/bin/env sh

apt-get update
apt-get -y install python3-lz4 python3-msgpack python3-brotli python3-cbor python3-ujson
pip3 install --upgrade https://gitlab.com/KOLANICH/py-lmdb/-/jobs/artifacts/gitlab/raw/wheels/lmdb-0.CI_cpython_latest-py3-none-any.whl?job=build
python3 ./fix_python_modules_paths.py
