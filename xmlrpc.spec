%define name		xmlrpc
%define version		2.0.1
%define release		2
%define	section		free
%define gcj_support     1

Name:		%{name}
Version:	%{version}
Release:	%mkrel %{release}
Epoch:		0
Summary:	Java XML-RPC implementation
License:	Apache License
Group:		Development/Java
Url:		http://xml.apache.org/%{name}/
Source0:	http://www.apache.org/dist/ws/xmlrpc/source/xmlrpc-%{version}-src.tar.bz2
Requires:	servletapi5
Requires:	commons-httpclient >= 0:2.0.2
Requires:	commons-codec >= 0:1.3
Requires:	junit >= 0:3.8.1
%if %{gcj_support}
Requires(post):		java-gcj-compat
Requires(postun):	java-gcj-compat
BuildRequires:	java-gcj-compat-devel
%endif
BuildRequires:	ant
BuildRequires:	jpackage-utils >= 0:1.5
BuildRequires:	servletapi5
BuildRequires:	junit >= 0:3.8.1
BuildRequires:	commons-httpclient >= 0:2.0.2	
BuildRequires:	commons-codec >= 0:1.3
Buildroot:	%{_tmppath}/%{name}-%{version}-buildroot
#Distribution:	JPackage
#Vendor:		JPackage Project

%description
Apache XML-RPC is a Java implementation of XML-RPC, a popular protocol
that uses XML over HTTP to implement remote procedure calls.
Apache XML-RPC was previously known as Helma XML-RPC. If you have code
using the Helma library, all you should have to do is change the import
statements in your code from helma.xmlrpc.* to org.apache.xmlrpc.*.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%build
export CLASSPATH=%(build-classpath jsse commons-httpclient commons-codec servletapi5 junit 2>/dev/null)
%ant -Dbuild.dir=./bin -Dbuild.dest=./bin -Dsrc.dir=./src -Dfinal.name=%{name}-%{version} -Djavadoc.destdir=./docs/apidocs -Dhave.deps=true jar
%ant -Dbuild.dir=./bin -Dbuild.dest=./bin -Dsrc.dir=./src -Dfinal.name=%{name}-%{version} -Djavadoc.destdir=./docs/apidocs -Dhave.deps=true javadocs

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 bin/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
install -m 644 bin/%{name}-%{version}-applet.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-applet-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do \
ln -sf ${jar} ${jar/-%{version}/}; done)

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%post
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi

%postun
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt README.txt
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
