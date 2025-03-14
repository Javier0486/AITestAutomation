import asyncio
import os

from browser_use.agent.service import Agent
from browser_use.controller.service import Controller
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import Secret, SecretStr, BaseModel


class CheckoutResult(BaseModel):
    login_status : str
    cart_status : str
    checkout_your_information_status : str
    checkout_overview_status : str
    delivery_location_status : str
    confirmation_message : str

controller = Controller(output_model = CheckoutResult)

async def SiteValidation():
    os.environ["GEMINI_API_KEY"] = "xxx"
    task = (
        'Important : I am UI Automation tested validating the tasks'
        'Open website https://www.saucedemo.com/'
        'Login with username(standard_user) and password. login Details available in the same page'
        'After login, select first 2 products and add them to cart'
        'story the names and price of the products added'
        'Then go to cart and search for the products'
        'click checkout and enter First Name (Javier), Last Name (Munoz), Zip/Postal Code (85796)'
        'click Continue'
        'verify products added are displayed'
        'click on Finish' 
        'verify thankyou message is displayed'
    )
    api_key = os.environ["GEMINI_API_KEY"]
    llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key= SecretStr(api_key))
    agent = Agent(task=task, llm=llm, controller=controller, use_vision=True)
    history = await  agent.run()
    test_result = history.final_resut()
    print(test_result)

    assert test_result.confirmation_message == "Thank you for your order! Your order has been dispatched, and will arrive just as fast as the pony can get there!"


asyncio.run(SiteValidation())