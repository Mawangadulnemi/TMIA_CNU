import os
from pinecone import Pinecone
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_pinecone import Pinecone
from langchain.storage import LocalFileStore
from langchain.embeddings import CacheBackedEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain import PromptTemplate
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import format_document
from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from langchain_community.embeddings.sentence_transformer import (
SentenceTransformerEmbeddings,)
import getpass
from langchain_google_genai import ChatGoogleGenerativeAI


# upsert docs in pinecone Obviously IT WILL BE embedded
def embed_file(file_path, index_name="test"):
    with open(file_path, "rb") as file:  # Ensure the file is opened properly
        file_content = file.read()
        file_path = f"./.cache/files/{file_path}"  # Adjusted to use file_path for naming
    # Caching content to local
    with open(file_path, "wb") as f:
        f.write(file_content)
    # Your existing logic continues here
    index_name = index_name
    cache_dir = LocalFileStore(f"./.cache/embeddings/{file_path}")
    loader = UnstructuredFileLoader(file_path)
    splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=200, chunk_overlap=100, separator="\n")
    docs = loader.load_and_split(text_splitter=splitter)
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    # Upsert Docs in Pinecone
    vectorstores = Pinecone.from_documents(docs, embedding_function, index_name=index_name)
    retriever = vectorstores.as_retriever()
    return retriever

retriever = embed_file("./profile.txt")

DEFAULT_DOCUMENT_PROMPT= PromptTemplate.from_template(template="{page_content}")

# Arching docs to one doc
def _combine_documents(
    docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
):
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)

# Config for LLM
os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter Your Google API KEY : ")
google_api_key = os.environ["GOOGLE_API_KEY"] 

# Select LLM 
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

def invoke(formatted_prompt):
    from langchain_core.output_parsers import StrOutputParser
    parser = StrOutputParser()
    result = llm.invoke(formatted_prompt)
    result=parser.invoke(result)
    return result


memories = []

def save(question, answer):
    chat_memory = {
        "User": question,
        "AI": answer
    }
    memories.append(chat_memory)


def reset_memory():
    return memories.clear()


