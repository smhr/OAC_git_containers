Working with dockerfiles
========================

To make your images shareable and adjustable, it's good practice to work with a `Dockerfile`. This is a script with a set of instructions to build your image from an existing image.

### Basic `Dockerfile`

You can generate an image from a `Dockerfile` using the command `docker build`. A `Dockerfile` has its own syntax for giving instructions. Luckily, they are rather simple. The script always contains a line starting with `FROM` that takes the image name from which the new image will be built. After that you usually want to run some commands to e.g. configure and/or install software. The instruction to run these commands during building starts with `RUN`.  In our `figlet` example that would be:

```dockerfile
FROM ubuntu
RUN apt-get update
RUN apt-get install figlet
```

### The `RUN` Instruction

We can install updates, install new software, or download code to our image by running commands with the RUN instruction. Each RUN instruction creates an intermediate image (called a ‘layer’). Too many layers makes the Docker image less performant, and makes building less efficient. 

**Note:** On writing reproducible `Dockerfiles`
At the `FROM` statement in the the above `Dockerfile` you see that we have added a specific tag to the image (i.e. `focal-20210401`). We could also have written:

```dockerfile
FROM ubuntu
RUN apt-get update
RUN apt-get install figlet
```

This will automatically pull the image with the tag `latest`. However, if the maintainer of the `ubuntu` images decides to tag another `ubuntu` version as `latest`, rebuilding with the above `Dockerfile` will not give you the same result. Therefore it's always good practice to add the (stable) tag to the image in a `Dockerfile`. More rules on making your `Dockerfiles` more reproducible [here](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008316).

**Exercise:** Create a file on your computer called `Dockerfile`, and paste the above instruction lines in that file. Make the directory containing the `Dockerfile` your current directory. Build a new image based on that `Dockerfile` with:

```sh
docker build -t ubuntu-figlet:v2 .
```

**Note:** The argument of `docker build`
The command `docker build` takes a directory as input (providing `.` means the current directory). This directory should contain the `Dockerfile`, but it can also contain more of the build context, e.g. (python, R, shell) scripts that are required to build the image.

### Using `CMD`

As you might remember the second positional argument of `docker run` is a command (i.e. `docker run IMAGE [CMD]`). If you leave it empty, it uses the default command. You can change the default command in the `Dockerfile` with an instruction starting with `CMD`. For example:

```dockerfile
FROM ubuntu
RUN apt-get update 
RUN apt-get install figlet
CMD figlet My image works!
```
---

**Exercise:** Build a new image based on the above `Dockerfile`. Can you validate the change using `docker image inspect`? Can you overwrite this default with `docker run`?

**Answer:** Copy the new line to your `Dockerfile`, and build the new image like this:

```sh
docker build -t ubuntu-figlet:v3 .
```

The command `docker inspect ubuntu-figlet:v3` will give:

```
    "Cmd": [
        "/bin/sh",
        "-c",
        "figlet My image works!"
    ]
```

So the default command (`/bin/bash`) has changed to `figlet My image works!`

Running the image (with clean-up (`--rm`)):

```sh
docker run --rm ubuntu-figlet:v3
```

Will result in:

