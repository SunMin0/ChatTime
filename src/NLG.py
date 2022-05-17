import pandas as pd
import requests
from bs4 import BeautifulSoup
from src.NLU import NaturalLanguageUnderstanding


class NaturalLanguageGenerator:
    def __init__(self):
        self.template_dir = "./search_template_dataset.csv"
        self.values = {
            "DATE": "",
            "LOCATION": "",
            "PLACE": "",
            "RESTAURANT": "",
        }
        self.template = pd.read_csv(self.template_dir)

    def make_search_key(self, nlu_result):
        intent = nlu_result.get("INTENT")
        keys = set()
        for name_value in nlu_result.get("SLOT"):
            slot_name = name_value.split("^")[0]
            slot_value = name_value.split("^")[1]
            keys.add(slot_name)
            self.values[slot_name] = slot_value
        slots = "^".join(keys)
        return intent, slots

    def search_template(self, nlu_result):
        intent, slots = self.make_search_key(nlu_result)
        matched_template = []

        for data in self.template.iterrows():
            intent_flag = False
            slot_flag = False

            row = data[1]
            if row['label'] == intent:
                intent_flag = True

            if isinstance(row.get("slot"), str):
                template_slots = sorted(row["slot"].split("^"))
                key_slots = sorted(slots.split("^"))
                if template_slots == key_slots:
                    slot_flag = True
            elif slots == "":
                slot_flag = True

            if intent_flag and slot_flag:
                matched_template.append(row["template"])

        return matched_template

    def replace_slot(self, flag, key, template):
        value = self.values.get(key)
        key = "{" + key + "}"
        if value != "":
            template = template.replace(key, value)
        else:
            template = ""
        flag = not flag
        return flag, template

    def filling_nlg_slot(self, templates):
        filling_templates = []

        for template in templates:
            date_index = template.find("{DATE}")
            location_index = template.find("{LOCATION}")
            place_index = template.find("{PLACE}")
            restaurant_index = template.find("{RESTAURANT}")

            date_flag = date_index == -1
            location_flag = location_index == -1
            place_flag = place_index == -1
            restaurant_flag = restaurant_index == -1

            cnt = 0
            while not (date_flag and location_flag and place_flag and restaurant_flag):
                if not date_flag:
                    key = "DATE"
                    date_flag, template = self.replace_slot(date_flag, key, template)
                if not location_flag:
                    key = "LOCATION"
                    location_flag, template = self.replace_slot(location_flag, key, template)
                if not place_flag:
                    key = "PLACE"
                    place_flag, template = self.replace_slot(place_flag, key, template)
                if not restaurant_flag:
                    key = "RESTAURANT"
                    restaurant_flag, template = self.replace_slot(restaurant_flag, key, template)
                filling_templates.append(template)
        return filling_templates

    def filling_crawl_slot(self, intent, template):
        nlu = NaturalLanguageUnderstanding()
        intent_key_list = list(nlu.dataset.intent_label.keys())
        search_text = ""
        search_keyword = {"dust":"미세먼지","restaurant":"맛집","travel":"관광지","weather":"날씨"}
        key_list = list(self.values.keys())
        for key in key_list:
            if self.values[key] != "":
                search_text = search_text + str(self.values[key]) + " "
            else:
                continue
        for intent_key in intent_key_list:
            if intent == intent_key:
                search_text = search_text + search_keyword[intent]
                search_result = self.crawl(search_text)
                template[0] = template[0].replace("{CRAWL}입니다.", "'%s'입니다." % search_result)
        return template

    def crawl(self, text):
        url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query="\
               + text.replace(" ", "+")
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')
        if "미세먼지" in text:
            select, select_am, select_pm = "", "", ""
            if "내일" in text:
                select_am = select_am + soup.select("dl")[2].text
                select_am = select_am.split()[0] + " " + select_am.split()[1]
                select_pm = select_pm + soup.select("dl")[3].text
                select_pm = select_pm.split()[0] + " " + select_pm.split()[1]
            elif "모레" in text:
                select_am = select_am + soup.select("dl")[4].text
                select_am = select_am.split()[0] + " " + select_am.split()[1]
                select_pm = select_pm + soup.select("dl")[5].text
                select_pm = select_pm.split()[0] + " " + select_pm.split()[1]
            else:
                select_am = select_am + soup.select("dl")[0].text
                select_am = select_am.split()[0] + " " + select_am.split()[1]
                select_pm = select_pm + soup.select("dl")[1].text
                select_pm = select_pm.split()[0] + " " + select_pm.split()[1]
            select = select_am + " " + select_pm
        elif "날씨" in text:
            print(text)
        return select

    def run_nlg(self, text):
        nlu = NaturalLanguageUnderstanding()
        nlu.model_load()
        intent, predict = nlu.predict(text)
        print("intent:",intent)
        print("predict:", predict)
        nlu_result = nlu.convert_nlu_result(text, intent, predict)
        print("nlu_result:", nlu_result)
        templates = self.search_template(nlu_result)
        print("templates:", templates)
        result = self.filling_nlg_slot(templates)
        print("result:", result)
        try:
            result = self.filling_crawl_slot(intent, result)
        except:
            print("크롤링 함수 실패")
        return result
