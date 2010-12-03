%define section         free
%define gcj_support     1

Name:           xmlrpc
Version:        2.0.1
Release:        %mkrel 8
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
Buildroot:      %{_tmppath}/%{name}-%{version}-buildroot

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
%{__rm} -rf %{buildroot}

# jars
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a bin/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
%{__cp} -a bin/%{name}-%{version}-applet.jar %{buildroot}%{_javadir}/%{name}-applet-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a docs/apidocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

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
