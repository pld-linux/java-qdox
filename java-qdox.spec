# TODO:
# - 1.12 was available but disappeared
# - tests

%bcond_without	javadoc	# don't build apidocs


%define		srcname	qdox
Summary:	Extract class/interface/method definitions from sources
Summary(pl.UTF-8):	Wyciąganie definicji klas/interfejsów/metod ze źródeł
Name:		java-qdox
Version:	1.11
Release:	1
License:	Apache v2.0
Group:		Libraries/Java
#Source0Download: http://qdox.codehaus.org/download.html
Source0:	http://repository.codehaus.org/com/thoughtworks/qdox/qdox/%{version}/%{srcname}-%{version}-sources.jar
# Source0-md5:	acb16e9037242322155631a32dba8661
URL:		http://qdox.codehaus.org/
# It don't use ant as build system, but it links with ant
BuildRequires:	ant
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.555
BuildConflicts:	java-gcj-compat-devel
Obsoletes:	qdox
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
QDox is a high speed, small footprint parser for extracting
class/interface/method definitions from source files complete with
JavaDoc @tags. It is designed to be used by active code generators or
documentation tools.

%description -l pl.UTF-8
QDox to bardzo szybki i mający niewielki narzut analizator do
wyciągania definicji klas/interfejsów/metod z plików źródłowych
uzupełnionych znacznikami @ JavaDoc. Jest zaprojektowany do używania z
aktywnymi generatorami kodu i narzędziami do tworzenia dokumentacji.

%package javadoc
Summary:	Javadoc for QDox
Summary(pl.UTF-8):	Dokumentacja javadoc dla pakietu QDox
Group:		Documentation
Requires:	jpackage-utils
Obsoletes:	qdox-javadoc

%description javadoc
Javadoc for QDox.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc dla pakietu QDox.

%package source
Summary:	Source code of QDox
Summary(pl.UTF-8):	Kod źródłowy narzędzia QDox
Group:		Documentation

%description source
Source code of QDox.

%description source -l pl.UTF-8
Kod źródłowy narzędzia QDox.

%prep
%setup -qc

%build

CLASSPATH=$(build-classpath ant)

install -d build

%javac \
	-classpath "$CLASSPATH" \
	-source 1.4 \
	-target 1.4 \
	-d build \
	$(find -name '*.java' | grep -v com/thoughtworks/qdox/junit)

%if %{with javadoc}
%javadoc -d apidocs \
	$(find -name '*.java' | grep -v ^com/thoughtworks/qdox/junit)
%endif

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

# source
install -d $RPM_BUILD_ROOT%{_javasrcdir}
install %{SOURCE0} $RPM_BUILD_ROOT%{_javasrcdir}/%{srcname}.src.jar

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%{_javadir}/qdox-%{version}.jar
%{_javadir}/qdox.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}

%files source
%defattr(644,root,root,755)
%{_javasrcdir}/%{srcname}.src.jar
