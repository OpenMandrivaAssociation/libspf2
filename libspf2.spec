%define	major 2
%define libname	%mklibname spf %{major}

Summary:	Implementation of the SPF specification
Name:		libspf2
Version:	1.2.9
Release:	%mkrel 3
License:	BSD
Group:		System/Libraries
URL:		http://www.libspf2.org/
Source0:	http://www.libspf2.org/spf/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
libspf2 is an implementation of the SPF (Sender Policy Framework)
specification as found at:
http://www.ietf.org/internet-drafts/draft-mengwong-spf-00.txt
SPF allows email systems to check SPF DNS records and make sure
that an email is authorized by the administrator of the domain
name that it is coming from. This prevents email forgery, commonly
used by spammers, scammers, and email viruses/worms.

A lot of effort has been put into making it secure by design, and
a great deal of effort has been put into the regression tests.

%if "%{_lib}" != "lib"
%package -n	%{libname}
Summary:	Implementation of the SPF specification
Group:		System/Libraries

%description -n	%{libname}
libspf2 is an implementation of the SPF (Sender Policy Framework)
specification as found at:
http://www.ietf.org/internet-drafts/draft-mengwong-spf-00.txt
SPF allows email systems to check SPF DNS records and make sure
that an email is authorized by the administrator of the domain
name that it is coming from. This prevents email forgery, commonly
used by spammers, scammers, and email viruses/worms.

A lot of effort has been put into making it secure by design, and
a great deal of effort has been put into the regression tests.
%endif

%package -n	%{libname}-devel
Summary:	Development tools needed to build programs that use libspf2
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	libspf-devel

%description -n	%{libname}-devel
The libspf2-devel package contains the header files and static
libraries necessary for developing programs using the libspf2
(Sender Policy Framework) library.

If you want to develop programs that will look up and process SPF
records, you should install libspf2-devel. You also need to
install the libspf2 package.

%package -n	spf2-utils
Summary:	Programs for making SPF queries using libspf2
Group:		System/Servers

%description -n	spf2-utils
Programs for making SPF queries and checking their results using
libspf2.

%prep

%setup -q

%build

# The configure script checks for the existence of __ns_get16 and uses the
# system-supplied version if found, otherwise one from src/libreplace.
# However, this function is marked GLIBC_PRIVATE in recent versions of glibc
# and shouldn't be called even if the configure script finds it. So we make
# sure that the configure script always uses the version in src/libreplace.
# This prevents us getting an unresolvable dependency in the built RPM.
cat > config.cache << EOF
ac_cv_func___ns_get16=no
EOF

%configure2_5x \
    --cache-file=config.cache

%make

%install
rm -rf %{buildroot}

%makeinstall_std

# install all headers
install -m0644 src/include/*.h %{buildroot}%{_includedir}/spf2/

# these binaries are needed by the tests above
rm -f %{buildroot}%{_bindir}/*_static

# rename the binaries to prevent file conflicts
cd  %{buildroot}%{_bindir}
    for f in *; do mv ${f} ${f}2; done
cd -

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc README INSTALL LICENSES TODO
%{_libdir}/lib*.so.%{major}*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_includedir}/spf2

%files -n spf2-utils
%defattr(-,root,root)
%{_bindir}/spfd2
%{_bindir}/spfquery2
%{_bindir}/spftest2
%{_bindir}/spf_example2
