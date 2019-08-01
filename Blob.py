import sys
print(sys.path)
sys.path.insert( 0, '/usr/local/lib/python3.5/dist-packages')

import os, uuid
from azure.storage.blob import BlockBlobService, PublicAccess

container_name ='finnblob'

def upload(file_name, path):
    print("Ruuning blob setup")
    sys.stdout.flush()
    try:
        block_blob_service = BlockBlobService(account_name='accountName', account_key='accountKey')

        block_blob_service.create_container(container_name)

        # Set the permission so the blobs are public.
        block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)
        print("Uploading files...")
        sys.stdout.flush()
        block_blob_service.create_blob_from_path(container_name, file_name, path)
    except Exception as e:
        print(e)

def run_sample():
    try:
        # Create the BlockBlockService that is used to call the Blob service for the storage account
        block_blob_service = BlockBlobService(account_name='accountName', account_key='accountKey')

        # Create a container called 'quickstartblobs'.
        block_blob_service.create_container(container_name)

        # Set the permission so the blobs are public.
        block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)

        # Create a file in Documents to test the upload and download.
        local_path="json/"
        local_file_name ="blob_json.txt"
        full_path_to_file =os.path.join(local_path, local_file_name)

        # Write text to the file.
        file = open(full_path_to_file,  'w')
        file.write("Hello, My World..")
        file.close()

        print("Temp file = " + full_path_to_file)
        print("\nUploading to Blob storage as: " + local_file_name)

        # Upload the created file, use local_file_name for the blob name
        block_blob_service.create_blob_from_path(container_name, local_file_name, full_path_to_file)

        # List the blobs in the container
        print("\nList blobs in the container")
        generator = block_blob_service.list_blobs(container_name)
        for blob in generator:
            print("\t Blob name: " + blob.name)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    run_sample()
