from sample_config import Config
from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import contextlib, asyncio

UPDATE_CHANNEL = Config.UPDATE_CHANNEL

# @Client.on_message(filters.text)
# async def forcesub(c:Client, m:Message):
#     print(True)
#     if Config.UPDATE_CHANNEL:
#         invite_link = await c.create_chat_invite_link(Config.UPDATE_CHANNEL)
#         try:
#             user = await c.get_chat_member(Config.UPDATE_CHANNEL, m.from_user.id)
#             if user.status == "kicked":
#                await m.reply_text("**Hey You Are Banned 😜**", quote=True)
#                return
#         except UserNotParticipant:
#             buttons = [[InlineKeyboardButton(text='🍿Updates Channel🍿', url=invite_link.invite_link)]]
            

#             delete_msg = await m.reply_text(
#                 "**Hey! 😊**\n\n"
#                 "**You Have To Join Our Update Channel To Use Me ✅**\n\n"
#                 "**Click Bellow Button To Join Now.👇**",
#                 reply_markup=InlineKeyboardMarkup(buttons),
#                 quote=True
#             )
#             await asyncio.sleep(60)
#             await delete_msg.delete()
#             return
#         except Exception as e:
#             print(e)
#             await m.reply_text("Something Wrong. Please try again later", quote=True)
#             return
            
#     await m.continue_propagation()