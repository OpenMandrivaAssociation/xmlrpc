%define section         free
%define gcj_support     1

Name:           xmlrpc
Version:        2.0.1
Release:        12
Epoch:          0
Summary:        Java XML-RPC implementation
License:        Apache License
Group:          Development/Java
Url:            http://ws.apache.org/xmlrpc/
Source0:        http://www.apache.org/dist/ws/xmlrpc/sources/xmlrpc-2.0.1-src.tar.gz
Requires:       servletapi5
Requires:       commons-httpclient >= 0:2.0.2
Requires:       commons-codec >= 0:1.3
Requires:       junit >= 0:3.8.1
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%endif
BuildRequires:  ant
BuildRequires:  java-rpmbuild >= 0:1.5
BuildRequires:  servletapi5
BuildRequires:  junit >= 0:3.8.1
BuildRequires:  commons-httpclient >= 0:2.0.2
BuildRequires:  commons-codec >= 0:1.3

%description
Apache XML-RPC is a Java implementation of XML-RPC, a popular protocol
that uses XML over HTTP to implement remote procedure calls.
Apache XML-RPC was previously known as Helma XML-RPC. If you have code
using the Helma library, all you should have to do is change the import
statements in your code from helma.xmlrpc.* to org.apache.xmlrpc.*.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q

%build
export CLASSPATH=%(build-classpath jsse commons-httpclient commons-codec servletapi5 junit 2>/dev/null)
%{ant} -Dbuild.dir=./bin -Dbuild.dest=./bin -Dsrc.dir=./src -Dfinal.name=%{name}-%{version} -Djavadoc.destdir=./docs/apidocs -Dhave.deps=true jar
%{ant} -Dbuild.dir=./bin -Dbuild.dest=./bin -Dsrc.dir=./src -Dfinal.name=%{name}-%{version} -Djavadoc.destdir=./docs/apidocs -Dhave.deps=true javadocs

%install
# jars
%{__mkdir_p} %{buildroot}%{_javadir}
cp -a bin/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
cp -a bin/%{name}-%{version}-applet.jar %{buildroot}%{_javadir}/%{name}-applet-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -a docs/apidocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt README.txt
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%dir %{_javadocdir}/%{name}


%changelog
* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0:2.0.1-8mdv2011.0
+ Revision: 608223
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 0:2.0.1-7mdv2010.1
+ Revision: 519081
- rebuild

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 0:2.0.1-6mdv2009.0
+ Revision: 226066
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:2.0.1-5mdv2008.1
+ Revision: 121060
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)
- remove unnecessary Requires(post) on java-gcj-compat

* Sun Jun 10 2007 David Walluck <walluck@mandriva.org> 0:2.0.1-3mdv2008.0
+ Revision: 37945
- birthday rebuild
- spec file cleanup
- Import xmlrpc



* Sun Jun 04 2006 David Walluck <walluck@mandriva.org> 0:2.0.1-2mdv2007.0
- rebuild for libgcj.so.7
- fix gcj support

* Wed Feb 22 2006 David Walluck <walluck@mandriva.org> 0:2.0.1-1mdk
- release (0:2.0.1-1jpp_4fc)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0:2.0.1-1jpp_4fc
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0:2.0.1-1jpp_3fc
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 25 2006 Igor Foox <ifoox@redhat.com>  0:2.0.1-1jpp_2fc
- ExcludeArch s390x and ppc64

* Wed Jan 18 2006 Andrew Overholt <overholt@redhat.com> 0:2.0.1-1jpp_2fc
- Comment out JPackage Distribution and Vendor tags

* Wed Jan 18 2006 Jesse Keating <jkeating@redhat.com> 0:2.0.1-1jpp_2fc
- bump for test

* Wed Jan 18 2006 Igor Foox <ifoox@redhat.com> 0:2.0.1-1jpp_1fc
- Update to version 2.0.1
- Natively compile

* Thu Aug 26 2004 Ralph Apel <r.apel at r-apel.de> 0:1.2-0.b1.3jpp
- Build with ant-1.6.2

* Thu Apr 29 2004 David Walluck <david@jpackage.org> 0:1.2-0.b1.2jpp
- add jar symlinks
- remove %%buildroot in %%install

* Tue May 06 2003 David Walluck <david@anti-microsoft.org> 0:1.2-0.b1.1jpp
- 1.2-b1
- update for JPackage 1.5

* Mon Mar 18 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.1-1jpp 
- 1.1
- generic servlet support
- used source release
- dropped.patch.bz2
- added applet jar

* Mon Jan 21 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-3jpp 
- versioned dir for javadoc
- no dependencies for javadoc package
- dropped jsse package
- adaptation to new servlet3 package
- adaptation to new jsse package
- section macro

* Fri Dec 7 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-2jpp
- javadoc into javadoc package

* Sat Nov 3 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-1jpp
- first JPackage release
