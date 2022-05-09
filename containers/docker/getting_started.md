Docker hands-on
===========================

Let’s create our first container from an existing image. We do this with the image `ubuntu`, generating an environment with a minimal installation of ubuntu. We first pull it:

```sh
sudo docker pull ubuntu
```
```console
Using default tag: latest
latest: Pulling from library/ubuntu
125a6e411906: Pull complete 
Digest: sha256:26c68657ccce2cb0a31b330cb0be2b5e108d467f641c62e13ab40cbec258c68d
Status: Downloaded newer image for ubuntu:latest
docker.io/library/ubuntu:latest
```

Now, we request an interactive shell into the created container:

```sh
sudo docker run -it ubuntu
```

This interactivity was invoked by the options `-i` and `-t`).

#### Question

Check out the operating system of the container by typing `cat /etc/os-release` in the container’s shell. Are we really in an ubuntu environment? Run the command `whoami` in the docker container. Who are you?

List all containers:

```sh
sudo docker container ls -a
```

Now let's install some software in our `ubuntu` environment. We'll install some simple software called [`figlet`](http://www.figlet.org/). Type into the container shell:

```sh
apt-get update
apt-get install figlet
```

Now, let's try it out. Type into the container shell:

```sh
figlet "Salam from inside!"
```

Now you have installed and used software `figlet` in an `ubuntu` environment (almost) completely separated from your host computer. This already gives you an idea of the power of containerization.

Exit the shell by typing `exit`.




