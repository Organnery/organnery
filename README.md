# organnery

Organnery is a linux image for an autonomous organ console on a Raspberry Pi

## build instructions

To generate the debian package:

```
$ apt install dh-systemd
$ dpkg-buildpackage -aarmhf -I.git -uc -us
```
