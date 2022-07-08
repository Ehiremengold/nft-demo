import os
from pathlib import Path
import requests


def main():
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    payload = {
        "pinataOptions": '{"cidVersion": 1}',
        "pinataMetadata": '{"name": "pug", "keyvalues": {"company": "bluecube"}}',
    }

    files = [
        (
            "file",
            (
                "pug.png",
                open("./img/pug.png", "rb"),
                "application/octet-stream",
            ),
        )
    ]
    headers = {
        # "Authorization": os.getenv("PINATA_JWT"),
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.json())
