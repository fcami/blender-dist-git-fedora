%global blenderlib  %{_datadir}/blender
%global blenderarch %{_libdir}/blender

%global fontname blender

Name:           blender
Version:        2.49b
Release: 	2%{?dist}

Summary:        3D modeling, animation, rendering and post-production

Group:          Applications/Multimedia
License:        GPLv2
URL:            http://www.blender.org
# This is a customized source package without bundled dependencies
# See blender-repack.sh
Source0:	blender-%{version}-repack.tar.bz2

Source5:        blender.xml
Source6:        blender-wrapper
Source7:	blenderplayer-wraper
Source8:	blender-2.49.config
Source100:      blender-repack.sh

Patch1:         blender-2.49-scons.patch
Patch2:		blender-2.44-bid.patch

# Both patches are forwarded to upstream via email
Patch100:	blender-2.46rc3-cve-2008-1103-1.patch
Patch101:	blender-2.48a-cve-2008-4863.patch

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
BuildRequires:  libGL-devel
BuildRequires:  libGLU-devel
BuildRequires:  freetype-devel
BuildRequires:  OpenEXR-devel
BuildRequires:  glew-devel
BuildRequires:	fontpackages-devel

BuildRequires:	fftw-devel
BuildRequires:	ftgl-devel
BuildRequires:	ode-devel
BuildRequires:	openjpeg-devel
BuildRequires:  qhull-devel

Requires(post): desktop-file-utils
Requires(post): shared-mime-info
Requires(postun): desktop-file-utils
Requires(postun): shared-mime-info

Requires:	  blender-fonts = %{version}-%{release}

%if 0%{?fedora} > 10
Requires:	  dejavu-sans-fonts
%endif

%if 0%{?fedora} <= 10
Requires:	  dejavu-fonts
%endif

Provides:	  blender-fonts = %{version}-%{release}
Obsoletes:	  blender-fonts <= 2.48a-9

%description
Blender is the essential software solution you need for 3D, from modeling,
animation, rendering and post-production to interactive creation and playback.

Professionals and novices can easily and inexpensively publish stand-alone,
secure, multi-platform content to the web, CD-ROMs, and other media.



%package -n blenderplayer
Summary:       Standalone blender player
Group:	       Applications/Multimedia

%description -n blenderplayer
This package contains a stand alone release of the blender player.
You will need this package to play games which are based on the
Blender Game Engine.



%prep
%setup -q 
%patch1 -p1 -b .org
%patch2 -p1 -b .bid

%patch100 -p1
%patch101 -p1

# binreloc is not a part of fedora
rm -rf extern/ffmpeg
rm -rf extern/fftw
rm -rf extern/glew
rm -rf extern/libmp3lame
rm -rf extern/libopenjpeg
rm -rf extern/libredcode
rm -rf extern/ode
rm -rf extern/x264
rm -rf extern/xvidcore
rm -rf extern/qhull
rm -rf extern/make
rm -rf extern/verse

PYVER=$(%{__python} -c "import sys ; print sys.version[:3]")

sed -e 's|@LIB@|%{_libdir}|g' -e "s/@PYVER@/$PYVER/g" \
	 <%{SOURCE8} >user-config.py

iconv -f iso-8859-1 -t utf-8 doc/bf-members.txt -o doc/bf-members.txt.utf8
mv doc/bf-members.txt.utf8 doc/bf-members.txt

%build
scons %{?_smp_mflags} blenderplayer BF_QUIET=0

