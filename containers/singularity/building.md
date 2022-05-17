# Building a Basic Container

In this section, we will build a brand new container.

To build a singularity container, you must use the `build` command.  The `build` command installs an OS, sets up your container's environment and installs the apps you need.  To use the `build` command, we need a definition file. A [Singularity definition file](https://sylabs.io/guides/3.8/user-guide/definition_files.html) is a set of instructions telling Singularity what software to install in the container.

We are going to use a standard development cycle (sometimes referred to as Singularity flow) to create this container. It consists of the following steps:

- create a writable container (called a `sandbox`)
- shell into the container with the `--writable` option and tinker with it interactively
- record changes that we like in our definition file
- rebuild the container from the definition file if we break it
- rinse and repeat until we are happy with the result
- rebuild the container from the final definition file as a read-only singularity image format (SIF) image for use in production

The Singularity source code contains several example definition files in the `/examples` subdirectory.  Let's make a new directory, copy the Debian example definition file, and inspect it.

Let's make a sample definition file.

```singularity
Bootstrap: library
From: ubuntu:20.04

%post
    echo "Hello from inside the container"

%runscript
    echo "This is what happens when you run the container..."
```

Here, we use the `ubuntu` image from [Sylab cloud](https://cloud.sylabs.io/) as a base. We could also use an `ubuntu` or `Debian` mirror URL.

## Developing a new container

Now let's use this definition file as a starting point to build our `lolcow.img` container. Note that the build command requires `sudo` privileges. (We'll discuss some ways around this restriction later in the class.)

```
$ sudo singularity build --sandbox pi pi.def
```

This is telling Singularity to build a container called `pi` from the `pi.def` definition file. The `--sandbox` option in the command above tells Singularity that we want to build a special type of container (called a sandbox) for development purposes. 

Singularity can build containers in several different file formats. The default is to build a SIF (singularity image format) container that uses [squashfs](https://en.wikipedia.org/wiki/SquashFS) for the file system. SIF files are compressed and immutable making them the best choice for reproducible, production-grade containers.

But if you want to shell into a container and tinker with it (like we will do here), you should build a sandbox (which is really just a directory).  This is great when you are still developing your container and don't yet know what to include in the definition file.

When your build finishes, you will have a basic Ubuntu container saved in a local directory called `pi`.

## Using `shell --writable` to explore and modify containers

Now let's enter our new container and look around.

```console
$ singularity shell --writable pi
```

Note the `--writable` option allows us to modify the container.  The changes will actually be saved into the container and will persist across uses.

```
Singularity> sudo apt-get update
bash: sudo: command not found
```

Whoops!

The `sudo` command is not found. But even if we had installed `sudo` into the
container and tried to run this command with it, or change to root using `su`,
we would still find it impossible to elevate our privileges within the
container:

```
Singularity> sudo apt-get update
sudo: effective uid is not 0, is /usr/bin/sudo on a file system with the 'nosuid' option set or an NFS file system without root privileges?
```

Once again, this is an important concept in Singularity. If you enter a container without root privileges, you are unable to obtain root privileges within the container. This insurance against privilege escalation is the reason that you will find Singularity installed in so many HPC environments.

Let's exit the container and re-enter as root.

```
Singularity> exit

$ sudo singularity shell --writable pi
```

Now we are the root user inside the container. Let's try install `wget` and `python` in our container.

```
Singularity> apt-get update && apt-get install -y wget python3
```

Try to run python:

```
Singularity> python3
```

Now, download a simple python script into `/opt` in the container [pi.py](https://raw.githubusercontent.com/smhr/OAC_git_containers/main/containers/codes/pi.py) that calculates the pi number.

```
Singularity> cd /opt && wget -c https://raw.githubusercontent.com/smhr/OAC_git_containers/main/containers/codes/pi.py
```

Calculate the pi number.

```
Singularity> python3 pi.py 10000
```

:ice_cream:


## Building the SIF image from the sandbox directory

We could now build an immutable image from our development directory.

```console
$ sudo singularity build pi-from-dir.sif pi
```

Let's test it.

```console
$ singularity shell pi-from-dir.sif 
```

```
Singularity> cd /opt
Singularity> python3 ./pi.py 10000
```

## Building the final production-grade SIF file

Although it is fine to shell into your Singularity container and make changes while you are debugging, you ultimately want all of these changes to be reflected in your definition file.  Otherwise if you need to reproduce it from scratch you will forget all of the changes you made. You will also want to rebuild you container into something more durable, portable, and robust than a directory.

Let's update our definition file with the changes we made to this container.

```
Singularity> exit

$ vim pi.def
```

Here is what our updated definition file should look like.

```singularity
Bootstrap: library
From: ubuntu:20.04

%post
    apt-get update && apt-get install -y wget python3
    cd /opt && wget https://raw.githubusercontent.com/smhr/OAC_git_containers/main/containers/codes/pi.py
    chmod +x pi.py

%runscript
    echo "The current time is $(date)"
    echo "The pi number with four digits precision:"
    exec pi.py 10000

%environment
    export PATH=$PATH:/opt
```

And build it.

```console
$ sudo singularity build pi.sif pi.def

```

**Exercise:** Try to `shell` into, `execute` the `pi.py` and `run` the image, using

```console
$ singularity shell pi.sif
$ singularity exec pi.sif pi.py 100000
$ singularity run pi.sif
```
Note that we changed the name of the container.  By omitting the `--sandbox` option, we are building our container in the standard Singularity file format (SIF).  We are denoting the file format with the (optional) `.sif` extension.  A SIF file is compressed and immutable making it a good choice for a production environment.

As we saw in the previous section when we used the `inspect` command to read the `runscript`, Singularity stores a lot of [useful metadata](https://sylabs.io/guides/3.8/user-guide/environment_and_metadata.html#container-metadata). For instance, if you want to see the definition file that was used to create the container you can use the `inspect` command like so:

```
$ singularity inspect --deffile  pi.sif
```

## Building from a Mirror URL

We can also use the following header in our definition file to build a container:

```
BootStrap: debootstrap
OSVersion: stable
MirrorURL: http://ftp.us.debian.org/debian/
```

This uses the program [`debootstrap`](https://wiki.debian.org/Debootstrap) to build the root file system using a mirror URL. In this case, we supply a URL that is maintained by Debian. We could also use an Ubuntu URL since it is a derivative of Debian and can also be built with the `debootstrap` program. If we wanted to build a CentOS container from the distribution mirror we could use the `yum` package manager similarly. There are actually a ton of different ways to build containers. See this list of ["bootstrap agents"](https://sylabs.io/guides/3.8/user-guide/appendix.html#build-modules) in the Singularity docs.

In practice, most people do not build containers from a distribution mirror like this. Instead they tend to build containers from existing containers on the Container Library or on Docker Hub and use the `%post` section to modify those containers to suit their needs.  

For instance, to use an existing Debian container from the Container library as your starting point, your header would look like this:


```
BootStrap: library
From: debian
```

Likewise to start from a Debian container on Docker Hub, your header would contain the following:

```
Bootstrap: docker
From: debian
```

## Building from a local image

You can also build a container from a base container on your local file system.

```
Bootstrap: localimage
From: /home/student/debian.sif
```

---
**Note:**

Each of these methods can also be called _without_ providing a definition file using the following shorthand.  For an added bonus, none of these `build` commands require root privileges.

```
$ singularity build debian1.sif library://debian

$ singularity build debian2.sif docker://debian

$ singularity build debian3.sif debian2.sif
```

Behind the scenes, Singularity creates a small definition file for each of these commands and then builds the corresponding container as you can see if you use the `inspect --deffile` command. 
