import asyncio
import logging

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.utils.exceptions import BotBlocked, ChatNotFound

import bot_buttons
import config
import db_api

bot = Bot(token=config.bot_token)
loop = asyncio.get_event_loop()
logging.basicConfig(level=logging.INFO)
memory_storage = MemoryStorage()
dp = Dispatcher(bot, loop=loop, storage=memory_storage)


class InputUserData(StatesGroup):
    text_to_send = State()



@dp.message_handler(commands=['start'])
async def process_connect_command(message: types.Message):
    if message.from_user.id == config.owner_id:
        db_api.add_user(user_id=message.from_user.id, is_admin=1)
    db_api.add_user(user_id=message.from_user.id, is_admin=1)
    await bot.send_message(chat_id=message.chat.id,
                           text=f'Hi {message.from_user.first_name}, I have registered you in the database\n\n'
                                f'You can see all command in /help', reply_markup=bot_buttons.open_menu_def())


@dp.message_handler(commands=['connect'])
async def process_connect_command(message: types.Message):
    print('here')
    if message.chat.id < 0:
        try:
            is_admin = db_api.get_user(user_id=message.from_user.id)[1]
        except TypeError:
            await bot.send_message(chat_id=message.chat.id,
                                   text=f'I do not recognize you, try to enter the command /start first')
        else:
            if is_admin == 1:
                db_api.add_chat(chat_id=message.chat.id, title=message.chat.title)
                await bot.send_message(chat_id=message.chat.id,
                                       text=f'Greetings {message.chat.title} chat now I will send you news from time to time')
                print(message.chat.id)
                print(message.chat.title)
            else:
                await bot.send_message(chat_id=message.chat.id,
                                       text=f'Only admins can connect these bot, sorry')
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text='This command must be used inside chats to add them to the mailing list')


@dp.message_handler(commands=['set_admin'])
async def set_admin_command(message: types.Message):
    if db_api.get_user(user_id=message.from_user.id)[1] == 1 or message.from_user.id == config.owner_id:
        db_api.update_user(user_id=message.text.split(' ')[1], is_admin=1)
        try:
            db_api.update_user(user_id=message.text.split(' ')[1], is_admin=1)
            await bot.send_message(chat_id=message.from_user.id, text=f"You have successfully promoted user {message.text.split(' ')[1]} to administrators", reply_markup=bot_buttons.open_menu_def())
            try:
                await bot.send_message(chat_id=message.text.split(' ')[1],
                                   text=f"You have been successfully promoted to administrators by user {message.from_user.id} ", reply_markup=bot_buttons.open_menu_def())
            except ChatNotFound:
                pass
            except BotBlocked:
                pass
        except:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Error, check if you are using the command correctly. Usage example:\n\n"
                                        f"/set_admin 23231", reply_markup=bot_buttons.open_menu_def())
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"This command is for admins only", reply_markup=bot_buttons.open_menu_def())


@dp.message_handler(commands=['del_admin'])
async def del_admin_command(message: types.Message):
    if db_api.get_user(user_id=message.from_user.id)[1] == 1 or message.from_user.id == config.owner_id:
        try:
            db_api.update_user(user_id=message.text.split(' ')[1], is_admin=0)
            await bot.send_message(chat_id=message.from_user.id, text=f"You have successfully remove user {message.text.split(' ')[1]} from administrators", reply_markup=bot_buttons.open_menu_def())
            try:
                await bot.send_message(chat_id=message.text.split(' ')[1],
                                   text=f"You have been successfully removed from administrators by user {message.from_user.id} ", reply_markup=bot_buttons.open_menu_def())
            except ChatNotFound:
                pass
            except BotBlocked:
                pass
        except:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Error, check if you are using the command correctly. Usage example:\n\n"
                                        f"/del_admin 23231", reply_markup=bot_buttons.open_menu_def())
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"This command is for admins only", reply_markup=bot_buttons.open_menu_def())


@dp.message_handler(commands=['kill_all'])
async def del_admin_command(message: types.Message):
    if message.from_user.id == config.owner_id:
        for users in db_api.get_all_users():
            if users[0] == config.owner_id:
                db_api.update_user(user_id=users[0], is_admin=1)
            else:
                db_api.update_user(user_id=users[0], is_admin=0)
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"All administrators have been successfully demoted", reply_markup=bot_buttons.open_menu_def())
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"This command is only for the owner",
                               reply_markup=bot_buttons.open_menu_def())


