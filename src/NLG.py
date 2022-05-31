import pandas as pd
from src.NLU import NaturalLanguageUnderstanding
import re
from cart.views import add2

class NaturalLanguageGenerator:
    def __init__(self):
        self.template_dir = "./cafe_search_template_dataset.csv"
        self.values = {
            "TEMP": "",
            "SIZE": "",
            "COUNT": "",
            "COFFEE": "",
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
            if slot_name == 'TEMP':
                if (slot_value.find('뜨') != -1) or (slot_value.find('따') != -1) or (slot_value.find('핫') != -1):
                    slot_value = '뜨거운'
                elif (slot_value.find('시원') != -1) or (slot_value.find('차') != -1) or (slot_value.find('아이스') != -1):
                    slot_value = '아이스'
            elif slot_name == 'SIZE':
                if (slot_value.find('작') != -1) or (slot_value.find('레귤러') != -1) or \
                        (slot_value.find('스몰') != -1) or (slot_value.find('숏') != -1):
                    slot_value = '스몰 사이즈'
                elif (slot_value.find('빅') != -1) or (slot_value.find('톨') != -1) or (slot_value.find('라지') != -1) or \
                        (slot_value.find('업') != -1) or (slot_value.find('큰') != -1) or (slot_value.find('그란데') != -1) or\
                        (slot_value.find('벤티') != -1):
                    slot_value = '라지 사이즈'
            elif slot_name == 'COUNT':
                slot_value = slot_value.replace(' 잔', '잔')
                slot_value = slot_value.replace('잔', '')
                slot_value = slot_value.replace(' 개', '개')
                slot_value = slot_value.replace('개', '')
                slot_value = slot_value.replace(' 조각', '조각')
                slot_value = slot_value.replace('조각', '')
                slot_value = slot_value.replace(' 봉지', '봉지')
                slot_value = slot_value.replace('봉지', '')
            print('slot_name',slot_name)
            print('slot_value',slot_value)
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
            size_index = template.find("{SIZE}")
            count_index = template.find("{COUNT}")
            coffee_index = template.find("{COFFEE}")

            temp_flag = temp_index == -1
            size_flag = size_index == -1
            count_flag = count_index == -1
            coffee_flag = coffee_index == -1

            cnt = 0
            while not (temp_flag and size_flag and count_flag and coffee_flag):
                if not temp_flag:
                    key = "TEMP"
                    temp_flag, template = self.replace_slot(temp_flag, key, template)
                if not size_flag:
                    key = "SIZE"
                    size_flag, template = self.replace_slot(size_flag, key, template)
                if not count_flag:
                    key = "COUNT"
                    count_flag, template = self.replace_slot(count_flag, key, template)
                if not coffee_flag:
                    key = "COFFEE"
                    coffee_flag, template = self.replace_slot(coffee_flag, key, template)
                filling_templates.append(template)
        return filling_templates

    def text_preprocessing(self, text):
        text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', text)  # 특수문자 제거
        text = re.sub('만 ', ' ', text)
        text = re.sub('도 ', ' ', text)
        text = re.sub('로 ', ' ', text)
        text = re.sub('라뗴', '라떼', text)
        text = re.sub('쥬스', '주스', text)
        text = re.sub('뜨신거', '따뜻한거', text)
        text = re.sub('따신거', '따뜻한거', text)
        text = re.sub('티라미수', '티라미슈', text)
        text = re.sub('티라미스', '티라미슈', text)
        text = re.sub('아인슈패너', '아인슈페너', text)
        text = re.sub('마키아토', '마끼아또', text)
        text = re.sub('마끼야또', '마끼아또', text)
        text = re.sub('캐러멜', '카라멜', text)
        text = re.sub('카라맬', '카라멜', text)
        text = re.sub('캬라멜', '카라멜', text)
        text = re.sub('캬라맬', '카라멜', text)
        text = re.sub('캐러맬', '카라멜', text)
        text = re.sub('이요', '', text)
        text = re.sub('잔요', '잔', text)
        text = re.sub('잔', ' 잔', text)
        text = re.sub('  잔', ' 잔', text)
        text = re.sub('개', ' 잔', text)
        text = re.sub('  개', ' 잔', text)
        text = re.sub('조각', ' 잔', text)
        text = re.sub('  조각', ' 잔', text)
        text = re.sub('봉지', ' 잔', text)
        text = re.sub('  봉지', ' 잔', text)
        text = re.sub('하나', '1잔', text)
        text = re.sub('한잔', '1잔', text)
        text = re.sub('한 ', '1 ', text)
        text = re.sub('둘', '2', text)
        text = re.sub('두 ', '2 ', text)
        text = re.sub('셋', '3', text)
        text = re.sub('세 ', '3 ', text)
        text = re.sub('넷', '4', text)
        text = re.sub('네 ', '4 ', text)
        text = re.sub('다섯', '5', text)
        text = re.sub(' 잔', '잔', text)
        return text

    def run_nlg(self, request, text):
        ptext = self.text_preprocessing(text)
        print('ptext',ptext)
        intent, predict = self.nlu.predict(ptext)
        print("intent:",intent)
        # ood일 경우 ood에 관련된 대답을 함
        if intent == 'ood':
            result = self.nlu.ood_answer.return_answer(ptext)
            return result
        # ood가 아닐경우 탬플릿에 맞게 대답을 함
        elif intent == '결제요청':
            # 결제 함수 실행
            data = {'temp':'C',
                    'size':'S',
                    'quantity': 1,
                    'product_id': 3
                    }
            add2(request, data)
            text = '장바구니에 담겼습니다.'
            return text
        else:
            nlu_result = self.nlu.convert_nlu_result(ptext, intent, predict)
            templates = self.search_template(nlu_result)
            result = self.filling_nlg_slot(templates)
            print("nlu_result:", nlu_result)
            print("templates:", templates)
            print("result:", result)
            return result