install -d release/plugins/include
install -m 644 source/blender/blenpluginapi/*.h release/plugins/include

chmod +x release/plugins/bmake

make -C release/plugins/

%install
rm -rf ${RPM_BUILD_ROOT}

install -D -m 755 build/linux2/bin/blender ${RPM_BUILD_ROOT}%{_bindir}/blender.bin
install -D -m 755 build/linux2/bin/blenderplayer ${RPM_BUILD_ROOT}%{_bindir}/blenderplayer.bin

install -D -m 755 %{SOURCE6} ${RPM_BUILD_ROOT}%{_bindir}/blender
install -D -m 755 %{SOURCE7} ${RPM_BUILD_ROOT}%{_bindir}/blenderplayer

#
#  Install miscellanous files to /usr/lib/blender
#

mkdir -p ${RPM_BUILD_ROOT}%{blenderlib}/scripts

#
# Create empty %%{_libdir}/blender/scripts to claim ownership
#

mkdir -p ${RPM_BUILD_ROOT}%{blenderarch}/{scripts,plugins/sequence,plugins/texture}

#
# Install plugins
#

install -pm 755 release/plugins/sequence/*.so ${RPM_BUILD_ROOT}%{blenderarch}/plugins/sequence
install -pm 755 release/plugins/texture/*.so ${RPM_BUILD_ROOT}%{blenderarch}/plugins/texture


find bin/.blender/locale -name '.svn' -exec rm -f {} ';'

cp -a bin/.blender/locale ${RPM_BUILD_ROOT}%{_datadir}

cp -R -a -p release/scripts/* ${RPM_BUILD_ROOT}%{blenderlib}/scripts

install -pm 644 release/VERSION ${RPM_BUILD_ROOT}%{blenderlib}
install -pm 644 bin/.blender/.Blanguages ${RPM_BUILD_ROOT}%{blenderlib}

#
# Create link to DejaVu-Sans
#
ln -sf %{_fontbasedir}/dejavu/DejaVuSans.ttf ${RPM_BUILD_ROOT}%{blenderlib}/.bfont.ttf

find ${RPM_BUILD_ROOT}%{blenderlib}/scripts -type f -exec sed -i -e 's/\r$//g' {} \;

# Install hicolor icons.
for i in 16x16 22x22 32x32 ; do
  mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/${i}/apps
  install -pm 0644 release/freedesktop/icons/${i}/%{name}.png \
    ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/${i}/apps/%{name}.png
done

install -p -D -m 644 %{SOURCE5} ${RPM_BUILD_ROOT}%{_datadir}/mime/packages/blender.xml

desktop-file-install --vendor fedora                    \
  --dir ${RPM_BUILD_ROOT}%{_datadir}/applications       \
  release/freedesktop/blender.desktop

#Fix perm
chmod +x ${RPM_BUILD_ROOT}%{blenderlib}/scripts/bpymodules/blend2renderinfo.py

%find_lang %{name}



%clean
rm -rf ${RPM_BUILD_ROOT}

%post
%{_bindir}/update-mime-database %{_datadir}/mime
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi 
%{_bindir}/update-desktop-database %{_datadir}/applications || :


%postun
%{_bindir}/update-mime-database %{_datadir}/mime
%{_bindir}/update-desktop-database %{_datadir}/applications
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING README doc/python-dev-guide.txt doc/GPL-license.txt doc/bf-members.txt
%{_bindir}/blender
%{_bindir}/blender.bin
%{_datadir}/applications/fedora-blender.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{blenderlib}/
%{blenderarch}/
%{_datadir}/mime/packages/blender.xml

%files -n blenderplayer
%doc COPYING
%defattr(-,root,root,-)
%{_bindir}/blenderplayer
%{_bindir}/blenderplayer.bin

%changelog
* Thu Nov 12 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.49b-2
- Rebuild

* Mon Sep  7 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.49b-1
- New upstream release (#520780)

* Tue Aug 11 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.49a-6
- Build again new freealut relase (openalut-soft)

* Mon Aug  3 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.49a-5
- Revoke using of system FTGL library

* Mon Aug  3 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.49a-4
- Rebuild for python-2.6.2

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.49a-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul  6 2009 kwizart < kwizart at gmail.com > - 2.49a-2
- Fix perm on blend2renderinfo.py - raised by #506957

* Fri Jun 19 2009 kwizart < kwizart at gmail.com > - 2.49a-1
- Update to 2.49a

* Fri Jun 19 2009 kwizart < kwizart at gmail.com > - 2.49-6
- Update blender-wrapper script.
- Repackage the sources archive.
- Remove deprecated import/export-3ds-0.7.py
- Pick desktop and icons from tarball and use hicolor icons.
- Hack config.py to add system libqhull along with gettexlib.

* Fri Jun 12 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.49-5
- Fix Type
- Change symlink to %%{_fontbasedir}/Dejavu/...

* Wed Jun  3 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.49-4
- Rework on the blender wrapper script

* Tue Jun  2 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.49-3
- Try to build agains more system libraries as possible

* Mon Jun  1 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.49-1
- New upstream release

* Wed May 13 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-22
- Copy bpydata/config/* into ~/.blender/.../bpydata/config in blender-wrapper script

* Mon Apr 20 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-21
- Chamge BR mesa-libGL* into libGL* 

* Mon Apr 20 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-20
- Remove x264 from source tar ball
- Some cosmetic changes

* Wed Apr  1 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-19
- Change nonfree to freeworld

* Tue Mar 31 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-18
- Fix typo

* Tue Mar 31 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-17
- Create drop-in for non-free blender release

* Wed Mar 11 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-16
- Put blenderplayer into a separate subpackage (#489685) 

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.48a-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-14
- Fix broken wrapper script

* Wed Jan 21 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-13
- Do some fixes on blender-wrapeer

* Sun Jan 18 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-12
- Change Req. for font package because fonts naming was changed (#480444)

* Thu Jan 15 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-11
- Rebuild for new openssl package

* Sun Jan 11 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-10
- Create symlink to DajaVu-Sans

* Tue Jan  6 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-9
- Create fonts sub-package (#477370)

* Sat Dec 27 2008 Lubomir Rintel <lkundrak@v3.sk> 2.48a-7
- Fix optflags use, this time for real

* Sat Dec 27 2008 Lubomir Rintel <lkundrak@v3.sk> 2.48a-6
- Use proper compiler flags (see #199418)
- Minor grammar & language fixes and tidy-ups

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 2.48a-5
- Rebuild for Python 2.6

* Mon Nov  3 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-4
- Fix security issue (#469655, CVE-2008-4863)
[5~
* Sun Oct 26 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-3
- Create %%{_libdir}/blender/scripts/ to claim ownership

* Sun Oct 26 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.48a-1
- New upstream release

* Wed Oct 15 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.48-1
- New upstream release
- Build agains system glew library (#466755)

* Tue Oct  7 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.47-5
- Reorganisation directory structure to fix sysinfo.py issue

* Tue Oct  7 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.47-4
- Avoid duplicate python script (#465810)

* Sun Sep  7 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.47-3
- Fix prerelease SPEC file

* Thu Aug 14 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.47-1
- New upstream release

* Tue Aug 12 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.47-0.2
- New upstream release (blender-2.47rc)

* Mon May 19 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.46-1
- New upstream release

* Wed May  7 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.46-0.3.1
- Some fixes for CVE-2008-1003

* Tue May  6 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.46-0.3
- Release Canditate for 2.46

* Sun Apr 27 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.45-13
- More generic patch for scons issue

* Thu Apr 24 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.45-12
- Fix odd scons compatibility issue

* Thu Apr 24 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.45-11
- Fix CVS-2008-1102 (#443937)

* Wed Mar 12 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.45-10
- Clarification of restrictions caused by legal issues

* Tue Mar  4 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.45-9
- Apply yafray patch only on 64-bit systems

* Thu Feb 28 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.45-8
- Fix yafray load bug (#451571)

* Sun Feb 10 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.45-7
- Rebuild for gcc-4.3

* Sat Jan 26 2008 Alex Lancaster <alexlan[AT]fedoraproject org> 2.45-6
- Rebuild for new gettext

* Thu Jan 17 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.45-5
- Fix gcc-4.3 related issues

* Tue Oct 16 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.45-4
- Rebuild again for OpenEXR

* Sun Oct 14 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.45-3
- Rebuild

* Sun Sep 23 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.45-2
- Change method how to determinate python version

* Thu Sep 20 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.45-1
- New upstream release

* Thu Aug  9 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.44-8
- Fix koji-python issue

* Wed Aug  8 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.44-6
- Changing license tag
- Add python as an BR

* Mon May 21 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.44-4
- Use of $$RPM_OPT_FLAGS to compile blender

* Sun May 20 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.44-2
- Increase release number

* Tue May 15 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.44-1
- New upstream release

* Wed May  9 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-24
- Remove ffmpeg lib during a legal issue (#239476)

* Tue May  8 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-23
- Exclude ppc64 arch

* Mon May  7 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-21
- Fix security issue (#239338)

* Sun Apr 22 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-20
- Romove package from the x86_64 arch (#237423)

* Mon Jan  8 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-18
- Rebult

* Thu Dec 14 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-17
- Replace x86-patch with one from the blender project

* Thu Dec 14 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-16
- Rebuild

* Tue Dec 12 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-12
- Fix typo

* Tue Dec 12 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.42a-11
- Try x64-patch for complle with python-2.5

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
