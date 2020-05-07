%define sonar_version 4.3.0.2102
Name:        sonar-scanner
Version:     %{versionModule}
Release:     %{sonar_version}.r%{releaseModule}
Epoch:       2
Summary:     Sonar scanner
Group:       develenv
License:     http://creativecommons.org/licenses/by/3.0/
Packager:    softwaresano.com
URL:         https://www.sonarqube.org/
BuildArch:   x86_64
BuildRoot:   %{_topdir}/BUILDROOT
Requires:    java-11-openjdk
AutoReqProv: no

Vendor:      softwaresano

%define package_name sonar-scanner
%define target_dir /
%define sonar_home /opt/ss/develenv/platform/%{package_name}
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
SONAR_VERSION=%{sonar_version}
%{__mkdir_p} $RPM_BUILD_ROOT/%{sonar_home}

cp -R %{_sourcedir}/* $RPM_BUILD_ROOT/%{target_dir}
cd $RPM_BUILD_ROOT
mkdir build
cd build
curl -L -k -O https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${SONAR_VERSION}-linux.zip
unzip sonar-scanner-cli-${SONAR_VERSION}-linux.zip
cd sonar-scanner-${SONAR_VERSION}-linux
rm -rf jre
sed -i 's:use_embedded_jre=true:use_embedded_jre=false:g' bin/sonar-scanner
cd ../../
mv build/sonar-scanner-${SONAR_VERSION}-linux/* $RPM_BUILD_ROOT/%{sonar_home}/
rm -rf build 
mkdir -p $RPM_BUILD_ROOT/usr/bin
ln -sf %{sonar_home}/bin/sonar-scanner $RPM_BUILD_ROOT/usr/bin/sonar-scanner
ln -sf %{sonar_home}/bin/sonar-scanner-debug $RPM_BUILD_ROOT/usr/bin/sonar-scanner-debug
mkdir -p $RPM_BUILD_ROOT/etc
ln -sf %{sonar_home}/conf $RPM_BUILD_ROOT/etc/%{package_name}

%files
%defattr(-,root,root,-)
%{sonar_home}/*
/usr/bin/*
/etc/%{package_name}
%config %{sonar_home}/conf/*

%doc ../../../../README.md
