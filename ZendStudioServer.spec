Summary:	ZendStudioServer - server management tools for PHP based Web servers
Summary(pl):	ZendStudioServer - narzêdzia zarz±dzaj±ce dla serwerów WWW opartych na PHP
Name:		ZendStudioServer
Version:	5.0.0
%define	_beta Beta
Release:	0.%{_beta}.1
Epoch:		0
License:	Zend Studio License
Group:		Applications
Source0:	http://downloads.zend.com/studio/5.0.0beta/%{name}-%{version}%{_beta}-linux-glibc21-i386.tar.gz
# NoSource0-md5:	1429e3a6263ded21e0827344a9bbd9b6
NoSource:	0
Source1:	http://downloads.zend.com/studio/5.0.0beta/%{name}-%{version}%{_beta}-linux-glibc23-x86_64.tar.gz
# NoSource1-md5:	885e25876d68d0b51f03c3dbd8717800
NoSource:	1
BuildRequires:	tar >= 1:1.15.1
Requires:	ZendOptimizer
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_datadir	%{_prefix}/share/Zend

%description
Includes server management tools that manage PHP based Web servers.
This module makes installation and integration seamless while
simplifying PHP and remote debugging configurations and security
maintenance.

%description -l pl
Ten pakiet zawiera narzêdzia zarz±dzaj±ce serwerem dla serwerów WWW
opartych na PHP. Ten modu³ pozwala na przezroczyst± instalacjê i
integracjê jednocze¶nie upraszczaj±c konfiguracje PHP ze zdaln±
diagnostyk± oraz zarz±dzanie bezpieczeñstwem.

%prep
%setup -q -c -T
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
#install dbgclient $RPM_BUILD_ROOT%{_bindir}
install ini_modifier  $RPM_BUILD_ROOT%{_sbindir}

install change_zend_gui_password.php $RPM_BUILD_ROOT%{_libdir}/Zend/lib/tools
cp -a phplib $RPM_BUILD_ROOT%{_libdir}/Zend/lib/tools

#install ZendExtensionManager{,_TS}.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib

for a in *_comp; do
	d=$(basename $a _comp|tr _ .)
	install -D $a/ZendDebugger.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Debugger-%{version}/php-$d/ZendDebugger.so
done
for a in *_comp/TS; do
	d=$(basename $(dirname $a) _comp|tr _ .)
	install -D $a/ZendDebugger.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Debugger_TS-%{version}/php-$d/ZendDebugger.so
done

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
sed -e 's,^#,;,' php.ini > $RPM_BUILD_ROOT%{_libdir}/Zend/php.ini

%clean
rm -rf $RPM_BUILD_ROOT

#%post
#umask 022
#for php in /etc/php{,4}/php.ini; do
#	if [ -f $php ]; then
#		echo "activating module 'ZendDebugger.so' in $php" 1>&2
#		cp $php{,.zend-backup}
#		grep -v zend_optimizer.optimization_level $php | \
#		grep -v zend_extension > $php.tmp
#		echo '[Zend]' >> $php.tmp
#		echo "zend_optimizer.optimization_level=$optlevel" >> $php.tmp
#		echo "zend_extension_manager.optimizer=%{_libdir}/Zend/lib/Optimizer-%{version}" >> $php.tmp
#		echo "zend_extension_manager.optimizer_ts=%{_libdir}/Zend/lib/Optimizer_TS-%{version}" >> $php.tmp
#		echo "zend_extension=%{_libdir}/Zend/lib/ZendExtensionManager.so" >> $php.tmp
#		echo "zend_extension_ts=%{_libdir}/Zend/lib/ZendExtensionManager_TS.so" >> $php.tmp
#		mv $php{.tmp,}
#	fi
#done

#%postun
#if [ "$1" = "0" ]; then
#	umask 022
#	for php in /etc/php{,4}/php.ini; do
#		if [ -f $php ]; then
#			echo "deactivating module 'ZendDebugger.so' in $php" 1>&2
#			grep -v '\[Zend\]' $php |\
#			grep -v zend_extension |grep -v zend_optimizer > $php.tmp
#			mv $php.tmp $php
#		fi
#	done
#fi

%files
%defattr(644,root,root,755)
%doc README LICENSE LICENSE-PHP
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_datadir}

#%dir %{_libdir}/Zend
#%dir %{_libdir}/Zend/lib
%dir %{_libdir}/Zend/lib/Debugger-%{version}
%dir %{_libdir}/Zend/lib/Debugger-%{version}/php-*
%dir %{_libdir}/Zend/lib/Debugger_TS-%{version}
%dir %{_libdir}/Zend/lib/Debugger_TS-%{version}/php-*
%attr(755,root,root) %{_libdir}/Zend/lib/Debugger-%{version}/php-*/ZendDebugger.so
%attr(755,root,root) %{_libdir}/Zend/lib/Debugger_TS-%{version}/php-*/ZendDebugger.so

%{_libdir}/Zend/lib/tools

%{_libdir}/Zend/php.ini
