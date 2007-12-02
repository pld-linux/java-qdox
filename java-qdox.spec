#
# TODO: 1.6.x from http://repository.codehaus.org/com/thoughtworks/qdox/qdox/
#
# Conditional build:
%bcond_with	maven		# use maven or straight ant for build
#
%include	/usr/lib/rpm/macros.java
Summary:	Extract class/interface/method definitions from sources
Summary(pl.UTF-8):	Wyciąganie definicji klas/interfejsów/metod ze źródeł
Name:		qdox
Version:	1.5
Release:	3
Epoch:		0
License:	Apache-style Software License
Group:		Development/Languages/Java
Source0:	http://repo1.maven.org/maven2/qdox/qdox/1.5/%{name}-%{version}-src.tar.gz
# Source0-md5:	501f05c8ac26efe5e0b64e51e894f788
#Source1:	pom-maven2jpp-depcat.xsl
#Source2:	pom-maven2jpp-newdepmap.xsl
#Source3:	pom-maven2jpp-mapdeps.xsl
#Source4:	%{name}-%{version}-jpp-depmap.xml
Source5:	%{name}-LocatedDef.java
Source6:	%{name}-build.xml
Patch0:		%{name}-project_xml.patch
Patch1:		%{name}-parser_y.patch
Patch2:		%{name}-yy_lexical_state.patch
URL:		http://qdox.codehaus.org/
BuildRequires:	ant >= 1.6
BuildRequires:	ant-junit
BuildRequires:	byaccj
BuildRequires:	jflex
BuildRequires:	jpackage-utils
BuildRequires:	junit >= 3.8.1
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	sed >= 4.0
%if %{with maven}
BuildRequires:	jmock >= 0:1.0
BuildRequires:	maven >= 0:1.1
BuildRequires:	mockobjects >= 0:0.09
BuildRequires:	saxon
%endif
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
%setup -q
find '(' -name '*.xml' -o -name '*.java' -o -name '*.flex' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'
cp %{SOURCE5} src/java/com/thoughtworks/qdox/parser/structs/LocatedDef.java
cp %{SOURCE6} build.xml
%patch0 -p0
%patch1 -p0
%patch2 -p1

%build
%if %{with maven}
export DEPCAT=$(pwd)/qdox-1.5-depcat.new.xml
echo '<?xml version="1.0" standalone="yes"?>' > $DEPCAT
echo '<depset>' >> $DEPCAT
for p in $(find . -name project.xml); do
	cd $(dirname $p)
	%{_bindir}/saxon project.xml %{SOURCE1} >> $DEPCAT
	cd -
done
echo >> $DEPCAT
echo '</depset>' >> $DEPCAT
%{_bindir}/saxon $DEPCAT %{SOURCE2} > qdox-1.5-depmap.new.xml
for p in $(find . -name project.xml); do
	cd $(dirname $p)
	cp project.xml project.xml.orig
	%{_bindir}/saxon -o project.xml project.xml.orig %{SOURCE3} map=%{SOURCE4}
	cd -
done

export MAVEN_HOME_LOCAL=$(pwd)/.maven

maven \
-Dmaven.repo.remote=file:%{_datadir}/maven/repository \
	-Dmaven.home.local=$MAVEN_HOME_LOCAL \
	-Dqdox.byaccj.executable=byaccj \
	jar javadoc
%else

mkdir -p target/src/java/com/thoughtworks/qdox/parser/impl
export CLASSPATH=$(build-classpath jflex)

%java JFlex.Main \
	-d target/src/java/com/thoughtworks/qdox/parser/impl \
	src/grammar/lexer.flex

cd target
byaccj \
	-Jnorun \
	-Jnoconstruct \
	-Jclass=Parser \
	-Jsemantic=Value \
	-Jpackage=com.thoughtworks.qdox.parser.impl \
	../src/grammar/parser.y
cd -

mv target/Parser.java target/src/java/com/thoughtworks/qdox/parser/impl
%ant jar javadoc \
	-Dnoget=1 \
	-Dbuild.sysclasspath=only
%endif

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a target/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a target/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc LICENSE.txt
%{_javadir}/*.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
