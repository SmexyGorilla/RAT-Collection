import requests
import os

def get_top_level_folders(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/"
    response = requests.get(url)
    if response.status_code == 200:
        contents = response.json()
        folders = [item["name"] for item in contents if item["type"] == "dir"]
        return folders
    else:
        print(f"Error: Unable to fetch contents (status code: {response.status_code})")
        return []

def download_folder(owner, repo, folder_name, save_path):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{folder_name}"
    response = requests.get(url)
    if response.status_code == 200:
        contents = response.json()
        os.makedirs(save_path, exist_ok=True)
        for item in contents:
            if item["type"] == "file":
                file_url = item["download_url"]
                file_response = requests.get(file_url)
                file_path = os.path.join(save_path, item["name"])
                with open(file_path, "wb") as file:
                    file.write(file_response.content)
                print(f"Downloaded: {item['name']}")
    else:
        print(f"Error: Unable to fetch folder contents (status code: {response.status_code})")

owner = "SmexyGorilla"
repo = "RAT-Collection"
folders = get_top_level_folders(owner, repo)
if folders:
    print("Top-level folders:")
    for i, folder in enumerate(folders, start=1):
        print(f"{i}. {folder}")
    choice = int(input("Enter the number of the folder you want to download: "))
    selected_folder = folders[choice - 1]
    save_path = input("Enter the folder where you want to save the files: ")
    print(f"Downloading contents of folder: {selected_folder}")
    download_folder(owner, repo, selected_folder, save_path=save_path)
else:
    print("No folders found or an error occurred.")
