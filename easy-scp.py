from yaml import load, dump
from paramiko import SSHClient
from scp import SCPClient
from getpass import getpass
from sys import argv

def getProjectConfigObjectFromConfigFile(projectName):
  with open('./config.yml') as configFile:
    configObject = load(configFile)
    return getProjectObjectFromYMLObject(configObject, projectName)

def getProjectObjectFromYMLObject(ymlObject, projectName):
  return ymlObject['projects'][projectName]

def getPasswordFromConfigIfNeeded(configObject):
  if configObject['isPasswordNeeded']:
    return getpass()
  return None

def connectSSHClientToHost(sshClient, remoteHostname, remoteUser, password):
  if password is None:
    sshClient.connect(hostname=remoteHostname, username=remoteUser)
  else:
    sshClient.connect(hostname=remoteHostname, username=remoteUser, password=password)

def main(argv):
  myProject = getProjectConfigObjectFromConfigFile(argv[1])
  password = getPasswordFromConfigIfNeeded(myProject)
  print(myProject)

  with SSHClient() as sshClient:
    sshClient.load_system_host_keys()
    connectSSHClientToHost(sshClient, myProject['remoteHostname'], myProject['remoteUser'], password)
    with SCPClient(sshClient.get_transport()) as scpClient:
      scpClient.get(myProject['remotePath'], myProject['localPath'], recursive=True)
  print('Task completed for project \'%s\'' % argv[1])

if __name__ == "__main__":
  main(argv)
