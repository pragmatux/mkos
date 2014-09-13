% MKOS(1) | Pragmatux Users Manual
% Ryan Kuester

# NAME

mkos - make an OS filesystem from packages and their dependencies

# SYNOPSIS

mkos [OPTION]... [PACKAGE_NAME]...

# DESCRIPTION

Make an operating system filesystem or filesystem image from a tree of
packages defined by the package names passed on the command line and
their dependencies, computed recursively (a "package tree").

The defaults produce a generic Pragmatux operating system in ./ptux.tgz
for the architecture of the workstation. mkos is commonly wrapped in a
script mkos-$device which creates an output image befitting the
target hardware platform, specifying an appropriate package tree
and, potentially, project-specific package sources.

mkos must run with root privlidges. `fakeroot`(1) is sufficient unless
the option --configure is used, in which case real root is required.

This program is part of [Pragmatux](http://pragmatux.org).

# OPTIONS

*PACKAGE_NAME*...
:	Names of the packages to include in the output repository.
	Dependencies of the named packages, computed recursively, are
	included as well. The default is device-$arch, where $arch is
	the debian architecture of the build machine given by
	`dpkg-architecture`(1).

--create-directory *DIRNAME*, -d *DIRNAME*:
:	Create the operating filesystem in the directory *DIRNAME*.

--create-initramfs *FILE*, -i *FILE*:
:	Create the operating filesystem in cpio archive *FILE* in a
	manner compatible with being used as an initramfs.

--copy-kernel *FILE*, -k *FILE*:
:	Copy the kernel (/boot/vmlinuz) from the target operating
	system, after composition, to *FILE*.

--sources *FILE*, -s *FILE*:
:	Download the needed packages from the package sources given in
	*FILE*, an .ini format file described below. The default sources
	are the official Pragmatux and Debian device repositories, see
	--print-default-sources.

--print-default-sources, -S:
:	Print the default package sources to stdout and exit. The output
	is in the same .ini format understood by the --sources argument.
	Append source sections of your own to this output to create
	--sources files which augment the default package sources.

--preferences *FILE*, -p *FILE*:
:	Use *FILE* as an `apt_preferences`(5) file to control the
	selection of packages. The default preferences prefer packages
	from repositories with the label "Pragmatux" over other
	repositories. This causes mkos to choose packages from the
	official Pragmatux repository or other repositories created with
	Pragmatux tools ahead of those in the official Debian repository
	should the same package be available from multiple sources.
	Ordinarily, the package with the greatest version would be
	chosen.

--print-default-preferences, -P:
:	Print the default preferences to stdout and exit. The output is
	in the same format understood by the --preferences argument.
	Append preferences paragraphs of your own to this output to
	create --preferences files which augment the default
	preferences.

--configure:
:	Configure the packages in the operating system before finalizing
	the output. Configuring only possible when the workstation and
	device architectures match, since package maintainer scripts may
	execute architecture-dependant binaries. The package
	`dpkg-autoconfigure` must be installed in the device operating
	system, as mkos invokes it to perform the configuration. Note
	that package maintainer scripts may operate differently than
	they would have if run the device, e.g., mistakenly saving some
	hardware-dependent value from the workstation in a device a
	configuration file. 

# SOURCES FORMAT

The sources file passed to --sources is an .ini format file giving the
URI, distribution name, and components for each package source -- the
same basic information in a `sources.list`(5) file, formatted
differently. The file is actually the package source sections of a
`multistrap`(1) configuration file.

Imitate the following example, which specifies two package sources.
Specify as many sources as necessary, but each must be given a unique
nickname in the section title (between the brackets).

	[ptux]
	source=http://packages.pragmatux.org/device
	suite=3.0
	components=main

	[debian]
	source=http://cdn.debian.net/debian
	suite=wheezy
	components=main

# EXAMPLES

To build the an OS filesystem for the ifc6410 platform:

	$ fakeroot mkos --arch armhf device-ifc6410

To build the an OS filesystem for the ifc6410 platform using packages
from a a local package repository in addition to the default sources:

	$ mkos -S >mysources
	$ cat >>mysources <<EOF
	  [local]
	  source=copy:///home/rkuester/development-ppa
	  suite=master
	  components=main
	  EOF
	$ fakeroot mkos --arch armhf --sources mysources device-ifc6410

# SEE ALSO

`multistrap`(1)

# BUGS

The heavy lifting is implemented by `multistrap`(1) and its error
messages may be slightly out of context when passed through by mkos.
