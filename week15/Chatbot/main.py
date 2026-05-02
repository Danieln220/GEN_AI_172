import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from pinecone import Pinecone, ServerlessSpec

load_dotenv()


class ChatBot():
    def __init__(self):
        loader = TextLoader('./horoscope.txt', encoding='utf-8')
        documents = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=4)
        docs = text_splitter.split_documents(documents)

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )

        index_name = "langchain-demo"

        pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                metric="cosine",
                dimension=768,
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
            docsearch = PineconeVectorStore.from_documents(docs, embeddings, index_name=index_name)
        else:
            docsearch = PineconeVectorStore.from_existing_index(index_name, embeddings)

        repo_id = "Qwen/Qwen2.5-7B-Instruct"
        llm = ChatHuggingFace(
            llm=HuggingFaceEndpoint(
                repo_id=repo_id,
                task="conversational",
                provider="auto",
                temperature=0.8,
                top_k=50,
                huggingfacehub_api_token=os.getenv('HUGGINGFACE_API_KEY')
            )
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a fortune teller. These Human will ask you a questions about their life.
Use following piece of context to answer the question.
If you don't know the answer, just say you don't know.
Keep the answer within 2 sentences and concise.

Context: {context}"""),
            ("human", "{question}")
        ])

        self.rag_chain = (
            {"context": docsearch.as_retriever(), "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )


if __name__ == "__main__":
    bot = ChatBot()
    user_input = input("Ask me anything: ")
    result = bot.rag_chain.invoke(user_input)
    print(result)
