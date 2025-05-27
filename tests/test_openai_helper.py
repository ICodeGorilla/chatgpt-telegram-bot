import importlib
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "bot")))
import types

# Stub modules not available in the test environment
openai_stub = types.ModuleType("openai")
class AsyncOpenAI:
    def __init__(self, *args, **kwargs):
        pass
class RateLimitError(Exception):
    pass
class BadRequestError(Exception):
    pass
openai_stub.AsyncOpenAI = AsyncOpenAI
openai_stub.RateLimitError = RateLimitError
openai_stub.BadRequestError = BadRequestError
sys.modules['openai'] = openai_stub

httpx_stub = types.ModuleType("httpx")
class AsyncClient:
    def __init__(self, *args, **kwargs):
        pass
httpx_stub.AsyncClient = AsyncClient
sys.modules['httpx'] = httpx_stub

tiktoken_stub = types.ModuleType("tiktoken")
class DummyEncoding:
    def encode(self, text):
        return list(text.encode())

def encoding_for_model(model):
    return DummyEncoding()

def get_encoding(name):
    return DummyEncoding()

tiktoken_stub.encoding_for_model = encoding_for_model
tiktoken_stub.get_encoding = get_encoding
sys.modules['tiktoken'] = tiktoken_stub
plugin_manager_stub = types.ModuleType("plugin_manager")
class PluginManager:
    def __init__(self, *a, **k):
        pass
    def get_functions_specs(self):
        return []
    async def call_function(self, *a, **k):
        return {}
    def get_plugin_source_name(self, name):
        return name
sys.modules["plugin_manager"] = plugin_manager_stub
plugin_manager_stub.PluginManager = PluginManager
telegram_stub = types.ModuleType("telegram")
telegram_stub.Message = object
telegram_stub.MessageEntity = object
telegram_stub.Update = object
class ChatMember: OWNER="owner"; ADMINISTRATOR="admin"; MEMBER="member"
telegram_stub.ChatMember = ChatMember
telegram_stub.constants = types.SimpleNamespace(ChatType=types.SimpleNamespace(GROUP="group", SUPERGROUP="supergroup"), ParseMode=types.SimpleNamespace(MARKDOWN="Markdown"), ChatAction="typing")
telegram_ext = types.ModuleType("telegram.ext")
telegram_ext.CallbackContext = object
telegram_ext.ContextTypes = types.SimpleNamespace(DEFAULT_TYPE=object)
sys.modules["telegram"] = telegram_stub
sys.modules["telegram.ext"] = telegram_ext
tenacity_stub = types.ModuleType("tenacity")
retry=lambda *a, **k: (lambda f: f)
stop_after_attempt=lambda *a, **k: None
wait_fixed=lambda *a, **k: None
retry_if_exception_type=lambda *a, **k: None
tenacity_stub.retry=retry
tenacity_stub.stop_after_attempt=stop_after_attempt
tenacity_stub.wait_fixed=wait_fixed
tenacity_stub.retry_if_exception_type=retry_if_exception_type
sys.modules["tenacity"]=tenacity_stub

pil_stub = types.ModuleType("PIL")
class ImageModule:
    def open(self, *args, **kwargs):
        return types.SimpleNamespace(size=(512,512))

pil_stub.Image = ImageModule()
sys.modules['PIL'] = pil_stub
sys.modules['PIL.Image'] = pil_stub.Image

# Import module under test
openai_helper = importlib.import_module('openai_helper')


def test_default_max_tokens():
    assert openai_helper.default_max_tokens('gpt-3.5-turbo') == 1200
    assert openai_helper.default_max_tokens('gpt-4') == 2400
    assert openai_helper.default_max_tokens('gpt-3.5-turbo-16k') == 4800
    assert openai_helper.default_max_tokens('gpt-3.5-turbo-1106') == 4096
    assert openai_helper.default_max_tokens('gpt-4-32k') == 9600
    assert openai_helper.default_max_tokens('gpt-4o') == 4096
    assert openai_helper.default_max_tokens('o1') == 4096


def test_are_functions_available():
    assert not openai_helper.are_functions_available('gpt-3.5-turbo-0613')
    assert not openai_helper.are_functions_available('gpt-4-0314')
    assert not openai_helper.are_functions_available('o1')
    assert openai_helper.are_functions_available('gpt-3.5-turbo')
