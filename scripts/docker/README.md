copyparty is availabe in these repos:
* https://hub.docker.com/u/copyparty
* https://github.com/9001?tab=packages&repo_name=copyparty


# getting started

run this command to grab the latest copyparty image and start it:
```bash
docker run --rm -it -u 1000 -p 3923:3923 -v /mnt/nas:/w -v $PWD/cfgdir:/cfg copyparty/ac
```

* `/w` is the path inside the container that gets shared by default, so mount one or more folders to share below there
* `/cfg` is an optional folder with zero or more config files (*.conf) to load
* `copyparty/ac` is the recommended [image edition](#editions)
* you can download the image from github instead by replacing `copyparty/ac` with `ghcr.io/9001/copyparty-ac`
* if you are using rootless podman, remove `-u 1000`
* if you have selinux, append `:z` to all `-v` args (for example `-v /mnt/nas:/w:z`)

this example is also available as a podman-compatible [docker-compose yaml](https://github.com/9001/copyparty/blob/hovudstraum/docs/examples/docker/basic-docker-compose); example usage: `docker-compose up` (you may need to `systemctl enable --now podman.socket` or similar)

i'm not very familiar with containers, so let me know if this section could be better 🙏


## portainer

* there is a [portainer howto](https://github.com/9001/copyparty/blob/hovudstraum/docs/examples/docker/portainer.md) which is mostly untested


## configuration

> this section basically explains how the [docker-compose yaml](https://github.com/9001/copyparty/blob/hovudstraum/docs/examples/docker/basic-docker-compose) works, so you may look there instead

the container has the same default config as the sfx and the pypi module, meaning it will listen on port 3923 and share the "current folder" (`/w` inside the container) as read-write for anyone

the recommended way to configure copyparty inside a container is to mount a folder which has one or more [config files](https://github.com/9001/copyparty/blob/hovudstraum/docs/example.conf) inside; `-v /your/config/folder:/cfg`

* but you can also provide arguments to the docker command if you prefer that
* config files must be named `something.conf` to get picked up

also see [docker-specific recommendations](#docker-specific-recommendations)


## editions

with image size after installation and when gzipped

* [`min`](https://hub.docker.com/r/copyparty/min) (57 MiB, 20 gz) is just copyparty itself
* [`im`](https://hub.docker.com/r/copyparty/im) (70 MiB, 25 gz) can thumbnail images with pillow, parse media files with mutagen
* [`ac` (163 MiB, 56 gz)](https://hub.docker.com/r/copyparty/ac) is `im` plus ffmpeg for video/audio thumbs + audio transcoding + better tags
* [`iv`](https://hub.docker.com/r/copyparty/iv) (211 MiB, 73 gz) is `ac` plus vips for faster heif / avic / jxl thumbnails
* [`dj`](https://hub.docker.com/r/copyparty/dj) (309 MiB, 104 gz) is `iv` plus beatroot/keyfinder to detect musical keys and bpm

[`ac` is recommended](https://hub.docker.com/r/copyparty/ac) since the additional features available in `iv` and `dj` are rarely useful

most editions support `x86`, `x86_64`, `armhf`, `aarch64`, `ppc64le`, `s390x`
* `dj` doesn't run on `ppc64le`, `s390x`, `armhf`
* `iv` doesn't run on `ppc64le`, `s390x`


## detecting bpm and musical key

the `dj` edition comes with `keyfinder` and `beatroot` which can be used to detect music bpm and musical keys

enable them globally in a config file:
```yaml
[global]
e2dsa, e2ts  # enable filesystem indexing and multimedia indexing
mtp: .bpm=f,t30,/mtag/audio-bpm.py  # should take ~10sec
mtp: key=f,t190,/mtag/audio-key.py  # should take ~50sec
```

or enable them for just one volume,
```yaml
[/music]  # share name / URL
  music   # filesystem path inside the docker volume `/w`
  flags:
    e2dsa, e2ts
    mtp: .bpm=f,t30,/mtag/audio-bpm.py
    mtp: key=f,t190,/mtag/audio-key.py
```

or using commandline arguments,
```
-e2dsa -e2ts -mtp .bpm=f,t30,/mtag/audio-bpm.py -mtp key=f,t190,/mtag/audio-key.py
```


# faq

the following advice is best-effort and not guaranteed to be entirely correct

* q: starting a rootless container on debian 12 fails with `failed to register layer: lsetxattr user.overlay.impure /etc: operation not supported`
  * a: docker's default rootless configuration on debian is to use the overlay2 storage driver; this does not work. Your options are to replace docker with podman (good choice), or to configure docker to use the `fuse-overlayfs` storage driver



# docker-specific recommendations

* copyparty will generally create a `.hist` folder at the top of each volume, which contains the filesystem index, thumbnails and such. For performance reasons, but also just to keep things tidy, it might be convenient to store these inside the config folder instead. Add the line `hist: /cfg/hists/` inside the `[global]` section of your `copyparty.conf` to do this


## enabling the ftp server

...is tricky because ftp is a weird protocol and docker is making it worse 🎉

add the following three config entries into the `[global]` section of your `copyparty.conf`:

* `ftp: 3921` to enable the service, listening for connections on port 3921

* `ftp-nat: 127.0.0.1` but replace `127.0.0.1` with the actual external IP of your server; the clients will only be able to connect to this IP, even if the server has multiple IPs

* `ftp-pr: 12000-12099` to restrict the [passive-mode](http://slacksite.com/other/ftp.html#passive) port selection range; this allows up to 100 simultaneous file transfers

then finally update your docker config so that the port-range you specified (12000-12099) is exposed to the internet


# build the images yourself

basically `./make.sh hclean pull img push` but see [devnotes.md](./devnotes.md)
