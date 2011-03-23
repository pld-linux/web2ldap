Summary:	WWW gateway to LDAP server
Summary(pl.UTF-8):	Bramka WWW do serwera LDAP
Name:		web2ldap
Version:	1.1.0a29
Release:	1
License:	distributable (mostly GPL)
Group:		Applications
Source0:	http://www.web2ldap.de/download/%{name}-%{version}.tar.gz
# Source0-md5:	c7abb40d5e679c47bbebe5c45c265fe9
Patch0:		%{name}-config.patch
URL:		http://www.web2ldap.de/
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
%pyrequires_eq	python-modules
Requires:	python-ldap
Requires:	python-pyweblib
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is:
- a generic LDAPv3 client which does not make any assumptions about
  the tree structure or LDAP schema.
- kind of a swiss-army knife for accessing/manipulating LDAP servers
  without having to configure anything.
- a secure LDAP client with clean login behaviour.
- a schema browser which displays references/dependencies within an
  LDAPv3 schema.
- continously maintained software.

%description -l pl.UTF-8
To jest:
- ogólny klient LDAPv3, nie czyniący żadnych założeń dotyczących
  struktury drzewa ani schematu LDAP
- narzędzie do dostępu i manipulacji na serwerach LDAP bez potrzeby
  konfiguracji
- bezpieczny klient LDAP czysto logujący się
- przeglądarka schematów wyświetlająca odwołania i zależności wewnątrz
  schematu LDAPv3
- stale utrzymywane oprogramowanie.

%prep
%setup -q
%patch0 -p1

%build
for dir in pylib sbin fcgi scgi; do
	python -c "import compileall; compileall.compile_dir('$dir')"
	python -O -c "import compileall; compileall.compile_dir('$dir')"
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_sbindir},%{_datadir}/%{name}/htdocs} \
		$RPM_BUILD_ROOT/var{/run,/lib,/log}/%{name}

cp -a etc/web2ldap $RPM_BUILD_ROOT%{_sysconfdir}
cp -a fcgi pylib scgi sbin $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a htdocs/css $RPM_BUILD_ROOT%{_datadir}/%{name}/htdocs
find $RPM_BUILD_ROOT%{_datadir}/%{name}/pylib -name "*.py" | xargs rm
%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/sbin/compile*
%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/sbin/*.py
echo '#!/bin/sh' > $RPM_BUILD_ROOT%{_sbindir}/%{name}
echo 'exec python %{_datadir}/%{name}/sbin/%{name}.pyc $*' \
	>> $RPM_BUILD_ROOT%{_sbindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README htdocs/* etc/httpd
%attr(755,root,root) %{_sbindir}/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/pylib
%{_datadir}/%{name}/htdocs
%{_datadir}/%{name}/sbin

%dir %{_datadir}/%{name}/fcgi
%attr(755,root,root) %{_datadir}/%{name}/fcgi/web2ldap.py
%{_datadir}/%{name}/fcgi/*.py[co]

%dir %{_datadir}/%{name}/scgi
%attr(755,root,root) %{_datadir}/%{name}/scgi/web2ldap.py
%{_datadir}/%{name}/scgi/*.py[co]

%dir %attr(775,root,http) /var/*/%{name}
