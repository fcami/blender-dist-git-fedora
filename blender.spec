%define blenderlib %{_datadir}/blender
%define plugins %{_libdir}/blender/plugins

Name:           blender
Version:        2.42a
Release: 	10%{?dist}

Summary:        3D modeling, animation, rendering and post-production

Group:          Applications/Multimedia
License:        GPL
URL:            http://www.blender.org
Source0:        http://download.blender.org/source/blender-%{version}.tar.gz
Source1:        http://bane.servebeer.com/programming/blender/import-3ds-0.7.py
Source2:        http://bane.servebeer.com/programming/blender/export-3ds-0.71.py
Source3:        blender.png
Source4:        blender.desktop
Source5:        blender.xml
Source6:        blender-wrapper
Source7:	blender-2.42.config

Patch1:         blender-2.42-scons.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  desktop-file-utils
BuildRequires:  esound-devel
BuildRequires:  freeglut-devel
BuildRequires:  gettext-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libogg-devel
BuildRequires:  libpng-devel
BuildRequires:  libtool
BuildRequires:  libvorbis-devel
BuildRequires:  freealut-devel
BuildRequires:  openssl-devel
BuildRequires:  python-devel
BuildRequires:  scons
BuildRequires:  SDL-devel
BuildRequires:  zlib-devel
BuildRequires:  libtiff-devel
BuildRequires:  libXi-devel
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
buildRequires:  freetype-devel
BuildRequires:  OpenEXR-devel

ExcludeArch: x86_64

Requires(post): desktop-file-utils
Requires(post): shared-mime-info
Requires(postun): desktop-file-utils
Requires(postun): shared-mime-info

%description
Blender is the essential software solution you need for 3D, from modeling,
animation, rendering and post-production to interactive creation and playback.

Professionals and novices can easily and inexpensively publish stand-alone,
secure, multi-platform content to the web, CD-ROMs, and other media.

%prep
%setup -q 
%patch1 -p1

%build
cp %{SOURCE7} user-config.py

#
# Don't use $RPM_OPT_FLAGS (see #199418)
#

scons %{?_smp_mflags} blenderplayer BF_QUIET=0

