from sentence_transformers import SentenceTransformer

model = SentenceTransformer("D:\\Workspace\\models\\bce-embedding-base_v1")


def embedding(sentence: str):
    return model.encode(sentence, normalize_embeddings=True)