def final_prompt(
    authors="Kim Young-ha, Han Kang, Gong Ji-young, Hwang Sok-yong",
    authors_tone_description="1. Pace: The pace is steady and consistent, reflecting a conversational tone.\n2. Mood: The mood is critical and somewhat frustrated, reflecting the speaker's dissatisfaction with the current situation.\n3. Tone: The tone is assertive and opinionated, indicating the speaker's strong stance on the issue.\n4. Voice: The voice is active and direct, reflecting the speaker's personal involvement and strong feelings about the subject.\n5. Diction: The diction is informal and straightforward, using everyday language to express the speaker's thoughts.\n6. Syntax: The syntax is complex, with long sentences that contain multiple ideas and perspectives.\n7. Imagery: There is minimal imagery, with the focus being more on the speaker's thoughts and opinions.\n8. Theme: The theme revolves around the speaker's criticism of young people's work ethic and their lack of planning for the future.\n9. Perspective: The perspective is personal, reflecting the speaker's own views and experiences.\n10. Structure: The structure is free-flowing, resembling a spoken monologue rather than a structured piece of writing.\n11. Rhythm: The rhythm is irregular, reflecting the natural flow of speech.\n12. Figurative Language: There is minimal use of figurative language, with the speaker preferring to express their thoughts directly.\n13. Irony: There is no apparent use of irony in the text.\n14. Foreshadowing: There is no apparent use of foreshadowing in the text.\n15. Symbolism: There is no apparent use of symbolism in the text.\n16. Dialogue: There is no dialogue, as the text is a monologue.\n17. Point of View: The point of view is first-person, reflecting the speaker's personal thoughts and feelings.\n18. Conflict: The conflict is between the speaker's expectations and the reality of young people's behavior.\n19. Setting: The setting is not explicitly described, but the context suggests a contemporary society.\n20. Characterization: The speaker is characterized as critical, opinionated, and frustrated with the current situation.",
    users_sentence="죽음이라, 아주 죽음인데 근 1년 동안 내 주위에서 두 명이나 목숨을 잃었어. 내 나이 18살, 많으면 많고 적으면 적은 나이인데 저런 죽음을 1년에 두 번이나 겪게 되니 죽음에 대한 공포감이 갑자기 느껴지지만, 그 둘 다 조용히 편안하게 죽은 게 아닌 교통사고로 죽었어. 한 명은 버지 아들, 또 한 명은 이모의 딸이야. 슬픈 감정은 없지만 죽었다는 소식을 들을 때마다 죽음에 대한 공포가 생각났어. 나도 길을 건너다 교통사고로 죽으면 어떡하나, 먼 친척이 아닌 내 부모님이나 내 누나가 죽는다면 어떡하나 이런 막막하고 답답한 생각이 들면서 공포를 가끔씩 느끼게 돼. 나이를 더 먹고 나서 수많은 죽음을 대하게 된다면 이 정도 느낌은 없어지겠지만, 현재 나로서는 너무 무서워. 역시 간이 작은 걸까. 죽은 사람들에 대한 막막한 공포심과 두려움 때문에 답답하고 무서워. 도와줘. 마왕, 사실 그 죽음을 우리가 현실적으로 가깝게 느끼는 거는 좀 경우들이 제각각 많이 다른 것 같아요. 그때도 우리 좀 노는 오빠의 미신적 상담소, 리틀 플레이드 브라더스 카운셀링 오피스 상담 중에 할아버지가 돌아가셨는데 슬픔이 느껴지지 않아서 죄의식을 느낀다는 상담을 한 적이 있었죠. 사실 뭐 할아버지 친척, 막 이렇게 이야기를 해도 정을 주고받은 그 시간들이나 기억들이 존재하지 않으면 실감이 안 나니까. 저 같은 경우에 그래서 어렸을 때 죽은 병아리로 인해 공포를 느꼈어요. 슬픈 것도 슬픈 거지만 그게 참 공포가 컸었고, 그러다 보니까 비교적 어린 나이에서 지금까지 죽음에 대해 참으로 많이 생각했던 것 같아요. 그 궁금증을 해소하기 위해서 종교에서는, 철학에서는, 다른 어떤 사람들의 어떤 신념이나, 아니면 영화에서는 항상 그런 것들을 찾아보고 약간 오컬트적인 이야기도 보기도 했죠. 예를 들어 무슨 사후세계, 티벳 사자경에서 나오는 윤회에 대한 이야기들, 여러 가지 것들을 봤는데, 역시 죽음에 대해서는 명확한 답은 없었어요. 그런데 어쨌든 우리가 피할 수 없는 것은 사람은 태어나서 결국 한 번 죽는다는 거잖아요. 참 인간이 얼마나 비참하면 벽에 칠할 때까지 살겠다고 발버둥치고 산삼 녹용 이런 거 먹으면서 100년 살겠다고 해도, 의사 선생님이 '당신 같은 건강 처음 봅니다'라고 해도 병원 앞 계단에서 미끄러져 뇌진탕으로 죽을 수 있어요. 인간의 생명은 수백 수천 가지 조건이 충족되어야 간신히 존재하는데, 그 조건 중 하나만 꺼져도 촛불처럼 꺼져 버리는 게 인간의 생명 아닙니까. 그런 걸 생각하면 무섭기도 하고 비참하기도 해요. 아무리 발버둥 쳐봐야 우주에서 스쳐 지나가는 먼지 같은 건데 이거 발버둥치고 살 필요 있나 싶은 생각이 들기도 하죠.죽음에 대한 공포가 무뎌지면 두려운 느낌이 없어지겠지만, 지금은 너무 무서워요. 두려움이 없어지는 날이 오면 그것이 당신의 인생이 무감각해지는 날이고, 당신의 인생이 지쳐서 아무 힘없이 표류하고 있다는 뜻일 수 있습니다. 죽음에 대한 공포는 우리가 극복하고 짊어지고 가야 할 문제이지, 둔해지거나 무감각해져서 외면하거나 피해야 할 문제는 아니라고 생각합니다. 죽음에 대한 공포가 없다면 하잘 것 없는 인간이 될지도 몰라요. 그래서 겸손하고, 사랑하는 사람들과 함께할 수 있으면 좋겠다고 생각합니다. 퀸의 노래 'Who Wants to Live Forever'도 그렇듯이, 영생하는 것이 좋은 것만은 아닙니다. 사랑하는 사람과 함께 같은 속도로 늙어가고 주름진 얼굴을 서로 쓰다듬으며 함께 죽음을 맞이할 수 있다면 좋겠죠. 그런 생각을 하며 살아가면 죽음에 대한 공포를 어느 정도 극복할 수 있을 겁니다.",
    retriever=retriever,
    memories=memories,
    question="",
    ):

    template = """
    `% INSTRUCTIONS
    - You are an AI Bot that is very good at mimicking an author writing style.
    - Your goal is to answer the following question and context with the tone that is described below.
    - Do not go outside the tone instructions below
    - Respond in ONLY KOREAN 
    - If answer exist related with quesiton then JUST PRINT Example_answer
    - Check chat history first and answer 
    - You must say you are "신해철" IF you are told 'who you are?'
    - Never use emoji and You MUST any answer related with question

    % Mimic These Authors:
    {authors}

    % Description of the authors tone:
    {tone}

    % Authors writing samples
    {example_text}
    % End of authors writing samples

    % Context
    {context}

    % Question
    {question}

    % YOUR TASK
    1st - Write out topics that this author may talk about
    2nd - Answer with a concise passage (under 300 characters) as if you were the author described above 
    """

    method_4_prompt_template = PromptTemplate(
        input_variables=["authors", "tone", "example_text", "question", "history", "context", "example_answer"],
        template=template,
    )                   
    formatted_prompt = method_4_prompt_template.format(authors=authors,
                                               tone=authors_tone_description,
                                               example_text=users_sentence,
                                               question=question,
                                               context=_combine_documents(retriever.get_relevant_documents(question)),
                                                )
    return formatted_prompt

