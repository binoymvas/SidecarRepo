# Shell script to install sidecar REST api
#
# CopyRight: 2016@NephoScale <info@nephoscale.com>
#
# Start Date: 20th August 2016
#
# Make sure the requirements.txt file is in the same folder
# Before executing this script

####################################################
# SIDECAR LINUX USER CREATION                      #
###################################################
groupadd sidecar
useradd -d /var/lib/sidecar -g sidecar -m sidecar
apt-get install crudini -y

#################################################################
# CONFIGURATION                                                 #
#################################################################
_PORT=9090
_CURRENT_DIR=$(pwd)
_MYSQL_ROOT_USER=root
_MYSQL_ROOT_PWD=demo

# For keystone version 3
_KEYSTONE_ADMIN_USERNAME=admin
_KEYSTONE_ADMIN_PASSWORD=demo
_KEYSTONE_ADMIN_PROJECTNAME=demo
_KEYSTONE_ADMIN_AUTH_URL=http://controller:35357/v3
_KEYSTONE_ADMIN_PROJECT_DOMAIN_ID=default
_KEYSTONE_ADMIN_USER_DOMAIN_ID=default
_KEYSTONE_AUTH_VERSION=3

# For Keystone version 2
_KEYSTONE_ADMIN_USERNAME=admin
_KEYSTONE_ADMIN_PASSWORD=demo
_KEYSTONE_ADMIN_TENANTNAME=demo
_KEYSTONE_ADMIN_AUTH_URL=http://controller:35357/v3
_KEYSTONE_AUTH_VERSION=2

_SIDECAR_DBNAME=sidecar
_SIDECAR_DBUSER=sidecar
_SIDECAR_DBPASS=demo
_SIDECAR_DBHOST=controller  # (this will be same as bind-params in useradd -d /var/lib/sidecar -g sidecar -m sidecar)

####################################################################
# MYSQL SETUP                                                      #
####################################################################
echo "CREATE DATABASE  $_SIDECAR_DBNAME" | mysql -u"$_MYSQL_ROOT_USER" -p"$_MYSQL_ROOT_PWD"
SQL1="GRANT ALL PRIVILEGES ON $_SIDECAR_DBNAME.* TO '$_SIDECAR_DBUSER'@'$_SIDECAR_DBHOST' IDENTIFIED BY '$_SIDECAR_DBPASS'"
SQL2="GRANT ALL PRIVILEGES ON $_SIDECAR_DBNAME.* TO '$_SIDECAR_DBUSER'@'%'                IDENTIFIED BY '$_SIDECAR_DBPASS'"
mysql -u "$_MYSQL_ROOT_USER" -p"$_MYSQL_ROOT_PWD" -e "$SQL1"
mysql -u "$_MYSQL_ROOT_USER" -p"$_MYSQL_ROOT_PWD" -e "$SQL2"
_DB_CONNECTION=mysql+pymysql://$_SIDECAR_DBUSER:$_SIDECAR_DBPASS@$_SIDECAR_DBHOST/$_SIDECAR_DBNAME?charset=utf8


##########################################################
# SIDECAR CONFIGURATION FILE                             #
##########################################################
mkdir /etc/sidecar
_SIDECAR_CONF_FILE=/etc/sidecar/sidecar.conf
touch $_SIDECAR_CONF_FILE

crudini --set $_SIDECAR_CONF_FILE   keystone_auth   username     $_KEYSTONE_ADMIN_USERNAME
crudini --set $_SIDECAR_CONF_FILE   keystone_auth   password     $_KEYSTONE_ADMIN_PASSWORD
crudini --set $_SIDECAR_CONF_FILE   keystone_auth   auth_url     $_KEYSTONE_ADMIN_AUTH_URL
crudini --set $_SIDECAR_CONF_FILE   keystone_auth   auth_plugin  password
crudini --set $_SIDECAR_CONF_FILE   keystone_auth   auth_version $_KEYSTONE_AUTH_VERSION
crudini --set $_SIDECAR_CONF_FILE   keystone_auth   tenant_name  $_KEYSTONE_ADMIN_TENANTNAME

crudini --set $_SIDECAR_CONF_FILE   database       connection    $_DB_CONNECTION


#########################################################
# CONFIGUREATION OF WSGI SCRIPT                         #
#########################################################
cp -p $_CURRENT_DIR/wsgi-sidecar             /usr/bin/
cp -pr $_CURRENT_DIR/sidecar/sidecar/sidecar /usr/local/lib/python2.7/dist-packages/

############################################################
# CONFIGURATION OF API_PASE.INI                            #
############################################################
cp $_CURRENT_DIR/api_paste.ini /etc/sidecar
cp $_CURRENT_DIR/policy.json /etc/sidecar


###################################################################
# APACHE CONFIGURATION                                            #
###################################################################
_WSGI_SIDECAR=/usr/bin/wsgi-sidecar
_ERROR_LOG=/var/log/apache2/sidecar.log
_ACCESS_LOG=/var/log/apache2/sidecar_access.log
_SITES_AVAILABLE="Listen $_PORT\n
<VirtualHost *:$_PORT>\n\t
WSGIDaemonProcess sidecar processes=2 threads=10 user=sidecar group=sidecar display-name=%{GROUP}\n\t
WSGIProcessGroup  sidecar\n\t
WSGIScriptAlias  / $_WSGI_SIDECAR\n\t
WSGIApplicationGroup %{GLOBAL}\n\t
<IfVersion >= 2.4>\n\t\t
ErrorLogFormat \"%{cu}t %M\"\n\t
</IfVersion>\n\t
<Directory /usr/bin>\n\t\t
<IfVersion >= 2.4>\n\t\t\t
Require all granted\n\t\t
</IfVersion>\n\t\t
<IfVersion < 2.4>\n\t\t\t
Order allow,deny\n\t\t\t
Allow from all\n\t\t
</IfVersion>\n\t
</Directory>\n\t
ErrorLog $_ERROR_LOG\n\t
CustomLog $_ACCESS_LOG combined\n
</VirtualHost>\n
WSGISocketPrefix /var/run/apache2"
touch /etc/apache2/sites-available/sidecar.conf
echo $_SITES_AVAILABLE > /etc/apache2/sites-available/sidecar.conf
ln -s /etc/apache2/sites-available/sidecar.conf /etc/apache2/sites-enabled/sidecar.conf

# Install the required packages and restart the apache2
pip install -r $_CURRENT_DIR/requirements.txt
service apache2 restart
