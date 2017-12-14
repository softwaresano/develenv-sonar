%define sonar_version 6.7
Name:       sonar-extras
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
Requires:   ss-develenv-sonar >=  %{versionModule}-%{sonar_version}
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
%{__mkdir_p} $RPM_BUILD_ROOT/%{target_dir}
cp -R %{_sourcedir}/extras/* $RPM_BUILD_ROOT/%{target_dir}

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
%{sonar_home}/extensions/*
%defattr(-,root,root,-)
%{sonar_home}/lib/*
%doc ../../../../README.md