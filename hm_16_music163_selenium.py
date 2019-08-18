from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
import json


class Music163Spider:
    def __init__(self):
        chrome_options = Options()
        # 沒有這一行會自動開啟瀏覽器
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=chrome_options,
                                       executable_path=r'D:\Study\Python2\chromedriver\chromedriver.exe')
        self.start_url = "https://music.163.com/#/discover/playlist"
        self.result_list = []
        self.domainname = "https://music.163.com"
        self.result_list = []
        self.result_dict = {}

    def get_content_list(self):
        print(self.driver.current_url)
        self.driver.get(self.driver.current_url)
        # time.sleep(3)
        i = self.driver.find_element_by_tag_name("iframe")
        print("i=", i)
        self.driver.switch_to.frame(i)
        # time.sleep(3)
        # wait = WebDriverWait(self.driver, 10)
        # # # VIP，内容加载完成后爬取
        # wait.until(
        #     lambda driver: driver.find_elements_by_xpath("//div[@class='g-bd']/div[@class='g-wrap p-pl f-pr']/ul/li"))

        li_list = self.driver.find_elements_by_xpath("//div[@class='g-bd']/div[@class='g-wrap p-pl f-pr']/ul/li")
        print(len(li_list))
        for li in li_list:
            item = {}
            item["title"] = li.find_element_by_xpath("./p[@class='dec']/a").text
            item["author"] = li.find_element_by_xpath("./p[last()]/a").text
            item["cover_img"] = li.find_element_by_xpath("./div[@class='u-cover u-cover-1']/img").get_attribute("src")
            item["counts"] = li.find_element_by_xpath("./div[@class='u-cover u-cover-1']/div[@class='bottom']/span[@class='nb']").text
            # print(item["counts"])
            self.result_list.append(item)
        # 翻頁
        next_url = self.driver.find_elements_by_xpath("//div[@id='m-pl-pager']/div[@class='u-page']/a[last()][@class='zbtn znxt']")
        if len(next_url) > 0:
            self.driver.execute_script('arguments[0].scrollIntoView();', next_url[-1])  # 拖动到可见的元素去
            # next_url = next_url[0].get_attribute("href")
            next_url = next_url[0]
        else:
            next_url = None

        return next_url

    def run(self):   # 主要實現邏輯
        print("music163爬蟲開始....")
        # 1. 取得start_url
        self.driver.get(self.start_url)
        # # 2. 獲取響應,取得資料
        next_url = self.get_content_list()
        print(next_url)
        n = 1
        while next_url is not None:
            n += 1
            print("n=%d" % n)
            next_url.click()
            next_url = self.get_content_list()

        self.result_dict["Result"] = self.result_list
        # 保存
        with open("網易雲音樂.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(self.result_dict, ensure_ascii=False, indent=2))
        print("music163爬蟲結束")


if __name__ == "__main__":
    music163spider = Music163Spider()
    music163spider.run()