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
    print('Password is needed, as specified in project config...')
    return getpass()
  return None

def connectSSHClientToHost(sshClient, remoteHostname, remoteUser, password):
  if password is None:
    sshClient.connect(hostname=remoteHostname, username=remoteUser)
  else:
    sshClient.connect(hostname=remoteHostname, username=remoteUser, password=password)

def hasInvalidArgs(argv):
  return len(argv) != 2

def printUsageMessage():
  print('Usage: python easy-scp.py <project_name>')

def main(argv):
  
  if hasInvalidArgs(argv):
    printUsageMessage()
    return
  
  myProject = None
  try:
    myProject = getProjectConfigObjectFromConfigFile(argv[1])
  except:
    print('No config found for project \'%s\'' % argv[1])
    return

  print('Config found for project %s :: scp -r %s@%s:%s %s' % (argv[1],
    myProject['remoteUser'], myProject['remoteHostname'],
    myProject['remotePath'], myProject['localPath']))

  password = getPasswordFromConfigIfNeeded(myProject)

  try:
    with SSHClient() as sshClient:
      
      sshClient.load_system_host_keys()
      connectSSHClientToHost(sshClient, myProject['remoteHostname'], myProject['remoteUser'], password)
      
      with SCPClient(sshClient.get_transport()) as scpClient:
        scpClient.get(myProject['remotePath'], myProject['localPath'], recursive=True)
      
      print('Task completed for project \'%s\': scp -r %s@%s:%s %s' % (argv[1],
        myProject['remoteUser'], myProject['remoteHostname'],
        myProject['remotePath'], myProject['localPath']))
  
  except Exception as ex:
    print('%s' % ex)
    print('Ensure correct information in project config, and correct password')

if __name__ == "__main__":
  main(argv)
