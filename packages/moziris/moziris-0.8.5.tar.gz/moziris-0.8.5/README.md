# moziris

![Travis (.com)](https://img.shields.io/travis/com/mozilla/iris)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/moziris)
![GitHub](https://img.shields.io/github/license/mozilla/iris)
![GitHub repo size](https://img.shields.io/github/repo-size/mozilla/iris)
![GitHub issues](https://img.shields.io/github/issues/mozilla/iris)

Mozilla Iris is a tool that uses on-screen pattern and text matching, while manipulating a machine's mouse and keyboard, to test visual and interactive states of an application.
For more detailed information and troubleshooting tips, please [view our wiki](https://github.com/mozilla/iris/wiki).

## Installation

### Mac instructions:

#### System Requirements

 - Python 3
 - git
 - [Firefox](https://www.mozilla.org/en-US/firefox/new/)

#### Setup

```
git clone https://github.com/mozilla/iris
# Run the Mac bootstrap script
cd iris
./bootstrap/bootstrap.sh
# Run this command to agree to xcode terms of service
sudo xcodebuild -license accept
```
 - **Restart** your Mac in order for certain libraries to be recognized
 - In System Preferences, go to Mission Control and change the keyboard shortcut for "Application Windows" to "-", or none
 - Launch Iris
```
cd iris
pipenv install
pipenv shell
iris sample
```

### Windows 7 / Windows 10 Professional instructions:

#### System Requirements

 - Python 3
 - git
 - [Firefox](https://www.mozilla.org/en-US/firefox/new/)
 - [Powershell 3](https://www.microsoft.com/en-us/download/details.aspx?id=34595)
 - [.NET framework version 4.5](https://www.microsoft.com/en-us/download/details.aspx?id=30653)

#### Setup

```
git clone https://github.com/mozilla/iris
cd iris
bootstrap\bootstrap.sh
# Install project requirements and activate the virtualenv
pipenv install
pipenv shell
# Run Iris
iris sample
```

### Ubuntu Linux 16.04 instructions:

#### System Requirements

 - Python 3
 - git
 - [Firefox](https://www.mozilla.org/en-US/firefox/new/)
 - [Follow instructions below for disabling Keyring](https://github.com/mozilla/iris/wiki/Setup#disable-system-keyring)
 - Open Settings > Displays > "Scale for Menu and Title bars:" and verify that it is set to 1

#### Setup
```
git clone https://github.com/mozilla/iris
cd iris
./bootstrap/bootstrap.sh
# Note: This will take around 10 minutes to download, compile, and install dependencies
# Run the following commands to complete installation and launch Iris
pipenv install
pipenv shell
iris sample
```

## Usage

The Iris project is meant to be used with your own "target" and tests. A target is basically a pytest plugin invoked by Iris, which will then gather data during the run to present in a web-based interface known as the Iris Control Center.

Iris is available as a PyPI library named `moziris`. It requires system dependencies that are installed using the bootstrap script from this repo.

Once your system is configured, and the setup instructions have been followed, you can test some of Iris' functionality.

To invoke the "sample" target - which is just a placeholder project for demonstration purposes:
```
iris sample
```

To open the Control Center, which is the web-based UI for managing local Iris runs:
```
iris -k
```

To verify that the Iris API itself exists, without running tests, this command will move your mouse on screen:
```
api-test
```

A complete list of command-line options is available when invoking the `-h` flag.

For more detailed examples, see the [project wiki](https://github.com/mozilla/iris/wiki/Command-line-examples).


## Contributing

See our [project wiki](https://github.com/mozilla/iris/wiki/Developer-Workflow) for more information on contributing to Iris.
