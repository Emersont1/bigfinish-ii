import imp
import requests
import re
from zipfile import ZipFile
import os

import big_finish

from pathlib import Path
from clint.textui import progress

def download_image(id, path):
    rsp = requests.get(f"https://www.bigfinish.com/image/release/{id}/large.jpg", stream=True)
    with open(f"{path}/cover.jpg", "wb") as f:
        for chunk in rsp.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()

def download(session, url, path):
    rsp = session.get(f"https://www.bigfinish.com/{url}", stream=True)
    cd = rsp.headers.get("Content-Disposition")
    filename = re.search(r'filename="(.+)"', cd).group(1)

    if os.path.exists(f"{path}/{filename}"):
        if os.path.getsize(f"{path}/{filename}") == rsp.headers.get("Content-Length"):
            print(f"{filename} already exists, skipping")
            return f"{path}/{filename}", False
        else:
            print(f"{filename} exists but is incomplete, downloading again")

    with open(f"{path}/{filename}", "wb") as f:
        total_length = int(rsp.headers.get('content-length'))
        for chunk in progress.bar(rsp.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()
    return f"{path}/{filename}", True



def main():
    print("Logging in...")
    email = input("Email: ")
    password = input("Password: ")
    s = big_finish.login(email, password)
    print ("Logged in!")
    print("Fetching products...")
    ps = big_finish.get_library(s)
    print("Fetched products...")

    media_dir = input("Media directory: ")
    if not media_dir:
        media_dir = "media"

    archive_dir = input("Archive directory: ")
    if not archive_dir:
        archive_dir = "archive"

    for id, path, mains, supps in ps:
        print(f"Downloading {path}")
        a_path = f"{archive_dir}/{path}"
        m_path = f"{media_dir}/{path}"
        Path(a_path).mkdir(parents=True, exist_ok=True)
        Path(m_path).mkdir(parents=True, exist_ok=True)
        
        download_image(id, a_path)
        download_image(id, m_path)

        for main in mains:
            path, try_extract = download(s, main, a_path)
            # We want to extract the M4Bs only
            if re.search(r'\.ab.\.zip$', path) and try_extract:
                print(f"Extracting M4B zip at {path}")
                with ZipFile(path, 'r') as zipObj:
                    for f in zipObj.namelist():
                        if f.endswith(".m4b") and not f.startswith("__MACOSX"):
                            filename = f.split("/")[-1]
                            print(f"Extracting {filename}")
                            with open(f"{m_path}/{filename}", "wb") as g:
                                g.write(zipObj.read(f))
                            print(f"Extracted {filename}")


        for supp in supps:
            Path(f"{a_path}/bonus").mkdir(parents=True, exist_ok=True)
            download(s, supp, f"{a_path}/bonus")


if __name__ == "__main__":
    main()
