#建索引
db.sms.createIndex({"smsid":1})
db.sms.ensureIndex({"keywords":"text"})

#安装python
wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz

tar -zxvf Python-2.7.3.tgz
cd Python-2.7.3
./configure –prefix=/usr/local/python2.7.10
make
make install
ln -s /usr/local/python2.7.3/bin/python /bin/python
# 安装numpy
tar -zxvf numpy-1.9.2.tar.gz
cd numpy-1.9.2
python setup.py install

# pip安装
 pip install --no-index --find-links=file:./py_packagesansible
pip install packages/*
“pip install --no-index --find-links=C:\packages -r PackagesInfo.txt”

pip freeze >> requirement.txt
pip download  -r requirements.txt  -d  /tmp/paks/
virtualenv venv

10.52.146.7/8
root
@G1W2S3S4I5
