#
# Conditional build:
%bcond_without	gnome		# build without GNOME support
#
Summary:	Mail notification program
Summary(pl.UTF-8):	Program powiadamiający o nowej poczcie
Name:		gnubiff
Version:	2.2.0
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/gnubiff/%{name}-%{version}.tar.gz
# Source0-md5:	a99a0294e8b53420be3c28389306c824
URL:		http://gnubiff.sourceforge.net/
%{?with_gnome:BuildRequires:	GConf2-devel >= 2.4.0}
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	fam-devel
BuildRequires:	gettext-devel
%{?with_gnome:BuildRequires:	gnome-panel-devel >= 2.4.0}
BuildRequires:	gtk+2-devel >= 2:2.4.3
BuildRequires:	intltool
BuildRequires:	libglade2-devel >= 1:2.4.0
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
Requires:	gtk+2 >= 2:2.4.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gnubiff is a mail notification program that checks for mail, displays
headers when new mail has arrived and allow to read first lines of new
mails.

%description -l pl.UTF-8
gnubiff jest programem powiadamiającym, który sprawdza pocztę,
wyświetla nagłówki i pozwala przeczytać pierwsze linie nowych listów.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	%{!?with_gnome:--disable-gnome} \
	--with-password

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# duplicates fr with no differences in translation
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/fr_FR
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/fr_CA
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
%{_datadir}/gnome-*/ui/*.xml
%{_libdir}/bonobo/servers/*.server
%endif
