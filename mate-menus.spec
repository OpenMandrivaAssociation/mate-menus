%define mate_ver	%(echo %{version}|cut -d. -f1,2)

%define major 2
%define libname %mklibname mate-menu
%define devname %mklibname mate-menu -d
%define oldlibname %mklibname mate-menu 2

%define gimajor 2.0
%define girname %mklibname mate-menu-gir %{gimajor}

Summary:	MATE menu library
Name:		mate-menus
Version:	1.28.0
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		https://mate-desktop.org
Source0:	https://pub.mate-desktop.org/releases/%{mate_ver}/%{name}-%{version}.tar.xz

BuildRequires:	autoconf-archive
BuildRequires:	intltool
BuildRequires:	mate-common
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)

Requires:	%{libname} = %{version}-%{release}

%description
The MATE Desktop Environment is the continuation of GNOME 2. It provides an
intuitive and attractive desktop environment using traditional metaphors for
Linux and other Unix-like operating systems.

MATE is under active development to add support for new technologies while
preserving a traditional desktop experience.

This package provides libmate-menu library, the layout configuration files
for the MATE menu, as well as a simple menu editor.

The libmate-menu library implements the "Desktop Menu Specification"
from freedesktop.org.

%files -f %{name}.lang
%doc README NEWS AUTHORS ChangeLog
%config(noreplace) %{_sysconfdir}/xdg/mate
%dir %{_datadir}/mate
%dir %{_datadir}/mate/desktop-directories
%{_datadir}/mate/desktop-directories/*
%{_datadir}/%{name}

#---------------------------------------------------------------------------

%package -n %{libname}
Summary:	MATE menu library
Group:		System/Libraries
Obsoletes:	%{libname} <= %{EVRD}

%description -n %{libname}
This package contains the shared libraries used by %{name}.

%files -n %{libname}
%{_libdir}/libmate-menu.so.%{major}*

#---------------------------------------------------------------------------

%package -n %{girname}
Summary:	GObject Introspection interface library for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description -n %{girname}
This package contains GObject Introspection interface library for %{name}.

%files -n %{girname}
%{_libdir}/girepository-1.0/MateMenu-%{gimajor}.typelib

#---------------------------------------------------------------------------

%package -n %{devname}
Summary:	MATE menu library development files
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
This package contains libraries and includes files for developing programs
based on %{name}.

%files -n %{devname}
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/MateMenu-%{gimajor}.gir

#---------------------------------------------------------------------------

%prep
%autosetup -p1

%build
#NOCONFIGURE=1 ./autogen.sh
%configure \
	--enable-introspection=yes \
	--disable-collection

%make_build

%install
%make_install

install -d %{buildroot}%{_sysconfdir}/xdg/mate
mv %{buildroot}%{_sysconfdir}/xdg/menus %{buildroot}%{_sysconfdir}/xdg/mate/

# locales
%find_lang %{name} --with-gnome --all-name
