import json
import requests
import re
import zipfile
from bs4 import BeautifulSoup
from contextlib import closing


class AddonsUpdater:
    download_path = "./Downloaded_Addons"
    download_suffix = ".zip"

    def __init__(self):
        self.wow_path = ""
        self.addons_page = []
        self.addons_info = []
        self.count_of_addons = -1
        self.saved_info = []
        self.updates_info = []

        self.load_config()
        self.load_saved_info()

    def load_config(self):
        with open("./请配置这里.txt", 'r') as f:
            for line in f.readlines():
                if -1 == self.count_of_addons:
                    self.wow_path = line.strip()
                    print("安装路径：" + self.wow_path)
                else:
                    self.addons_page.append(line.strip())
                self.count_of_addons += 1
            print("插件总数：", self.count_of_addons)

    def load_saved_info(self):
        try:
            with open('savedInfo.txt', 'r') as f:
                self.saved_info = json.load(f)
        except json.decoder.JSONDecodeError:
            print("Load SavedInfo Error!")

    def if_addon_need_update(self, addon):
        for i in self.saved_info:
            if i["id"] == addon["id"]:
                if i["version"] == addon["version"]:
                    print(addon["name"] + " 已是最新版")
                    return False
                else:
                    print(addon["name"] + " 需要更新")
                    return True
        print(addon["name"] + " 需要更新")
        return True

    def get_addons_will_update(self):
        for addon in self.addons_info:
            if self.if_addon_need_update(addon):
                self.updates_info.append(addon)

    def retrieve_addons_info(self):
        load_count = 0
        for addon_page in self.addons_page:
            load_count += 1
            progress = (load_count / self.count_of_addons) * 100
            self.addons_info.append(get_addon_info(addon_page))
            print("\r查询进度：%d%%" % progress, end=" ")
            print('\n')

    def download_and_unzip_addons(self):
        for update_info in self.updates_info:
            download_addon(update_info)
            unzip_file(update_info)

    def unload_saved_info(self):
        with open('./savedInfo.txt', 'w') as f:
            json.dump(self.addons_info, f)


def get_addon_info(url):
    url_prefix = ''
    if re.search("curseforge", url):
        url_prefix = "https://wow.curseforge.com"
    elif re.search("wowace", url):
        url_prefix = "https://www.wowace.com"
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")
    addon_name = soup.find("span", class_="overflow-tip").string
    print("插件名称：" + addon_name)
    download_url = url_prefix + soup.find('a', "fa-icon-download")["href"]
    print("下载链接：" + download_url)
    addon_version = soup.find("abbr", class_="tip standard-date standard-datetime")["data-epoch"]
    print("插件版本：" + addon_version)
    addon_id = soup.find("div", class_="info-data").string
    print("插件ID：" + addon_id)

    return dict(name=addon_name, url=download_url, version=addon_version, id=addon_id)


def download_addon(addon):
    print("下载插件 " + addon["name"] + " 中...")
    with closing(requests.get(addon["url"], stream=True)) as response:
        chunk_size = 500 * 1024  # 单次请求最大值
        content_size = int(response.headers['content-length'])  # 内容体总大小
        data_count = 0
        with open(AddonsUpdater.download_path + '/' + addon["id"] + AddonsUpdater.download_suffix, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                data_count = data_count + len(data)
                download_progress = (data_count / content_size) * 100
                print("\r文件下载进度：%d%%(%d/%d) - %s" % (
                    download_progress, data_count, content_size, addon["id"] + AddonsUpdater.download_suffix), end='')


def unzip_file(addon):
    print("解压插件 " + addon["name"] + " 中...")
    addon_zip = zipfile.ZipFile(AddonsUpdater.download_path + '/' + addon["id"] + AddonsUpdater.download_suffix)
    addon_zip.extractall("./Interface/Addons")


if __name__ == '__main__':
    au = AddonsUpdater()

    au.retrieve_addons_info()
    au.get_addons_will_update()
    au.download_and_unzip_addons()
    au.unload_saved_info()
