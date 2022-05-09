Managing containers and images
==============================

#### Restarting an exited container

If you would like to go back to your container with the `figlet` installation, you could try to run again:

```sh
docker run -it ubuntu
```

**Question:** Is your `figlet` installation still there? Why?

To restart a container you can use:

```sh
docker start [CONTAINER NAME]
```

And after that to re-attach to the shell:

```sh
docker attach [CONTAINER NAME]
```

And you're back in the container shell.

#### Note `docker attach` and `docker exec`

In addition to `docker attach`, you can also "re-attach" a container with `docker exec`. However, these two are quite different. While `docker attach` gets you back to your stopped shell process, `docker exec` creates a new one (more information on [stackoverflow](https://stackoverflow.com/questions/30960686/difference-between-docker-attach-and-docker-exec)). The command `docker exec` enables you to have multiple shells open in the same container. That can be convenient if you have one shell open with a program running in the foreground, and another one for e.g. monitoring. 

To see sn example for using `docker exec` on a running container, let's run the `busybox` container ([BusyBox](https://en.wikipedia.org/wiki/BusyBox) is a software suite that provides several Unix utilities in a single executable file.):

```sh
docker run -it busybox
```

If you start another terminal and do

```sh
docker attach [the busybox container_name]
```

you will see these two shells are mirrored. But if you do

```sh
docker exec [the busybox container_name] [command]
```

this will run the `[command]` in another new shell.

#### Creating a new image

You can store your changes and create a new image based on the `ubuntu` image like this:

```sh
docker commit [CONTAINER NAME] ubuntu-figlet
```

**Exercise:** Run the above command with the name of the container containing the `figlet` installation. Check out `docker image ls`. What have we just created?

Now you can generate a new container based on the new image:

```sh
docker run -it ubuntu-figlet
```

**Exercise:** Run the above command. Is the `figlet` installation in the created container?

#### Commands

The second positional argument of `docker run` can be a command followed by its arguments. So, we could run a container non-interactively (without `-it`), and just let it run a single command:

```sh
docker run ubuntu-figlet figlet 'non-interactive salam'
```

Resulting in just the output of the `figlet` command.

In the previous exercises we have run containers without a command as positional argument. This doesn't mean that no command has been run, because the container would do nothing without a command. The default command is stored in the image, and you can find it by `docker image inspect [IMAGE NAME]`.

**Exercise:** What is the default command (`CMD`) of the ubuntu image?


Running `docker image inspect ubuntu` gives (among other information):
```
"Cmd": [
           "/bin/sh",
           "-c",
           "#(nop) ",
           "CMD [\"/bin/bash\"]"
       ],
```
    
The first part in the list following `"Cmd":` is the shell in which the command is executed (`/bin/sh -c`; i.e. *Bourne shell*), the second part, following `CMD`, is the default command. In the case of the ubuntu image this is `/bin/bash`, returning a shell in `bash` (i.e. *Bourne again shell* in stead of `sh`). Adding the options `-i` and `-t` (`-it`) to your `docker run` command will therefore result in an interactive `bash` shell. You can modify this default behaviour.

#### Removing containers

In the meantime, with every call of `docker run` we have created a new container (check your containers with `docker container ls -a`). You probably don't want to remove those one-by-one. These two commands are very useful to clean up your Docker cache:

* `docker container prune`: removes stopped containers
* `docker image prune`: removes dangling images (i.e. images without a name)

So, remove your stopped containers with:

```sh
docker container prune
```

Unless you're developing further on a container, or you're using it for an analysis, you probably want to get rid of it once you have exited the container. You can do this with adding `--rm` to your `docker run` command, e.g.:

```sh
docker run --rm ubuntu-figlet figlet 'non-interactive run'
```

