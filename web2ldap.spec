%include	/usr/lib/rpm/macros.python
Summary:	WWW gateway to LDAP server
Summary(pl):	Bramka WWW do serwera LDAP
Name:		web2ldap
Version:	0.11.9
Release:	1
License:	distributable (mostly GPL)
Group:		Applications
Source0:	http://www.web2ldap.de/download/%{name}-%{version}.tar.gz
Patch0:		%{name}-config.patch
URL:		http://www.web2ldap.de/
%pyrequires_eq	python-modules
Requires:	python-ldap
Requires:	python-PyWebLib
BuildArch:      noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is:
- a generic LDAPv3 client which does not make any assumptions about the tree
  structure or LDAP schema.
- kind of a swiss-army knife for accessing/manipulating LDAP servers without
  having to configure anything.
- a secure LDAP client with clean login behaviour.
- a schema browser which displays references/dependencies within an LDAPv3
  schema.
- continously maintained software.

%prep
%setup -q
%patch0 -p1

%build
for dir in fcgi pylib scgi templates sbin; do
	python -c "import compileall; compileall.compile_dir('$dir')"
	python -O -c "import compileall; compileall.compile_dir('$dir')"
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_sbindir},%{_datadir}/%{name}} \
		$RPM_BUILD_ROOT/var{/run,/lib,/log}/%{name}

cp -R etc/web2ldap $RPM_BUILD_ROOT%{_sysconfdir}
cp -R fcgi pylib scgi templates sbin $RPM_BUILD_ROOT%{_datadir}/%{name}
find $RPM_BUILD_ROOT%{_datadir}/%{name} -name "*.py" | xargs rm
echo '#!/bin/sh' > $RPM_BUILD_ROOT%{_sbindir}/%{name}
echo 'exec python %{_datadir}/%{name}/sbin/%{name}.pyc $*' \
	>> $RPM_BUILD_ROOT%{_sbindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc htdocs/* etc/httpd
%attr(755,root,root) %{_sbindir}/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}
%{_datadir}/%{name}
%dir %attr(664,root,http) /var/*/%{name}
