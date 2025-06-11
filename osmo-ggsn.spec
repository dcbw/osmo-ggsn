Name:           osmo-ggsn
Version:        1.13.0
Release:        1.dcbw%{?dist}
Summary:        Open Source GGSN
License:        GPL-2.0-only AND LGPL-2.1-or-later AND MIT

URL:            https://osmocom.org/projects/openggsn/wiki

BuildRequires:  git gcc autoconf automake libtool doxygen systemd-devel
BuildRequires:  libosmocore-devel >= 1.10.0

Patch1: build-fixes.patch
Patch2: ppc64.patch
Source0: %{name}-%{version}.tar.bz2

Requires: osmo-usergroup

%description
C-language implementation of a GGSN (Gateway GPRS Support Node),
a core network element of ETSI/3GPP cellular networks such as
GPRS, EDGE, UMTS or HSPA.
 
%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Development files for %{name}.


%prep
%autosetup -p1


%build
%global optflags %(echo %optflags | sed 's|-Wp,-D_GLIBCXX_ASSERTIONS||g')
echo "%{version}" >.tarball-version
autoreconf -fiv
%configure --enable-shared \
           --disable-static \
           --with-systemdsystemunitdir=%{_unitdir}

# Fix unused direct shlib dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
# Remove libtool archives
find %{buildroot} -name '*.la' -exec rm -f {} \;
sed -i -e 's|UNKNOWN|%{version}|g' %{buildroot}/%{_libdir}/pkgconfig/*.pc


%check
make check

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%post
%systemd_post %{name}.service

%ldconfig_scriptlets

%files
%doc README.md
%doc %{_docdir}/%{name}
%license COPYING
%{_sbindir}/*
%{_bindir}/*
%{_unitdir}/%{name}.service
%attr(0644,root,root) %config(missingok,noreplace) %{_sysconfdir}/osmocom/%{name}.cfg
%{_libdir}/*.so.*
%{_mandir}/*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Sun Jun  8 2025 Dan Williams <dan@ioncontrol.co> - 1.13.0
- Update to 1.13.0

* Sun Aug 26 2018 Cristian Balint <cristian.balint@gmail.com>
- git update releases
