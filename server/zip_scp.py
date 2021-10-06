import os
import shutil
import paramiko
from scp import SCPClient, SCPException
import requests

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

        except:
            pass
        #SCPException:
        #    raise SCPException.message

    def send_command(self, command):
        """Send a single command"""
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        return stdout.readlines()

if __name__ == '__main__':

    remote_server = "10.246.246.72"
    remote_id = "icns"
    remote_pw = "ilove_aigo331"
    toCore = "/home/aigo/toCore/"

    #Create SCP Client
    ssh_manager = SSHManager()
    ssh_manager.create_ssh_client(remote_server, remote_id, remote_pw)
    while True:
        # If 1000 images and labels are saved in /home/aigo/toCore/car
        if len(os.listdir(toCore + "car/images")) == 1000:
            if len(os.listdir(toCore + "car/labels")) == 1000:
                
                remote_path_image = "/home2/icns/aigo/car_train/images"
                remote_path_label = "/home2/icns/aigo/car_train/labels"
                remote_file_image = remote_path_image + "/images.zip"
                remote_file_label = remote_path_label + "/labels.zip"

                #Archive folder to zipfile
                local_folder_image = toCore + 'car/images'
                local_folder_label = toCore + 'car/labels'

                local_file_image = shutil.make_archive(local_folder_image, 'zip', local_folder_image)
                local_file_label = shutil.make_archive(local_folder_label, 'zip', local_folder_label)

                #Send zipfile
                ssh_manager.send_file(local_file_image, remote_path_image)
                ssh_manager.send_file(local_file_label, remote_path_label)
                ssh_manager.get_file(remote_file_image, local_file_image)
                ssh_manager.get_file(remote_file_label, local_file_label)
                
                #Remove all images in dir
                os.system("rm /home/aigo/toCore/car/images/*")
                os.system("rm /home/aigo/toCore/car/labels/*")
                
                requests.get("http://10.246.246.72:10222/car_training")

                break


        # If 1000 images and labels are saved in /home/aigo/toCore/trafficlight
        print(len(os.listdir(toCore + "trafficlight/images")), len(os.listdir(toCore + "trafficlight/labels")))
        if len(os.listdir(toCore + "trafficlight/images")) == 1000:
            if len(os.listdir(toCore + "trafficlight/labels")) == 1000:

                remote_path_image = "/home2/icns/aigo/tl_train/images"
                remote_path_label = "/home2/icns/aigo/tl_train/labels"
                remote_file_image = remote_path_image + ".zip"
                remote_file_label = remote_path_label + ".zip"

                #Archive folder to zipfile
                local_folder_image = toCore + "trafficlight/images"
                local_folder_label = toCore + 'trafficlight/labels'

                local_file_image = shutil.make_archive(local_folder_image, 'zip', local_folder_image)
                local_file_label = shutil.make_archive(local_folder_label, 'zip', local_folder_label)

                #Send zipfile
                ssh_manager.send_file(local_file_image, remote_path_image)
                ssh_manager.send_file(local_file_label, remote_path_label)
                ssh_manager.get_file(remote_file_image, local_file_image)
                ssh_manager.get_file(remote_file_label, local_file_label)

                #Remove all images in dir
                os.system("rm /home/aigo/toCore/trafficlight/images/*")
                os.system("rm /home/aigo/toCore/trafficlight/labels/*")

                requests.get("http://10.246.246.72:10222/tl_training")

                break