```
__  __         _                                                 _        _
|  \/  |_   _  (_)_ __ ___   __ _  __ _  ___  __      _____  _ __| | _____| |
| |\/| | | | | | | '_ ` _ \ / _` |/ _` |/ _ \ \ \ /\ / / _ \| '__| |/ / __| |
| |  | | |_| | | | | | | | | (_| | (_| |  __/  \ V  V / (_) | |  |   <\__ \_|
|_|  |_|\__, | |_|_| |_| |_|\__,_|\__, |\___|   \_/\_/ \___/|_|  |_|\_\___(_)
       |___/                     |___/
```

And of course you can overwrite the default command:

```sh
docker run --rm ubuntu-figlet:v3 figlet another text
```

Resulting in:

```
_   _                 _            _
__ _ _ __   ___ | |_| |__   ___ _ __  | |_ _____  _| |_
/ _` | '_ \ / _ \| __| '_ \ / _ \ '__| | __/ _ \ \/ / __|
| (_| | | | | (_) | |_| | | |  __/ |    | ||  __/>  <| |_
\__,_|_| |_|\___/ \__|_| |_|\___|_|     \__\___/_/\_\\__|

```

---

**Note:** Two flavours of `CMD`
You have seen in the output of `docker inspect` that docker translates the command (i.e. `figlet "my image works!"`) into this: `["/bin/sh", "-c", "figlet 'My image works!'"]`. The notation we used in the `Dockerfile` is the *shell notation* while the notation with the square brackets (`[]`) is the *exec-notation*. You can use both notations in your `Dockerfile`. Altough the *shell notation* is more readable, the *exec notation* is directly used by the image, and therefore less ambiguous.

A `Dockerfile` with shell notation:

```dockerfile
FROM ubuntu
RUN apt-get update
RUN apt-get install figlet
CMD figlet My image works!
```

A `Dockerfile` with exec notation:

```dockerfile
FROM ubuntu
RUN apt-get update
RUN apt-get install figlet
CMD ["/bin/sh", "-c", "figlet My image works!"]
```
---

Now push our created image (with a version tag) to docker hub:

```sh
docker tag ubuntu-figlet:v3 [USER NAME]/ubuntu-figlet:v3
docker push [USER NAME]/ubuntu-figlet:v3
```

## Build image for your own script

Often containers are built for a specific purpose. For example, you can use a container to ship all dependencies together with your developed set of scripts/programs. For that you will need to add your scripts to the container. That is quite easily done with the instruction `COPY`. However, in order to make your container more user-friendly, there are several additional instructions that can come in useful. We will treat the most frequently used ones below. 

In the exercises we will use a simple script called `pi.py`. You can download it [here](../codes/pi.py).

Let's make a simple `Dockerfile` as:

```dockerfile
FROM ubuntu

RUN apt-get update && apt-get upgrade -y && apt-get install -y python3

COPY pi.py /code/pi.py
```

**Exercise:** Download the `pi.py` and build the image with `docker build`:

```sh
chmod +x ./pi.py
docker build -t pi:v0.1 .
```

Run the container:

```sh
docker run -it --rm pi /bin/bash
```

Inside the container we look up the script:

```sh
cd /code
ls
```

Now you can execute it from inside the container:

```sh
./pi.py 10000
```

We can ship our python script inside our container. However, we don't want to run it interactively every time. So let's make some changes to make it easy to run it as an executable. For example, we can add `/code` to the global `$PATH` variable with `ENV`. 

### The `ENV` Instruction

Another useful instruction is the ENV instruction. This allows the image developer to set environment variables inside the container runtime. In our interactive build, we added the `/code` folder to the `PATH`.

```dockerfile
ENV PATH "/code:$PATH"
```

The path variable is a special variable that consists of a list of path seperated by colons (`:`). These paths are searched if you are trying to run an executable. More info this topic at e.g. [wikipedia](https://en.wikipedia.org/wiki/PATH_(variable)).

```dockerfile
FROM ubuntu

RUN apt-get update && apt-get upgrade -y && apt-get install -y python3

COPY pi.py /code/pi.py

ENV PATH=/code:$PATH
```

**Exercise**: Start an interactive bash session inside the new container. Is the path variable updated? (i.e. can we execute `pi.py` from anywhere?). Hint: re-build the container and run it. Then echo the `PATH` variable.

Now, instead of starting an interactive session with `/bin/bash` we can now more easily run the script non-interactively:

```sh
docker run --rm pi pi.py 10000
```

Now, add your script to the `CMD` instruction, so your script will be executed in the container if the user calls the container without any arguments.

```dockerfile
FROM ubuntu

RUN apt-get update && apt-get upgrade -y && apt-get install -y python3

COPY pi.py /code/pi.py

ENV PATH=/code:$PATH

CMD ["pi.py", "1000"]
```

