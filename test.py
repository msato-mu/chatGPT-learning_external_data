import ipywidgets as widgets
from IPython.display import display
import os
import pandas as pd
import requests
import textract
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from transformers import GPT2TokenizerFast
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain

# ここにOpenAIから取得したキーを設定します。
os.environ["OPENAI_API_KEY"] = ''

""" # インターネット上からマニュアルファイルをダウンロード（BuffaloTerastation)
url = 'https://manual.buffalo.jp/buf-doc/35021178-39.pdf'
response = requests.get(url)
# Ensure that the request was successful
if response.status_code == 200:
    # Save the content of the response as a PDF file
    with open('sample_document1.pdf', 'wb') as file:
        file.write(response.content)
else:
    print("Error: Unable to download the PDF file. Status code:",
          response.status_code)

# インターネット上からマニュアルファイルをダウンロード（サイボウズOfficeユーザマニュアル）
url = 'https://jp.cybozu.help/o/pdf/manual_o_user.pdf'
response = requests.get(url)
# Ensure that the request was successful
if response.status_code == 200:
    # Save the content of the response as a PDF file
    with open('sample_document2.pdf', 'wb') as file:
        file.write(response.content)
else:
    print("Error: Unable to download the PDF file. Status code:",
          response.status_code)
 """

# ページごとに分割。この方法だと、メタデータの情報が取得できるので、マニュアルのページ数などを表示することも可能となるが、
# トークンサイズが大きくなりがち。
# また、PDFの様なページ分割されている情報がソースとなっている必要がある
# Simple method - Split by pages
# https://manual.buffalo.jp/buf-doc/35021178-39.pdf
# loader = PyPDFLoader("/content/sample_data/buffalo_manual.pdf")
loader = PyPDFLoader("data/sample_document1.pdf")
pages = loader.load_and_split()
print(pages[0])

# SKIP TO STEP 2 IF YOU'RE USING THIS METHOD
chunks = pages

# 上級者向けの方法　チャンクに分割。これだとメタデータの情報が取れない

# Step 1: Convert PDF to text
doc = textract.process("data/sample_document2.pdf")
# Step 2: Save to .txt and reopen (helps prevent issues)
with open('attention_is_all_you_need.txt', 'w') as f:
    f.write(doc.decode('utf-8'))

with open('attention_is_all_you_need.txt', 'r') as f:
    text = f.read()

# Step 3: Create function to count tokens
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")


def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))


# Step 4: Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=512,
    chunk_overlap=24,
    length_function=count_tokens,
)

chunks2 = text_splitter.create_documents([text])

# chank3つ目。3つ目は、インターネット上のドキュメントから情報を取得する
""" url = "https://mui.com/material-ui/getting-started/overview/"
response = requests.get(url)

if response.status_code == 200:
    html_content = response.text
else:
    print("Failed to fetch the webpage")

# インターネット上のサイトから抽出した情報をDBに入れる
# Step 2: Save to .txt and reopen (helps prevent issues)
with open('internet_info1.txt', 'w') as f:
    f.write(html_content)

with open('internet_info1.txt', 'r') as f:
    text = f.read()

# Step 3: Create function to count tokens
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")


def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))


# Step 4: Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    # chunk_size = 512,
    chunk_size=512,
    chunk_overlap=24,
    length_function=count_tokens,
)
 """
# chunks3 = text_splitter.create_documents([text])
chunks3 = chunks2

# Get embedding model
embeddings = OpenAIEmbeddings()

#  vector databaseの作成
db = FAISS.from_documents(chunks+chunks2+chunks3, embeddings)

query = "ランプが点滅しているが、これは何が原因か？"
docs = db.similarity_search(query)
docs  # ここで関係のありそうなデータが返ってきていることを確認できる

# 得られた情報から回答を導き出すためのプロセスを以下の4つから選択する。いずれもProsとConsがあるため、適切なものを選択する必要がある。
# staffing ... 得られた候補をそのままインプットとする
# map_reduce ... 得られた候補のサマリをそれぞれ生成し、そのサマリのサマリを作ってインプットとする
# map_rerank ... 得られた候補にそれぞれスコアを振って、いちばん高いものをインプットとして回答を得る
# refine  ... 得られた候補のサマリを生成し、次にそのサマリと次の候補の様裏を作ることを繰り返す
chain = load_qa_chain(
    OpenAI(temperature=0.2, max_tokens=1000), chain_type="stuff")
query = "ランプが赤色に点滅しているが、これは何が原因か？"
docs = db.similarity_search(query)
# langchainを使って検索
chain.run(input_documents=docs, question=query)


# vextordbをretrieverとして使うconversation chainを作成します。これはチャット履歴の管理も可能にします。
qa = ConversationalRetrievalChain.from_llm(
    OpenAI(temperature=0.1), db.as_retriever())
chat_history = []


def on_submit(_):
    query = input_box.value
    input_box.value = ""

    if query.lower() == 'exit':
        print("Thank you for using the State of the Union chatbot!")
        return

    result = qa({"question": query, "chat_history": chat_history})
    chat_history.append((query, result['answer']))

    display(widgets.HTML(f'<b>User:</b> {query}'))
    display(widgets.HTML(
        f'<b><font color="blue">Chatbot:</font></b> {result["answer"]}'))


print("Welcome to the Transformers chatbot! Type 'exit' to stop.")

input_box = widgets.Text(placeholder='Please enter your question:')
input_box.on_submit(on_submit)

display(input_box)
