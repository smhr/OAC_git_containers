Basics
======

Prerequisites
-------------

1)  Install Docker on your laptop:

> - [Mac](https://docs.docker.com/desktop/mac/)
> -   [Windows](https://docs.docker.com/desktop/windows//)
> -   [Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

To check if the installation was successful, open up your favorite
Terminal (Mac,Linux) or the Docker Terminal (Windows) and try running

```bash
docker version
```
```console
Client: Docker Engine - Community
 Version:           20.10.12
 API version:       1.41
 Go version:        go1.16.12
 Git commit:        e91ed57
 Built:             Mon Dec 13 11:45:41 2021
 OS/Arch:           linux/amd64
 Context:           default
 Experimental:      true

Server: Docker Engine - Community
 Engine:
  Version:          20.10.12
  API version:      1.41 (minimum version 1.12)
  Go version:       go1.16.12
  Git commit:       459d0df
  Built:            Mon Dec 13 11:44:05 2021
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.4.12
  GitCommit:        7b11cfaabd73bb80907dd23182b9347b4245eb5d
 runc:
  Version:          1.0.2
  GitCommit:        v1.0.2-0-g52b36a2
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
```



If you do not have Docker installed on your laptop, you could also use [play-with-docker](https://labs.play-with-docker.com/):

2)  Create a [Docker Hub account](https://hub.docker.com/signup/)

Having a Docker Hub account makes it easier to share your containers
with other researchers. Use the Docker CLI to login to Docker Hub to be
able to push images to your repository:

```bash
docker login
```
```console
(Enter username/password)
```

**Exercise:** While everyone gets set up, take a few minutes to run `docker --help`
and a few examples of `docker <verb> --help` to make sure you can find
and read the help text.

Working with Images from Docker Hub
-----------------------------------

To introduce ourselves to some of the most essential Docker commands, we
will go through the process of listing images that are currently
available on our local machines, and we will pull a \'hello-world\'
image from Docker Hub. Then we will run the \'hello-world\' image to see
what happens.

List images on your local machine with the `docker images` command. This
peaks into the Docker daemon, which is shared by all users on this
system, to see which images are available, when they were created, and
how large they are:

```bash
docker images
```
```console
REPOSITORY           TAG                 IMAGE ID       CREATED        SIZE
ubuntu               18.04               6ad7e71ba7d    2 days ago     63.2MB
```
**Note:** If this is your first time using Docker, you may not have any images stored on your local machine.

Pull an image from Docker hub with the `docker pull` command. This looks
through the Docker Hub registry and downloads the \'latest\' version of
that image:

```bash
docker pull hello-world
```
```console
Using default tag: latest
latest: Pulling from library/hello-world
2db29710123e: Pull complete
Digest: sha256:10d7d58d5ebd2a652f4d93fdd86da8f265f5318c6a73cc5b6a9798ff6d2b2e67
Status: Downloaded newer image for hello-world:latest
docker.io/library/hello-world:latest
```

Run the image we just pulled with the `docker run` command. In this
case, running the container will execute a simple shell script inside
the container that has been configured as the \'default command\' when
the image was built:

```bash
docker run hello-world
```
```console
Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

Verify that the image you just pulled is now available on your local
machine:

```bash
docker images
```
```console
REPOSITORY           TAG                 IMAGE ID       CREATED        SIZE
ubuntu               18.04               6ad7e71ba7d    2 days ago     63.2MB
hello-world          latest              feb5d9fea6a5   7 months ago   13.3kB
```

Check to see if any containers are still running using `docker ps`:

```bash
docker ps
```
```console
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

**Exercise:** The command `docker ps` shows only currently running containers. Pull up
the help text for that command and figure out how to show all
containers, not just currently running containers.

**Exercise:** Closely inspect metadata for your downloaded image(s) using the
`docker inspect` command:

```bash
docker inspect hello-world
```
```console
[
    {
        "Id": "sha256:feb5d9fea6a5e9606aa995e879d862b825965ba48de054caab5ef356dc6b3412",
        "RepoTags": [
            "hello-world:latest"
...
```

#### Docker Core Commands

| Command        | Usage                                                        |
| -------------- | ------------------------------------------------------------ |
| docker login   | Authenticate to Docker Hub using username and  password      |
| docker images  | List images on the local machine                             |
| docker ps      | List containers on the local machine                         |
| docker pull    | Download an image from Docker Hub                            |
| docker run     | Run an instance of an image (a container)                    |
| docker inspect | Provide detailed information on Docker objects               |
| docker rmi     | Delete an image                                              |
| docker rm      | Delete a container                                           |
| docker stop    | Stop a container                                             |
| docker build   | Build a docker image from a Dockerfile in the  current working directory |
| docker tag     | Add a new tag to an image                                    |
| docker push    | Upload an image to Docker Hub                                |


#### Additional Resources

The command line tools are very well documented:

```bash
docker --help
```
```console
shows all docker options and summaries
```

```bash
docker COMMAND --help
```
```console
shows options and summaries for a particular command
```

-   [Official Docker Documentation](https://docs.docker.com/get-started/)

