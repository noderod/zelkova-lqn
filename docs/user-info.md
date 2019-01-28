### LDAP connections

All user credentials are stored inside an external LDAP for security purposes. Therefore, any organization wishing to utilize
Kauri must provide information on how to connect to its own LDAP server or create their own according to the bwlo information:


* **Creating an LDAP server**

The following commands will set-up a basic LDAP server to which users can be added built on docker containers. The server will issue a self-signed certificate,
some browsers may detect this and mark the page as unsafe.



```bash

cd ./pocket-ldap

# Start an ldap server
chmod +x build-test-ldap.sh
# admin_password is optional, and will be set to "test" if it is not provided
sudo ./build-test-ldap.sh $ORGANIZATION $URL $ADMIN_PASSWORD


# Open a browser and go to https://$URL:6443
















# NOTE: to bring down the LDAP server (deleting all information in it)
cd ./pocket-ldap
docker-compose down -v


```