import os
import re
import io
import asyncio
import pyrogram
import contextlib
import traceback
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.errors import UserNotParticipant
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from database.filters_mdb import (add_filter, find_filter, get_filters,
                                  delete_filter, count_filters)

from database.connections_mdb import active_connection
from database.users_mdb import add_user, all_users

from plugins.helpers import parser, split_quotes


@Client.on_message(filters.command(Config.ADD_FILTER_CMD))
async def addfilter(client, message):
    userid = message.from_user.id
    chat_type = message.chat.type
    args = message.text.html.split(None, 1)

    if str(userid) not in Config.AUTH_USERS:
        return

    if chat_type == "private":
        grp_id = message.chat.id
        title = "All Filters"
    elif chat_type in ["group", "supergroup"]:
        grp_id = message.chat.id
        title = "All Filters"
    else:
        return

    if chat_type in ["group", "supergroup"]:
        st = await client.get_chat_member(grp_id, userid)
        if st.status != "administrator" and st.status != "creator" and str(
                userid) not in Config.AUTH_USERS:
            return

    if len(args) < 2:
        await message.reply_text("Command Incomplete :(", quote=True)
        return
    extracted = split_quotes(args[1])
    text = extracted[0].lower()
    if not message.reply_to_message and len(extracted) < 2:
        await message.reply_text("Add some content to save your filter!",
                                 quote=True)
        return
    if len(extracted) >= 2 and not message.reply_to_message:
        reply_text, btn, alert = parser(extracted[1], text)
        fileid = None
        if not reply_text:
            await message.reply_text(
                "You cannot have buttons alone, give some text to go with it!",
                quote=True)

            return
    elif message.reply_to_message and message.reply_to_message.reply_markup:
        try:
            rm = message.reply_to_message.reply_markup
            btn = rm.inline_keyboard
            if msg := message.reply_to_message.document or message.reply_to_message.video or message.reply_to_message.photo or message.reply_to_message.audio or message.reply_to_message.animation or message.reply_to_message.sticker:
                fileid = msg.file_id
                reply_text = message.reply_to_message.caption.html
            else:
                reply_text = message.reply_to_message.text.html
                fileid = None
            alert = None
        except:
            reply_text = ""
            btn = "[]"
            fileid = None
            alert = None
    elif message.reply_to_message and message.reply_to_message.photo:
        try:
            fileid = message.reply_to_message.photo.file_id
            reply_text, btn, alert = parser(
                message.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    elif message.reply_to_message and message.reply_to_message.video:
        try:
            fileid = message.reply_to_message.video.file_id
            reply_text, btn, alert = parser(
                message.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    elif message.reply_to_message and message.reply_to_message.audio:
        try:
            fileid = message.reply_to_message.audio.file_id
            reply_text, btn, alert = parser(
                message.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    elif message.reply_to_message and message.reply_to_message.document:
        try:
            fileid = message.reply_to_message.document.file_id
            reply_text, btn, alert = parser(
                message.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    elif message.reply_to_message and message.reply_to_message.animation:
        try:
            fileid = message.reply_to_message.animation.file_id
            reply_text, btn, alert = parser(
                message.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    elif message.reply_to_message and message.reply_to_message.sticker:
        try:
            fileid = message.reply_to_message.sticker.file_id
            reply_text, btn, alert = parser(extracted[1], text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    elif message.reply_to_message and message.reply_to_message.text:
        try:
            fileid = None
            reply_text, btn, alert = parser(message.reply_to_message.text.html,
                                            text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    else:
        return
    await add_filter("filters", text, reply_text, btn, fileid, alert)
    await message.reply_text(f"Filter for  `{text}`  added in  **{title}**",
                             quote=True,
                             parse_mode="md")


@Client.on_message(filters.command('viewfilters'))
async def get_all(client, message):
    chat_type = message.chat.type
    userid = message.from_user.id

    if str(userid) not in Config.AUTH_USERS:
        return

    if chat_type == "private":
        grp_id = message.chat.id
        title = "All Filters"
    elif chat_type in ["group", "supergroup"]:
        grp_id = message.chat.id
        title = "All Filters"
    else:
        return

    if chat_type in ["group", "supergroup"]:
        st = await client.get_chat_member(grp_id, userid)
        if st.status != "administrator" and st.status != "creator" and str(
                userid) not in Config.AUTH_USERS:
            return

    texts = await get_filters("filters")
    count = await count_filters("filters")
    if count:
        filterlist = f"Total number of filters in **{title}** : {count}\n\n"
        for text in texts:
            keywords = f" ×  `{text}`\n"
            filterlist += keywords
        if len(filterlist) > 4096:
            with io.BytesIO(str.encode(filterlist.replace(
                    "`", ""))) as keyword_file:
                keyword_file.name = "keywords.txt"
                await message.reply_document(document=keyword_file, quote=True)
            return
    else:
        filterlist = f"There are no active filters in **{title}**"
    await message.reply_text(text=filterlist, quote=True, parse_mode="md")


@Client.on_message(filters.command(Config.DELETE_FILTER_CMD))
async def deletefilter(client, message):
    userid = message.from_user.id
    chat_type = message.chat.type
    if str(userid) not in Config.AUTH_USERS:
        return

    if chat_type == "private":
        grp_id = message.chat.id
        title = "All Filters"
    elif chat_type in ["group", "supergroup"]:
        grp_id = message.chat.id
        title = "All Filters"
    else:
        return

    if chat_type in ["group", "supergroup"]:
        st = await client.get_chat_member(grp_id, userid)
        if st.status != "administrator" and st.status != "creator" and str(
                userid) not in Config.AUTH_USERS:
            return
    try:
        cmd, text = message.text.split(" ", 1)
    except:
        await message.reply_text(
            "<i>Mention the filtername which you wanna delete!</i>\n\n<code>/del filtername</code>\n\nUse /viewfilters to view all available filters",
            quote=True)

        return
    query = text.lower()
    await delete_filter(message, query, "filters")


@Client.on_message(filters.command(Config.DELETE_ALL_CMD))
async def delallconfirm(client, message):
    userid = message.from_user.id
    chat_type = message.chat.type
    if str(userid) not in Config.AUTH_USERS:
        return

    if chat_type == "private":
        grp_id = message.chat.id
        title = "All Filters"
    elif chat_type in ["group", "supergroup"]:
        grp_id = message.chat.id
        title = "All Filters"
    else:
        return

    if str(userid) in Config.AUTH_USERS:
        await message.reply_text(
            f"This will delete all filters from '{title}'.\nDo you want to continue??",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(text="YES",
                                         callback_data="delallconfirm")
                ],
                 [
                     InlineKeyboardButton(text="CANCEL",
                                          callback_data="delallcancel")
                 ]]),
            quote=True)


@Client.on_message(filters.text)
async def give_filter(client, message):
    m = message
    # Getting the owner of the bot.

    is_return = False

    if "livegram" in message.text.lower():
        await message.delete()
        is_return = True
    if "language" in message.text.lower():
        await message.delete()
        is_return = True

    if is_return:
        return

    if Config.UPDATE_CHANNEL:
        invite_link = await client.create_chat_invite_link(
            Config.UPDATE_CHANNEL)
        try:
            user = await client.get_chat_member(Config.UPDATE_CHANNEL,
                                                m.from_user.id)
            if user.status == "kicked":
                await m.reply_text("**Hey You Are Banned 😜**", quote=True)
                return
        except UserNotParticipant:
            buttons = [[
                InlineKeyboardButton(text='🍿Updates Channel🍿',
                                     url=invite_link.invite_link)
            ]]

            delete_msg = await m.reply_text(
                "**Hey! 😊**\n\n"
                "**You Have To Join Our Update Channel To Use Me ✅**\n\n"
                "**Click Bellow Button To Join Now.👇**",
                reply_markup=InlineKeyboardMarkup(buttons),
                quote=True)
            await asyncio.sleep(60)
            await delete_msg.delete()
            return
        except Exception as e:
            traceback.print_exc()
            print("Error in force sub")
            print(e)
            await m.reply_text(
                "**Start Me For Searching Anything...👇**",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "✳️ Click Here To Start ✳️",
                        url=f'https://t.me/MdiskSearchRobot')
                ]]))
            return
    if message.text.startswith("/"):
        return

    group_id = message.chat.id
    name = message.text
    print(name)
    keywords = await get_filters("filters")

    txt = None
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(
                "filters", keyword)
            if reply_text:
                reply_text = reply_text.replace("\\n",
                                                "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            txt = await message.reply_text(
                                reply_text, disable_web_page_preview=True)
                            if os.environ.get('AUTO_DELETE', False):
                                await asyncio.sleep(60)
                                await txt.delete()
                        else:
                            button = eval(btn)
                            txt = await message.reply_text(
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button))

                    elif btn == "[]":
                        txt = await message.reply_cached_media(
                            fileid, caption=reply_text or "")
                    else:
                        button = eval(btn)
                        txt = await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button))

                except Exception as e:
                    print(e)
                break
    if not txt:
        txt = await message.reply_text(
            Config.NO_RESULTS_MSG,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "📤 Click Here To Download 📤",
                        url=
                        f'https://{Config.MOVIE_WEBSITE}'
                    )
                ],
                [
                    InlineKeyboardButton(
                        "💌 Click To Report 💌",
                        url=
                        f'https://instagram.com/royalkrrishna?igshid=YmMyMTA2M2Y='
                    )
                ]
            ]))
    if os.environ.get('AUTO_DELETE', False):
        await asyncio.sleep(60)
        await txt.delete()

    if Config.SAVE_USER == "yes":
        try:
            await add_user(
                str(message.from_user.id), str(message.from_user.username),
                str(f"{message.from_user.first_name} " +
                    (message.from_user.last_name or "")),
                str(message.from_user.dc_id))

        except Exception:
            pass
