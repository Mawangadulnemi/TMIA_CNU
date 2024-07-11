import funs
import time


while True:
    # question="요즘 너무 힘들어요. 저는 그냥 쉬고싶어요."  # 사용자 input
    question=input("신해철에게 무슨 말을 하고싶으신가요? : ")
    return_ai=funs.run(question)
    print(f"return from Shin Hae Chul\n{return_ai}")
    # print(f"Memory Check {funs.memories}")
