Summary:	ZendStudioServer
Name:		ZendStudioServer
Version:	4.0.0
Release:	0.3
Epoch:		0
License:	Zend Studio License
#Vendor:		-
Group:		Applications
#Icon:		-
Source0:	%{name}-%{version}-linux-glibc21-i386.tar.gz
# Source0-md5:	b7b24ac8736830e4b7a3a4d8124b3de0
NoSource:	0
#Source1:	-
# Source1-md5:	-
#Patch0:		%{name}-what.patch
#URL:		-
#BuildRequires:	-
#PreReq:		-
#Requires(pre,post):	-
#Requires(preun):	-
#Requires(postun):	-
Requires:	ZendOptimizer
#Requires:	php-sqlite
#Provides:	-
#Obsoletes:	-
#Conflicts:	-
#BuildArch:	noarch
#ExclusiveArch:  %{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_datadir	%{_prefix}/share/Zend

%description
Includes server management tools that manage PHP based Web servers.
This module makes installation and integration seamless while
simplifying PHP and remote debugging configurations and security
maintenance.

%prep
%setup -q -c -T
tar --strip-path=1 -xzf %{SOURCE0}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}/Zend/lib/tools,%{_datadir}/htdocs}
install -d $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Debugger-%{version}/php-{4.0.6,4.1.x,4.2.0,4.2.x,4.3.x,5.0.x}
install -d $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Debugger_TS-%{version}/php-{4.2.x,4.3.x,5.0.x}

cd data
install dummy.php $RPM_BUILD_ROOT%{_datadir}/htdocs
cp -a gui/* $RPM_BUILD_ROOT%{_datadir}/htdocs
install runas $RPM_BUILD_ROOT%{_bindir}
#install dbgclient $RPM_BUILD_ROOT%{_bindir}
install ini_modifier  $RPM_BUILD_ROOT%{_sbindir}

install change_zend_gui_password.php $RPM_BUILD_ROOT%{_libdir}/Zend/lib/tools
cp -a phplib $RPM_BUILD_ROOT%{_libdir}/Zend/lib/tools

#install ZendExtensionManager{,_TS}.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib

install 4_1_x_comp/ZendDebugger.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Debugger-%{version}/php-4.1.x
install 4_2_0_comp/ZendDebugger.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Debugger-%{version}/php-4.2.0
install 4_2_x_comp/ZendDebugger.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Debugger-%{version}/php-4.2.x
install 4_3_x_comp/ZendDebugger.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Debugger-%{version}/php-4.3.x
install 5_0_x_comp/ZendDebugger.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Debugger-%{version}/php-5.0.x

install 4_2_x_comp/TS/ZendDebugger.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Debugger_TS-%{version}/php-4.2.x
install 4_3_x_comp/TS/ZendDebugger.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Debugger_TS-%{version}/php-4.3.x
install 5_0_x_comp/TS/ZendDebugger.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Debugger_TS-%{version}/php-5.0.x

cat > php.ini <<EOF
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
#zend_extension_manager.optimizer=%{_libdir}/Zend/lib/Optimizer-2.5.8
zend_extension_manager.debug_server=%{_libdir}/Zend/lib/Debugger-4.0.0
#zend_extension_manager.optimizer_ts=%{_libdir}/Zend/lib/Optimizer_TS-2.5.8
zend_extension_manager.debug_server_ts=%{_libdir}/Zend/lib/Debugger_TS-4.0.0
#zend_extension=%{_libdir}/Zend/lib/ZendExtensionManager.so
#zend_extension_ts=%{_libdir}/Zend/lib/ZendExtensionManager_TS.so
EOF

#install php.ini $RPM_BUILD_ROOT%{_sysconfdir}/zendstudioserver.ini

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
for php in /etc/php{,4}/php.ini; do
	if [ -f $php ]; then
		echo "activating module 'ZendDebugger.so' in $php" 1>&2
		cp $php{,.zend-backup}
		grep -v zend_optimizer.optimization_level $php | \
		grep -v zend_extension > $php.tmp
		echo '[Zend]' >> $php.tmp
		echo "zend_optimizer.optimization_level=$optlevel" >> $php.tmp
		echo "zend_extension_manager.optimizer=%{_libdir}/Zend/lib/Optimizer-%{version}" >> $php.tmp
		echo "zend_extension_manager.optimizer_ts=%{_libdir}/Zend/lib/Optimizer_TS-%{version}" >> $php.tmp
		echo "zend_extension=%{_libdir}/Zend/lib/ZendExtensionManager.so" >> $php.tmp
		echo "zend_extension_ts=%{_libdir}/Zend/lib/ZendExtensionManager_TS.so" >> $php.tmp
		mv $php{.tmp,}
	fi
done

%postun
if [ "$1" = "0" ]; then
	umask 022
	for php in /etc/php{,4}/php.ini; do
		if [ -f $php ]; then
			echo "deactivating module 'ZendDebugger.so' in $php" 1>&2
			grep -v '\[Zend\]' $php |\
			grep -v zend_extension |grep -v zend_optimizer > $php.tmp
			mv $php.tmp $php
		fi
	done
fi

%files
%defattr(644,root,root,755)
%doc README LICENSE LICENSE-PHP
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_datadir}

#%dir %{_libdir}/Zend
#%dir %{_libdir}/Zend/lib
%dir %{_libdir}/Zend/lib/Debugger-%{version}/php-4.1.x
%dir %{_libdir}/Zend/lib/Debugger-%{version}/php-4.2.0
%dir %{_libdir}/Zend/lib/Debugger-%{version}/php-4.2.x
%dir %{_libdir}/Zend/lib/Debugger-%{version}/php-4.3.x
%dir %{_libdir}/Zend/lib/Debugger-%{version}/php-5.0.x
%dir %{_libdir}/Zend/lib/Debugger-%{version}
%dir %{_libdir}/Zend/lib/Debugger_TS-%{version}
%dir %{_libdir}/Zend/lib/Debugger_TS-%{version}/php-4.2.x
%dir %{_libdir}/Zend/lib/Debugger_TS-%{version}/php-4.3.x
%dir %{_libdir}/Zend/lib/Debugger_TS-%{version}/php-5.0.x
%{_libdir}/Zend/lib/Debugger-%{version}/php-4.1.x/ZendDebugger.so
%{_libdir}/Zend/lib/Debugger-%{version}/php-4.2.0/ZendDebugger.so
%{_libdir}/Zend/lib/Debugger-%{version}/php-4.2.x/ZendDebugger.so
%{_libdir}/Zend/lib/Debugger-%{version}/php-4.3.x/ZendDebugger.so
%{_libdir}/Zend/lib/Debugger-%{version}/php-5.0.x/ZendDebugger.so
%{_libdir}/Zend/lib/Debugger_TS-%{version}/php-4.2.x/ZendDebugger.so
%{_libdir}/Zend/lib/Debugger_TS-%{version}/php-4.3.x/ZendDebugger.so
%{_libdir}/Zend/lib/Debugger_TS-%{version}/php-5.0.x/ZendDebugger.so

%{_libdir}/Zend/lib/tools
