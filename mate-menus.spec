%define url_ver %(echo %{version}|cut -d. -f1,2)

%define gimajor	2.0
%define major	2
%define libname	%mklibname mate-menu %{major}
%define girname	%mklibname matemenu-gir %{gimajor}
%define devname	%mklibname -d mate-menu

Summary:	MATE menu library
Name:		mate-menus
Version:	1.18.0
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		https://mate-desktop.org
Source0:	https://pub.mate-desktop.org/releases/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	intltool
BuildRequires:  chrpath
BuildRequires:	mate-common
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(python-2.7)

%description
The package contains an implementation of the draft "Desktop Menu
Specification" from freedesktop.org:
http://www.freedesktop.org/Standards/menu-spec

Also contained here are the MATE menu layout configuration files,
.directory files and assorted menu related utility programs.

%package -n python2-%{name}
Group:		Development/Python
Summary:	Module to access XDG menu
Requires:	python2-gobject

%description -n python2-%{name}
Python2 module to access XDG menu.

%package -n %{libname}
Group:		System/Libraries
Summary:	MATE menu library

%description -n %{libname}
This package contains the shared libraries of %{name}.

%package -n %{girname}
Group:		System/Libraries
Summary:	GObject Introspection interface library for %{name}

%description -n %{girname}
GObject Introspection interface library for %{name}.

%package -n %{devname}
Group:		Development/C
Summary:	MATE menu library development files
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
This package contains the development libraries of %{name}.

%prep
%setup -q
%apply_patches

%build
export PYTHON=%{__python2}
#NOCONFIGURE=yes ./autogen.sh
%configure \
	--enable-python \
	--enable-introspection=yes \
	%{nil}
%make

%install
%makeinstall_std
install -d %{buildroot}%{_sysconfdir}/xdg/mate
mv %{buildroot}%{_sysconfdir}/xdg/menus %{buildroot}%{_sysconfdir}/xdg/mate/

# locales
%find_lang %{name} --with-gnome --all-name

%files -f %{name}.lang
%doc README NEWS AUTHORS ChangeLog
%config(noreplace) %{_sysconfdir}/xdg/mate
%dir %{_datadir}/mate
%dir %{_datadir}/mate/desktop-directories
%{_datadir}/mate/desktop-directories/*
%{_datadir}/%{name}

%files -n python2-%{name}
%{python2_sitearch}/matemenu.so

%files -n %{libname}
%{_libdir}/libmate-menu.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/MateMenu-%{gimajor}.typelib

%files -n %{devname}
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/MateMenu-%{gimajor}.gir

