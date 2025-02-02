%{?_javapackages_macros:%_javapackages_macros}
Name:           xmlrpc
Version:        3.1.3
Release:        11.3
Epoch:          1
Summary:        Java XML-RPC implementation
Group:		Development/Java
License:        ASL 2.0
URL:            https://ws.apache.org/xmlrpc/
BuildArch:      noarch

Source0:        http://www.apache.org/dist/ws/xmlrpc/sources/apache-xmlrpc-%{version}-src.tar.bz2
Patch0:         %{name}-client-addosgimanifest.patch
Patch1:         %{name}-common-addosgimanifest.patch
Patch2:         %{name}-javax-methods.patch
Patch3:		xmlrpc-server-addosgimanifest.patch

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache:apache)
BuildRequires:  mvn(commons-httpclient:commons-httpclient)
BuildRequires:  mvn(commons-logging:commons-logging)
BuildRequires:  mvn(javax.servlet:servlet-api)
BuildRequires:  mvn(org.apache.ws.commons.util:ws-commons-util)


%description
Apache XML-RPC is a Java implementation of XML-RPC, a popular protocol
that uses XML over HTTP to implement remote procedure calls.
Apache XML-RPC was previously known as Helma XML-RPC. If you have code
using the Helma library, all you should have to do is change the import
statements in your code from helma.xmlrpc.* to org.apache.xmlrpc.*.

%package javadoc
Summary:    Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%package common
Summary:    Common classes for XML-RPC client and server implementations
# Provide xmlrpc is not here because it would be useless due to different jar names
Obsoletes:  %{name} < 3.1.3
Obsoletes:  %{name}3-common < 3.1.3-13
Provides:   %{name}3-common = 3.1.3-13

%description common
%{summary}.

%package client
Summary:    XML-RPC client implementation
Obsoletes:  %{name}3-client < 3.1.3-13
Provides:   %{name}3-client = 3.1.3-13

%description client
%{summary}.

%package server
Summary:    XML-RPC server implementation
Obsoletes:  %{name}3-server < 3.1.3-13
Provides:   %{name}3-server = 3.1.3-13

%description server
%{summary}.

%prep
%setup -q -n apache-%{name}-%{version}-src
%patch2 -p1
pushd client
%patch0
popd
pushd common
%patch1
popd
pushd server
%patch3
popd

sed -i 's/\r//' LICENSE.txt

%pom_disable_module dist
%pom_remove_dep jaxme:jaxmeapi common
%mvn_file :{*} @1
%mvn_package :*-common %{name}

%build
# FIXME: ignore test failure because server part needs network
%mvn_build -s -- -Dmaven.test.failure.ignore=true

%install
%mvn_install

%files common -f .mfiles-%{name}
%doc LICENSE.txt NOTICE.txt

%files client -f .mfiles-%{name}-client

%files server -f .mfiles-%{name}-server

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.1.3-6
- Update to current packaging guidelines

* Fri May 17 2013 Alexander Kurtakov <akurtako@redhat.com> 1:3.1.3-5
- Remove javax.xml.bind from osgi imports - it's part of the JVM now.
- Drop the ws-jaxme dependency for the same reason.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1:3.1.3-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Oct 20 2012 Peter Robinson <pbrobinson@fedoraproject.org> 3.1.3-2
- xmlrpc v2 had an Epoch so we need one here. Add it back

* Fri Sep 14 2012 Alexander Kurtakov <akurtako@redhat.com> 3.1.3-1
- First release of version 3.x package