install -d release/plugins/include
install -m 644 source/blender/blenpluginapi/*.h release/plugins/include

chmod +x release/plugins/bmake

make -C release/plugins/

%install
rm -rf ${RPM_BUILD_ROOT}

install -D -m 755 build/linux2/bin/blender ${RPM_BUILD_ROOT}/%{_bindir}/blender.bin

install -D -m 755 build/linux2/bin/blenderplayer ${RPM_BUILD_ROOT}/%{_bindir}/blenderplayer

install -D -m 755 %{SOURCE6} ${RPM_BUILD_ROOT}/%{_bindir}/blender

# install -D -m 755 blenderplayer ${RPM_BUILD_ROOT}/%{_bindir}/blenderplayer

#
#  Install miscellanous files to /usr/lib/blender
#

mkdir -p ${RPM_BUILD_ROOT}/%{blenderlib}

cp -a release/scripts/bpydata ${RPM_BUILD_ROOT}/%{blenderlib}
cp -a release/scripts ${RPM_BUILD_ROOT}/%{blenderlib}

pushd bin/.blender/locale
mv pt_br pt_BR
mv zh_cn uh_CN
popd

cp -a bin/.blender/locale ${RPM_BUILD_ROOT}/%{_datadir}

install -p -D -m 644 release/scripts/*.py ${RPM_BUILD_ROOT}/%{blenderlib}

install -m 644 release/VERSION ${RPM_BUILD_ROOT}/%{blenderlib}
install -m 644 bin/.blender/.Blanguages ${RPM_BUILD_ROOT}/%{blenderlib}
install -m 644 bin/.blender/.bfont.ttf ${RPM_BUILD_ROOT}/%{blenderlib}

install -p -D -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}%{blenderlib}/import-3ds-0.7.py
install -p -D -m 644 %{SOURCE2} ${RPM_BUILD_ROOT}%{blenderlib}/export-3ds-0.71.py

install -p -D -m 644 %{SOURCE3} ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/blender.png

install -p -D -m 644 %{SOURCE5} ${RPM_BUILD_ROOT}%{_datadir}/mime/packages/blender.xml

#
# Install plugins
#

install -d ${RPM_BUILD_ROOT}/%{plugins}/sequence
install -d ${RPM_BUILD_ROOT}/%{plugins}/texture

install -m 644 release/plugins/sequence/*.so ${RPM_BUILD_ROOT}/%{plugins}/sequence
install -m 655 release/plugins/texture/*.so ${RPM_BUILD_ROOT}/%{plugins}/texture

desktop-file-install --vendor fedora                    \
  --dir ${RPM_BUILD_ROOT}%{_datadir}/applications       \
  --add-category X-Fedora                               \
  %{SOURCE4}

%find_lang %name

%clean
rm -rf ${RPM_BUILD_ROOT}


%post
update-mime-database %{_datadir}/mime > /dev/null 2>&1 || :
update-desktop-database %{_datadir}/applications > /dev/null 2>&1 || :


%postun
update-mime-database %{_datadir}/mime > /dev/null 2>&1 || :
update-desktop-database %{_datadir}/applications > /dev/null 2>&1 || :


%files -f %name.lang
%defattr(-,root,root,-)
%doc COPYING README doc/python-dev-guide.txt doc/GPL-license.txt doc/bf-members.txt
%{_bindir}/*
%{_datadir}/applications/fedora-blender.desktop
%{_datadir}/pixmaps/*.png
%{blenderlib}/
%{_libdir}/blender/
%{_datadir}/mime/packages/blender.xml

%changelog
* Tue Dec 12 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-10
- Exclude x86_64 arch (#219329)

* Mon Dec 11 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-9
- New build to solve broken deps

* Wed Nov 29 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-6
- Rebuild to solve broken deps

* Tue Oct 31 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-5
- Rebuilt to fix broken deps

* Mon Oct 16 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-4
- /usr/lib/blender should own by the package

* Wed Oct 11 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-3
- Correct invalid locale paths (#210209)

* Wed Sep 13 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-2
- Update to new upstream release

* Tue Sep 12 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42-10
- Rebuild to solve broken deps

* Sun Sep  3 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42-9
- Rebuild for FC-6

* Thu Aug 10 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42-7
- Remove %%ghost for pyo files for fullfilling new packaging guidelines

* Thu Aug 10 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42-6
- Rebuilt to solve broken deps

* Wed Jul 26 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42-5
- Fix symlink in blender-wrapper to locale

* Thu Jul 20 2006 Jochen Schmitt <jochen herr-schmitt de> 2.42-4
- Fix UI Problem (#199418)

* Mon Jul 17 2006 Jochen Schmitt <jochen herr-schmitt de> 2.42-3
- Fix some BR stuff.

* Sun Jul 16 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42-1
- New upstream release.

* Sun Feb 19 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.41-3
- Rebuild for FC-5.

* Mon Feb  6 2006 Jochen Schmitt <Jochen herr-schmitt.de> 2.41-2
- Add freealut as dependancy.

* Sun Jan 30 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.41-1
- Update to new upstream release.

* Wed Jan 18 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.40-2
- New upstream release.
- adapting to mudular X.
- add libtiff-devel as BuildRequires.

* Mon Jun 6 2005 Toshio Kuratomi <toshio-tiki-lounge.com> 2.37-3
- Bump release for development.

* Sun Jun 5 2005 Toshio Kuratomi <toshio-tiki-lounge.com> 2.37-2
- Patch to fix compilation errors on x86_64.

* Sun Jun 5 2005 Toshio Kuratomi <toshio-tiki-lounge.com> 2.37-1
- Update to 2.37.
- Drop gcc4 patch.

* Mon May 16 2005 Toshio Kuratomi <toshio-tiki-lounge.com> 2.36-3
- Bump and rebuild now that scons is available on all platforms.

* Sat May 14 2005 Toshio Kuratomi <toshio-tiki-lounge.com> 2.36-2
- Fix a gcc4 error.

* Fri May 13 2005 Toshio Kuratomi <toshio-tiki-lounge.com> 2.36-1
- Update to 2.36.
- Rebuild with new gcc4.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Mon Nov 15 2004 Phillip Compton <pcompton[AT]proteinmedia.com> 2.35-1
- 2.35.

* Thu Nov 11 2004 Phillip Compton <pcompton[AT]proteinmedia.com> 2.34-0.fdr.3
- Mime-type corrections for FC3.
- Dropped redundent BR XFree86-devel.

* Thu Aug 05 2004 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.34-0.fdr.2
- blender.applications file.
- blender.xml file.
- post/postun update-mime-database.

* Thu Aug 05 2004 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.34-0.fdr.1
- Updated to 2.34.

* Thu Aug 05 2004 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.33-0.fdr.2.a
- Include 3ds import/export scripts.
- Added mime info.
- Added mime icon (from yattacier theme).

* Wed Aug 04 2004 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.33-0.fdr.1.a
- 2.33a.
- Now building with scons.

* Tue Feb 10 2004 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.32-0.fdr.2
- Now including scripts.

* Thu Feb 05 2004 Phillip Compton <pcompton[AT]proteinmedia.com> 0:2.32-0.fdr.1
- Updated to 2.32.

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
