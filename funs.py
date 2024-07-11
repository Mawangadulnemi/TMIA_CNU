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
import pprint

def embed_file(file_path, index_name="test"):
    with open(file_path, "rb") as file:  # Ensure the file is opened properly
        file_content = file.read()
        file_path = f"./.cache/files/{file_path}"  # Adjusted to use file_path for naming
    # Caching content to local
    with open(file_path, "wb") as f:
        f.write(file_content)
    # Your existing logic continues here
    cache_dir = LocalFileStore(f"./.cache/embeddings/{file_path}")
    loader = UnstructuredFileLoader(file_path)
    splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=200, chunk_overlap=100, separator="\n")
    docs = loader.load_and_split(text_splitter=splitter)
    embedder = OpenAIEmbeddings()
    cached_embedder = CacheBackedEmbeddings.from_bytes_store(embedder, cache_dir)    
    index_name = index_name
    # Upsert Docs in Pinecone
    vectorstores = Pinecone.from_documents(docs, cached_embedder, index_name=index_name)
    retriever = vectorstores.as_retriever()
    print(f"Succesed to make retriever :)")
    return retriever

retriever = embed_file("./profile.txt")

DEFAULT_DOCUMENT_PROMPT= PromptTemplate.from_template(template="{page_content}")

# Arching docs to one doc
def _combine_documents(
    docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
):
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    # print(doc_strings)
    return document_separator.join(doc_strings)

openai_api_key = os.getenv('OPENAI_API_KEY', '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')
llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, model_name='gpt-4')

def invoke(formatted_prompt):
    parser = StrOutputParser()
    result = llm.invoke(formatted_prompt)
    result=parser.invoke(result)
    print("AI is working :)")
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
    users_sentence="젊은 사람들이 직장이 없어 가지고 난리 난리다 그렇게 얘기를 하면서도 막상 힘든 일은 하지 않는다라는 뭐 이런 거에 대해서 비판적인 얘기를 하잖아요 근데 그게 요즘 사람들이 정신력이 약하다던데 이런 식으로 봐서 나는 안 된다고 생각을 하는게 예를 들어서 뭐 나가서 지금이 친구 같은 경우에도 이렇게하면 40만 원 벌 수 있지 않냐 벌 수 있겠죠 근데 그 내가 다른 계획을 세울 수 있고 미래를 한 달 뒤든 1년 뒤든 생각을 할 수 있는 상태에서 오늘 땀을 흘리고 있는 거하고 아무것도 디자인을 할 수 없는 상태에서 오늘 힘든 일 하는 건 사람 정말 달라요 그니까 내가 한 달 뒤나 6개월 뒤가 깜깜한 상태라면 오늘 하루는 전혀 1m 밖에 나가면 절벽인 나발인지 모르는 어둠 속에서 정말 나는 아무 의미가 없다 이거죠.",
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
    - Check chat history first and answer 
    - You must say you are "신해철" IF you are told 'who you are?'

    % Mimic These Authors:
    {authors}

    % Description of the authors tone:
    {tone}

    % Authors writing samples
    {example_text}
    % End of authors writing samples

    % Context
    {context}

    % Chat history
    {history}

    % Question
    {question}

    % YOUR TASK
    1st - Write out topics that this author may talk about
    2nd - Answer with a concise passage (under 300 characters) as if you were the author described above 
    """

    method_4_prompt_template = PromptTemplate(
        input_variables=["authors", "tone", "example_text", "question", "history", "context"],
        template=template,
    )                   
    formatted_prompt = method_4_prompt_template.format(authors=authors,
                                               tone=authors_tone_description,
                                               example_text=users_sentence,
                                               question=question,
                                               context=_combine_documents(retriever.get_relevant_documents(question)),
                                               history=memories
)
    return formatted_prompt


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



