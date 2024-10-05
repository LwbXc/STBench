from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


class chatgpt(object):

    def __init__(self, api_key, max_new_tokens=5):
        OpenAIChatModel = ChatOpenAI(
            temperature=0,
            max_tokens=max_new_tokens,
            openai_api_key=api_key,
            model_name="gpt-3.5-turbo-1106"
        )
        self.api_key = api_key
        self.max_new_tokens = max_new_tokens
        self._init_chain(OpenAIChatModel)
        self.model_path = "chatgpt"

    def _init_chain(self, chat_model):
        common_prompt = ChatPromptTemplate.from_messages(
            [
                "{question}"
            ]
        )
        self.common_chain = (
            {"question": RunnablePassthrough()}
            | common_prompt
            | chat_model
            | StrOutputParser()
        )

    def generate(self, code: str, max_new_tokens: int):
        if max_new_tokens is not None and max_new_tokens!=self.max_new_tokens:
            OpenAIChatModel = ChatOpenAI(
                temperature=0,
                max_tokens=max_new_tokens,
                openai_api_key=self.api_key,
                model_name="gpt-3.5-turbo-1106"
            )
            self.max_new_tokens = max_new_tokens
            self._init_chain(OpenAIChatModel)
        return self.common_chain.invoke(code)
    
if __name__=='__main__':
    model = chatgpt()
    print(model.generate("Yesterday was Thursday, today is Friday, so tomorrow is ", 5))
    print(model.generate("Yesterday was 2022-01-01, today is 2022-01-02, so tomorrow is ", 20))