# Geoffrey Devops CLI

Geoffrey is a Python based CLI application which provides a GUI for installing components, it is installed using pip and can be called
simply with ```geoffrey```. Calling it for the first time will trigger a new config to be created and you will be asked to provide a remote
URL that contains a YML file for configuration.

A Sample YML can be seen in the FXQuants geoffrey Repository:  
 - https://bitbucket.org/snippets/fxquants/neGkz8/geoffrey

![Readme Animation](https://bitbucket.org/fxquants/geoffrey/raw/master/readme.gif)

## Getting Started
The best way to get started is to simply install Geoffrey.
Once Installed start geoffrey with:
```
geoffrey
```
You will be asked to provide a config location, do so, for an example you could use the FXQuants Repo:
 - https://bitbucket.org/!api/2.0/snippets/fxquants/neGkz8/master/files/choices.yml

### Installing
I Highly recommend using PIPX to install geoffrey to ensure you do not run into issues with other environments and CLI apps installed using PIP   
https://packaging.python.org/guides/installing-stand-alone-command-line-tools/

Install geoffrey with pip into a Python3 Environment.
```
yum -y install epel-release
yum -y install gcc wget python36 python36-pip python36-devel && \
pip3 install fxq-geoffrey
```

The YML that is loaded by Geoffrey is composed of sections containing tasks within a choices model the following is a 
simple model with some examples:

As you can see it's simple Bash Lines that are called with os.system(), they can be any valid bash.

I would recommend they are not overly complex however and more complex scripts should be 
housed separately for better Version Control.
```text
choices:
  sections:
    - section:
        name: Hypervisor Tools
        tasks:
          - task:
              name: Open VM Tools
              default: y
              script:
                - yum -y install open-vm-tools
    - section:
        name: Operating System
        tasks:
          - task:
              name: Update All Packages
              default: y
              script:
                - yum -y update
          - task:
              name: Docker Host
              default: n
              script:
                - yum -y install curl
                - curl -s 'https://bitbucket.org/!api/2.0/snippets/fxquants/beGAbx/master/files/install-docker.sh' | bash
```

## Contributing

Contributions are most welcome to the project, please raise issues first and contribute in response to the issue with a pull request.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://bitbucket.org/fxquants/fxq-ioc-core/downloads/?tab=tags). 

## Authors

* **Jonathan Turnock** - *Initial work* - [fxquants - profile](https://fxquants.atlassian.net/people/5c4e3005043b4f5d172a732a)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
