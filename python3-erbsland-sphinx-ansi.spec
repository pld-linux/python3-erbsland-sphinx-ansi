#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

Summary:	Sphinx extension to format ANSI colored/formated terminal output
Summary(pl.UTF-8):	Rozszerzenie Sphinksa do formatowania wyjścia terminalowego z kolorami ANSI i formatowaniem
Name:		python3-erbsland-sphinx-ansi
Version:	1.1.0
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/erbsland-sphinx-ansi/
Source0:	https://files.pythonhosted.org/packages/source/e/erbsland-sphinx-ansi/erbsland_sphinx_ansi-%{version}.tar.gz
# Source0-md5:	8067db3b3727d26c462d81d3f86cdcd9
URL:		https://pypi.org/project/erbsland-sphinx-ansi/
BuildRequires:	python3-build
BuildRequires:	python3-hatch-vcs
BuildRequires:	python3-hatchling
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.10
%if %{with tests}
BuildRequires:	python3-pytest >= 8.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-sphinx_copybutton
BuildRequires:	python3-sphinx_design
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.10
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
erbsland-sphinx-ansi is a lightweight Sphinx extension that renders
ANSI-colored and formatted terminal output directly in your
documentation.

It is useful for command-line tools, build logs, and interactive
sessions where terminal colors improve readability.

%description -l pl.UTF-8
erbsland-sphinx-ansi to lekkie rozszerzenie Sphinksa, renderujące
wyjście terminalowe z kolorami ANSI i formatowaniem bezpośrednio w
dokumentacji.

Jest przydatne dla narzędzi linii poleceń, logów budowania czy
secji interaktywnych, gdzie kolory na terminalu poprawiają czytelność.

%package apidocs
Summary:	API documentation for Python erbsland-sphinx-ansi module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona erbsland-sphinx-ansi
Group:		Documentation

%description apidocs
API documentation for Python erbsland-sphinx-ansi module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona erbsland-sphinx-ansi.

%prep
%setup -q -n erbsland_sphinx_ansi-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3 \
	SOURCEDIR=.
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%dir %{py3_sitescriptdir}/erbsland
%dir %{py3_sitescriptdir}/erbsland/sphinx
%{py3_sitescriptdir}/erbsland/sphinx/ansi
%{py3_sitescriptdir}/erbsland_sphinx_ansi-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/build/html/{_sphinx_design_static,_static,contribute,*.html,*.js}
%endif
