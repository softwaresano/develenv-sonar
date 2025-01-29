#!/bin/bash -ex
systemctl daemon-reload
systemctl stop develenv-sonar || true
postgresql_version=16
sonar_repo=http://cdn-nfs.cdn.hi.inet/develenv/repositories/releases/38/el8/developers/initiative/x86_64/
dnf remove -y ss-develenv-sonar postgresql-server postgresql postgresql-contrib
rm -rfv /var/lib/pgsql /etc/postgresql-* /var/lib/sonar /var/log/sonar /etc/sonar
dnf clean all
dnf --enablerepo=mirror-rhel-8-for-x86_64-appstream-rpms module disable postgresql -y
dnf --enablerepo=mirror-rhel-8-for-x86_64-appstream-rpms module enable "postgresql:${postgresql_version:?}" -y
dnf --enablerepo=mirror-rhel-8-for-x86_64-appstream-rpms install -y polkit initscripts httpd java-17-openjdk postgresql-server postgresql postgresql-contrib
alternatives --set java /usr/lib/jvm/"$(rpm -q --queryformat '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}\n' java-17-openjdk)"/bin/java
postgresql-setup --initdb
# Descomprimir conf
curl -f http://cdn-nfs.cdn.hi.inet/develenv/repositories/releases/latest/el8/rc/resources/cdn-build/docs/includes/cdn-builder/postgresql_conf.tar.gz | tar xvz -C /
systemctl start postgresql
systemctl enable postgresql
sudo -u postgres psql <<EOF
CREATE ROLE sonar WITH LOGIN PASSWORD 'sonar';
CREATE DATABASE sonar OWNER sonar;
EOF
sysctl -w vm.max_map_count=262144 || true
echo "If is a docker container, run sudo sysctl -w vm.max_map_count=262144"
sysctl vm.max_map_count | grep "262144" || exit 1
dnf install -y --repofrompath=sonar_repo,"${sonar_repo:?}" --enablerepo=sonar_repo --setopt=sonar_repo.gpgcheck=0 httpd ss-develenv-sonar
systemctl start develenv-sonar
systemctl enable develenv-sonar
sleep 70
systemctl restart httpd
/opt/ss/develenv/platform/sonar/bin/users/change_admin_password.sh temporal
/opt/ss/develenv/platform/sonar/bin/users/add_sonar_user.sh
/opt/ss/develenv/platform/sonar/bin/profiles/configure_profiles.rb
