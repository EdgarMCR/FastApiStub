
import os
import json
from typing import Annotated

from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from azure.storage.blob import BlobServiceClient


class Item(BaseModel):
    download_link: str
    upload_link: str
    setting1: str
    setting2: str


class UploadItem(BaseModel):
    upload_link: str
    setting1: str
    setting2: str


app = FastAPI()


@app.post("/process-links")
async def process_links(item: Item):
    """ Example: download from link, and upload a list of contents to the upload link."""
    blob_service_client = BlobServiceClient.from_connection_string(item.download_link)
    container_client = blob_service_client.get_container_client(os.path.basename(item.download_link))

    blobs_list = container_client.list_blobs()
    contents = [blob.name for blob in blobs_list]

    with open('contents.json', 'w') as f:
        json.dump(contents, f)

    blob_service_client = BlobServiceClient.from_connection_string(item.upload_link)
    blob_client = blob_service_client.get_blob_client(os.path.basename(item.upload_link), 'contents.json')

    with open('contents.json', 'rb') as data:
        blob_client.upload_blob(data)


@app.post("/upload-video")
async def upload_video(upload_connection_string: Annotated[str, Form()], file: UploadFile = File(...)):
    """ Receive a file and upload output to the upload link. """

    with open(file.filename, 'wb') as f:
        f.write(await file.read())

    contents = {'filename': file.filename}#, 'setting1': item.setting1, 'setting2': item.setting2}
    with open('contents.json', 'w') as f:
        json.dump(contents, f)

    blob_service_client = BlobServiceClient.from_connection_string(upload_connection_string)
    blob_client = blob_service_client.get_blob_client('upload', 'contents.json')

    with open('contents.json', 'rb') as data:
        blob_client.upload_blob(data)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=4000)
