import os
import shutil
import paramiko
from scp import SCPClient, SCPException

class SSHManager:
    """ usage:
        >>> import SSHManager
        >>> ssh_manager = SSHManager()
        >>> ssh_manager.create_ssh_client(hostname, username, password)
        >>> ssh_manager.send_command("ls -al")
        >>> ssh_manager.send_file("/path/to/local_path", "/path/to/remote_path")
        >>> ssh_manager.get_file("/path/to/remote_path", "/path/to/local_path")
        ...
        >>> ssh_manager.close_ssh_client()
    """
    def __init__(self):
        self.ssh_client = None

    def create_ssh_client(self, hostname, username, password):
        """Create SSH client session to remote server"""
        if self.ssh_client is None:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(hostname, username=username, password=password)
        else: print("SSH client session exist.")

    def close_ssh_client(self):
        """Close SSH client session"""
        self.ssh_client.close()

    def send_file(self, local_path, remote_path):
        """Send a single file to remote path"""
        try:
            with SCPClient(self.ssh_client.get_transport()) as scp:
                scp.put(local_path, remote_path, preserve_times=True)

        except SCPException:
            raise SCPException.message

    def get_file(self, remote_path, local_path):
        """Get a single file from remote path"""
        try:
            with SCPClient(self.ssh_client.get_transport()) as scp:
                scp.get(remote_path, local_path)

        except SCPException:
            raise SCPException.message

    def send_command(self, command):
        """Send a single command"""
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        return stdout.readlines()

if __name__ == '__main__':

    remote_server = "10.246.246.72"
    remote_id = "icns"
    remote_pw = "ilove_aigo331"

    #Create SCP Client
    ssh_manager = SSHManager()
    ssh_manager.create_ssh_client(remote_server, remote_id, remote_pw)

    while True:
        # If more than 1000 images are saved in /home/aigo/toCore/car
        if len(os.listdir('/home/aigo/toCore/car') == 1000:
        
            remote_path = "/home2/icns/aigo/car_train"
            remote_file = remote_path + "/car.zip"
            #Archive folder to zipfile
            local_folder = '/home/aigo/toCore/car'
            local_file = shutil.make_archive(local_folder, 'zip', local_folder)
               
            #Send zipfile
            ssh_manager.send_file(local_file, remote_path)
            ssh_manager.get_file(remote_file, local_file)
    
            #Remove all images in dir
            os.system("rm /home/aigo/toCore/car/*")

            requests.get("http://10.246.246.72:10222/car_training")
    
        # If more than 1000 images are saved in /home/aigo/toCore/car_dist
        if len(os.listdir('/home/aigo/toCore/car_dist')) >= 1000:
    
            remote_path = "/home2/icns/aigo/car_dist_train"
            remote_file = remote_path + "/car_dist.zip"
            #Archive folder to zipfile
            local_folder = '/home/aigo/toCore/car_dist'
            local_file = shutil.make_archive(local_folder, 'zip', local_folder)
               
            #Send zipfile
            ssh_manager.send_file(local_file, remote_path)
            ssh_manager.get_file(remote_file, local_file)

            #Remove all images in dir
            os.system("rm /home/aigo/toCore/car_dist/*")

            requests.get("http://10.246.246.72:10222/car_dist_training")

        # If more than 1000 images are saved in /home/aigo/toCore/crosswalk
        if len(os.listdir('/home/aigo/toCore/car')) >= 1000:

            remote_path = "/home2/icns/aigo/cw_train"
            remote_file = remote_path + "/crosswalk.zip"
            #Archive folder to zipfile
            local_folder = '/home/aigo/toCore/crosswalk'
            local_file = shutil.make_archive(local_folder, 'zip', local_folder)

            #Send zipfile
            ssh_manager.send_file(local_file, remote_path)
            ssh_manager.get_file(remote_file, local_file)

            #Remove all images in dir
            os.system("rm /home/aigo/toCore/crosswalk/*")

            requests.get("http://10.246.246.72:10222/cw_training")

        # If more than 1000 images are saved in /home/aigo/toCore/trafficlight
        if len(os.listdir('/home/aigo/toCore/trafficlight')) >= 1000:

            remote_path = "/home2/icns/aigo/tl_train"
            remote_file = remote_path + "/trafficlight.zip"
            #Archive folder to zipfile
            local_folder = '/home/aigo/toCore/trafficlight'
            local_file = shutil.make_archive(local_folder, 'zip', local_folder)
    
            #Send zipfile
            ssh_manager.send_file(local_file, remote_path)
            ssh_manager.get_file(remote_file, local_file)
    
            #Remove all images in dir
            os.system("rm /home/aigo/toCore/trafficlight/*")

            requests.get("http://10.246.246.72:10222/tl_training")

