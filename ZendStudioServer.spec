Summary:	ZendStudioServer - server management tools for PHP based Web servers
Summary(pl.UTF-8):   ZendStudioServer - narzędzia zarządzające dla serwerów WWW opartych na PHP
Name:		ZendStudioServer
Version:	5.1.0a
Release:	0.1
Epoch:		0
License:	Zend Studio License
Group:		Applications
Source0:	http://downloads.zend.com/studio/5.1.0/%{name}-%{version}-linux-glibc21-i386.tar.gz
# NoSource0-md5:	99672eec3502fb0aa6d779cc66333772
NoSource:	0
Source1:	http://downloads.zend.com/studio/5.1.0/%{name}-%{version}-linux-glibc23-x86_64.tar.gz
# NoSource1-md5:	a7ddb3b964fe0c1746b0f7b8a5093423
NoSource:	1
URL:		http://downloads.zend.com/studio/5.1.0/
BuildRequires:	rpmbuild(macros) >= 1.344
BuildRequires:	tar >= 1:1.15.1
# circular dependency, so ones upgraded are forced to choose php and
# ones that want to install specific for specific version need not to
# install ZendStudioServer separately
Requires:	%{name}(php) = %{version}-%{release}
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_datadir	%{_prefix}/share/Zend
%define		no_install_post_strip		1
%define		no_install_post_chrpath		1

%description
Includes server management tools that manage PHP based Web servers.
This module makes installation and integration seamless while
simplifying PHP and remote debugging configurations and security
maintenance.

%description -l pl.UTF-8
Ten pakiet zawiera narzędzia zarządzające serwerem dla serwerów WWW
opartych na PHP. Ten moduł pozwala na przezroczystą instalację i
integrację jednocześnie upraszczając konfiguracje PHP ze zdalną
diagnostyką oraz zarządzanie bezpieczeństwem.

%package -n php4-%{name}
Summary:	ZendStudioServer for PHP 4.x
Summary(pl.UTF-8):   ZendStudioServer dla PHP 4.x
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	php4-ZendOptimizer
Provides:	%{name}(php) = %{version}-%{release}

%description -n php4-%{name}
ZendStudioServer for PHP 4.x.

%description -n php4-%{name} -l pl.UTF-8
ZendStudioServer dla PHP 4.x.

%package -n php-%{name}
Summary:	ZendStudioServer for PHP 5.x
Summary(pl.UTF-8):   ZendStudioServer dla PHP 5.x
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	php-ZendOptimizer
Provides:	%{name}(php) = %{version}-%{release}

%description -n php-%{name}
ZendStudioServer for PHP 5.x.

%description -n php-%{name} -l pl.UTF-8
ZendStudioServer dla PHP 5.x.

%prep
%setup -qcT
%ifarch %{x8664}
tar --strip-components=1 -xzf %{SOURCE1}
%else
tar --strip-components=1 -xzf %{SOURCE0}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}/Zend/lib/tools,%{_datadir}/htdocs}

cd data
install dummy.php $RPM_BUILD_ROOT%{_datadir}/htdocs
cp -a gui/* $RPM_BUILD_ROOT%{_datadir}/htdocs
install runas $RPM_BUILD_ROOT%{_bindir}
install ini_modifier  $RPM_BUILD_ROOT%{_sbindir}

install change_gui_password.php $RPM_BUILD_ROOT%{_libdir}/Zend/lib/tools
cp -a phplib $RPM_BUILD_ROOT%{_libdir}/Zend/lib/tools

for a in *_comp; do
	d=$(basename $a _comp | tr _ .)
	install -D $a/ZendDebugger.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Debugger-%{version}/php-$d/ZendDebugger.so
done
for a in *_comp/TS; do
	d=$(basename $(dirname $a) _comp | tr _ .)
	install -D $a/ZendDebugger.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Debugger_TS-%{version}/php-$d/ZendDebugger.so
done

cat > zend.ini <<EOF
[Zend]
studio.install_dir=%{_datadir}
zend_debugger.expose_remotely=allowed_hosts
zend_debugger.httpd_uid=51
zend_gui_password=69fb46f4c18463dd25002aeffc0257d1
zend_gui.ini_modifier=%{_sbindir}/ini_modifier
zend_debugger.allow_hosts=127.0.0.1/32,192.168.2.0/24
zend_debugger.allow_tunnel=127.0.0.1/32
zend_debugger.deny_hosts=
zend_root_dir=%{_datadir}
EOF

cat <<'EOF' > pack.ini
; ZendStudioServer package settings. Overwritten with each upgrade.
; if you need to add options, edit %{name}.ini instead
[Zend]
zend_extension_manager.debug_server=%{_libdir}/Zend/lib/Debugger-%{version}
zend_extension_manager.debug_server_ts=%{_libdir}/Zend/lib/Debugger_TS-%{version}
EOF

install -d $RPM_BUILD_ROOT%{_sysconfdir}/php{,4}/conf.d
install zend.ini $RPM_BUILD_ROOT/etc/php4/conf.d/%{name}.ini
install zend.ini $RPM_BUILD_ROOT/etc/php/conf.d/%{name}.ini
install pack.ini $RPM_BUILD_ROOT/etc/php4/conf.d/%{name}_pack.ini
install pack.ini $RPM_BUILD_ROOT/etc/php/conf.d/%{name}_pack.ini

%clean
rm -rf $RPM_BUILD_ROOT

%preun -n php4-%{name}
if [ "$1" = "0" ]; then
	%php4_webserver_restart
fi

%post -n php4-%{name}
%php4_webserver_restart

%preun -n php-%{name}
if [ "$1" = "0" ]; then
	%php_webserver_restart
fi

%post -n php-%{name}
%php_webserver_restart

%files
%defattr(644,root,root,755)
%doc README* LICENSE LICENSE-PHP
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*

%dir %{_libdir}/Zend/lib/Debugger-%{version}
%dir %{_libdir}/Zend/lib/Debugger-%{version}/php-*
%dir %{_libdir}/Zend/lib/Debugger_TS-%{version}
%dir %{_libdir}/Zend/lib/Debugger_TS-%{version}/php-*
%attr(755,root,root) %{_libdir}/Zend/lib/Debugger-%{version}/php-*/ZendDebugger.so
%attr(755,root,root) %{_libdir}/Zend/lib/Debugger_TS-%{version}/php-*/ZendDebugger.so
%{_libdir}/Zend/lib/tools

# html documents
%{_datadir}

%files -n php4-%{name}
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/php4/conf.d/%{name}.ini
%config %verify(not md5 mtime size) /etc/php4/conf.d/%{name}_pack.ini

%files -n php-%{name}
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/php/conf.d/%{name}.ini
%config %verify(not md5 mtime size) /etc/php/conf.d/%{name}_pack.ini
