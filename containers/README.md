## What is a container?

In short, a container is a lightweight Linux kernel plus some other stuffs (packages, libraries, executables, etc) that performs a specific task(s). Containers are created to make maintaining and running software easier, but could be also used to make scientific research reproducible.

For an in-depth explanation see: 

[OS-level virtualization](https://en.wikipedia.org/wiki/OS-level_virtualization).

For some enterprise viewpoints see:

[Docker](https://www.docker.com/resources/what-container/)
[IBM](https://www.ibm.com/cloud/learn/containers)
[Microsoft](https://azure.microsoft.com/en-us/overview/what-is-a-container/)
[Redhat](https://www.redhat.com/en/topics/containers)

## Installing docker

### Going around blocking of Iran's IP

Unfortunately docker restricts its service for Iran. So you need a workaround. You can use VPN or some other services like [Shekan](https://shecan.ir/) to install docker and use [dockerhub](https://hub.docker.com/). For more information, see [its FAQ](https://shecan.ir/faq/).

### Installation steps

Depending on your OS and distro, you can install docker. If you use Gnu/Linux, please install [docker server](https://docs.docker.com/engine/install/) according to the documentation for your platform. If you have Mac or Windows, please install [docker desktop](https://docs.docker.com/get-docker/).
