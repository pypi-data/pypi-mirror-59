# Fedora Checksum Tester

**Fedora Checksum Tester** is a little script that can automatically run checksum
tests as defined in https://fedoraproject.org/wiki/QA:Testcase_Mediakit_Checksums.

## Installation

The program is packed for PyPi, so you can install it easily using the **pip** 
command.

`pip install --user fedora_checksum_tester`

## Usage

Navigate into the directory where you have downloaded the images to check and
run `fedora_checksum_tester` with those options. If you have not downloaded any 
images to check, the program downloads the images automatically from Koji.

## Options

**--release** : The release number of the Fedora compose, for which you want
to download the images. *Rawhide* is used by default.

**--compose** : The compose identification. Mostly, this is a date in the form of
YYYYMMDD except for the release candidates. If left out, the program connects to
the release validation matrix and gets the number of the current compose. This is
probably how this program will be used mostly.

**--arch** : Architecture for which to download the images. *x86_64* used by default.

**--variant** : One possible variant, such as *Cloud*, *Everything*, *Server*, 
*Spins*, *Workstation*. If not chosen, the **Everything** will be used as default.

**--subvariant** : Can be used with **Spins variant**, to distinguish between
various spins, such as *KDE*, *LXCD*, *Xfce*. If left out, all spins will be 
tested.

**--type** : Can be used with **Server** to distinguish between *boot* and *dvd*. If
not selected, both images will be checked.

**--purge** : If set to *True*, all downloaded images will be deleted after the test 
has finished, independently of the result.

**--forcedownload** : Not yet implemented. Normally, if the script finds out
that the requested image has already been downloaded, it will not download it again 
to save time and bandwidth. If you explicitely want to download it anyway, use *True* 
to download the image.

**--report** : If this is set to *True*, the script will report the results to the
Wiki matrix automatically. Also see **--user**.

**--user** : The name of the user who reports the results. If left out, user *donkey*
will be used.

## Bugs

If you find a bug, report an issue at https://github.com/lruzicka/checksum-tester.

