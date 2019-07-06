# easy-scp

## Preface

Please note that this is currently a custom solution created by a single user, and is far from a complete one-size-fits-all solution at this point in time. Development is ongoing at an unscheduled pace. Contributors are welcome, and criticism is appreciated.

## Overview

When scp-ing files from a remote to local machine (and vice-versa), you often have to enter a very verbose command, and must get the path correct. Additionally, you're probably hitting the same set of remote machines. 

A decent solution is to have:
+ One-time initial configuration setup
+ Daily usage involving aliase leveraging configuration

This would eliminate error and save keystrokes and time in the long run.

## System Requirements

So far, this project has only been tested on Ubuntu LTS 16.04, so use with caution.

## Dependencies

+ python3
+ pip

External Dependency | Description | Installation
--- | --- | ---
[pyyaml](https://pyyaml.org/wiki/PyYAMLDocumentation) | YAML parser and emtter for Python | pip install pyyaml
[paramiko](https://www.paramiko.org/) | A python implementation of SSHv2 | pip install paramiko
[scp](https://pypi.org/project/scp/) | A python implementation of SCP using paramiko SSHv2 | pip install scp

## Usage

### Installation

```sh
? git clone https://github.com/nkumar0727/easy-scp.git
```

### Initial Setup

If you've never used YAML, a [Complete Idiot's Introduction to YAML](https://github.com/Animosity/CraftIRC/wiki/Complete-idiot's-introduction-to-yaml) is a 5 minute read.

easy-scp uses a file called *config.yml* to store your preconfigured hostnames and associated data for file copying.

The file looks something like this:
```yaml
projects:
  projectAlias:
    remotePath: '/remotePath'
    remoteUser: 'user'
    remoteHostname: 'hostname'
    isPasswordNeeded: 'Y'
    localPath: '/localPath'
```

#### Fields

+ *projectAlias* - [**REQUIRED**] this alias serves as a handle for one set of scp configurations
+ *remotePath* - [**REQUIRED**] this is the filepath of the file/directory you wish to copy on your remote machine
+ *remoteUser* - this is the user on the remote machine with which you want to login as
+ *remoteHostname* [**REQUIRED**] - the hostname of the machine you want to log into
+ *isPasswordNeeded* [**REQUIRED**] - put 'Y' if a password prompt is needed to login, and 'N' if otherwise
+ *localPath* [**REQUIRED**] - the local file/directory path in which you want to put the copied files

Simply add a new project alias to *config.yml* with the required fields.

### Daily Usage

**Note**: As of 2019-07-06, you must be with in the easy-scp directory in order to use this tool.

```sh
> cd easy-scp
> python easy-scp <project_alias>
```

### Typical Workflow

**Scenario**: I use a local laptop on which I do my development work with the power of an IDE, and a remote machine on which I build and test my projects. I want to copy generated documentation files from my cloud desktop onto my local laptop so that I can see it within the browser.

1) Add project alias to config.yml

```yaml
projects:
  projectDocumentation:
    remotePath: '/path/on/remote/machine/docs'
    remoteUser: 'user123'
    remoteHostname: 'cloud-machine-hostname'
    isPasswordNeeded: 'Y'
    localPath: '/path/on/local/machine'
```

2) Go into easy-scp directory and run script

```sh
> cd easy-scp
> python easy-scp projectDocumentation
```

3) (*if password needed*) Enter password in prompt, and hit 'Return'

```sh
> Password: 
```

With that, all the files in /path/on/remote/machine should be located in /path/on/local/machine/docs.

## Additional Usage Notes/Defects

### Notes

+ If a directory path is specified for the remotePath, the script will recursively copy the directory and its contents into the local path

### Defects

+ There is currently no support for passwordless ssh via public keys
+ There is currently no error handling for anything; anything marked as [**REQUIRED**] is, in fact, required
+ Any 'non-happy cases' (as of now, those that do not match the example given above) have not been tested -- **use at your own risk**

## TODOs

+ Add basic error handling
+ Test 'non-happy' cases
+ Investigate cross-platform usage (Windows, MacOS, other Linux distros)
+ Add support for passwordless ssh
