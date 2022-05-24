import pandas as pd
from src.NLU import NaturalLanguageUnderstanding


class NaturalLanguageGenerator:
    def __init__(self):
        self.template_dir = "./cafe_search_template_dataset.csv"
        self.values = {
            "TEMP": "",
            "LOCATION": "",
            "PLACE": "",
            "RESTAURANT": "",
        }
        self.template = pd.read_csv(self.template_dir)
        self.nlu = nlu = NaturalLanguageUnderstanding()
        self.nlu.model_load()

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
            temp_index = template.find("{TEMP}")
            location_index = template.find("{LOCATION}")
            place_index = template.find("{PLACE}")
            restaurant_index = template.find("{RESTAURANT}")

            temp_flag = temp_index == -1
            location_flag = location_index == -1
            place_flag = place_index == -1
            restaurant_flag = restaurant_index == -1

            cnt = 0
            while not (temp_flag and location_flag and place_flag and restaurant_flag):
                if not temp_flag:
                    key = "TEMP"
                    temp_flag, template = self.replace_slot(temp_flag, key, template)
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

    def run_nlg(self, text):
        intent, predict = self.nlu.predict(text)
        print("intent:",intent)
        print("predict:", predict)
        # ood일 경우 ood에 관련된 대답을 함
        if intent == 'ood':
            result = self.nlu.ood_answer.return_answer(text)
            return result
        # ood가 아닐경우 탬플릿에 맞게 대답을 함
        else:
            nlu_result = self.nlu.convert_nlu_result(text, intent, predict)
            templates = self.search_template(nlu_result)
            result = self.filling_nlg_slot(templates)
            print("nlu_result:", nlu_result)
            print("templates:", templates)
            print("result:", result)
            return result
