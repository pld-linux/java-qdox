#
%include	/usr/lib/rpm/macros.java
Summary:	Extract class/interface/method definitions from sources
Summary(pl.UTF-8):	Wyciąganie definicji klas/interfejsów/metod ze źródeł
Name:		qdox
Version:	1.8
Release:	0.1
License:	Apache v2.0
Group:		Development/Languages/Java
Source0:	http://repository.codehaus.org/com/thoughtworks/qdox/qdox/1.8/qdox-1.8-sources.jar
# Source0-md5:	9cbc745194a39ec27f54bbe16c2342cc
URL:		http://qdox.codehaus.org/
BuildRequires:	ant
BuildRequires:	java-gcj-compat-devel
BuildRequires:	junit
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
QDox is a high speed, small footprint parser for extracting
class/interface/method definitions from source files complete with
JavaDoc @tags. It is designed to be used by active code generators or
documentation tools.

%description -l pl.UTF-8
QDox to bardzo szybki i o niewielkim narzucie analizator do wyciągania
definicji klas/interfejsów/metod z plików źródłowych uzupełnionych
znacznikami @ JavaDoc. Jest zaprojektowany do używania z aktywnymi
generatorami kodu i narzędziami do tworzenia dokumentacji.

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl.UTF-8):	Dokumentacja javadoc dla pakietu %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc dla pakietu %{name}.

%prep
%setup -qc

mkdir build
mkdir apidoc

%build

CLASSPATH=$(build-classpath junit ant)
export CLASSPATH
export SHELL=/bin/sh

%javac -source 1.4 -target 1.4 -d build $(find -name '*.java')
%javadoc -d apidocs $(find -name '*.java')
%jar -cf %{name}-%{version}.jar -C build com

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
