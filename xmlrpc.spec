Name:           xmlrpc
Version:        2.0.1
Release:        %mkrel 10
Summary:        Java XML-RPC implementation
License:        Apache License
Group:          Development/Java
Url:            http://ws.apache.org/xmlrpc/
Source0:        http://www.apache.org/dist/ws/xmlrpc/sources/xmlrpc-2.0.1-src.tar.gz
Requires:       servlet25
Requires:       commons-httpclient >= 0:2.0.2
Requires:       commons-codec >= 0:1.3
Requires:       junit >= 0:3.8.1
Requires:       jpackage-utils
Requires:       ws-commons-util
BuildRequires:  ant
BuildRequires:  java-rpmbuild >= 0:1.5
BuildRequires:  servlet25
BuildRequires:  junit >= 0:3.8.1
BuildRequires:  commons-httpclient >= 0:2.0.2        
BuildRequires:  apache-commons-codec >= 0:1.3
BuildRequires:  jpackage-utils >= 0:1.6

Buildarch:	noarch

%description
Apache XML-RPC is a Java implementation of XML-RPC, a popular protocol
that uses XML over HTTP to implement remote procedure calls.
Apache XML-RPC was previously known as Helma XML-RPC. If you have code
using the Helma library, all you should have to do is change the import
statements in your code from helma.xmlrpc.* to org.apache.xmlrpc.*.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Requires:   jpackage-utils

%description javadoc
Javadoc for %{name}.

%prep
%setup -q

%build
export CLASSPATH=%(build-classpath commons-httpclient apache-commons-codec servlet25 junit 2>/dev/null)
%{ant} -Dbuild.dir=./bin -Dbuild.dest=./bin -Dsrc.dir=./src -Dfinal.name=%{name}-%{version} -Djavadoc.destdir=./docs/apidocs -Dhave.deps=true jar
%{ant} -Dbuild.dir=./bin -Dbuild.dest=./bin -Dsrc.dir=./src -Dfinal.name=%{name}-%{version} -Djavadoc.destdir=./docs/apidocs -Dhave.deps=true javadocs

%install
%{__rm} -rf %{buildroot}

# jars
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a bin/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
%{__cp} -a bin/%{name}-%{version}-applet.jar %{buildroot}%{_javadir}/%{name}-applet-%{version}.jar

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr docs/apidocs/* %{buildroot}%{_javadocdir}/%{name}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt README.txt
%{_javadir}/*

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}
