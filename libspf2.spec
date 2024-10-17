%define	major 2
%define libname	%mklibname spf %{major}

Summary:	Implementation of the SPF specification
Name:		libspf2
Version:	1.2.10
Release:	6
License:	BSD
Group:		System/Libraries
URL:		https://www.libspf2.org/
Source0:	http://www.libspf2.org/spf/%{name}-%{version}.tar.gz

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
Provides:	%{libname}-devel = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

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

%files -n %{libname}
%doc README INSTALL LICENSES TODO
%{_libdir}/lib*.so.%{major}*

%files -n %{libname}-devel
%{_libdir}/*.a
%{_libdir}/*.so
%{_includedir}/spf2

%files -n spf2-utils
%{_bindir}/spfd2
%{_bindir}/spfquery2
%{_bindir}/spftest2
%{_bindir}/spf_example2


%changelog
* Mon May 30 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1.2.9-4mdv2011.0
+ Revision: 681769
- fix devel provides

* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2.9-3mdv2011.0
+ Revision: 620226
- the mass rebuild of 2010.0 packages

* Mon Sep 14 2009 Thierry Vignaud <tv@mandriva.org> 1.2.9-2mdv2010.0
+ Revision: 439444
- rebuild

* Tue Nov 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.9-1mdv2009.1
+ Revision: 299895
- 1.2.9
- drop redundant patches; P0

* Sun Jul 27 2008 Thierry Vignaud <tv@mandriva.org> 1.2.5-8mdv2009.0
+ Revision: 250564
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1.2.5-6mdv2008.1
+ Revision: 170957
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sun Sep 09 2007 Oden Eriksson <oeriksson@mandriva.com> 1.2.5-5mdv2008.0
+ Revision: 83757
- rebuild


* Fri Dec 08 2006 Oden Eriksson <oeriksson@mandriva.com> 1.2.5-4mdv2007.0
+ Revision: 93759
- Import libspf2

* Mon Jul 03 2006 Oden Eriksson <oeriksson@mandriva.com> 1.2.5-4mdv2007.0
- added one patch by debian

* Tue Oct 25 2005 Oden Eriksson <oeriksson@mandriva.com> 1.2.5-3mdk
- fix #19226

* Thu Mar 31 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.2.5-2mdk
- install missing headers

* Thu Mar 31 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.2.5-1mdk
- 1.2.5
- use the %%mkrel macro
- remove the resolv patch, it's integrated upstream
- cleaned up the spec file and used naming as in the libalsa2 package

* Tue Feb 22 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.2.4-1mdk
- 1.2.4

* Sun Feb 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.2.1-1mdk
- 1.2.1
- remove the lowercase diff (P0)

* Sat Jan 01 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.4-2mdk
- make it build on amd64 (duh!)

* Thu Oct 21 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.4-1mdk
- initial mandrake import

* Tue Aug 17 2004 Paul Howarth <paul@city-fan.org> 1.0.4-7
- Configure fix to find -lresolv on x64_64
- Portability fixes for x64_64

* Mon Aug 02 2004 Paul Howarth <paul@city-fan.org> 1.0.4-6
- Fix case-sensitivity bug.

* Thu Jul 29 2004 Paul Howarth <paul@city-fan.org> 1.0.4-5
- Revert -pthread option as it didn't improve anything.

* Wed Jul 28 2004 Paul Howarth <paul@city-fan.org> 1.0.4-4
- Use `alternatives' so that the spfquery and spfd programs can co-exist
  with versions from other implementations.
- Ensure thread-safe operation by building with -pthread.

* Fri Jul 16 2004 Paul Howarth <paul@city-fan.org> 1.0.4-3
- Install the libtool library in the devel package so that
  dependent libraries are found properly.
- Use the libtool supplied with the package rather than the
  system libtool.

* Wed Jul 14 2004 Paul Howarth <paul@city-fan.org> 1.0.4-2
- Cosmetic changes for building on Mandrake Linux
- Require rpm-build >= 4.1.1 for building to avoid strange error messages
  from old versions of rpm when they see %%check
- Require glibc-devel and make for building
- Require perl for building with checks enabled
- Improved description text for the packages

* Sat Jul 10 2004 Paul Howarth <paul@city-fan.org> 1.0.4-1
- Update to 1.0.4
- Added facility to build without running test suite
  (rpmbuild --without checks)

* Sun Jul 04 2004 Paul Howarth <paul@city-fan.org> 1.0.3-1
- Initial RPM build.

