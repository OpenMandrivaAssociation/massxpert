Name:		massxpert
Version:	2.1.1
Release:	%mkrel 1
Summary:	Linear polymer mass spectrometry software
Group:		Sciences/Chemistry
License:	GPLv3
Url:		http://massxpert.org/
Source0:	http://download.tuxfamily.org/massxpert/source/%{name}-%{version}.tar.gz
Patch0:		%{name}-2.1.0-mdv-fix-linkage.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	qt4-devel
BuildRequires:	cmake
BuildRequires:	freetype2-devel
BuildRequires:	tetex-latex
BuildRequires:	desktop-file-utils

Requires:	%{name}-data = %{version}
Suggests:	%{name}-doc
Obsoletes:	polyxmass <= 0.9.7
Obsoletes:	polyxmass-common <= 0.8.7
Obsoletes:	%{mklibname polyxmass 11} <= 0.9.1
Obsoletes:	%{mklibname polyxmass 11 -d} <= 0.9.1

%description
Massxpert is a software environment for polymer chemistry modelling 
and simulation/analysis of mass spectrometric data.

It is the successor of GNU polyxmass.

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}*.xpm
%{_mandir}/man1/%{name}.1*

#-------------------------------------------------------------------------

%package data
Summary:	Data for massxpert
Group:		Sciences/Chemistry

Obsoletes:	polyxmass-data <= 0.8.7

%description data
This package contains the data files for %{name}.

%files data
%defattr(-,root,root,-)
%{_datadir}/%{name}
%{_mandir}/man7/%{name}-data.7*

#-------------------------------------------------------------------------

%package doc
Summary:	Documentation for %{name}
Group:		Sciences/Chemistry

Obsoletes:	polyxmass-doc <= 0.9.0

%description doc
This package contains the pdf manual for %{name}.

%files doc
%defattr(-,root,root,-)
%doc build/usermanual/%{name}.pdf
%{_mandir}/man7/%{name}-doc.7*

#-------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p1 -b .linkage

%build
%cmake_qt4 -DBUILD_ALL=1
%make

%install
rm -rf %{buildroot}
%makeinstall_std -C build

# icon
install -d %{buildroot}%{_datadir}/pixmaps
install -D -m 0644 gui/images/%{name}-icon-32.xpm %{buildroot}%{_datadir}/pixmaps

# fix desktop file
sed -i -e 's:%{name}-icon-32.xpm:%{name}-icon-32:' %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-install	--remove-category=Education \
			--remove-category=Physics \
			--remove-category=Biology \
			--dir %{buildroot}%{_datadir}/applications \
			%{buildroot}%{_datadir}/applications/%{name}.desktop

# drop the installed doc
# GPLv3 license text not needed and manual relocated in the doc subpackage
rm -rf %{buildroot}%{_defaultdocdir}/%{name}

%clean
rm -rf %{buildroot}
