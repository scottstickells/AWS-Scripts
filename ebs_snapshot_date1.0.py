#Built with Python 3.3.2
#This script allows for the interactive input from a user to create an EBS volume snapshot and select from what date and time snapshots should be retained and anything older than the specified date and time will be deleted
#The script will prompt for access & secret keys as well as region information
#The script will then prompt to enter the volume to snapshot and then the script will request a description for the snapshot, finally the user will be asked to input the date and time in UTC from which older snapshots will be deleted
import boto.ec2
import datetime
import time
from boto.ec2.connection import EC2Connection
from boto.ec2.regioninfo import RegionInfo
from boto.ec2.snapshot import Snapshot
 
aws_access_key = str(input("AWS Access Key: ")) #Requesting user to enter their AWS access key
aws_secret_key = str(input("AWS Secret Key: ")) #Requesting user to enter their AWS secret key
regionname = str(input("AWS Region Name: ")) #Requesting user to enter the AWS region name they will connect to
regionendpoint = str(input("AWS Region Endpoint: ")) #Requesting user to enter the AWS region endpoint they will connect to
region = RegionInfo(name=regionname, endpoint=regionendpoint) #This sets the region based on the user inputs above
conn = EC2Connection(aws_access_key_id = aws_access_key, aws_secret_access_key = aws_secret_key, region = region) #This establishes the connection using the information provided by the user
print (conn) #This prints the output of the connection, if None is shown the connection is unsuccessful or incorrect and the remainder of the script will fail

volumes = conn.get_all_volumes() #This grabs a list of all volumes available to the authenticated account in the region
print ("%s" % repr(volumes)) #This prints the list of volumes captured by the above command so the user can select the volume they wish to snapshot

vol_id = str(input("Enter Volume ID to snapshot: ")) #Requesting the user to enter the volume to create the snapshot from
volume = volumes[0] #Sets volume to the first position on the volumes output
description = str(input("Enter volume snapshot description: ")) #Requesting the snapshot description

 
if volume.create_snapshot(description): #Creates the snapshot adding the description entered above
    print ('Snapshot created with description: %s' % description) #Confirms snapshot is complete and provides description
 
snapshots = volume.snapshots() #Creates the list of current snapshots for the volume selected earlier

user_time = str(input("Enter date and time in UTC from when you want to delete snapshots, enter in the format Year-Month-Date Hours:Minutes:Seconds, eg 2015-3-4 14:00:00 : ")) #Requests the user to input the date and time in UTC and not local timezone from when the snapshots should be deleted
real_user_time = datetime.datetime.strptime(user_time, '%Y-%m-%d %H:%M:%S') #This converts the user_time from a string to a datetime object

for snap in snapshots: #This for loop firstly converts the start_time of the snapshots list into a datetime object, it then takes any snapshots older than the user specified date and the deletes them
    start_time = datetime.datetime.strptime(snap.start_time[:-5], '%Y-%m-%dT%H:%M:%S')
    if start_time < real_user_time:
        snap.delete()
        print (snap.delete)
