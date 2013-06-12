# TODO: setup firefox for ed2k links using triggers and a file in /usr/lib/firefox-3.0.1/defaults/preferences/
%global _hardened_build 1

Name:           amule
Version:        2.3.1
Release:        4%{?dist}
Summary:        File sharing client compatible with eDonkey
License:        GPLv2+
Group:          Applications/Internet
Source0:        http://dl.sourceforge.net/%{name}/aMule-%{version}.tar.xz
Patch0:         aMule-2.3.1-gcc47.patch
URL:            http://amule.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# See http://www.amule.org/wiki/index.php/Requirements
BuildRequires:  wxGTK-devel >= 0:2.8.7, desktop-file-utils, expat-devel
BuildRequires:  gd-devel >= 2.0.0, libpng-devel
BuildRequires:  gettext-devel, flex, bison
BuildRequires:  readline-devel, cryptopp-devel, libupnp-devel
BuildRequires:  GeoIP-devel
Requires(pre):  chkconfig
Requires:       %{name}-nogui

%description
aMule is an easy to use multi-platform client for ED2K Peer-to-Peer
Network. It is a fork of xMule, whis was based on eMule for
Windows. aMule currently supports (but is not limited to) the
following platforms: Linux, *BSD and MacOS X.

%package nogui
Summary:        Components of aMule which don't require a GUI (for servers)
Group:          Applications/Internet

%description nogui
This package contains the aMule components which don't require a GUI.
It is useful for servers which don't have Xorg.


%package -n xchat-%{name}
Summary:        Plugin to display aMule's statistics in XChat
Group:          Applications/Internet
Requires:       %{name} = %{version}-%{release}
Requires:       xchat
%if 0%{?fedora} > 9 || 0%{?rhel} > 5 
BuildArch:      noarch 
%endif 

%description -n xchat-%{name}
This plugins allows you to display aMule statistics in XChat


%prep
%setup -q -n aMule-%{version}
%patch0 -p1 -b .gcc47
manfiles=`find . -name "*.1"`
for manfile in $manfiles; do
    iconv -f ISO-8859-1 -t UTF-8 < $manfile > $manfile.utf8
    touch -r $manfile $manfile.utf8
    mv -f $manfile.utf8 $manfile
done

%build
%configure \
    --disable-rpath \
    --disable-debug \
    --docdir=%{_datadir}/doc/%{name}-%{version} \
    --enable-wxcas \
    --enable-cas \
    --enable-alc \
    --enable-alcc \
    --enable-xas \
    --enable-amule-daemon \
    --enable-amulecmd \
    --enable-webserver \
    --enable-amule-daemon \
    --enable-geoip \
    --enable-ccache \
    --enable-amule-gui \
    --enable-optimize \
    --with-denoise-level=0

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT _docs

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%find_lang %{name}

# desktop files
desktop-file-install --vendor livna \
                     --delete-original\
                     --dir $RPM_BUILD_ROOT%{_datadir}/applications\
                     --add-category Network\
                     $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

iconv -f ISO-8859-1 -t UTF-8 < src/utils/aLinkCreator/alc.desktop \
      > $RPM_BUILD_ROOT%{_datadir}/applications/alc.desktop
desktop-file-install --vendor livna \
                     --delete-original\
                     --dir $RPM_BUILD_ROOT%{_datadir}/applications\
                     $RPM_BUILD_ROOT%{_datadir}/applications/alc.desktop

desktop-file-install --vendor livna \
                     --delete-original\
                     --dir $RPM_BUILD_ROOT%{_datadir}/applications\
                     $RPM_BUILD_ROOT%{_datadir}/applications/wxcas.desktop

