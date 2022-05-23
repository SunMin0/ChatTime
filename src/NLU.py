import torch
from src.dataset import MakeDataset
from src.model import MakeEmbed, textCNN, DAN, BiLSTM_CRF

class NaturalLanguageUnderstanding:
    def __init__(self):
        self.dataset = MakeDataset()
        self.embed = MakeEmbed()
        self.embed.load_word2vec()

        self.weights = self.embed.word2vec.wv.vectors
        self.weights = torch.FloatTensor(self.weights)

        self.intent_clsf = textCNN(self.weights, 256, [3,4,5], 0.5, len(self.dataset.intent_label))
        self.ood_clsf = DAN(self.weights, 256, 0.5, 2)
        self.entity_recog = BiLSTM_CRF(self.weights, self.dataset.entity_label, 256, 128)

    def model_load(self):
        intent_pretrain_path = "./nlp/pretrained/cafe_intent_clsf_98.525_steps_94.pt"
        entity_pretrain_path = "./nlp/pretrained/cafe_entity_recog_90.804_steps_7.pt"
        ood_pretrain_path = "./nlp/pretrained/ood_clsf_99.801_steps_8.pt"

        self.intent_clsf.load_state_dict(torch.load(intent_pretrain_path))
        self.entity_recog.load_state_dict(torch.load(entity_pretrain_path))
        # self.ood_clsf.load_state_dict(torch.load(ood_pretrain_path))

        self.intent_clsf.eval()
        self.entity_recog.eval()
        # self.ood_clsf.eval()

    def predict(self, query):
        tokens = self.dataset.tokenize(query)
        q2idx = self.embed.query2idx(tokens)
        x = self.dataset.prep.pad_idx_sequencing(q2idx)
        x = torch.tensor(x)
        # f = self.ood_clsf(x.unsqueeze(0))
        # ood = torch.argmax(f).tolist()
        #
        # if ood:
        #     f = self.intent_clsf(x.unsqueeze(0))
        #     intent = self.dataset.intents[torch.argmax(f).tolist()]
        # else:
        #     intent = 'ood'
        f = self.intent_clsf(x.unsqueeze(0))
        intent = self.dataset.intents[torch.argmax(f).tolist()]
        f = self.entity_recog(x.unsqueeze(0))

        mask = torch.where(x>0, torch.tensor([1.]), torch.tensor([0.])).type(torch.uint8)

        predict = self.entity_recog.decode(f, mask.view(1, -1))

        return intent, predict

    def convert_nlu_result(self, query, intent, predict):
        NLU_result = {
            "INTENT" : "",
            "SLOT" : []
        }
        x_token = query.split()
        slots = []
        BIE = []
        prev = "";
        for i, slot in enumerate([self.dataset.entitys[p] for p in predict[0]]):
            name = slot[2:]
            if "S-" in slot:
                if BIE != []:
                    slots.append(prev[2:]+"^"+" ".join(BIE))
                    BIE = []
                slots.append(name+"^"+x_token[i])
            elif "B-" in slot:
                BIE.append(x_token[i])
                prev = slot
            elif "I-" in slot and ("B" in prev or "I" in prev):
                BIE.append(x_token[i])
                prev = slot
            elif "E-" in slot and ("I" in prev or "B" in prev):
                BIE.append(x_token[i])
                slots.append(name+"^"+" ".join(BIE))
            else:
                if BIE != []:
                    slots.append(prev[2:]+"^"+" ".join(BIE))
                    BIE = []

        NLU_result["INTENT"] = intent
        NLU_result["SLOT"] = slots
        return NLU_result