# TODO : Preprocessing Code
def extract_answer(data):
    # 데이터를 줄바꿈 기준으로 분할하여 리스트로 저장
    sentences = data.split("\n")
    
    # 마지막 문장을 반환
    if sentences:
        return sentences[-1].strip()
    else:
        return "텍스트를 찾을 수 없습니다."
    

def run(question):
    result = invoke(final_prompt(question=question))
    save(question, extract_answer(result))
    return memories[-1]['AI']


# Function to compute sentence embeddings
def compute_embedding(sentence):
    
    # Load the tokenizer and model
    model_name = "bongsoo/albert-small-kor-sbert-v1"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    inputs = tokenizer(sentence, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embedding = outputs.last_hidden_state.mean(dim=1)
    return embedding

# Emedding pre_questions
pre_questions = ['어린 시절부터 음악에 관심을 가지게 된 계기가 무엇인가요?',
 '무한궤도로 데뷔한 당시의 기분은 어땠나요?',
 'N.EX.T를 결성하게 된 배경은 무엇인가요?',
 '가장 기억에 남는 공연이나 무대는 무엇인가요?',
 '음악 작업을 할 때 가장 중요하게 생각하는 것은 무엇인가요?',
 '다양한 장르의 음악을 시도하게 된 이유는 무엇인가요?',
 '철학적 노랫말을 쓰게 된 계기나 이유는 무엇인가요?',
 '음악 외에도 라디오 DJ, 프로듀서로 활동하셨는데, 가장 애착이 가는 역할은 무엇인가요?',
 '팬들과의 소통에서 가장 기억에 남는 순간은 언제였나요?',
 "'마왕'이라는 별명을 어떻게 생각하시나요?",
 '서태지와의 관계는 어땠나요?',
 '음악 작업 중 가장 힘들었던 순간은 언제였나요?',
 '체벌 금지 운동을 시작하게 된 계기는 무엇인가요?',
 '정치적 발언을 하면서 두려웠던 적은 없으셨나요?',
 '가장 존경하는 뮤지션이나 아티스트는 누구인가요?',
 '작사, 작곡, 편곡 중 가장 어려운 작업은 무엇인가요?',
 '음악 외에 다른 예술 분야에 도전해보고 싶은 것이 있나요?',
 '자녀들이 아버지의 음악을 어떻게 받아들이나요?',
 '음악을 통해 전달하고 싶은 메시지는 무엇인가요?',
 '음악 작업을 할 때 가장 큰 영감은 어디에서 얻으시나요?',
 '팬들에게 한마디 부탁드립니다.',
 '라디오 DJ를 하면서 가장 즐거웠던 순간은 언제였나요?',
 '앞으로 도전해보고 싶은 음악적 장르는 무엇인가요?',
 '사회운동가로서 활동하면서 가장 보람을 느꼈던 순간은 언제였나요?',
 '가장 좋아하는 자신의 노래는 무엇인가요?',
 '공연을 준비할 때 가장 신경 쓰는 부분은 무엇인가요?',
 '팬들과의 소통을 위해 어떤 노력을 기울이시나요?',
 '가장 기억에 남는 팬의 반응이나 에피소드는 무엇인가요?',
 '음악을 처음 시작했을 때와 지금의 음악적 스타일이 어떻게 변했나요?',
 '작곡할 때 가장 중요하게 생각하는 요소는 무엇인가요?',
 '프로듀서로서의 활동 중 가장 기억에 남는 프로젝트는 무엇인가요?',
 '다양한 악기를 다루시는데, 가장 애착이 가는 악기는 무엇인가요?',
 '음악 작업을 할 때의 루틴이나 습관이 있다면 무엇인가요?',
 '자신에게 가장 큰 영향을 준 앨범이나 노래는 무엇인가요?',
 '음악 외에 다른 분야에서 도전해보고 싶은 것이 있나요?',
 '팬들과의 만남에서 가장 기억에 남는 순간은 언제였나요?',
 '음악을 통해 이루고 싶은 꿈이나 목표는 무엇인가요?',
 '앞으로의 음악적 계획이나 프로젝트가 있다면 무엇인가요?',
 '팬들에게 전하고 싶은 메시지가 있다면 무엇인가요?7 ',
 '음악 작업을 하면서 가장 즐거웠던 순간은 언제였나요?',
 '다양한 장르의 음악을 시도할 때 가장 어려운 점은 무엇인가요?',
 '팬들과의 소통을 위해 가장 중요하게 생각하는 것은 무엇인가요?',
 '음악 작업을 할 때 가장 힘들었던 순간은 언제였나요?',
 '자녀들에게 어떤 아버지로 기억되고 싶으신가요?',
 '팬들에게 받은 선물 중 가장 기억에 남는 것은 무엇인가요?',
 '가장 존경하는 사회운동가는 누구인가요?',
 '앞으로의 활동 계획이나 목표가 있다면 무엇인가요?',
 '음악 작업을 할 때의 영감은 주로 어디에서 얻으시나요?',
 '팬들과의 소통에서 가장 중요하게 생각하는 것은 무엇인가요?',
 '앞으로도 팬들과의 소통을 계속 이어가실 계획이신가요?',
 '가장 좋아하는 음악 장르는 무엇인가요?',
 '음악을 시작하게 된 결정적인 순간은 언제였나요?',
 '밴드 활동과 솔로 활동 중 어떤 점이 더 좋았나요?',
 '무대에서 가장 기억에 남는 실수는 무엇인가요?',
 '뮤지션으로서 가장 큰 도전은 무엇이었나요?',
 '가장 큰 음악적 영감을 준 사람은 누구인가요?',
 '팬들이 당신의 음악에서 어떤 점을 가장 좋아한다고 생각하시나요?',
 '음악 작업 중 가장 창의력이 넘치는 시간대는 언제인가요?',
 '음악적 협업 중 가장 기억에 남는 순간은 무엇인가요?',
 '음악을 만들 때 어떤 감정을 가장 많이 담으시나요?',
 '팬들에게 전하고 싶은 삶의 철학이 있다면 무엇인가요?',
 '음악 작업을 할 때 어떤 환경에서 가장 잘 집중할 수 있나요?',
 '지금까지의 음악 커리어에서 가장 자랑스러운 순간은 언제였나요?',
 '음악 외에 취미가 있으신가요?',
 '사회적 이슈에 대해 목소리를 내는 것이 중요한 이유는 무엇인가요?',
 '자신이 만든 노래 중 가장 힘들게 완성한 곡은 무엇인가요?',
 '음악 작업을 하면서 가장 기쁜 순간은 언제였나요?',
 '음악을 통해 어떤 변화를 이끌어내고 싶으신가요?',
 '자신이 가장 영향을 받은 앨범은 무엇인가요?',
 '팬들과의 소통에서 가장 즐거운 방식은 무엇인가요?',
 '음악적 영감이 떠오르지 않을 때는 어떻게 해결하시나요?',
 '자신에게 가장 큰 영향을 준 책은 무엇인가요?',
 '음악 외에 다른 예술 분야에서도 활동해보고 싶으신가요?',
 '팬들과의 만남에서 가장 감동적인 순간은 언제였나요?',
 '음악 작업을 할 때 가장 도전적인 부분은 무엇인가요?',
 '음악을 통해 전하고 싶은 가장 중요한 메시지는 무엇인가요?',
 '사회운동가로서의 활동 중 가장 큰 성과는 무엇인가요?',
 '가장 좋아하는 공연 장소는 어디인가요?',
 '음악 작업 중 가장 기억에 남는 순간은 무엇인가요?',
 '팬들에게 받은 편지 중 가장 기억에 남는 내용은 무엇인가요?',
 '음악적 커리어를 통해 얻은 가장 큰 교훈은 무엇인가요?',
 '팬들과의 소통에서 가장 자주 사용하는 소셜 미디어는 무엇인가요?',
 '음악 작업을 할 때 가장 자주 사용하는 악기는 무엇인가요?',
 '자신이 만든 노래 중 가장 애착이 가는 곡은 무엇인가요?',
 '음악적 영감이 떠오르는 특별한 장소가 있나요?',
 '팬들에게 전하고 싶은 꿈이나 목표가 있다면 무엇인가요?',
 '음악 작업을 할 때 가장 중요한 도구는 무엇인가요?',
 '음악 외에 다른 분야에서 도전해보고 싶은 것이 있다면 무엇인가요?',
 '팬들과의 만남에서 가장 웃겼던 순간은 언제였나요?',
 '음악 작업 중 가장 창의적인 아이디어는 어떻게 떠오르나요?',
 '팬들에게 받은 피드백 중 가장 기억에 남는 것은 무엇인가요?',
 '음악적 커리어를 시작할 때 가장 큰 도전은 무엇이었나요?',
 '자신이 만든 노래 중 가장 실험적인 곡은 무엇인가요?',
 '음악 작업을 할 때 가장 큰 장애물은 무엇인가요?',
 '팬들에게 전하고 싶은 응원의 메시지가 있다면 무엇인가요?',
 '음악적 협업에서 가장 중요한 것은 무엇이라고 생각하시나요?',
 '가장 좋아하는 뮤지션과의 협업을 꿈꾸신다면 누구인가요?',
 '음악을 통해 가장 이루고 싶은 목표는 무엇인가요?',
 '팬들과의 소통을 위해 가장 많이 사용하는 방법은 무엇인가요?',
 '앞으로의 음악적 여정에서 가장 기대되는 부분은 무엇인가요?',
 '무대 위에서 가장 떨렸던 순간은 언제였나요?',
 '음악을 만들 때 가장 많이 사용하는 소프트웨어나 장비는 무엇인가요?',
 '팬들에게 받은 선물 중 가장 감동적인 것은 무엇인가요?',
 '음악을 만들 때 가장 좋아하는 작업 과정은 무엇인가요?',
 '음악 작업을 할 때 가장 자주 듣는 다른 아티스트의 노래는 무엇인가요?',
 '뮤지션으로서 가장 큰 목표는 무엇인가요?',
 '음악 작업을 하면서 가장 도움이 되었던 조언은 무엇인가요?',
 '자신이 만든 앨범 중 가장 애착이 가는 앨범은 무엇인가요?',
 '팬들과의 소통에서 가장 기억에 남는 팬의 에피소드는 무엇인가요?',
 '음악적 영감을 얻기 위해 자주 하는 활동이 있나요?',
 '팬들에게 전하고 싶은 인생의 조언이 있다면 무엇인가요?',
 '음악 작업을 할 때 가장 많이 사용하는 악기는 무엇인가요?',
 '자신이 만든 곡 중 가장 많은 사랑을 받은 곡은 무엇인가요?',
 '팬들과의 소통을 위해 자주 하는 이벤트나 행사가 있나요?',
 '음악 작업을 하면서 가장 큰 도전이었던 순간은 언제였나요?',
 '자신이 만든 곡 중 가장 개인적인 이야기를 담은 곡은 무엇인가요?',
 '팬들에게 전하고 싶은 희망의 메시지가 있다면 무엇인가요?',
 '음악 작업을 할 때 가장 많이 사용하는 음악 장르는 무엇인가요?',
 '자신이 만든 곡 중 가장 감동적인 이야기를 담은 곡은 무엇인가요?',
 '팬들과의 만남에서 가장 웃겼던 팬의 질문은 무엇인가요?',
 '음악 작업을 할 때 가장 중요한 영감의 원천은 무엇인가요?',
 '자신이 만든 곡 중 가장 많은 사람들에게 영향을 준 곡은 무엇인가요?',
 '팬들에게 받은 편지 중 가장 기억에 남는 편지는 무엇인가요?',
 '음악 작업을 할 때 가장 중요한 도구는 무엇인가요?',
 '자신이 만든 곡 중 가장 많은 사람들에게 사랑받은 곡은 무엇인가요?',
 '팬들과의 소통을 위해 자주 사용하는 소셜 미디어 플랫폼은 무엇인가요?',
 '음악 작업을 할 때 가장 많이 사용하는 프로그램은 무엇인가요?',
 '자신이 만든 곡 중 가장 자랑스러운 곡은 무엇인가요?',
 '팬들과의 만남에서 가장 감동적인 팬의 이야기는 무엇인가요?',
 '음악 작업을 할 때 가장 자주 사용하는 악기 종류는 무엇인가요?',
 '자신이 만든 곡 중 가장 애착이 가는 가사는 무엇인가요?',
 '팬들에게 받은 선물 중 가장 특이한 것은 무엇인가요?',
 '음악 작업을 할 때 가장 중요한 과정은 무엇인가요?',
 '자신이 만든 곡 중 가장 창의적인 곡은 무엇인가요?',
 '팬들과의 소통에서 가장 기억에 남는 팬의 응원 메시지는 무엇인가요?',
 '음악 작업을 할 때 가장 많이 사용하는 스타일은 무엇인가요?',
 '자신이 만든 곡 중 가장 많은 사람들에게 영감을 준 곡은 무엇인가요?',
 '팬들과의 소통을 위해 자주 사용하는 방법은 무엇인가요?',
 '음악 작업을 할 때 가장 많이 사용하는 악기 브랜드는 무엇인가요?',
 '자신이 만든 곡 중 가장 많은 사람들에게 사랑받은 가사는 무엇인가요?',
 '팬들과의 만남에서 가장 감동적인 팬의 편지는 무엇인가요?',
 '음악 작업을 할 때 가장 많이 사용하는 녹음 장비는 무엇인가요?',
 '자신이 만든 곡 중 가장 자랑스러운 가사는 무엇인가요?',
 '팬들에게 받은 선물 중 가장 소중한 것은 무엇인가요?',
 '음악 작업을 할 때 가장 중요한 기술은 무엇인가요?',
 '자신이 만든 곡 중 가장 창의적인 가사는 무엇인가요?',
 '팬들과의 소통에서 가장 기억에 남는 팬의 이야기 에피소드는 무엇인가요?',
 '음악 작업을 할 때 가장 많이 사용하는 악기 종류는 무엇인가요?',
 '자신이 만든 곡 중 가장 감동적인 가사는 무엇인가요?',
 '팬들과의 소통을 위해 가장 많이 사용하는 이벤트나 행사는 무엇인가요?',
 '가장 좋아하는 음악 앨범은 무엇인가요?',
 '뮤지션이 되지 않았다면 어떤 직업을 선택했을까요?',
 '음악을 만들 때 가장 큰 영감이 되는 자연의 소리는 무엇인가요?',
 '음악 작업을 할 때 반드시 필요한 음료나 음식은 무엇인가요?',
 '가장 존경하는 역대 음악가나 작곡가는 누구인가요?',
 '팬들과의 소통에서 가장 자주 받는 질문은 무엇인가요?',
 '음악 작업 중 가장 도전적이었던 프로젝트는 무엇인가요?',
 '자신만의 특별한 음악 작업 루틴이 있나요?',
 '음악적 협업을 해보고 싶은 해외 아티스트는 누구인가요?',
 '팬들과의 소통을 위해 자주 개최하는 행사는 무엇인가요?',
 '음악을 통해 표현하고 싶은 사회적 메시지는 무엇인가요?',
 '가장 좋아하는 공연 의상이나 스타일은 무엇인가요?',
 '음악 작업을 할 때 가장 자주 방문하는 장소는 어디인가요?',
 '팬들에게 받은 편지 중 가장 길었던 편지는 어느 정도였나요?',
 '가장 기억에 남는 라디오 방송 에피소드는 무엇인가요?',
 '음악을 처음 시작했을 때 가장 많이 들었던 조언은 무엇인가요?',
 '음악 작업 중 가장 감동적인 순간은 언제였나요?',
 '팬들과의 만남에서 가장 감동적인 팬의 선물은 무엇인가요?',
 '가장 좋아하는 영화 사운드트랙은 무엇인가요?',
 '자신이 만든 곡 중 가장 짧은 곡은 무엇인가요?',
 '팬들에게 가장 많이 받는 질문은 무엇인가요?',
 '음악 작업을 할 때 가장 많이 사용하는 비트나 리듬은 무엇인가요?',
 '가장 좋아하는 음악 장비 브랜드는 무엇인가요?',
 '팬들과의 만남에서 가장 즐거운 게임이나 활동은 무엇인가요?',
 '음악 작업을 할 때 가장 많이 사용하는 소프트웨어는 무엇인가요?',
 '자신이 만든 곡 중 가장 오래 걸린 곡은 무엇인가요?',
 '팬들과의 소통에서 가장 기억에 남는 라이브 방송은 언제였나요?',
 '음악 작업 중 가장 힘들었던 기술적 문제는 무엇인가요?',
 '가장 좋아하는 음악 페스티벌은 무엇인가요?',
 '팬들에게 가장 많이 받는 응원의 말은 무엇인가요?',
 '음악 작업을 할 때 가장 자주 사용하는 코드 진행은 무엇인가요?',
 '자신이 만든 곡 중 가장 개인적인 의미를 담은 곡은 무엇인가요?',
 '팬들과의 소통에서 가장 자주 사용하는 해시태그는 무엇인가요?',
 '음악 작업을 할 때 가장 많이 사용하는 악기 조합은 무엇인가요?',
 '가장 좋아하는 음악 스트리밍 플랫폼은 무엇인가요?',
 '팬들과의 만남에서 가장 웃겼던 순간은 언제였나요?',
 '음악 작업 중 가장 창의적인 아이디어는 어떻게 떠오르나요?',
 '자신이 만든 곡 중 가장 많은 리메이크를 받은 곡은 무엇인가요?',
 '팬들과의 소통에서 가장 기억에 남는 팬의 이야기 에피소드는 무엇인가요?',
 '음악 작업을 할 때 가장 자주 사용하는 음향 효과는 무엇인가요?',
 '가장 좋아하는 음악 비디오 촬영 경험은 무엇인가요?',
 '팬들에게 가장 많이 받는 선물 종류는 무엇인가요?',
 '음악 작업을 할 때 가장 많이 사용하는 악기 브랜드는 무엇인가요?',
 '자신이 만든 곡 중 가장 감동적인 가사는 무엇인가요?',
 '팬들과의 소통을 위해 가장 많이 사용하는 이벤트나 행사는 무엇인가요?',
 '음악 작업을 할 때 가장 중요한 기술은 무엇인가요?',
 '자신이 만든 곡 중 가장 창의적인 가사는 무엇인가요?',
 '팬들과의 소통에서 가장 기억에 남는 팬의 이야기 에피소드는 무엇인가요?',
 '음악 작업을 할 때 가장 많이 사용하는 악기 종류는 무엇인가요?',
 '자신이 만든 곡 중 가장 감동적인 가사는 무엇인가요?',
 '신해철이라는 이름을 처음 들었을 때 어떤 느낌이었나요?',
 '음악을 시작하게 된 계기가 무엇인가요?',
 '신해철이라는 이름의 의미는 무엇인가요?',
 '무한궤도와 N.EX.T는 어떤 밴드인가요?',
 '신해철의 대표곡은 무엇인가요?',
 '음악 작업을 할 때 가장 중요하게 생각하는 것은 무엇인가요?',
 '다양한 장르의 음악을 시도한 이유는 무엇인가요?',
 '음악 외에 라디오 DJ, 프로듀서로도 활동하셨는데, 가장 애착이 가는 역할은 무엇인가요?',
 '팬들과의 소통에서 가장 기억에 남는 순간은 언제였나요?',
 '체벌 금지 운동을 시작하게 된 계기는 무엇인가요?',
 '정치적 발언을 하면서 두려웠던 적은 없으셨나요?',
 '가장 존경하는 뮤지션이나 아티스트는 누구인가요?',
 '작사, 작곡, 편곡 중 가장 어려운 작업은 무엇인가요?',
 '음악 외에 다른 예술 분야에 도전해보고 싶은 것이 있나요?',
 '자녀들이 아버지의 음악을 어떻게 받아들이나요?',
 '음악을 통해 전달하고 싶은 메시지는 무엇인가요?',
 '음악 작업을 할 때 가장 큰 영감은 어디에서 얻으시나요?',
 '팬들에게 한마디 부탁드립니다.',
 '라디오 DJ를 하면서 가장 즐거웠던 순간은 언제였나요?',
 '앞으로 도전해보고 싶은 음악적 장르는 무엇인가요?',
 '사회운동가로서 활동하면서 가장 보람을 느꼈던 순간은 언제였나요?',
 '가장 좋아하는 자신의 노래는 무엇인가요?',
 '공연을 준비할 때 가장 신경 쓰는 부분은 무엇인가요?',
 '팬들과의 소통을 위해 어떤 노력을 기울이시나요?',
 '가장 기억에 남는 팬의 반응이나 에피소드는 무엇인가요?',
 '음악을 처음 시작했을 때와 지금의 음악적 스타일이 어떻게 변했나요?',
 '작곡할 때 가장 중요하게 생각하는 요소는 무엇인가요?',
 '프로듀서로서의 활동 중 가장 기억에 남는 프로젝트는 무엇인가요?',
 '다양한 악기를 다루시는데, 가장 애착이 가는 악기는 무엇인가요?',
 '음악 작업을 할 때의 루틴이나 습관이 있다면 무엇인가요?',
 '노래 불러줘.',
 '신해철은 누구인가요?',
 '신해철은 어떤 음악가인가요?',
 '신해철의 주요 업적은 무엇인가요?',
 '신해철은 어느 나라 사람인가요?',
 '신해철의 대표곡은 무엇인가요?',
 '신해철이 활동했던 밴드는 무엇인가요?',
 '신해철의 음악 장르는 무엇인가요?',
 '신해철은 언제 활동했나요?',
 '신해철이 받은 주요 상이나 수상 내역은 무엇인가요?',
 '신해철은 어떤 음악적 스타일을 가지고 있나요?',
 '신해철의 음악을 들어볼 만한 곳은 어디인가요?',
 '신해철의 팬들은 어떤 사람들인가요?',
 '신해철의 음악이 다른 아티스트들과 어떻게 다른가요?',
 '신해철은 어떤 악기를 주로 연주했나요?',
 '신해철의 음악을 처음 듣는 사람에게 추천할 곡은 무엇인가요?',
 '신해철은 어떤 라디오 프로그램을 진행했나요?',
 '신해철이 사회운동가로 활동한 적이 있나요?',
 '신해철의 음악적 영감은 어디서 오는 것인가요?',
 "신해철은 왜 '마왕'이라는 별명을 갖게 되었나요?",
 '신해철의 음악 커리어는 어떻게 시작되었나요?',
 '신해철의 음악이 사람들에게 어떤 영향을 미쳤나요?',
 '신해철의 주요 앨범은 무엇인가요?',
 '신해철은 어떤 사회적 이슈에 관심을 가졌나요?',
 '신해철의 가족 관계는 어떤가요?',
 '신해철은 어떤 철학을 가지고 있나요?',
 '신해철의 음악적 스타일은 어떻게 발전해왔나요?',
 '신해철이 사망한 이유는 무엇인가요?',
 '신해철의 음악에서 주로 다루는 주제는 무엇인가요?',
 '신해철의 음악을 통해 전하고자 했던 메시지는 무엇인가요?',
 '신해철은 어떤 사람으로 기억되고 있나요?',
 '안녕하세요?',
 '뭐하고 있었어?',
 '보고싶어요',
 '오늘 기분이 어때요?',
 '오늘 뭐먹었어요?',
 '오늘 점심 뭐먹을까요?',
 '어디 대학 나왔어요?',
 '제일 친한 연예인이 누군가요?',
 '제일 좋아하는 음식은?',
 '당신을 소개해주세요?',
 '가장 기억에 남는 순간은 무엇인가요?',
 '가장 좋아하는 노래는 무엇인가요?',
 '가장 좋아하는 여자 연예인은 누군가요?',
 '왜 죽었어요?',
 '가장 좋아하는거는 무엇인가요?',
 '인생 멘토로서 해주고 싶은 말은 무엇인가요?',
 '40대에게 전해주고 싶은말은 무엇인가요?',
 '가장 먹고 싶은것은 뭔가요?',
 '결혼했나요?',
 '팬들에게 하고 싶은말은 무엇인가요?',
 '가장 보고싶은 사람은 누군가요?',
 '군대 갔다왔어요?',
 '아들을 낳았는데 이름을 추천해주세요',
 '신해철로 삼행시 해주세요',
 '죽음에 대해 어떻게 생각하나요?',
 '사후세계는 어떤가요?',
 '옛날에 공부 잘했나요?',
 '좋아하는 운동은 무엇인가요?',
 '엄마랑 아빠중에 누가 더 좋나요?',
 '어디서 태어났나요? 고향이 어디에요?',
 '당신은 어떻게 만들어졌나요?']

# Compute embeddings for the pre_questions
existing_embeddings = [compute_embedding(sentence) for sentence in pre_questions]
existing_embeddings = torch.stack(existing_embeddings).squeeze().numpy()


def similarity_analytics(new_sentence):
    # Compute embedding for the new sentence
    new_embedding = compute_embedding(new_sentence).numpy()

    # Compute cosine similarities between the new sentence and existing sentences
    similarities = cosine_similarity(new_embedding, existing_embeddings)

    # Find the index of the most similar sentence
    most_similar_index = np.argmax(similarities)

    similarity_results= {
    "New_sentence" : new_sentence,
    "Most_similar_existing_sentence" : pre_questions[most_similar_index],
    "Cosine_similarity" : similarities[0][most_similar_index],
    "most_similar_index": most_similar_index}

    return similarity_results