desktop-file-install --vendor livna \
                     --delete-original\
                     --dir $RPM_BUILD_ROOT%{_datadir}/applications\
                     --add-category Network\
                     $RPM_BUILD_ROOT%{_datadir}/applications/%{name}gui.desktop


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc ABOUT-NLS
%{_bindir}/alc
%{_bindir}/amule
%{_bindir}/cas
%{_bindir}/wxcas
%{_bindir}/amulegui
%{_datadir}/%{name}/
%{_datadir}/cas
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*
%{_mandir}/man1/alc.1.gz
%{_mandir}/*/man1/alc.1.gz
%{_mandir}/man1/amule.1.gz
%{_mandir}/*/man1/amule.1.gz
%{_mandir}/man1/cas.1.gz
%{_mandir}/*/man1/cas.1.gz
%{_mandir}/man1/wxcas.1.gz
%{_mandir}/*/man1/wxcas.1.gz
%{_mandir}/man1/amulegui.1.gz
%{_mandir}/*/man1/amulegui.1.gz
%exclude %{_datadir}/%{name}/webserver

%files nogui
%defattr(-,root,root,-)
%{_bindir}/alcc
%{_bindir}/amulecmd
%{_bindir}/amuled
%{_bindir}/amuleweb
%{_bindir}/ed2k
%{_datadir}/%{name}/webserver
%{_mandir}/man1/alcc.1.gz
%{_mandir}/*/man1/alcc.1.gz
%{_mandir}/man1/amulecmd.1.gz
%{_mandir}/*/man1/amulecmd.1.gz
%{_mandir}/man1/amuled.1.gz
%{_mandir}/*/man1/amuled.1.gz
%{_mandir}/man1/amuleweb.1.gz
%{_mandir}/*/man1/amuleweb.1.gz
%{_mandir}/man1/ed2k.1.gz
%{_mandir}/*/man1/ed2k.1.gz


