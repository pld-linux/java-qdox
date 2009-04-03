# TODO:
# - execute tests
# - fix javadoc with java-sun

%bcond_without	javadoc		# build javadoc
%if "%{pld_release}" == "ti"
%bcond_without	java_sun		# build with gcj
%else
%bcond_with	java_sun		# build with java-sun
%endif

%include	/usr/lib/rpm/macros.java

%define		srcname	qdox
Summary:	Extract class/interface/method definitions from sources
Summary(pl.UTF-8):	Wyciąganie definicji klas/interfejsów/metod ze źródeł
Name:		java-qdox
Version:	1.8
Release:	2
License:	Apache v2.0
Group:		Libraries/Java
Source0:	http://repository.codehaus.org/com/thoughtworks/qdox/qdox/%{version}/%{srcname}-%{version}-sources.jar
# Source0-md5:	9cbc745194a39ec27f54bbe16c2342cc
URL:		http://qdox.codehaus.org/
BuildRequires:	ant
%{!?with_java_sun:BuildRequires:	java-gcj-compat-devel}
%{?with_java_sun:BuildRequires:	java-sun}
BuildRequires:	jpackage-utils
BuildRequires:	junit
BuildRequires:  rpm >= 4.4.9-56
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Obsoletes:	qdox
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
Obsoletes:	qdox-javadoc

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc dla pakietu %{name}.

%prep
%setup -qc

%build

CLASSPATH=$(build-classpath junit ant)

install -d build

%javac \
	-classpath $CLASSPATH \
	-source 1.4 \
	-target 1.4 \
	-d build \
	$(find -name '*.java')

%{?with_javadoc:%javadoc -all -d apidocs}
%jar -cf %{srcname}-%{version}.jar -C build com

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

%if %{with javadoc}
# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