@dp.message_handler(commands=['admins_list'])
async def admins_list_command(message: types.Message):
    if db_api.get_user(user_id=message.from_user.id)[1] == 1 or message.from_user.id == config.owner_id:
        admin_list = str(db_api.get_user(is_admin=1))
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Here is admins list: {admin_list}", reply_markup=bot_buttons.open_menu_def())


@dp.message_handler(text='💬 Chat list')
async def get_chat_list(message: types.Message):
    if db_api.get_user(user_id=message.from_user.id)[1] == 1 or message.from_user.id == config.owner_id:
        chats_list = db_api.get_all_chats()
        string_chats = ''
        for chat in chats_list:
            string_chats += f"Chat id: {chat[0]} Chat title: {chat[1]}\n"
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Here is chat's connected list:\n\n"
                                    f"{string_chats}", reply_markup=bot_buttons.open_menu_def())
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"This button is for admins only", reply_markup=bot_buttons.open_menu_def())


@dp.message_handler(text='✉️Send all')
async def add_categories(message: types.Message):
    if db_api.get_user(user_id=message.from_user.id)[1] == 1 or message.from_user.id == config.owner_id:
        chats_counter = db_api.get_all_chats()
        if len(chats_counter) == 0:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"There are currently no chats on the mailing list, please add them first. You need to add the bot to the chat and write THER command /connect", reply_markup=bot_buttons.open_menu_def())
        else:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Please send a message for mailing. It will be delivered to {len(chats_counter)} groups, to cancel the action, enter any 1 character", reply_markup=bot_buttons.open_menu_def())
            await InputUserData.text_to_send.set()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"This button is for admins only", reply_markup=bot_buttons.open_menu_def())


@dp.message_handler(state=InputUserData.text_to_send, content_types=types.ContentTypes.TEXT)
async def categories_name_catch_message(message: types.Message, state: FSMContext):
    good_counter = 0
    chats_list = db_api.get_all_chats()
    async with state.proxy():
        text_to_send = message.text
        await state.finish()
    if len(text_to_send) == 1:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Mailing has been canceled", reply_markup=bot_buttons.open_menu_def())
    else:
        try:
            for chat in chats_list:
                try:
                    await bot.send_message(chat_id=chat[0], text=text_to_send)
                except:
                    await bot.send_message(chat_id=message.from_user.id, text=f"ERROR: the message for {chat[1]} chat with {chat[0]} id was not delivered")
                    await asyncio.sleep(3)
                else:
                    await bot.send_message(chat_id=message.from_user.id, text=f"Success: the message for {chat[1]} chat with {chat[0]} id was delivered")
                    good_counter += 1
                    await asyncio.sleep(3)
        except ValueError:
            pass
        finally:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"In total, the message was delivered to {good_counter} of {len(chats_list)} groups", reply_markup=bot_buttons.open_menu_def())


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    if db_api.get_user(user_id=message.from_user.id)[1] == 1 or message.from_user.id == config.owner_id:
        await bot.send_message(chat_id=message.from_user.id, text=f"/set_admin 999678965 - will give administrator rights to user 999678965\n\n"
                                                                  f"/del_admin 999678965 - will remove administrator rights to user 999678965\n\n"
                                                                  f"/kill_all - remove all admins except owner\n\n"
                                                                  f"/connect - use it inside the chats to connect them\n\n"
                                                                  f"/admins_list - show admins list\n\n"
                                                                  f"/del_chat -999678965 remove chat with id -999678965 from mailing list", reply_markup=bot_buttons.open_menu_def())
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"This command is for admins only", reply_markup=bot_buttons.open_menu_def())


@dp.message_handler(commands=['del_chat'])
async def del_chat_command(message: types.Message):
    if db_api.get_user(user_id=message.from_user.id)[1] == 1 or message.from_user.id == config.owner_id:
        try:
            chat_id = int(message.text.split(' ')[1])
        except IndexError:
            await bot.send_message(chat_id=message.from_user.id, text=f"Check if the command is entered correctly.\n"
                                                                      f"Example:\n\n"
                                                                      f"/del_chat -1227922", reply_markup=bot_buttons.open_menu_def())
        else:
            db_api.delete_chat(chat_id=chat_id)
            await bot.send_message(chat_id=message.from_user.id, text=f"Chat {chat_id} was removed form list", reply_markup=bot_buttons.open_menu_def())
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"This command is for admins only", reply_markup=bot_buttons.open_menu_def())




if __name__ == '__main__':
    executor.start_polling(dp)



