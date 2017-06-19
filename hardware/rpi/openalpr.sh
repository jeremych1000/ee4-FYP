sudo apt-get -y install libopencv-dev libtesseract-dev git cmake build-essential libleptonica-dev
sudo apt-get -y install liblog4cplus-dev libcurl3-dev

# If using the daemon, install beanstalkd
sudo apt-get -y install beanstalkd

cd ~
# Clone the latest code from GitHub
git clone https://github.com/openalpr/openalpr.git

# Setup the build directory
cd openalpr/src
mkdir build
cd build

# setup the compile environment
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc ..

# compile the library
make

# Install the binaries/libraries to your local system (prefix is /usr)
sudo make install

# Test the library
wget http://plates.openalpr.com/h786poj.jpg -O lp.jpg
alpr lp.jpg