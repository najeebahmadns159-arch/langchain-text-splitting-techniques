from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
loader=PyPDFLoader('Edge-Computing-Cousre-Meterail_all.pdf')
docs=loader.load()
splitter=CharacterTextSplitter(
    chunk_size=10000000000000000000,
    chunk_overlap=0,
    separator=''
)
result=splitter.split_documents(docs)
print(result)