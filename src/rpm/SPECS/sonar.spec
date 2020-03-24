%define sonar_version 8.2.0.32929
Name:        sonar
Version:     %{versionModule}
Release:     %{sonar_version}.r%{releaseModule}
Epoch:       2
Summary:     An extendable open source continuous inspection
Group:       develenv
License:     http://creativecommons.org/licenses/by/3.0/
Packager:    softwaresano.com
URL:         https://www.sonarqube.org/
BuildArch:   x86_64
BuildRoot:   %{_topdir}/BUILDROOT
Requires:    httpd java-11-openjdk postgresql-server >= 10.6
AutoReqProv: no

Vendor:      softwaresano

%define package_name sonar
%define target_dir /
%define sonar_home /opt/ss/develenv/platform/sonar
%define sonar_home_logs /var/log/sonar
%define sonar_home_data /var/lib/sonar

%description
Sonar is the central place to manage code quality, offering visual reporting on
and across projects and enabling to replay the past to follow metrics evolution

# ------------------------------------------------------------------------------
# CLEAN
# ------------------------------------------------------------------------------
%clean
rm -rf $RPM_BUILD_ROOT

# ------------------------------------------------------------------------------
# INSTALL
# ------------------------------------------------------------------------------
%install
%{__mkdir_p} $RPM_BUILD_ROOT/%{target_dir} $RPM_BUILD_ROOT/%{sonar_home}

cp -R %{_sourcedir}/* $RPM_BUILD_ROOT/%{target_dir}
rm -rf $RPM_BUILD_ROOT/%{target_dir}/extras
cd $RPM_BUILD_ROOT/%{target_dir}
mkdir build
cd build
curl -L -k -O https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-%{sonar_version}.zip
unzip sonarqube-%{sonar_version}.zip
cd sonarqube-%{sonar_version}
cd extensions/plugins
rm -f sonar-csharp-plugin*.jar \
     sonar-vbnet-plugin*.jar \
     sonar-kotlin-plugin*.jar \
     sonar-flex-plugin*.jar \
     sonar-python-plugin*.jar \
     sonar-java-plugin*.jar \
     sonar-scm-git-plugin*.jar
curl -f -L -k -O https://github.com/Inform-Software/sonar-groovy/releases/download/1.6/sonar-groovy-plugin-1.6.jar
curl -f -L -k -O https://github.com/sbaudoin/sonar-yaml/releases/download/v1.5.1/sonar-yaml-plugin-1.5.1.jar
curl -f -L -k -O https://binaries.sonarsource.com/Distribution/sonar-python-plugin/sonar-python-plugin-2.7.0.5975.jar
curl -f -L -k -O https://github.com/sbaudoin/sonar-shellcheck/releases/download/v2.3.0/sonar-shellcheck-plugin-2.3.0.jar
curl -f -L -k https://binaries.sonarsource.com/Distribution/sonar-java-plugin/sonar-java-plugin-6.2.0.21135.jar
curl -f -L -k https://binaries.sonarsource.com/Distribution/sonar-scm-git-plugin/sonar-scm-git-plugin-1.11.0.11.jar
cd ../../
rm -rf bin/windows-x86-64
cd ../../
mv build/sonarqube-%{sonar_version}/* $RPM_BUILD_ROOT/%{sonar_home}/
rm -rf build 
sed -i s:^PIDDIR.*:PIDDIR=/tmp:g $RPM_BUILD_ROOT/%{sonar_home}/bin/linux-x86-64/sonar.sh
%{__mkdir_p} $RPM_BUILD_ROOT/%{sonar_home_logs}/http
%{__mkdir_p} $RPM_BUILD_ROOT/%{sonar_home_data}/temp $RPM_BUILD_ROOT/%{sonar_home_data}/data
mv ${RPM_BUILD_ROOT}/%{sonar_home}/temp $RPM_BUILD_ROOT/%{sonar_home_data}/
mv ${RPM_BUILD_ROOT}/%{sonar_home}/data $RPM_BUILD_ROOT/%{sonar_home_data}/
ln -sf %{sonar_home_data}/temp $RPM_BUILD_ROOT/%{sonar_home}
ln -sf %{sonar_home_data}/data $RPM_BUILD_ROOT/%{sonar_home}

cat <<EOF >>  $RPM_BUILD_ROOT/%{sonar_home}/conf/sonar.properties
# Default configuration for sonar with develenv
sonar.path.logs=%{sonar_home_logs}
sonar.jdbc.username=sonar
sonar.jdbc.password=sonar
sonar.jdbc.url=jdbc:postgresql://localhost/sonar
sonar.path.data=%{sonar_home_data}/data
sonar.path.temp=%{sonar_home_data}/temp
EOF

mkdir -p $RPM_BUILD_ROOT/etc
ln -sf %{sonar_home}/conf $RPM_BUILD_ROOT/etc/sonar
rm -rf $RPM_BUILD_ROOT/%{sonar_home}/logs
ln -sf %{sonar_home_logs} $RPM_BUILD_ROOT/%{sonar_home}/logs

%{__mkdir_p} $RPM_BUILD_ROOT/%{sonar_home}/extensions/downloads
# ------------------------------------------------------------------------------
# PRE-INSTALL
# ------------------------------------------------------------------------------
%pre
groupadd -r -f sonar
grep -q sonar /etc/passwd
if [ $? -ne 0 ]; then
  useradd -d /var/lib/sonar -g sonar -M -r sonar -s /sbin/nologin
fi

# ------------------------------------------------------------------------------
# POST-INSTALL
# ------------------------------------------------------------------------------
%post
systemctl daemon-reload
systemctl try-restart httpd

# ------------------------------------------------------------------------------
# PRE-UNINSTALL
# ------------------------------------------------------------------------------
%preun
if [ "$1" = 0 ] ; then
    # if this is uninstallation as opposed to upgrade, delete the service
    systemctl stop develenv-sonar > /dev/null 2>&1
    systemctl disable develenv-sonar > /dev/null 2>&1
    systemctl try-restart httpd
    exit 0
fi
# ------------------------------------------------------------------------------
# POST-UNINSTALL
# ------------------------------------------------------------------------------
%postun
%files
%defattr(-,sonar,sonar,-)
%dir %{sonar_home_logs}
%dir %{sonar_home_logs}/http
%dir %{sonar_home_data}/data
%dir %{sonar_home_data}/temp
/etc/sonar
%{sonar_home}/data
%{sonar_home}/temp
%{sonar_home}/logs
%{sonar_home}/extensions/*
%dir %{sonar_home}/extensions/downloads
%defattr(-,root,root,-)
%{sonar_home}/bin/*
%config %{sonar_home}/conf/*
%{sonar_home}/elasticsearch/*
%{sonar_home}/lib/*
%{sonar_home}/web/*
%{sonar_home}/COPYING
%{target_dir}/etc/httpd/conf.d/*
/etc/systemd/system/*
%doc ../../../../README.md
