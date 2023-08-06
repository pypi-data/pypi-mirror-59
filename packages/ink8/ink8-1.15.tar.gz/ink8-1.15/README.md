# infra
`infra` is short for infrastructure. This is the temporary place for spinning up all of the systems required to run **Inspirae.me**. As the infrastructure matures, we will be able to automate our development more and gaurantee a stable, resistent and working system.

## tldr;

**NOTE** The test-app is not ready to demo yet. I still have a few steps to take but no more unknowns at this point.

There are servers in charge of **user info**, **chat rooms**, and the **website/app**. This repository is for spinning all these servers up. To do that, follow these steps:
1. Download [Docker](https://docs.docker.com/docker-for-mac/install/) and open it
2. Install [git](https://gist.github.com/derhuerst/1b15ff4652a867391f03) command line tools if necessary
3. Open the terminal and clone:
```
$ git clone git@github.com:wywfalcon/infra.git
```
4. Go to the `infra` repo and spin up the environment
```
$ cd ./infra
$ make install
$ make clone
$ make all
```
5. Wait for probably a few minutes.
6. Check that everything is `running`
```
$ kubectl get pods
```
7. Visit https://localhost:8443/app and try the test app out (again, not done)

# Sections below are very much under construction

## Architecture

### Repositories
Currently, the architecture consists of:
- Applications or `app-*` which runs front-end applications
- Libraries or `lib-*` used by either/both back-end and front-end to accomplish some lower level / functional utility
- Services or `svc-*` which are back-end servers providing some abstract functionality

### Orchestration
These services and applications are currently orchestrated with `docker-compose`. Although this can work in the meantime, it is to be replaced with `Terraform` and `Kubernetes` in order to be a little less of a toy example.

### Current Set-up (TODO: Docs for each...)
- `svc-chat`: A WebSocket server that serves chat streams allowing users to publish their messages to other users
- `svc-user`: An HTTP server that manages user information.
- `app-test`: A test application that demonstrates features of `lib-web-sdk`
- `app-website`: The front-end marketing website for our organization
- `app-inspirae`: The Online Avatar Site where user interacts and creates their online persona.

`svc-user` directs requests to Kong - our API Gateway ([learn more](https://konghq.com/faqs/))
