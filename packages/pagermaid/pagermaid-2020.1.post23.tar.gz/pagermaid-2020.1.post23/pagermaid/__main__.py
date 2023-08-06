""" PagerMaid launch sequence. """

from sys import path
from os import getcwd
from importlib import import_module
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from pagermaid import logs, bot
from pagermaid.modules import module_list, plugin_list

invalid_phone = '\nInvalid phone number entered.' \
                '\nPlease make sure you specified' \
                '\nyour country code in the string.'

path.insert(1, f"{getcwd()}/plugins")

try:
    bot.start()
except PhoneNumberInvalidError:
    print(invalid_phone)
    exit(1)
for module_name in module_list:
    try:
        imported_module = import_module("pagermaid.modules." + module_name)
    except BaseException:
        logs.info(f"Unable to load module {module_name}.")
for plugin_name in plugin_list:
    try:
        imported_plugin = import_module("plugins." + plugin_name)
    except BaseException:
        logs.info(f"Unable to load plugin {plugin_name}.")
logs.info("PagerMaid have started, The prefix is -, type -help for help message.")
bot.run_until_disconnected()
