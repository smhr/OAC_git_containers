# Downloading and Interacting with Containers

This section will be useful for container consumers. (i.e. those who really just want to use containers somebody else built.) The next chapter will explore topics more geared toward container producers (i.e. those who want/need to build containers from scratch).

You can find pre-built containers in lots of places. Singularity can convert and run containers in many different formats, including those built by Docker.

In this class, we'll be using containers from:

- [The Singularity Container Library](https://cloud.sylabs.io/library), developed and maintained by [Sylabs](https://sylabs.io/)
- [Docker Hub](https://hub.docker.com/), developed and maintained by [Docker](https://www.docker.com/)

There are lots of other places to find pre-build containers too. Here are some of the more popular ones:

- [Singularity Hub](https://singularity-hub.org/), an early collaboration between Stanford University and the Singularity community
- [Quay.io](https://quay.io/), developed and maintained by Red Hat
- [NGC](https://ngc.nvidia.com/catalog/all?orderBy=modifiedDESC&pageNumber=3&query=&quickFilter=&filters=), developed and maintained by NVIDIA
- [BioContainers](https://biocontainers.pro/#/registry), develped and maintained by the Bioconda group
- Cloud providers like Amazon AWS, Microsoft Azure, and Google cloud also have container registries that can work with Singularity

## Downloading containers

In the last section, we validated our Singularity installation by "running" a container from the Container Library. Let's download that container using the `pull` command.

```console
$ cd ~

$ singularity pull library://smhr/collection/figlet:v1.0
```
List your files.

```console
$ ls figlet_v1.0.sif
figlet_v1.0.sif
```

This is your container. Or more precisely, it is a Singularity Image Format (SIF) file containing an image of a root level filesystem. This image is mounted to your host filesystem (in a new "mount namespace") and then entered when you run a Singularity command.

Note that you can also download images from Docker Hub with the following command:

```
$ singularity pull docker://username/image:tag
```


## Entering containers with `shell`

Now let's enter our new container and look around. We can do so with the `shell` command.

```console
$ singularity shell figlet_v1.0.sif
```

Depending on the environment of your host system you may see your shell prompt change. Let's look at what OS is running inside the container.

```console
$ cat /etc/os-release
NAME="Alpine Linux"
ID=alpine
VERSION_ID=3.14.0
PRETTY_NAME="Alpine Linux v3.14"
HOME_URL="https://alpinelinux.org/"
BUG_REPORT_URL="https://bugs.alpinelinux.org/"
```

No matter what OS is running on your host, your container is running Alpine 3.14!


**NOTE**

In general, the Singularity action commands (like `shell`, `run`, and `exec`) are expected to work with URIs like `library://` and `docker://` the same as they would work with a local image.

Let's try a few more commands:

```
Singularity> whoami
dave

Singularity> hostname
hal-9000
```

This is one of the core features of Singularity that makes it so attractive from a security and usability standpoint. The user remains the same inside and outside of the container.

```
Singularity> which figlet
/usr/bin/figlet

Singularity> figlet salam
           _                 
 ___  __ _| | __ _ _ __ ___  
/ __|/ _` | |/ _` | '_ ` _ \ 
\__ \ (_| | | (_| | | | | | |
|___/\__,_|_|\__,_|_| |_| |_|
```

More on "running" the container in a minute. For now, don't forget to `exit` the container when you are finished playing!

```
Singularity> exit
exit
```

## Executing containerized commands with `exec`

Using the `exec` command, we can run commands within the container from the host system.

```console
$ singularity exec figlet_v1.0.sif figlet 'How did you get out of the container?'
```

In this example, singularity entered the container, ran the `figlet` command with supplied arguments, displayed the standard output on our host system terminal, and then exited.

## "Running" a container with (and without) `run`

You can "run" a container like so:

```console
$ singularity run library://godlovedc/funny/lolcow
INFO:    Using cached image
 ________________________________________
/ Q: What's buried in Grant's tomb? A: A \
\ corpse.                                /
 ----------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

So what actually happens when you run a container? There is a special file within the container called a `runscript` that is executed when a container is run. You can see this (and other meta-data about the container) using the inspect command.

```
$ singularity inspect --runscript lolcow_latest.sif
#!/bin/sh

    fortune | cowsay | lolcat
```
