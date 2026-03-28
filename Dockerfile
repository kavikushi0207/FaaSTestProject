# 1. Start with the official Azure Functions Python base image
FROM --platform=linux/amd64 mcr.microsoft.com/azure-functions/python:4-python3.10 
#I took this specifically, becausemy mac has an M1 chip, and I want to make sure the image is compatible with my architecture. If you're using a different architecture, you might need to adjust this.

# 2. Tell the container where the code will live
ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

# 3. Copy your requirements.txt into the container first
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

# 4. Copy everything from your local folder into the container
COPY . /home/site/wwwroot

