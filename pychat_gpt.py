from pyChatGPT import ChatGPT

conversation_id=input("What conversation id should be used?")
session_token=input("What session token should be used?")

if conversation_id == None or conversation_id == '':
    conversation_id=os.getenv('CONVERSATION_ID')

if session_token == None or session_token == '':
    session_token=os.getenv('SESSION_TOKEN' )# `__Secure-next-auth.session-token` cookie from https://chat.openai.com/chat

api = ChatGPT(session_token)  # auth with session token
api = ChatGPT(session_token, conversation_id=conversation_id)  # specify conversation id
api = ChatGPT(session_token, chrome_args=['--window-size=1920,768'])  # specify chrome args
api = ChatGPT(session_token, moderation=False)  # disable moderation
api = ChatGPT(session_token, verbose=True)  # verbose mode (print debug messages)

login_type=input("What type of auth would you like to use to login to the OpenAI api? (1 - Google, 2 - Microsoft, 3 - OpenAI)")
email_input=input("What email should be used to login?")
password=input("What password should be used to login?")

if login_type == 1:
    # auth with google login
    api = ChatGPT(auth_type='google', email=email_input, password=password)
elif login_type == 2:
    # auth with microsoft login
    api = ChatGPT(auth_type='microsoft', email=email_input, password=password)
elif login_type == 3:
    # auth with openai login (captcha solving using speech-to-text engine)
    api = ChatGPT(auth_type='openai', email=email_input, password=password)
    # auth with openai login (manual captcha solving)
    api = ChatGPT(
        auth_type='openai', captcha_solver=None,
        email=email_input, password=password
    )
    # auth with openai login (2captcha for captcha solving)
    api = ChatGPT(
        auth_type='openai', captcha_solver='2captcha', solver_apikey='abc',
        email=email_input, password=password
    )
    # reuse cookies generated by successful login before login,
    # if `login_cookies_path` does not exist, it will process logining  with `auth_type`, and save cookies to `login_cookies_path`
    # only works when `auth_type` is `openai` or `google`
    api = ChatGPT(auth_type='openai', email='example@xxx.com', password=password,
        login_cookies_path='your_cookies_path',
    )

resp = api.send_message('Hello, world!')
print(resp['message'])

api.reset_conversation()  # reset the conversation
api.clear_conversations()  # clear all conversations
api.refresh_chat_page()  # refresh the chat page