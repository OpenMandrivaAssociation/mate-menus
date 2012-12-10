%define major		2
%define girmajor	2.0
%define libname		%mklibname mate-menu %{major}
%define girname		%mklibname matemenu-gir %{girmajor}
%define develname	%mklibname -d mate-menu

Summary:	MATE menu library
Name:		mate-menus
Version:	1.4.0
Release:	2
License:	LGPLv2+
Group:		System/Libraries
Url:		http://mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz

BuildRequires:	intltool
BuildRequires:	mate-common
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(python)

#Requires:	python-%{name}

%description
The package contains an implementation of the draft "Desktop Menu
Specification" from freedesktop.org:
http://www.freedesktop.org/Standards/menu-spec

Also contained here are the MATE menu layout configuration files,
.directory files and assorted menu related utility programs.

%package -n python-%{name}
Group:		Development/Python
Summary:	Module to access XDG menu
Requires:	python-gobject

%description -n python-%{name}
Python module to access XDG menu.

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

%package -n %{develname}
Group:		Development/C
Summary:	MATE menu library development files
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}
Provides:	%{name}-devel = %{EVRD}

%description -n %{develname}
This package contains the development libraries of %{name}.

%prep
%setup -q
%apply_patches

%build
NOCONFIGURE=yes ./autogen.sh
%configure2_5x \
	--disable-static \
	--enable-python

%make

%install
%makeinstall_std
find %{buildroot} -name *.la | xargs rm
install -d %{buildroot}%_sysconfdir/xdg/mate
mv %{buildroot}%{_sysconfdir}/xdg/menus %{buildroot}%{_sysconfdir}/xdg/mate/

%find_lang %{name}

%files -f %{name}.lang
%doc README NEWS AUTHORS ChangeLog
%config(noreplace) %{_sysconfdir}/xdg/mate
%dir %{_datadir}/mate
%dir %{_datadir}/mate/desktop-directories
%{_datadir}/mate/desktop-directories/*
%{_datadir}/%{name}

%files -n python-%{name}
%{python_sitearch}/matemenu.so
#{python_sitearch}/MateMenuSimpleEditor/*

%files -n %{libname}
%{_libdir}/libmate-menu.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/MateMenu-%{girmajor}.typelib

%files -n %{develname}
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/MateMenu-%{girmajor}.gir