%files -n xchat-%{name}
%defattr(-,root,root,-)
%{_bindir}/autostart-xas
%attr(0755, root, root) %{_libdir}/xchat/plugins/xas.pl
%{_mandir}/man1/xas.1.gz
%{_mandir}/*/man1/xas.1.gz


%changelog
* Wed Jun 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-4
- Rebuilt for GD 2.1.0

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-3
- Mass rebuilt for Fedora 19 Features

* Sun May 13 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-2
- Add hardened build
- Fix build with gcc47

* Mon Jan 23 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-0
- Update to 2.3.1

* Thu Oct 14 2010 Nicolas Chauvet <kwizart@gmail.com> - 2.2.6-3
- Fix FTBFS and gcc compiler bug
- Conditionalize noarch subpackage

* Fri Sep 24 2010 Felix Kaechele <heffer@fedoraproject.org> - 2.2.6-2
- rebuild for new wx

* Sun Sep 20 2009 Felix Kaechele <heffer@fedoraproject.org> - 2.2.6-1
- 2.2.6

* Tue May 19 2009 Felix Kaechele <heffer@fedoraproject.org> - 2.2.5-1
- 2.2.5

* Wed Apr 15 2009 Felix Kaechele <felix at fetzig dot org> - 2.2.4-1
- upstream 2.2.4
- spec fixup

* Sun Mar 22 2009 Felix Kaechele <felix at fetzig dot org> - 2.2.3-1
- updated to 2.2.3
- replaced patch3 with new one for gcc4.4

* Thu Nov 20 2008 Aurelien Bompard <abompard@fedoraproject.org> 2.2.2-2
- add remote GUI

* Sat Nov 08 2008 Aurelien Bompard <abompard@fedoraproject.org> 2.2.2-1
- version 2.2.2
- patch 0 and 2 applied upstream
- drop patch1
- split off non-X-dependent tools

* Sun Oct 26 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.3-5
- rebuilt

* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 2.1.3-4
- rebuild

* Tue Mar 04 2007 kwizart <kwizart at gmail.com > - 2.1.3-3
- Fix wxGTK 2.8.x
- Fix open with O_CREATE
- Prevent timestramps on install
- Add missing BR
- Fix gcc43
- Fix multiple parameter named ProgName

* Sat Oct 07 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> 2.1.3-2
- rebuild

* Mon Jun 12 2006 Aurelien Bompard <gauret[AT]free.fr> 2.1.3-1
- version 2.1.3

* Tue May 30 2006 Aurelien Bompard <gauret[AT]free.fr> 2.1.2-1
- version 2.1.2

* Sat Apr 08 2006 Aurelien Bompard <gauret[AT]free.fr> 2.1.1-1
- version 2.1.1

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Thu Jun 16 2005 Aurelien Bompard <gauret[AT]free.fr> 2.0.3-0.lvn.1
- version 2.0.3

* Sun Jun 05 2005 Aurelien Bompard <gauret[AT]free.fr> 2.0.2-0.lvn.1
- version 2.0.2

* Sat Jun 04 2005 Thorsten Leemhuis <fedora[AT]leemhuis.info> 2.0.1-0.lvn.2
- BR /usr/bin/autopoint instead of gettext; This gives us gettext on pre
  FC4 and gettext-devel on FC4

* Mon May 23 2005 Aurelien Bompard <gauret[AT]free.fr> 2.0.1-0.lvn.1
- version 2.0.1

* Wed May 04 2005 Aurelien Bompard <gauret[AT]free.fr> 0:2.0.0-0.lvn.1
- version 2.0 final(ly)
- drop epoch

* Fri Dec 24 2004 Aurelien Bompard <gauret[AT]free.fr> 0:2.0.0-0.lvn.0.7.rc8
- update to rc8

* Wed Oct 20 2004 Aurelien Bompard <gauret[AT]free.fr> 0:2.0.0-0.lvn.0.6.rc7
- update to rc7: no need for cryptopp anymore

* Mon Jul 19 2004 Aurelien Bompard <gauret[AT]free.fr> 0:2.0.0-0.lvn.0.5.rc5
- update to rc5

* Wed Jul 14 2004 Aurelien Bompard <gauret[AT]free.fr> 0:2.0.0-0.lvn.0.4.rc4a
- update to rc4a (hotfix)

* Wed Jul 14 2004 Aurelien Bompard <gauret[AT]free.fr> 0:2.0.0-0.lvn.0.3.rc4
- fix desktop files for alc and wxcas
- convert tabs into spaces (use diff -b)

* Tue Jul 13 2004 Dams <anvil[AT]livna.org> 0:2.0.0-0.lvn.0.2.rc4
- Removing temporary _docs directory before attempting to create it

* Mon Jul 12 2004 Aurelien Bompard <gauret[AT]free.fr> 0:2.0.0-0.lvn.0.1.rc4
- Version 2.0.0rc4
- new xchat-amule subpackage

* Sun Jun 13 2004 Aurelien Bompard <gauret[AT]free.fr> 0:2.0.0-0.lvn.0.1.rc3
- Version 2.0.0rc3

* Tue Feb 17 2004 Aurelien Bompard <gauret[AT]free.fr> 1.2.6-0.lvn.1
- Version 1.2.6

* Tue Feb 10 2004 Aurelien Bompard <gauret[AT]free.fr> 1.2.5-0.lvn.1
- Version 1.2.5
- Dropped alternatives support (we conflict and obsolete xmule)

* Mon Jan 19 2004 Dams <anvil[AT]livna.org> 0:1.2.4-0.lvn.4
- Added explicit BuildReq:openssl-devel (else it wont build on rh9/rh8
  because of curl-devel packaging bug)

* Mon Jan 19 2004 Dams <anvil[AT]livna.org> 0:1.2.4-0.lvn.3
- Re-add explicit conflits:xmule

* Tue Jan 13 2004 Aurelien Bompard <gauret[AT]free.fr> 1.2.4-0.lvn.2
- Obsoletes xmule (the project seems to have stopped)

* Mon Jan 12 2004 Aurelien Bompard <gauret[AT]free.fr> 1.2.4-0.lvn.1
- version 1.2.4 (small bugfix release)

* Sat Jan 03 2004 Aurelien Bompard <gauret[AT]free.fr> 1.2.3-0.lvn.1
- new version: 1.2.3
- added webserver support (still a little buggy according to aMule's website)

* Thu Dec 18 2003 Aurelien Bompard <gauret[AT]free.fr> 1.2.1-0.lvn.2
- remove enable-optimize
- update Conflicts
- add Epoch: 0

* Mon Dec 15 2003 Aurelien Bompard <gauret[AT]free.fr> 1.2.1-0.lvn.1
- version 1.2.1
- doesn't require wget anymore : libcurl is used instead
- add BuildRequires: curl-devel
- Move Prereq to Requires(pre)
- add enable-optimise to configure

* Thu Nov 27 2003 Aurelien Bompard <gauret[AT]free.fr> 1.2.0-0.lvn.1
- version 1.2.0

* Fri Nov 14 2003 Aurelien Bompard <gauret[AT]free.fr> 1.1.2-0.lvn.3
- Change conflicts
- s/Fedora/Livna/

* Wed Nov 12 2003 Aurelien Bompard <gauret[AT]free.fr> 1.1.2-0.lvn.2
- fix preun

* Wed Nov 12 2003 Aurelien Bompard <gauret[AT]free.fr> 1.1.2-0.lvn.1
- lots of fixes, thanks to Dams (anvil[AT]livna.org)

* Wed Nov 05 2003 Aurelien Bompard <gauret[AT]free.fr> 1.1.2-1
- new version

* Sat Nov 01 2003 Aurelien Bompard <gauret[AT]free.fr> 1.1.1-1
- RedHatification (from PLF/Mandrake)
