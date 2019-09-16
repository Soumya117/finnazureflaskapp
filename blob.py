import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess
from logger import log

container_name ='finnblob'
account_name = 'accountName'
account_key = 'accountKey'

def writeBlob(file_name, text):
    log("Writing blob: {}".format(file_name))
    sys.stdout.flush()
    try:
        block_blob_service = BlockBlobService(account_name=account_name,
                                              account_key=account_key)
        block_blob_service.create_container(container_name)
        # Set the permission so the blobs are public.
        block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)
        block_blob_service.create_blob_from_text(container_name, file_name, text)
    except Exception as e:
        log("Error while writing blob..{}".format(e))

def readBlob(blobName):
    log("Reading blob: {}".format(blobName))
    sys.stdout.flush()
    blob = None
    try:
        block_blob_service = BlockBlobService(account_name=account_name,
                                              account_key=account_key)
        blob = block_blob_service.get_blob_to_text(container_name, blobName)
    except Exception as e:
        log("Error while reading blob..{}".format(e))
    return blob.content