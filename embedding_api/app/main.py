from fastapi import FastAPI
from google.cloud import storage
import pickle
import faiss


class IVFIndex():
    def __init__(self, mapping, labels, embedding_list):
        self.mapping = mapping
        self.labels = labels
        self.embedding_list = embedding_list

    def add_index(self, index):
        self.index = index

    def query(self, vectors, k=10, n_probe=10):
        self.index.nprobe = n_probe
        distances, indices = self.index.search(vectors, k)
        # I expect only query on one vector thus the slice
        return [self.labels[i] for i in indices[0]]

    def query_by_word(self, word, k=10, n_probe=10):
        self.index.nprobe = n_probe
        vectors = self.embedding_list[self.mapping[word]]
        vectors = vectors.reshape(1, vectors.shape[0])
        distances, indices = self.index.search(vectors, k)
        # I expect only query on one vector thus the slice
        return [self.labels[i] for i in indices[0]]


class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if name == 'IVFIndex':
            return IVFIndex
        return super().find_class(module, name)


app = FastAPI()

# storage_client = storage.Client.from_service_account_json('/home/linchenxiao/gcp_keys/playground-linchen-2774599fb4bc.json')
storage_client = storage.Client()
bucket = storage_client.get_bucket("playground-linchen")

blob = bucket.blob('search_engine.pickle')
blob.download_to_filename("search_engine.pickle")

search_engine = CustomUnpickler(open('search_engine.pickle', 'rb')).load()

blob = bucket.blob('faiss_IVFIndex_45000')
blob.download_to_filename("faiss_IVFIndex_45000")
index = faiss.read_index("faiss_IVFIndex_45000")

search_engine.add_index(index)


@app.get("/")
def read_root():
    return search_engine.query_by_word("特朗普")


@app.get("/similarword/{word}/{top_n}")
def read_item(word: str, top_n: int = 10):
    return search_engine.query_by_word(str(word), k=int(top_n))
