#
# Conditional build:
%bcond_without	gnome		# build without GNOME support
#
Summary:	Mail notification program
Summary(pl):	Program powiadamiaj�cy o nowej poczcie
Name:		gnubiff
Version:	2.0.1
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	4963ff7e23cdc5396cdda035554e46c9
Patch0:		%{name}-gcc34.patch
URL:		http://gnubiff.sourceforge.net/
%{?with_gnome:BuildRequires:	GConf2-devel >= 2.4.0}
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
%{?with_gnome:Buildrequires:	gnome-panel-devel >= 2.4.0}
BuildRequires:	gtk+2-devel >= 2:2.4.3
Buildrequires:	intltool
BuildRequires:	libglade2-devel >= 1:2.4.0
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	popt-devel
Requires:	gtk+2 >= 2:2.4.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gnubiff is a mail notification program that checks for mail, displays
headers when new mail has arrived and allow to read first lines of new
mails.

%description -l pl
gnubiff jest programem powiadamiaj�cym, kt�ry sprawdza poczt�,
wy�wietla nag��wki i pozwala przeczyta� pierwsze linie nowych list�w.

%prep
%setup -q
%patch0 -p1

%build
intltoolize --copy --force
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	%{?with_gnome:--with-gnome} \
	--with-password

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_infodir}/*.info*
%{_mandir}/man1/%{name}.1*
%{_pixmapsdir}/*.png

%if %{with gnome}
%{_libdir}/bonobo/servers/*.server
%{_datadir}/gnome-*/ui/*.xml
%endif
