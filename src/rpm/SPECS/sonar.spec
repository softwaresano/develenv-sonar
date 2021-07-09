%define sonar_version 9.0.0.45539
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
function download(){
  curl -f -L -k -O "$1" || exit 1
}

%{__mkdir_p} $RPM_BUILD_ROOT/%{target_dir} $RPM_BUILD_ROOT/%{sonar_home}
cp -R %{_sourcedir}/* $RPM_BUILD_ROOT/%{target_dir}
rm -rf $RPM_BUILD_ROOT/%{target_dir}/extras
cd $RPM_BUILD_ROOT/%{target_dir}
mkdir build
cd build
download https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-%{sonar_version}.zip
unzip sonarqube-%{sonar_version}.zip
cd sonarqube-%{sonar_version}
cd extensions/plugins
rm -f sonar-csharp-plugin*.jar \
     sonar-vbnet-plugin*.jar \
     sonar-kotlin-plugin*.jar \
     sonar-flex-plugin*.jar \
     sonar-python-plugin*.jar \
     sonar-java-plugin*.jar \
     sonar-scm-git-plugin*.jar \
     sonar-cxx-plugin-*.jar \
     sonar-c-plugin-*.jar \
     sonar-rci-plugin-*.jar \
     qualinsight-plugins-sonarqube-badges-*.jar \
     sonar-scm-git-plugin-*.jar \
     sonar-perl-plugin-*.jar
# http://cdn-nfs.cdn.hi.inet/develenv/repositories/artifacts/sonar-shellcheck-plugin-1.1.3.jar
for i in \
  https://github.com/sonar-perl/sonar-perl/releases/download/0.5.3/sonar-perl-plugin-0.5.3-all.jar \
  https://binaries.sonarsource.com/Distribution/sonar-scm-git-plugin/sonar-scm-git-plugin-1.12.1.2064.jar \
  https://github.com/Inform-Software/sonar-groovy/releases/download/1.7/sonar-groovy-plugin-1.7.jar \
  https://github.com/sbaudoin/sonar-yaml/releases/download/v1.5.2/sonar-yaml-plugin-1.5.2.jar \
  https://binaries.sonarsource.com/Distribution/sonar-python-plugin/sonar-python-plugin-3.5.0.8244.jar \
  http://cdn-nfs.cdn.hi.inet/develenv/repositories/artifacts/sonar-shellcheck-plugin-1.1.3.jar \
  https://binaries.sonarsource.com/Distribution/sonar-java-plugin/sonar-java-plugin-7.1.0.26670.jar \
  https://binaries.sonarsource.com/Distribution/sonar-html-plugin/sonar-html-plugin-3.4.0.2754.jar \
  https://github.com/SonarOpenCommunity/sonar-cxx/releases/download/cxx-2.04/sonar-cxx-plugin-2.0.4.2806.jar \
  https://github.com/willemsrb/sonar-rci-plugin/releases/download/sonar-rci-plugin-1.0.2/sonar-rci-plugin-1.0.2.jar \
  https://github.com/cnescatlab/sonar-hadolint-plugin/releases/download/1.0.0/sonar-hadolint-plugin-1.0.0.jar \
  https://binaries.sonarsource.com/Distribution/sonar-php-plugin/sonar-php-plugin-3.9.0.6331.jar \
  https://binaries.sonarsource.com/Distribution/sonar-ruby-plugin/sonar-ruby-plugin-1.8.3.2219.jar \
  https://binaries.sonarsource.com/Distribution/sonar-xml-plugin/sonar-xml-plugin-2.2.0.2973.jar \
  https://binaries.sonarsource.com/Distribution/sonar-typescript-plugin/sonar-typescript-plugin-2.1.0.4359.jar \
  https://github.com/QualInsight/qualinsight-plugins-sonarqube-badges/releases/download/qualinsight-plugins-sonarqube-badges-3.0.1/qualinsight-sonarqube-badges-3.0.1.jar; do
  download "$i" 
done
cd ../../
cd lib
rm -f sslr-cxx-toolkit-*.jar
download https://github.com/SonarOpenCommunity/sonar-cxx/releases/download/cxx-1.3.2/sslr-cxx-toolkit-1.3.2.1853.jar
cd ../
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
