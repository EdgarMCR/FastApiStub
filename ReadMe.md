# Upload Example

1. Configure an Azure storage account and create a container called `upload`.
2. Generate a SAS connection string for the account.
![AzureCreateUploadLink.png](docs%2FAzureCreateUploadLink.png)
3. Run `api.py` and send a request with e.g. Postman
![PostmanRequest.png](docs%2FPostmanRequest.png)
Here the postman collection: [FastApiUpload.postman_collection.json](docs%2FFastApiUpload.postman_collection.json)
4. Profit
![AzureUploadedFile.png](docs%2FAzureUploadedFile.png)