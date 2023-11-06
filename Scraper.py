from datetime import datetime
import requests
import json

from bs4 import BeautifulSoup as bs4, PageElement


class Scraper:
    updateDate: dict

    def __init__(self):
        self.url = "https://base-donnees-publique.medicaments.gouv.fr/telechargement.php"
        self._load_updateDate()

    def get_files_to_download(self):
        res = requests.get(self.url)

        if not res.ok:
            raise Exception(f"Erreur lors de la requête, url: {self.url}")

        soup = bs4(res.text, "html.parser")

        urls_to_donwload = []
        ul = soup.find_all("ul")[0]
        for li in ul.find_all_next("li"):
            # == Get str == #
            if "(génération en direct)" in li.text:
                file_url = self._get_a_href_from_li(li)
                urls_to_donwload.append(file_url)

            if "mise à jour" not in li.text:
                continue

            date_str = li.text.split("mise à jour : ")[1]
            date_str = date_str.split(", ")[0]

            file_name = li.text.split("Fichier des ")[1]
            file_name = file_name.split(" (date de mise")[0]

            file_url = self._get_a_href_from_li(li)

            # == Save in json == #
            if file_name not in self.updateDate:
                self.updateDate[file_name] = date_str
                urls_to_donwload.append(file_url)
            else:
                new_date = datetime.strptime(date_str, "%d/%m/%Y")
                old_date = datetime.strptime(self.updateDate[file_name], "%d/%m/%Y")

                if new_date > old_date:
                    self.updateDate[file_name] = date_str
                    urls_to_donwload.append(file_url)

        self._save_updateDate()
        return urls_to_donwload

    def _get_a_href_from_li(self, tag_li: PageElement) -> str:
        for a in tag_li.find_all_next("a"):
            return self.url + a["href"]

        return ""

    def download_file(self, url: str):
        filename = self._get_name_by_url(url)

        params = {"downloadformat": "csv"}
        res = requests.get(url, params=params)

        if not res.ok:
            raise Exception(f"Erreur lors de la requête, url: {url}")

        open(f"csv/{filename}", "wb").write(res.content)
        print(f"💾 {filename} téléchargé")
        return filename

    def _load_updateDate(self):
        try:
            self.updateDate = json.load(open("./updateDate.json", "r", encoding="utf-8"))
        except:
            self.updateDate = {}

    def _save_updateDate(self):
        json.dump(self.updateDate, open("./updateDate.json", "w", encoding="utf-8"))

    def _get_name_by_url(self, url: str) -> str:
        return url.split("?fichier=")[1]
