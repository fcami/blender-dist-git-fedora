Name:           blender
Version:        2.31
Release:        0.fdr.3.a.1
Epoch:          0
Summary:        3D modeling, animation, rendering and post-production.

Group: 		Applications/Multimedia
License:        GPL
URL:            http://www.blender.org
Source0:	http://download.blender.org/source/blender-2.31a.tar.bz2
Source1:	blender.png
Source2: 	blender.desktop
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	zlib-devel 
BuildRequires:  libjpeg-devel 
BuildRequires:  libpng-devel 
BuildRequires:  freeglut-devel 
BuildRequires:  python-devel
BuildRequires:  XFree86-devel
BuildRequires:  openssl-devel
BuildRequires:	SDL-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libogg-devel
BuildRequires:	esound-devel
BuildRequires:  openal-devel
BuildRequires:	libtool
BuildRequires:	gettext
BuildRequires:  desktop-file-utils

%description
Blender is the essential software solution you need for 3D, from modeling,
animation, rendering and post-production to interactive creation and playback.

Professionals and novices can easily and inexpensively publish stand-alone,
secure, multi-platform content to the web, CD-ROMs, and other media.



%prep
%setup -q -n blender-2.31a



%build
aclocal
autoheader
automake --gnu --add-missing --foreign
autoconf

%configure              \
--disable-shared        \
--enable-openal         \
--disable-rpath
make %{?_smp_mflags}



%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT}

install -p -D -m0644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/blender.png
desktop-file-install --vendor fedora                    \
  --dir ${RPM_BUILD_ROOT}%{_datadir}/applications   	\
  --add-category X-Fedora                               \
  %{SOURCE2}


%clean
rm -rf ${RPM_BUILD_ROOT}



%files
%defattr(-,root,root,-)
%doc COPYING README release_* doc/python-dev-guide.txt doc/GPL-license.txt doc/bf-members.txt
%{_bindir}/*
%{_datadir}/applications/fedora-blender.desktop
%{_datadir}/pixmaps/%{name}.png



%changelog
* Sun Jan 11 2004 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.31-0.fdr.3.a
- --enable-openal.
- --disable-rpath.
- remove --enable-international.
- modify .desktop to execute with -w.

* Thu Dec 04 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.31-0.fdr.2.a
- Updated to 2.31a.

* Sun Nov 30 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.31-0.fdr.1
- Updated to 2.31.
- enable-international.

* Tue Nov 18 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.30-0.fdr.1
- Updated to 2.30. 

* Fri Oct 10 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.28-0.fdr.5.c
- Updated to 2.28c.

* Tue Oct 07 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.28-0.fdr.4.a
- Removed BuildReq smpeg-devel

* Mon Sep 15 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.28-0.fdr.3.a
- Moved 'a' out of version according to naming guidelines.

* Fri Sep 12 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.28a-0.fdr.2
- changed file permission on tarball.
- dropped redundant messages about aclocal, etc.
- configure --disable-shared.
- automake --foreign.
- added doc/python-dev-guide.txt doc/GPL-license.txt doc/bf-members.txt to %%doc.

* Wed Sep 10 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.28a-0.fdr.1
- Updated to 2.28a.

* Wed Aug 13 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.28-0.fdr.2
- New Icon.

* Thu Jul 24 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.28-0.fdr.1
- Updated to 2.28.
- BuildReq libvorbis-devel.
- BuildReq smpeg-devel.
- BuildReq esound-devel.
- BuildReq libogg-devel.
- BuildReq vorbis-tools.
- BuildReq openal-devel
- BuildReq libtool

* Mon May 26 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.27-0.fdr.2
- Removed post/postun ldconfig.
- Added autoconf workaround.

* Mon May 19 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.27-0.fdr.1
- Updated to 2.27.
- Removed devel package.

* Wed Apr 09 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.26-0.fdr.9
- Corrected devel Group.

* Tue Apr 01 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.26-0.fdr.8
- Added desktop-file-utils to BuildRequires.
- Changed category to X-Fedora-Extra.

* Mon Mar 31 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.26-0.fdr.7
- Added Missing BuildRequires.

* Sun Mar 30 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.26-0.fdr.6
- Cleaned up BuildRequires.
- Added Epoch:0.

* Sat Mar 22 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 2.26-0.fdr.5
- Spec file cleanup.

* Sat Mar 08 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 2.26-1.fdr.4
- Spec file cleanup.

* Wed Feb 26 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 2.26-1.fedora.3
- Spec file cleanup.

* Thu Feb 20 2003 Warren Togami
- Add BuildRequires python-devel

* Wed Feb 19 2003 Phillip Compton
- Initial RPM release.
