import os
import boto3
from dotenv import load_dotenv

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.vectorstores import Chroma

class SimpleTextLoader:
    """ Custom document loader class to load documents for indexing. """
    def __init__(self, documents):
        self.documents = documents

    def load(self):
        return self.documents

def setup_logging():
    """ Sets up logging configuration. """
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

def initialize_environment():
    """ Loads environment variables and checks essential keys. """
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in the environment.")
    return api_key

def get_s3_content(bucket_name, key):
    """ Retrieves content from an S3 bucket and key, returns as a string. """
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=bucket_name, Key=key)
        return response['Body'].read().decode('utf-8')
    except Exception as e:
        logger.error("Failed to download or decode the file: %s", str(e))
        raise

def handle_new_query(query, PERSIST=False):
    """ Processes a new query using a conversational retrieval chain. """
    if query.lower() in ['quit', 'q', 'exit']:
        return {"error": "Query to exit received."}

    if PERSIST and os.path.exists("persist"):
        logger.info("Reusing index...\n")
        vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
        index = VectorStoreIndexWrapper(vectorstore=vectorstore)
    else:
        file_content = get_s3_content("cyclic-plum-cautious-woodpecker-ap-southeast-2", "text_files/Kevin_resume.txt")
        loader = SimpleTextLoader(documents=[file_content])
        if PERSIST:
            os.makedirs("persist", exist_ok=True)
            logger.info("Persisting index data...")
            index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": "persist"}).from_loaders([loader])
        else:
            index = VectorstoreIndexCreator().from_loaders([loader])

    try:
        chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(model="gpt-3.5-turbo"),
            retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
        )
        result = chain({"question": query, "chat_history": []})
        return {"answer": result['answer']}
    except Exception as e:
        logger.error("Error processing the query: %s", str(e))
        return {"error": str(e)}

if __name__ == "__main__":
    logger = setup_logging()
    try:
        api_key = initialize_environment()
        result = handle_new_query("How does the vectorstore work?")
        print(result)
    except Exception as e:
        logger.error("An error occurred: %s", str(e))
