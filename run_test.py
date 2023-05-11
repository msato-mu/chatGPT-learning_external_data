from IPython.display import display
import ipywidgets as widgets

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
