# conditional build
# _without_dist_kernel - without distribution kernel

%define		_orig_name	Device3Dfx

Summary:	Device driver for 3Dfx boards for 2.[0-2] kernels
Summary(pl):	Sterownik DRM do kart 3Dfx
Name:		kernel-video-%{_orig_name}
Version:	2.3
%define _rel	16
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	%{_orig_name}-%{version}.tar.gz
# Source0-md5:	e6f16311addfec8aa7b42260c320de11
Patch0:		%{_orig_name}-Makefile.patch
Icon:		3dfx.gif
%{!?_without_dist_kernel:BuildRequires:	kernel-headers < 2.4.0 }
PreReq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Obsoletes:	%{_orig_name}
Exclusivearch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package installs the 3Dfx device driver to allow access to 3Dfx
boards without the user having root privledges. It should work on both
2.0 and 2.1/2.2 kernels and set the MTRR settings correctly.

%description -l pl
Ten pakiet zawiera driver do kart 3Dfx pozwalaj±cy na udostêpnienie
karty bez dawania u¿ytkownikom praw roota. Powinien dzia³aæ z j±drami
2.0 oraz 2.1/2.2 (tak¿e z wieloprocesorowymi 2.1/2.2) i ustawiaæ
prawid³owo MTRR.

%package -n kernel-smp-video-%{_orig_name}
Summary:	Device driver for 3Dfx boards for 2.[0-2] kernels SMP
Summary(pl):	Sterownik DRM do kart 3Dfx dla kerneli SMP
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
PreReq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Obsoletes:	%{_orig_name}

%description -n kernel-smp-video-%{_orig_name}
This package installs the 3Dfx device driver to allow access to 3Dfx
boards without the user having root privledges. It should work on both
2.0 and 2.1/2.2 SMP kernels and set the MTRR settings correctly.

%description -n kernel-smp-video-%{_orig_name} -l pl
Ten pakiet zawiera driver do kart 3Dfx pozwalaj±cy na udostêpnienie
karty bez dawania u¿ytkownikom praw roota. Powinien dzia³aæ z j±drami
2.0 oraz wieloprocesorowymi (SMP) 2.1/2.2 i ustawiaæ prawid³owo MTRR.

%prep
%setup -c -q
%patch -p1

%build
%{__cc} -I%{_kernelsrcdir}/include -D__KERNEL_SMP=1 -o kinfo kinfo.c
ln -sf /bin/true grep
( PATH=.:$PATH %{__make} 3dfx.o \
	ARCH="%{arch}" \
	CFLAGS="-DMODULE -D__KERNEL__ -D__KERNEL_SMP=1 %{rpmcflags} \
	-fomit-frame-pointer -I%{_kernelsrcdir}/include \
	-fno-strength-reduce -fno-strict-aliasing" )
mv -f 3dfx.o 3dfx.o-smp

( PATH=.:$PATH %{__make} clean )
%{__cc} -I%{_kernelsrcdir}/include -o kinfo kinfo.c
ln -sf /bin/true grep
( PATH=.:$PATH %{__make} 3dfx.o \
	ARCH="%{arch}" \
	CFLAGS="-DMODULE -D__KERNEL__ %{rpmcflags} \
	-fomit-frame-pointer -I%{_kernelsrcdir}/include \
	-fno-strength-reduce -fno-strict-aliasing" )

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc

install 3dfx.o-smp $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/3dfx.o
install 3dfx.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/3dfx.o

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%post -n kernel-smp-video-%{_orig_name}
/sbin/depmod -a

%postun -n kernel-smp-video-%{_orig_name}
/sbin/depmod -a

%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*

%files -n kernel-smp-video-%{_orig_name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/*
