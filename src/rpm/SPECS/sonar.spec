# rpmbuild -bb SPECS/jenkins.spec --define '_topdir '`pwd` -v --clean
%define sonar_version 6.7
Name:       sonar
Version:    %{versionModule}
Release:    %{sonar_version}.%{releaseModule}
Epoch:      2
Summary:    An extendable open source continuous integration server
Group:      develenv
License:    http://creativecommons.org/licenses/by/3.0/
Packager:   softwaresano.com
URL:        http://jenkins-ci.org/
BuildArch:  x86_64
BuildRoot:  %{_topdir}/BUILDROOT
Requires:   ss-develenv-user >= 33 httpd jdk mod_proxy_html
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
%{__mkdir_p} $RPM_BUILD_ROOT/%{target_dir} $RPM_BUILD_ROOT/%{sonar_home}/logs
%{__mkdir_p} $RPM_BUILD_ROOT/%{sonar_home}/temp $RPM_BUILD_ROOT/%{sonar_home}/web

cp -R %{_sourcedir}/* $RPM_BUILD_ROOT/%{target_dir}
# ------------------------------------------------------------------------------
# PRE-INSTALL
# ------------------------------------------------------------------------------
%pre
# ------------------------------------------------------------------------------
# POST-INSTALL
# ------------------------------------------------------------------------------
%post


# ------------------------------------------------------------------------------
# PRE-UNINSTALL
# ------------------------------------------------------------------------------
%preun
# ------------------------------------------------------------------------------
# POST-UNINSTALL
# ------------------------------------------------------------------------------
%postun
%files
%defattr(-,develenv,develenv,-)
%dir %{sonar_home}/logs
%dir %{sonar_home}/data
%dir %{sonar_home}/temp
%defattr(-,root,root,-)
%{sonar_home}
%{target_dir}/etc/httpd/conf.d/*
/etc/systemd/system/*
%doc ../../../../README.md