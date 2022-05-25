from gensim.models.callbacks import CallbackAny2Vec
from gensim.models import Word2Vec
from torch import nn
import torch.nn.functional as F
import torch
from torchcrf import CRF
from sentence_transformers import SentenceTransformer
from numpy import dot
from numpy.linalg import norm
import pandas as pd
import numpy as np

class SBERT():
    def __init__(self):
        self.model_pretrain_path = "./nlp/pretrained/ood_answer_pretrained_model"
        self.model = SentenceTransformer(self.model_pretrain_path)
        self.train_data = pd.read_csv('cafe_ood_answer_data.csv')
        self.data_preprocessing()

    def data_preprocessing(self):
        self.train_data['embedding'] = self.train_data['embedding'].str.replace('\[ ', '[')
        self.train_data['embedding'] = self.train_data['embedding'].str.replace(' \]', ']')
        self.train_data['embedding'] = self.train_data['embedding'].str.replace('    ', ' ')
        self.train_data['embedding'] = self.train_data['embedding'].str.replace('   ', ' ')
        self.train_data['embedding'] = self.train_data['embedding'].str.replace('  ', ' ')
        self.train_data['embedding'] = self.train_data['embedding'].str.replace(' ', ',')
        self.train_data['embedding'] = self.train_data['embedding'].apply(eval).apply(np.array)

    def cos_sim(self, A, B):
        return dot(A, B) / (norm(A) * norm(B))

    def return_answer(self, question):
        embedding = self.model.encode(question)
        self.train_data['score'] = self.train_data.apply(lambda x: self.cos_sim(x['embedding'], embedding), axis=1)
        return self.train_data.loc[self.train_data['score'].idxmax()]['A']

class DAN(nn.Module):
    def __init__(self, w2v, dim, dropout, num_class = 2):
        super(DAN, self).__init__()
        #load pretrained embedding in embedding layer.
        vocab_size = w2v.size()[0]
        emb_dim = w2v.size()[1]
        self.embed = nn.Embedding(vocab_size+2, emb_dim)
        self.embed.weight[2:].data.copy_(w2v)
        #self.embed.weight.requires_grad = False

        self.dropout1 = nn.Dropout(dropout)
        self.bn1 = nn.BatchNorm1d(emb_dim)
        self.fc1 = nn.Linear(emb_dim, dim)
        self.dropout2 = nn.Dropout(dropout)
        self.bn2 = nn.BatchNorm1d(dim)
        self.fc2 = nn.Linear(dim, num_class)

    def forward(self, x):
        emb_x = self.embed(x)
        #(128,20,300)
        x = emb_x.mean(dim=1)
        #(128,300)
        x = self.dropout1(x)
        x = self.bn1(x)
        x = self.fc1(x)
        #(128,256)
        x = self.dropout2(x)
        x = self.bn2(x)
        logit = self.fc2(x)
        #(128,2 )
        return logit

