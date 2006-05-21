%define section free

Summary:	Extract class/interface/method definitions from sources
Summary(pl):	Wyci±ganie definicji klas/interfejsów/metod ze ¼róde³
Name:		qdox
Version:	1.5
Release:	2
Epoch:		0
License:	Apache-style Software License
Group:		Development/Languages/Java
# cvs -d:pserver:anonymous@cvs.qdox.codehaus.org:/home/projects/qdox/scm login
# cvs -z3 -d:pserver:anonymous@cvs.qdox.codehaus.org:/home/projects/qdox/scm export -r QDOX_1_5 qdox
Source0:	%{name}-%{version}-src.tar.gz
Source1:	pom-maven2jpp-depcat.xsl
Source2:	pom-maven2jpp-newdepmap.xsl
Source3:	pom-maven2jpp-mapdeps.xsl
Source4:	%{name}-%{version}-jpp-depmap.xml
Source5:	%{name}-LocatedDef.java
Patch0:		%{name}-1.5-parser_y.patch
URL:		http://qdox.codehaus.org/
BuildRequires:	ant >= 1.6
BuildRequires:	byaccj
BuildRequires:	jflex
BuildRequires:	jmock >= 1.0
BuildRequires:	junit >= 3.8.1
BuildRequires:	maven
BuildRequires:	mockobjects >= 0.09
#BuildRequires:	rpm-javaprov
BuildRequires:	saxon
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
QDox is a high speed, small footprint parser for extracting
class/interface/method definitions from source files complete with
JavaDoc @tags. It is designed to be used by active code generators or
documentation tools.

%description -l pl
QDox to bardzo szybki i o niewielkim narzucie analizator do wyci±gania
definicji klas/interfejsów/metod z plików ¼ród³owych uzupe³nionych
znacznikami @ JavaDoc. Jest zaprojektowany do u¿ywania z aktywnymi
generatorami kodu i narzêdziami do tworzenia dokumentacji.

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl):	Dokumentacja javadoc dla pakietu %{name}
Group:		Documentation

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl
Dokumentacja javadoc dla pakietu %{name}.

%prep
%setup -q -n %{name}
cp %{SOURCE5} src/java/com/thoughtworks/qdox/parser/structs/LocatedDef.java
%patch0

%build
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

for p in $(find . -name project.properties); do
	echo >> $p
echo maven.repo.remote=file:%{_datadir}/maven-1.0/repository >> $p
	echo maven.home.local=$(pwd)/.maven >> $p
done

mkdir -p .maven/repository/maven/jars
build-jar-repository .maven/repository/maven/jars maven-jelly-tags

mkdir -p .maven/repository/JPP/jars
build-jar-repository -s -p .maven/repository/JPP/jars \
ant \
jmock \
junit \

rm -rf bootstrap/*
build-jar-repository -s -p bootstrap jflex
maven -Dqdox.byaccj.executable=byaccj \
	jar javadoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p target/%{name}-%{version}.jar \
      $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr target/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
	rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(644,root,root,755)
%doc LICENSE.txt
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar

%files javadoc
%defattr(644,root,root,755)
%doc %{_javadocdir}/*
