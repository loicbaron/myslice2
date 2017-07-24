import socket
import select
import os
import glob
import hashlib
import paramiko
from paramiko.ssh_exception import BadAuthenticationType, BadHostKeyException, AuthenticationException, SSHException

# static atm
username = 'root'
rsa_private_key = "/Users/moray/.ssh/planetlab_root_ssh_key.rsa"
remote_dir = "/root/.myslice"
local_dir = os.path.realpath(os.path.dirname(__file__) + '/../scripts')

def setup(hostname):

    result = { "status" : False, "message" : None }

    try:
        pkey = paramiko.RSAKey.from_private_key_file(rsa_private_key)
    except Exception as e:
        #print 'Failed loading' % (rsa_private_key, e)
        result["message"] = 'Failed loading' % (rsa_private_key, e)
        return result

    try:
        transport = paramiko.Transport((hostname, 22))
    except SSHException as e:
        # Transport setup error
        result['message'] = 'Failed SSH connection (%s)' % (e)
        return result
    except Exception as e:
        result['message'] = 'Transport error (%s)' % (e)
        return result

    try:
        transport.start_client()
    except SSHException as e:
        # if negotiation fails (and no event was passed in)
        result['message'] = 'Failed SSH negotiation (%s)' % (e)
        return result

    try:
        transport.auth_publickey(username, pkey)
    except BadAuthenticationType as e:
        # if public-key authentication isn't allowed by the server for this user (and no event was passed in)
        result['message'] = 'Failed public-key authentication (%s)' % (e)
        return result
    except AuthenticationException as e:
        # if the authentication failed (and no event was passed in)
        result['message'] = 'Failed authentication (%s)' % (e)
        return result
    except SSHException as e:
        # if there was a network error
        result['message'] = 'Network error (%s)' % (e)
        return result


    sftp = paramiko.SFTPClient.from_transport(transport)

    try:
        sftp.chdir(remote_dir)  # Test if remote_path exists
    except IOError:
        sftp.mkdir(remote_dir)  # Create remote_path
        sftp.chdir(remote_dir)
        pass

    for file_name in glob.glob(local_dir + '/*.*'):
        local_file = os.path.join(local_dir, file_name)
        remote_file = remote_dir + '/' + os.path.basename(file_name)

        # check if remote file exists
        try:
            if sftp.stat(remote_file):
                local_file_data = open(local_file, "rb").read()
                remote_file_data = sftp.open(remote_file).read()
                md1 = hashlib.md5(local_file_data).digest()
                md2 = hashlib.md5(remote_file_data).digest()
                if md1 == md2:
                    pass
                    #print "UNCHANGED:", os.path.basename(file_name)
                else:
                    #print "MODIFIED:", os.path.basename(file_name)
                    sftp.put(local_file, remote_file)
        except:
            #print "NEW: ", os.path.basename(file_name)
            sftp.put(local_file, remote_file)
            sftp.chmod(remote_file, 0755)
    sftp.close()

    result['status'] = True
    result['message'] = 'Setup complete'
    return result

def connect(hostname):
    '''
    Try to connect to remote host
    '''
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname=hostname, username="root", key_filename=rsa_private_key)
    except BadHostKeyException as e:
        print(e)
        raise
    except AuthenticationException as e:
        print(e)
        raise
    except SSHException as e:
        print(e)
        raise
    except socket.error as e:
        print(e)
        raise
    except IOError as e:
        print(e)
        raise

    return ssh

def execute(hostname, command):

    result = ''

    ssh = connect(hostname)

    # Send the command (non-blocking)
    stdin, stdout, stderr = ssh.exec_command(command)

    # Wait for the command to terminate
    while not stdout.channel.exit_status_ready():
        # Only print data if there is data to read in the channel
        if stdout.channel.recv_ready():
            rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
            if len(rl) > 0:
                # Print data from stdout
                result += stdout.channel.recv(1024)

    ssh.close()

    return result.strip()

def script(hostname, script):
    '''
    Executes a script on the remote node.
    Scripts will return a json formatted string with result and information
    '''
    result = execute(hostname, remote_dir + "/" + script)

    return result

if __name__ == '__main__':
    node = 'mimas.ipv6.lip6.fr'
    setup(node)
    r = script(node, 'networks.sh')
    print r