class BiLSTM_CRF(nn.Module):
    def __init__(self, w2v, tag_to_ix, hidden_dim, batch_size):
        super(BiLSTM_CRF, self).__init__()
        self.embedding_dim = w2v.size()[1]
        self.hidden_dim = hidden_dim
        self.vocab_size = w2v.size()[0]
        self.tag_to_ix = tag_to_ix
        self.tagset_size = len(tag_to_ix)
        self.batch_size = batch_size
        self.START_TAG = "<START_TAG>"
        self.STOP_TAG = "<STOP_TAG>"

        self.word_embeds = nn.Embedding(self.vocab_size + 2, self.embedding_dim)
        # self.word_embeds.weight[2:].data.(w2v)
        # self.word_embeds.weight.requires_grad = False
        self.lstm = nn.LSTM(self.embedding_dim, hidden_dim // 2, batch_first=True,
                            num_layers=1, bidirectional=True)

        self.hidden2tag = nn.Linear(hidden_dim, self.tagset_size)

        self.hidden = self.init_hidden()

        self.crf = CRF(self.tagset_size, batch_first=True)

    def init_hidden(self):
        return (torch.randn(2, self.batch_size, self.hidden_dim // 2),
                torch.randn(2, self.batch_size, self.hidden_dim // 2))

    def forward(self, sentence):
        self.batch_size = sentence.size()[0]
        self.hidden = self.init_hidden()
        embeds = self.word_embeds(sentence)
        lstm_out, self.hidden = self.lstm(embeds, self.hidden)

        lstm_feats = self.hidden2tag(lstm_out)

        return lstm_feats

    def decode(self, logits, mask):
        return self.crf.decode(logits, mask)

    def compute_loss(self, label, logits, mask):
        log_likelihood = self.crf(logits, label, mask=mask, reduction='mean')
        return - log_likelihood

class textCNN(nn.Module):
    def __init__(self, w2v, dim, kernels, dropout, num_class):
        super(textCNN, self).__init__()
        vocab_size = w2v.size()[0]
        emb_dim = w2v.size()[1]
        self.emb_dim = emb_dim
        self.vocab_size = vocab_size
        self.w2v = w2v
        self.embed = nn.Embedding(vocab_size +2, emb_dim)
        self.embed.weight[2:].data.copy_(w2v)
        self.convs = nn.ModuleList([nn.Conv2d(1, dim, (w,emb_dim)) for w in kernels])
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(len(kernels)*dim, num_class) # softmax같은 역할. Linear = Dense + Actv

    def forward(self, x):
        emb_x = self.embed(x)
        emb_x = emb_x.unsqueeze(1) # 예를들어 32x32일 경우 1x32x32로 만들어줌
        con_x = [conv(emb_x) for conv in self.convs]
        pool_x = [F.max_pool1d(x.squeeze(-1), x.size()[2]) for x in con_x]
        fc_x = torch.cat(pool_x, dim=1) # concatenate. 다 이어지게 함. (768,1)
        fc_x = fc_x.squeeze(-1) # (768)
        result = self.fc(fc_x)
        return result

# 각 모델 트레이닝 시 에폭의 출력을 확인하는 용도
class EpochLogger(CallbackAny2Vec):
    def __init__(self):
        self.epoch = 0
    def on_epoch_begin(self, model):
        print("Epoch", self.epoch, "start")
    def on_epoch_end(self, model):
        print("Epoch", self.epoch, "end")
        self.epoch += 1

class MakeEmbed:
    def __init__(self):
        self.model_dir = "./nlp"
        self.vector_size = 300
        self.window_size = 3
        self.workers = 4
        self.min_count = 2
        self.iter = 1000
        self.sg = 1 # sg가 1이면 스킵그램, 0이면 CBOW
        self.model_file = "./nlp/pretrained/word2vec_skipgram"
        self.epoch_logger = EpochLogger()

    def word2vec_init(self):
        self.word2vec = Word2Vec(
            vector_size = self.vector_size,
            window = self.window_size,
            workers= self.workers,
            min_count = self.min_count,
            epochs = self.iter,
            compute_loss = True,
            sg = self.sg
        )

    def word2vec_build_vocab(self, dataset):
        self.word2vec.build_vocab(dataset)
    def word2vec_most_similar(self, query):
        print(self.word2vec.most_similar(query))

    def word2vec_train(self, embed_dataset, epoch=0):
        if epoch == 0:
            epoch == self.word2vec.epochs + 1
        self.word2vec.train(
            corpus_iterable = embed_dataset,
            total_examples = self.word2vec.corpus_count,
            epochs = epoch,
            callbacks = [self.epoch_logger]
        )
        self.word2vec.save(self.model_file + ".gensim")
        self.vocab = self.word2vec.wv.index_to_key
        self.vocab = {word: i for i, word in enumerate(self.vocab)}

    def load_word2vec(self):
        self.word2vec = Word2Vec.load(self.model_file + ".gensim")
        self.vocab = self.word2vec.wv.index_to_key
        self.vocab.insert(0, "<UNK>")
        self.vocab.insert(0, "<PAD>")
        self.vocab = {word: i for i, word in enumerate(self.vocab)}

    def query2idx(self, query):
        sent_idx = []
        for word in query:
            if self.vocab.get(word):
                idx = self.vocab[word]
            else:
                idx = 1
            sent_idx.append(idx)
        return sent_idx

