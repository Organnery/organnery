# organnery

Organnery is a GNU/Linux image for an autonomous organ console on a Raspberry Pi. 

This repository contains the custom scripts which set up the instrument. This code is installed via a Debian package as one part of the [organnery-distro](https://git.audiotronic.fr/64Studio/organnery-distro) project.

## build instructions

To generate the Debian package:

```
$ apt install dh-systemd
$ dpkg-buildpackage -aarmhf -I.git -uc -us
```
