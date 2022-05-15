Install Singularity
===================

### Dependencies

#### Debian/Ubuntu

```sh
sudo apt-get update && sudo apt-get install -y \
    build-essential \
    uuid-dev \
    libgpgme-dev \
    squashfs-tools \
    libseccomp-dev \
    wget \
    pkg-config \
    git \
    cryptsetup-bin
```

#### CentOS/Fedora

```sh
sudo yum update -y && \
     sudo yum groupinstall -y 'Development Tools' && \
     sudo yum install -y \
     openssl-devel \
     libuuid-devel \
     libseccomp-devel \
     wget \
     squashfs-tools \
     cryptsetup
```

### Install Go language

Singularity is written primarily in Go, and you will need to have Go v1.13 or above installed to compile it from source.

Download Go v1.18.2 from the IPM storage:

```sh
wget -c https://storage.ipm.ir/cstorage/index.php/s/ZKnk91u4Dp9jFrd/download -O go1.18.2.linux-amd64.tar.gz
```
Unpack it:

```sh
sudo tar -C /usr/local -xzvf go1.18.2.linux-amd64.tar.gz
```

Setup the environment:

```sh
echo 'export GOPATH=${HOME}/go' >> ~/.bashrc && \
    echo 'export PATH=/usr/local/go/bin:${PATH}:${GOPATH}/bin' >> ~/.bashrc && \
    source ~/.bashrc
```

Verify your Go installation:

```sh
go version
```

Now, download Singularity v3.8.6, unpack and build it:

```sh
wget -c https://github.com/apptainer/singularity/releases/download/v3.8.6/singularity-3.8.6.tar.gz
```

```sh
tar -xzvf ./singularity-3.8.6.tar.gz
```

```sh
cd ./singularity-3.8.6 && \
    ./mconfig && \
    make -C ./builddir && \
    sudo make -C ./builddir install
```

Test your installation:

```sh
singularity --version
```






