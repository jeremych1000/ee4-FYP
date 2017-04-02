sudo apt-get -y update

# remove changelogs
sudo apt-get remove apt-listchanges

sudo apt-get -y upgrade

sudo apt-get -y install sudo cmake curl dos2unix emacs g++ gedit git git-core java-common java-package make perl python3 python3-pip ssh 
sudo apt-get -y install libtiff5-dev libopencv-dev libjpeg-dev libssl-dev
sudo apt-get -y install apache2

pip3 install django django-bootstrap3 djangorestframework django-sendfile Sphinx django-docs django-ipware geopy geoip2 django_cron
