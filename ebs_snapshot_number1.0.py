#Built with Python 3.3.2
#This script allows for the interactive input from a user to create an EBS volume snapshot and select how many snapshots should be retained
#The script will prompt for access & secret keys as well as region information
#The script will then prompt to enter the volume to snapshot and the amount of snapshots to keep, finally the script will request a description for the snapshot
import boto.ec2
from boto.ec2.connection import EC2Connection
from boto.ec2.regioninfo import RegionInfo
from boto.ec2.snapshot import Snapshot
import datetime
from functools import cmp_to_key
 
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
keep = int(input("Enter number of snapshots to keep:  ")) #Requesting the user to enter the number of snapshots to maintain for the volume, eg 2 will keep the snapshot created and 1 other, 0 will delete all snapshots including the snapshot created in this script
volume = volumes[0] #Sets volume to the first position on the volumes output
description = str(input("Enter volume snapshot description: ")) #Requesting the snapshot description

 
if volume.create_snapshot(description): #Creates the snapshot adding the description entered above
    print ('Snapshot created with description: %s' % description) #Confirms snapshot is complete and provides description
 
snapshots = volume.snapshots() #Creates the list of current snapshots for the volume selected earlier
print (snapshots) #Displays the list of snapshots for this volume

def date_compare(snap1, snap2): #This function compares the snapshot start times and used by a call from a sort so we can order the snapshots so we delete only the oldest snapshots
    if snap1.start_time < snap2.start_time:
        return -1
    elif snap1.start_time == snap2.start_time:
        return 0
    return 1

snapshots.sort(key=cmp_to_key(date_compare)) #This calls the date compare and sorts the snapshots in order by start time so we delete only the oldest snapshots first
delta = len(snapshots) - keep #Delta uses the keep input from the user and determines how many snapshots are to be deleted
for i in range(delta): #This for loop takes the number of snapshots to delete from delta and then uses the ordered snapshot list to then delete only the oldest snapshots and the amount specified by delta
    print ('Deleting snapshot %s' % snapshots[i].description)
    snapshots[i].delete()

