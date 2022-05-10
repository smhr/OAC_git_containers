Managing containers and images
==============================

### Restarting an exited container

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

### Note `docker attach` and `docker exec`

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

### Creating a new image

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

### Commands

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

### Removing containers

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

### Pushing to dockerhub

Now that we have created our first own docker image, we can store it and share it with the world on docker hub. Before we get there, we first have to (re)name and tag it.

Before pushing an image to dockerhub, `docker` has to know to which user and which repository the image should be added. That information should be in the name of the image, like this: `user/imagename`. We can rename an image with `docker tag` (which is a bit of misleading name for the command). So we could push to dockerhub like this:

```sh
docker tag ubuntu-figlet [USER NAME]/ubuntu-figlet
docker push [USER NAME]/ubuntu-figlet
```

We didn't specify the tag for our new image. That's why `docker tag` gave it the default tag called `latest`. Pushing an image without a tag will overwrite the current image with the tag `latest` (more on (not) using `latest` [here](https://vsupalov.com/docker-latest-tag/)). If you want to maintain multiple versions of your image, you will have to add a tag, and push the image with that tag to dockerhub:

```sh
docker tag ubuntu-figlet [USER NAME]/ubuntu-figlet:v0.2
docker push [USER NAME]/ubuntu-figlet:v0.2
```

### Mounting a directory

For many analyses you do calculations with files or scripts that are on your host (local) computer. But how do you make them available to a docker container? You can do that in several ways, but here we will use bind-mount. You can bind-mount a directory with `-v` (`--volume`) or `--mount`. Most old-school `docker` users will use `-v`, but `--mount` syntax is easier to understand and now recommended, so we will use the latter here:

```sh
docker run \
--mount type=bind,source=/host/source/path,target=/path/in/container \
[IMAGE]
```

The target directory will be created if it does not yet exist. The source directory should exist.

**Exercise:** Mount a host (local) directory to a target directory `/working_dir` in a container created from the `ubuntu-figlet` image and run it interactively. Check whether the target directory has been created.

```sh
docker run \
-it \
--mount type=bind,source=/tmp/working_dir,target=/working_dir/ \
ubuntu-figlet
```

This creates a directory called `working_dir` in the directory (`/tmp`). This mounted directory is both available for the host (locally) and for the container. You can therefore e.g. copy files in there, and write output generated by the container.


