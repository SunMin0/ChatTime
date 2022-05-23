import json
import random
import pandas as pd
import torch
from torch.utils.data import TensorDataset
import torch.utils.data as data

class Preprocessing:
    def __init__(self, max_len=20):
        self.max_len = max_len
        self.PAD = 0

    def pad_idx_sequencing(self, q_vec):
        q_len = len(q_vec)
        diff_len = q_len - self.max_len
        if diff_len > 0:
            q_vec = q_vec[:self.max_len]
            q_len = self.max_len
        else:
            pad_vac = [0] * abs(diff_len)
            q_vec += pad_vac

        return q_vec


class EntityDataset(data.Dataset):
    def __init__(self, x_tensor, y_tensor, lengths):
        super(EntityDataset, self).__init__()
        self.x = x_tensor
        self.y = y_tensor
        self.lengths = lengths

    def __getitem__(self, index):
        return self.x[index], self.y[index], self.lengths[index]

    def __len__(self):
        return len(self.x)


class MakeDataset:
    def __init__(self):
        self.intent_data_dir = "./cafe_intent_data.csv"
        self.intent_label_dir = "./cafe_intent_label.json"
        self.entity_data_dir = "./cafe_entity_data.csv"
        self.entity_label_dir = "./cafe_entity_label.json"
        self.ood_data_dir = "./ood_data.csv"
        self.intent_label = self.load_intent_label()
        self.entity_label = self.load_entity_label()
        self.prep = Preprocessing()


    # 의도 레이블 데이터 불러오기
    def load_intent_label(self):
        f = open(self.intent_label_dir, encoding='UTF-8')
        intent_label = json.loads(f.read())
        self.intents = list(intent_label.keys())
        return intent_label

    def load_entity_label(self):
        f = open(self.entity_label_dir, encoding='UTF-8')
        entity_label = json.loads(f.read())
        self.entitys = list(entity_label.keys())
        return entity_label

    # 띄어쓰기를 기준으로 문장 자르기
    def tokenize(self, sentence):
        return sentence.split()

    # 전달 받은 데이터셋을 띄어쓰기 기준으로 자른 문장의 리스트로 만들기
    def tokenize_dataset(self, dataset):
        token_dataset = []
        for data in dataset:
            token_dataset.append(self.tokenize(data))
        return token_dataset

    # 문장을 idx로 변환하고 레이블도 숫자로 변환
    def make_intent_dataset(self, embed):
        intent_dataset = pd.read_csv(self.intent_data_dir)
        labels = [self.intent_label[label] for label in intent_dataset["label"].to_list()]
        intent_querys = self.tokenize_dataset(intent_dataset["question"].tolist())
        dataset = list(zip(intent_querys, labels))
        intent_train_dataset, intent_test_dataset = self.word2idx_dataset(dataset, embed)
        return intent_train_dataset, intent_test_dataset

    def make_entity_dataset(self, embed):
        entity_dataset = pd.read_csv(self.entity_data_dir)
        entity_querys = self.tokenize_dataset(entity_dataset["question"].tolist())
        labels = []
        for label in entity_dataset["label"].to_list():
            temp = []
            for entity in label.split():
                temp.append(self.entity_label[entity])
            labels.append(temp)
        dataset = list(zip(entity_querys, labels))
        entity_train_dataset, entity_test_dataset = self.word2idx_dataset(dataset, embed)
        return entity_train_dataset, entity_test_dataset

    def make_ood_dataset(self, embed):
        intent_dataset = pd.read_csv(self.intent_data_dir)
        ood_dataset = pd.read_csv(self.ood_data_dir)
        intent_dataset = pd.concat([intent_dataset, ood_dataset])
        labels = []
        for label in intent_dataset["label"].to_list():
            if label == "OOD":
                labels.append(0)
            else:
                labels.append(1)

        intent_querys = self.tokenize_dataset(intent_dataset["question"].tolist())
        dataset = list(zip(intent_querys, labels))
        intent_train_dataset, intent_test_dataset = self.word2idx_dataset(dataset, embed)
        return intent_train_dataset, intent_test_dataset

    def word2idx_dataset(self, dataset, embed, train_ratio = 0.8):
        question_list, label_list, lengths = [], [], []
        flag = True
        random.shuffle(dataset)
        for query, label in dataset:
            q_vec = embed.query2idx(query)
            lengths.append(len(q_vec))
            q_vec = self.prep.pad_idx_sequencing(q_vec)

            question_list.append(torch.tensor([q_vec]))

            if isinstance(label, list):
                label = self.prep.pad_idx_sequencing(label)
                label_list.append(label)
                flag=False
            else:
                label_list.append(torch.tensor([label]))

        x = torch.cat(question_list)
        if flag :                       # Intent Dataset
            y = torch.cat(label_list)
        else:                           # Entity Dataset
            y = torch.tensor(label_list)

        x_len = x.size()[0]
        y_len = y.size()[0]
        if (x_len == y_len) :
            train_size = int(x_len * train_ratio)
            train_x = x[:train_size]
            train_y = y[:train_size]

            test_x = x[train_size+1:]
            test_y = y[train_size+1:]

        if flag:
            train_dataset = TensorDataset(train_x, train_y)
            test_dataset = TensorDataset(test_x, test_y)
        else :
            train_length = lengths[:train_size]
            test_length = lengths[train_size+1:]

            train_dataset = EntityDataset(train_x, train_y, train_length)
            test_dataset = EntityDataset(test_x, test_y, test_length)

        return train_dataset, test_dataset

    def make_embed_dataset(self, ood=False):
        embed_dataset = pd.read_csv(self.intent_data_dir)
        embed_dataset = embed_dataset["question"].to_list()
        embed_dataset = self.tokenize_dataset(embed_dataset)

        return embed_dataset