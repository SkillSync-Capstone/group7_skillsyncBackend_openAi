import os
from dotenv import load_dotenv
import boto3

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.vectorstores import Chroma

# Define a custom document loader
class SimpleTextLoader:
    def __init__(self, documents):
        self.documents = documents

    def load(self):
        return self.documents

load_dotenv()
os.environ['OPENAI_API_KEY']

def handle_new_query(query, PERSIST=False):
    s3 = boto3.client('s3')

    if PERSIST and os.path.exists("persist"):
        print("Reusing index...\n")
        vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
        index = VectorStoreIndexWrapper(vectorstore=vectorstore)
    else:
        response = s3.get_object(
            Bucket="cyclic-plum-cautious-woodpecker-ap-southeast-2",
            Key="text_files/Kevin_resume.txt"
        )
        file_content = response['Body'].read().decode('utf-8')
        # Use the custom loader
        loader = SimpleTextLoader(documents=[file_content])
        
        if PERSIST:
            index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": "persist"}).from_loaders([loader])
        else:
            index = VectorstoreIndexCreator().from_loaders([loader])

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-3.5-turbo"),
        retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
    )

    if query.lower() in ['quit', 'q', 'exit']:
        return {"error": "Query to exit received."}
    
    result = chain({"question": query, "chat_history": []})
    
    return {"answer": result['answer']}

