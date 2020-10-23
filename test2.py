from pprint import pprint

import dropbox
DB_TOKEN = "RfH15ItBqVcAAAAAAAAAAYaswJ3ZlkUbgdAQhW48JTssGkQ_Vs4mI6xtDtWPoQjN"
dbx = dropbox.Dropbox(DB_TOKEN)

url = "https://www.dropbox.com/sh/ojpfbx89bygzq00/AAAwQuBhayP_cQ1enL50OmvAa?dl=0"
# shared_link = dropbox.files.SharedLink(url=url)shared_link = dropbox.files.SharedLink(url=url)
# shared_link =
def dsasd():
    enteries = dbx.files_list_folder(path="/графики смен")._entries_value
    for folder in enteries:
        print(folder.name)
    # print(dbx.files_list_folder(path="/графики смен")._entries_value[1].name)

if __name__ == '__main__':
    dsasd()
    print("Example:")
