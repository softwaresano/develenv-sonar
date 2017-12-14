%define sonar_version 6.7
Name:       sonar
Version:    %{versionModule}
Release:    %{sonar_version}.%{releaseModule}
Epoch:      2
Summary:    An extendable open source continuous inspection
Group:      develenv
License:    http://creativecommons.org/licenses/by/3.0/
Packager:   softwaresano.com
URL:        https://www.sonarqube.org/
BuildArch:  x86_64
BuildRoot:  %{_topdir}/BUILDROOT
Requires:   ss-develenv-user >= 33 httpd jdk mysql-server
AutoReqProv: no

Vendor:     softwaresano

%define package_name sonar
%define target_dir /
%define sonar_home /opt/ss/develenv/platform/sonar

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
curl -L -k -O https://sonarsource.bintray.com/Distribution/sonarqube/sonarqube-%{sonar_version}.zip
unzip sonarqube-%{sonar_version}.zip
cd sonarqube-%{sonar_version}
cd ../../
mv build/sonarqube-%{sonar_version}/* $RPM_BUILD_ROOT/%{sonar_home}/
rm -rf build 
sed -i s:^PIDDIR.*:PIDDIR=/tmp:g $RPM_BUILD_ROOT/%{sonar_home}/bin/linux-x86-64/sonar.sh
%{__mkdir_p} $RPM_BUILD_ROOT/%{sonar_home}/logs
%{__mkdir_p} $RPM_BUILD_ROOT/%{sonar_home}/temp $RPM_BUILD_ROOT/%{sonar_home}/data
%{__mkdir_p} $RPM_BUILD_ROOT/%{sonar_home}/extensions/downloads
# ------------------------------------------------------------------------------
# PRE-INSTALL
# ------------------------------------------------------------------------------
%pre
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
%defattr(-,develenv,develenv,-)
%dir %{sonar_home}/logs
%dir %{sonar_home}/data
%dir %{sonar_home}/temp
%{sonar_home}/extensions/*
%dir %{sonar_home}/extensions/downloads
%defattr(-,root,root,-)
%{sonar_home}/bin/*
%config(noreplace) %{sonar_home}/conf/*
%{sonar_home}/elasticsearch/*
%{sonar_home}/lib/*
%{sonar_home}/web/*
%{sonar_home}/COPYING
%{target_dir}/etc/httpd/conf.d/*
/etc/systemd/system/*
%doc ../../../../README.md