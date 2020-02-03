## environment
python 3.8.1

## Ubuntu 16.04
```
sudo apt-get update
sudo apt install python3-pip
pip3 install --upgrade pip
sudo apt-get install xvfb
pip3 install pyvirtualdisplay

sudo apt install firefox
# OR
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A6DCF7707EBC211F
sudo apt-add-repository "deb http://ppa.launchpad.net/ubuntu-mozilla-security/ppa/ubuntu bionic main"
sudo apt-get update
sudo apt-get install firefox

```
### python3.8
```
sudo apt update
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget
sudo apt install libsqlite3-dev libbz2-dev liblzma-dev tk-dev tcl-dev
# uuid-dev

sudo apt install libncursesw5-dev  libdb-dev

cd ~/src
wget https://www.python.org/ftp/python/3.8.1/Python-3.8.1.tgz
tar -xf Python-3.8.1.tgz
cd Python-3.8.1/
./configure --enable-optimizations
make -j 1
sudo make altinstall
```

```
Python build finished successfully!
The necessary bits to build these optional modules were not found:
_bz2                  _lzma                 _sqlite3
_tkinter              _uuid
To find the necessary bits, look in setup.py in detect_modules() for the module's name.


The following modules found by detect_modules() in setup.py, have been
built by the Makefile instead, as configured by the Setup files:
_abc                  atexit                pwd
time
```
https://github.com/python/cpython/blob/3.8/README.rst

### selenium
https://selenium.dev/documentation/en/selenium_installation/installing_selenium_libraries/

web driver
Firefoxのを使う
https://github.com/mozilla/geckodriver/releases


```
pip3 install selenium
```
### pandas 等
```
pip3 install pandas
pip3 install matplotlib
pip3 install scikit-learn
```

### slack
```
pip3 install slackclient
```

### cron sample
毎週月曜と金曜の9:15分に実行
```
15 9 * * 1,5 user LC_CTYPE="C.UTF-8" /usr/local/bin/python3.8 /home/user/apps/mfme/dlCSV.py
```