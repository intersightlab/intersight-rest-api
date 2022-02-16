"""
    intersight_ops.py - shows how to use intersight REST API

    author: 
"""
import json
import requests

from intersight_auth import IntersightAuth
############ Users Need to Update following Code ##################################
# Create an AUTH object
AUTH = IntersightAuth(
    # Secret Key file location downloaded from Intersight
    secret_key_filename='C:\\Users\\administrator\\Downloads\\SecretKey.txt',
    # APID Key ID for the Intersight Account
    api_key_id='replace with api key ID'
    )
## Replace X with POD Number ####
PODno='POD01'
## This script assume your Organization Name same as PODX
MyOrg=PODno 
## Change the value to True for only the Required REST Operation, others should be False ##
rest_get=True           # For GET operation
rest_post=False         # For POST operation
rest_patch=False        # For PATCH operation
rest_delete=False       # For DELETE operation
############ Do not Edit Code below this ###########################################
# Intersight REST API Base URL
BURL = 'https://www.intersight.com/api/v1/'

if __name__ == "__main__":

    # Details for intersight operations, GET, POST, PATCH, DELETE
    # OPERATIONS array
    OPERATIONS = [
        {
            "request_process":rest_get,
            "resource_path":"ntp/Policies",
            "request_method":"GET"
        },
        {
            "request_process":rest_post,
            "resource_path":"ntp/Policies",
            "request_method":"POST",
            "request_body":{
                "Enabled":True,
                "Name":PODno+"-ntp-policy",
                "Organization":"MyOrgid",
                "Description":"NTP Policy for ntp.org",
                "NtpServers":[
                    "pool.ntp.org"
                    ],
                "Tags":[]
            }
        },
        {
            "request_process":rest_patch,
            "resource_name":PODno+"-ntp-policy",
            "resource_path":"ntp/Policies",
            "request_method":"PATCH",
            "request_body":{
                "NtpServers":[
                    "pool.ntp.org",
                    "10.20.1.6"
                    ]
                }
        },
        {
            "request_process":rest_delete,
            "resource_name":PODno+"-ntp-policy",
            "resource_path":"ntp/Policies",
            "request_method":"DELETE"
        }
    ]

    # iterate each Operation object from Operations array
    for operation in OPERATIONS:
        # Checking operation object need to run the Operation
        if operation['request_process']:
            response = None
            print(operation['request_method'])
            # GET Operation
            if operation['request_method'] == "GET":
                response = requests.get(
                    BURL + operation['resource_path'],
                    auth=AUTH
                    )
            # POST Operation
            if operation['request_method'] == "POST":
                #GET the Moid of the Organization
                response = requests.get(
                    (
                        BURL + 'organization/Organizations' +
                        "?$filter=Name eq '" + MyOrg + "'"
                        ),
                    auth=AUTH
                    )
                # Extract the Moid from the Results
                json_result = json.loads(response.text)
                moid = json_result["Results"][0]["Moid"]
                # Replace Organization ID with moid in Request body and run the POST operation
                response = requests.post(
                    BURL + operation['resource_path'],
                    data=json.dumps(operation['request_body']).replace('MyOrgid',moid),
                    auth=AUTH
                    )
            # PATCH Operation
            if operation['request_method'] == "PATCH":
                # GET the Moid of the resource to PATCH
                response = requests.get(
                    (
                        BURL + operation['resource_path'] +
                        "?$filter=Name eq '" + operation['resource_name'] + "'"
                        ),
                    auth=AUTH
                    )
                # Extract the Moid from the Results
                json_result = json.loads(response.text)
                moid = json_result["Results"][0]["Moid"]

                response = requests.patch(
                    BURL + operation['resource_path'] + "/" + moid,
                    data=json.dumps(operation['request_body']),
                    auth=AUTH
                    )
            # DELETE Operation
            if operation['request_method'] == "DELETE":
                # GET the Moid of the resource to DELETE
                response = requests.get(
                    (
                        BURL + operation['resource_path'] +
                        "?$filter=Name eq '" + operation['resource_name'] + "'"
                        ),
                    auth=AUTH
                    )
                # Extract the Moid from the Results
                json_result = json.loads(response.text)
                moid = json_result["Results"][0]["Moid"]

                response = requests.delete(
                    BURL + operation['resource_path'] + "/" + moid,
                    auth=AUTH
                    )

            print(response)
            print(response.text)
