import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess

container_name ='finnblob'

def upload(file_name, path):
    print("Ruuning blob setup")
    sys.stdout.flush()
    try:
        block_blob_service = BlockBlobService(account_name='finnminingblob', account_key='rCzjwJWgDl10l+9SBw1C0iWnKOMDmN9PES083C+gim+ZPEbfPg6rLU4D4bk/URNw2CLxG2e8bWQzW3C4QROhWw==')
        block_blob_service.create_container(container_name)
        # Set the permission so the blobs are public.
        block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)
        print("Uploading files...")
        sys.stdout.flush()
        block_blob_service.create_blob_from_path(container_name, file_name, path)
    except Exception as e:
        print("Error while blobing..: ",e)
