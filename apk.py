import requests
from bs4 import BeautifulSoup as bs
from dl import Downloader
USER_AGENT = "Mozilla/5.0 (Windows; U; Windows NT 10.0; en-US) AppleWebKit/604.1.38 (KHTML, like Gecko) Chrome/68.0.3325.162"

basic_headers = {
    "Accept-Encoding": "gzip, deflate",
    "User-Agent": USER_AGENT,
    "Upgrade-Insecure-Requests": "1",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "chrome-proxy": "frfr",
    "dnt": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
}
HOST = "https://apkmirror.com"


def search(term: str) -> None:
    url = f"https://www.apkmirror.com/?post_type=app_release&searchtype=apk&s={term}"
    app_url_class_name = "fontBlack"
    page = requests.get(url, headers=basic_headers)
    soup = bs(page.text, "html5lib")
    divs = soup.find_all("a", attrs={"class": app_url_class_name})
    for s in divs:
        print(f"{divs.index(s)+1}){s.attrs.get('href')}")
    try:
        x = int(input("Enter Number of the url you want to download:\n")) - 1
        main(HOST + divs[x].attrs.get("href"))
    except:
        print("Failed no url exists for this number")
    return


def dict_print(el: dict, v: bool = True) -> str:
    if v:
        total = []
        total.append("{\n")
        for r in el:
            total.append("\t%s:%s\n" % (r, el[r]))
        total.append("}\n")
    return "".join(total)


def main(url: str) -> None:
    app_url_class_name = "headerFont"
    page = requests.get(url, headers=basic_headers)
    soup = bs(page.text, "html5lib")
    divs = [
        s
        for s in soup.find_all(attrs={"class": app_url_class_name})
        if s.findChild("a")
    ]
    data = []
    for d in divs:
        details = "||".join([s.text for s in d.findChildren("div")[::-1][:3]])
        url = HOST + d.findChild("a").attrs.get("href", "")
        data.append({"URL": url, "details": details})
    for d in data:
        print(f"{data.index(d)+1}){dict_print(d)}")
    x = int(input("Enter Number of url you want to download:")) - 1
    try:
        urlm = data[x].get("URL")
    except:
        print("Error")
    print("Fetching:", urlm + "download/")
    page = requests.get(urlm + "download/", headers=basic_headers)
    soup = bs(page.text, "html5lib")
    link = soup.find(attrs={"data-google-vignette": "false"})
    if link:
        print(f"URL:{HOST+link.attrs['href']}")
        url = HOST + link.attrs["href"]
        d = Downloader(url)
        d.start()
if __name__ == "__main__":
    search(input("Enter Name of the app:"))

