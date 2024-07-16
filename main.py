import funs
import time
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

while True:

    # If bigger than 0.5 in similarity
    question=input("신해철에게 무슨 말을 하고싶으신가요? : ")  # question="요즘 너무 힘들어요. 저는 그냥 쉬고싶어요."  # 사용자 input
    similarity_results = funs.similarity_analytics(question)

    if similarity_results["Cosine_similarity"] >= 0.5:
        print(similarity_results)

    else:
        # If smaller than 0.5 in similarity
        return_ai=funs.run(question)
        print(f"return from Shin Hae Chul\n{return_ai}")
        # print(f"Memory Check {funs.memories}")


