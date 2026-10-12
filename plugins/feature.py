import math
import asyncio
import uuid
from pyrogram import Client, filters
from pyrogram.types import (
    ChatMemberUpdated, Message, InlineKeyboardMarkup, 
    InlineKeyboardButton, CallbackQuery
)
from pyrogram.enums import ChatMemberStatus, ParseMode, ButtonStyle
from pyrogram.errors import FloodWait, ChatAdminRequired

from database.database import save_channel, delete_channel, get_channels
from helper_func import is_owner_or_admin
from config import DATABASE_CHANNEL

# --- MEMORY STORES ---
CHANNEL_CACHE = {}
POST_STATE = {}
SAVED_POSTS = {} # Resend feature ke liye posts yahan save hongi

# ==========================================
# 1️⃣ CHANNEL MANAGEMENT SYSTEM & LOGGING
# ==========================================

@Client.on_chat_member_updated(filters.channel)
async def channel_tracker(client: Client, update: ChatMemberUpdated):
    bot = await client.get_me()
    new_member = update.new_chat_member
    
    if new_member and new_member.user.id == bot.id:
        chat_id = update.chat.id
        chat_title = update.chat.title
        CHANNEL_CACHE[chat_id] = chat_title
        
        adder = update.from_user
        adder_mention = adder.mention if adder else "Unknown User"
        adder_id = adder.id if adder else "Unknown ID"
        
        if new_member.status == ChatMemberStatus.ADMINISTRATOR:
            success = await save_channel(chat_id)
            if success:
                try:
                    chat_link = f"https://t.me/{update.chat.username}" if update.chat.username else await client.export_chat_invite_link(chat_id)
                    log_text = (
                        "<blockquote><b>✅ Bᴏᴛ Aᴅᴅᴇᴅ As Aᴅᴍɪɴ!</b>\n\n"
                        f"<b>📣 Cʜᴀɴɴᴇʟ:</b> {chat_title}\n"
                        f"<b>🆔 ID:</b> <code>{chat_id}</code>\n"
                        f"<b>🔗 Lɪɴᴋ:</b> {chat_link}\n\n"
                        f"<b>👤 Aᴅᴅᴇᴅ Bʏ:</b> {adder_mention} (<code>{adder_id}</code>)</blockquote>"
                    )
                    await client.send_message(DATABASE_CHANNEL, log_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
                except Exception: pass
                
        elif new_member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]:
            await delete_channel(chat_id)
            if chat_id in CHANNEL_CACHE: del CHANNEL_CACHE[chat_id]
            try:
                remove_log = (
                    "<blockquote><b>❌ Bᴏᴛ Rᴇᴍᴏᴠᴇᴅ Fʀᴏᴍ Cʜᴀɴɴᴇʟ!</b>\n\n"
                    f"<b>📣 Cʜᴀɴɴᴇʟ:</b> {chat_title}\n"
                    f"<b>🆔 ID:</b> <code>{chat_id}</code>\n"
                    f"<b>👤 Rᴇᴍᴏᴠᴇᴅ Bʏ:</b> {adder_mention} (<code>{adder_id}</code>)</blockquote>"
                )
                await client.send_message(DATABASE_CHANNEL, remove_log, parse_mode=ParseMode.HTML)
            except Exception: pass

@Client.on_message(filters.command("channels") & filters.private & is_owner_or_admin)
async def list_channels(client: Client, message: Message):
    channels = await get_channels()
    if not channels:
        return await message.reply("<blockquote><b>❌ No channels added yet!</b></blockquote>", parse_mode=ParseMode.HTML)
    
    channel_data = []
    for ch_id in channels:
        title = CHANNEL_CACHE.get(ch_id)
        if not title:
            try:
                title = (await client.get_chat(ch_id)).title
                CHANNEL_CACHE[ch_id] = title
            except: title = f"ID: {ch_id}"
        channel_data.append({"id": ch_id, "title": title})
        
    channel_data.sort(key=lambda x: x["title"].lower())
    text = f"<blockquote><b>📊 Connected Channels ({len(channels)}):</b>\n\n"
    for ch in channel_data: text += f"• {ch['title']} (<code>{ch['id']}</code>)\n"
    text += "</blockquote>"
    await message.reply(text, parse_mode=ParseMode.HTML)


# ==========================================
# 2️⃣ POST CREATOR FSM & PREVIEW
# ==========================================

async def get_channel_list_markup(client: Client, page: int, mode: str, selected: list):
    channels = await get_channels()
    channel_data = []
    for ch_id in channels:
        title = CHANNEL_CACHE.get(ch_id)
        if not title:
            try:
                title = (await client.get_chat(ch_id)).title
                CHANNEL_CACHE[ch_id] = title
            except: title = f"ID: {str(ch_id)[-6:]}"
        channel_data.append({"id": ch_id, "title": title})
        
    channel_data.sort(key=lambda x: x["title"].lower())
    total_pages = math.ceil(len(channel_data) / 10) if channel_data else 1
    
    markup = []
    start_idx = page * 10
    current_channels = channel_data[start_idx:start_idx + 10]
    
    row = []
    for ch in current_channels:
        display_title = ch["title"][:14] + ".." if len(ch["title"]) > 15 else ch["title"]
        prefix = "✅ " if ch["id"] in selected and mode == "multi" else ""
        
        callback = f"select_ch_{ch['id']}_{page}" if mode == "multi" else f"send_to_{ch['id']}"
        row.append(InlineKeyboardButton(f"{prefix}{display_title}", callback_data=callback))
        if len(row) == 2:
            markup.append(row)
            row = []
    if row: markup.append(row)
    
    nav_row = []
    if page > 0: nav_row.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"ch_page_{page-1}"))
    if page < total_pages - 1: nav_row.append(InlineKeyboardButton("Next ➡️", callback_data=f"ch_page_{page+1}"))
    if nav_row: markup.append(nav_row)
    
    if mode == "multi":
        markup.append([InlineKeyboardButton("🚀 Send to Selected (Done)", callback_data="execute_multi_post")])
        markup.append([InlineKeyboardButton("☑️ Select All", callback_data=f"select_all_{page}")])
        
    markup.append([InlineKeyboardButton("⬅️ Back to Preview", callback_data="show_preview")])
    return InlineKeyboardMarkup(markup)

def preview_markup(mode: str):
    nav_button = [InlineKeyboardButton("➡️ Next (Choose Channel)", callback_data="ch_list_single")] if mode == "single" else [InlineKeyboardButton("📚 Next (Choose Channels)", callback_data="ch_list_multi")]
    
    return InlineKeyboardMarkup([
        nav_button,
        [InlineKeyboardButton("🕒 Schedule Post", callback_data="schedule_post"), 
         InlineKeyboardButton("📌 Pin Post", callback_data="pin_post")],
        [InlineKeyboardButton("⚙️ Change Button", callback_data="edit_button")],
        [InlineKeyboardButton("📝 Change Caption", callback_data="edit_caption"), InlineKeyboardButton("🖼 Change Media", callback_data="edit_media")],
        [InlineKeyboardButton("⬅️ Back", callback_data="start_menu"), InlineKeyboardButton("🏠 Menu", callback_data="start_menu")]
    ])

@Client.on_callback_query(filters.regex("^(create_post|multi_post)$"))
async def wait_for_post(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    mode = "single" if query.data == "create_post" else "multi"
    POST_STATE[user_id] = {"state": "WAITING_FOR_MESSAGE", "mode": mode, "selected_channels": []}
    await query.message.edit_caption("<blockquote><b>Send the post message or media</b>\n💡 To attach a media under the post, send it here.</blockquote>", parse_mode=ParseMode.HTML)

@Client.on_message(filters.private & is_owner_or_admin, group=-1)
async def catch_post_content(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id not in POST_STATE: return
    state = POST_STATE[user_id].get("state")
    
    if state.startswith("WAITING_FOR_TIME_"): 
        return # Schedule feature ko intercept karne dene ke liye
        
    if state in ["WAITING_FOR_MESSAGE", "EDIT_MEDIA", "EDIT_CAPTION"]:
        POST_STATE[user_id]["message_obj"] = message
        if state == "WAITING_FOR_MESSAGE":
            POST_STATE[user_id]["state"] = "WAITING_FOR_BUTTONS"
            button_text = """<blockquote expandable><b>⚙️ Sᴇᴛ ᴛʜᴇ Iɴʟɪɴᴇ Bᴜᴛᴛᴏɴs</b>\n\n• <b>Sᴛᴀɴᴅᴀʀᴅ Bᴜᴛᴛᴏɴs:</b>\n<code>Button text - t.me/LinkExample</code>\n\n• <b>Mᴜʟᴛɪᴘʟᴇ ɪɴ Sᴀᴍᴇ Rᴏᴡ:</b>\n<code>Btn 1 - Link && Btn 2 - Link</code>\n\n• <b>🎨 Cᴏʟᴏʀᴇᴅ Bᴜᴛᴛᴏɴs (Kurigram):</b>\n<code>#g Green - Link</code>\n<code>#r Red - Link</code>\n<code>#b Blue - Link</code>\n\n<i>(Send 'skip' if you don't want any buttons)</i></blockquote>"""
            await message.reply(button_text, parse_mode=ParseMode.HTML)
        else:
            POST_STATE[user_id]["state"] = "PREVIEW"
            await show_preview(client, user_id, message.chat.id)
        message.stop_propagation()

    elif state in ["WAITING_FOR_BUTTONS", "EDIT_BUTTON"]:
        if message.text.lower() == "skip":
            POST_STATE[user_id]["buttons"] = None
        else:
            buttons = []
            try:
                for row in message.text.split('\n'):
                    row_buttons = []
                    for btn in row.split('&&'):
                        name, link = btn.split('-', 1)
                        name = name.strip()
                        link = link.strip()
                        
                        btn_style = None
                        if name.lower().startswith("#g "): btn_style = ButtonStyle.SUCCESS; name = name[3:].strip()
                        elif name.lower().startswith("#r "): btn_style = ButtonStyle.DANGER; name = name[3:].strip()
                        elif name.lower().startswith("#b "): btn_style = ButtonStyle.PRIMARY; name = name[3:].strip()
                        
                        if btn_style: row_buttons.append(InlineKeyboardButton(name, url=link, style=btn_style))
                        else: row_buttons.append(InlineKeyboardButton(name, url=link))
                    buttons.append(row_buttons)
                POST_STATE[user_id]["buttons"] = InlineKeyboardMarkup(buttons)
            except Exception:
                return await message.reply("<blockquote><b>❌ Invalid Button Format!</b>\nTry again or type 'skip'.</blockquote>", parse_mode=ParseMode.HTML)
                
        POST_STATE[user_id]["state"] = "PREVIEW"
        await show_preview(client, user_id, message.chat.id)
        message.stop_propagation()

async def show_preview(client, user_id, chat_id):
    post_data = POST_STATE[user_id]
    await post_data["message_obj"].copy(chat_id, reply_markup=post_data.get("buttons"))
    await client.send_message(
        chat_id, 
        "<blockquote><b>👀 Post Preview Ready!</b>\nWhat do you want to do next?</blockquote>", 
        reply_markup=preview_markup(post_data["mode"]), 
        parse_mode=ParseMode.HTML
    )

@Client.on_callback_query(filters.regex("^(edit_button|edit_caption|edit_media|show_preview)$"))
async def edit_post_callbacks(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in POST_STATE: return await query.answer("❌ Session expired!", show_alert=True)
    data = query.data
    
    if data == "show_preview":
        await query.message.delete()
        await show_preview(client, user_id, query.message.chat.id)
    elif data == "edit_button":
        POST_STATE[user_id]["state"] = "EDIT_BUTTON"
        await query.message.edit_text("<blockquote>Send the new button format (or 'skip'):</blockquote>", parse_mode=ParseMode.HTML)
    elif data == "edit_caption":
        POST_STATE[user_id]["state"] = "EDIT_CAPTION"
        await query.message.edit_text("<blockquote>Forward/Send the message with the new caption:</blockquote>", parse_mode=ParseMode.HTML)
    elif data == "edit_media":
        POST_STATE[user_id]["state"] = "EDIT_MEDIA"
        await query.message.edit_text("<blockquote>Send the new media (Pic/Video/File/Music):</blockquote>", parse_mode=ParseMode.HTML)


# ==========================================
# 3️⃣ PIN & SCHEDULE POST FEATURES
# ==========================================

@Client.on_callback_query(filters.regex("^pin_post$"))
async def execute_pin_post(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in POST_STATE or "message_obj" not in POST_STATE[user_id]:
        return await query.answer("❌ No post found in memory!", show_alert=True)
    channels = await get_channels()
    if not channels:
        return await query.answer("❌ No channels connected!", show_alert=True)
    await query.message.edit_text("<blockquote><i>📌 Sending and Pinning post in channels...</i></blockquote>", parse_mode=ParseMode.HTML)
    post_data = POST_STATE[user_id]
    msg_to_send = post_data["message_obj"]
    buttons = post_data.get("buttons")
    success = 0
    for ch_id in channels:
        try:
            sent_msg = await msg_to_send.copy(chat_id=ch_id, reply_markup=buttons)
            await sent_msg.pin(both_sides=True)
            success += 1
        except Exception: pass
    del POST_STATE[user_id]
    await query.message.edit_text(f"<blockquote><b>✅ Pᴏsᴛ Sᴇɴᴛ & Pɪɴɴᴇᴅ ɪɴ {success} Cʜᴀɴɴᴇʟs!</b></blockquote>", parse_mode=ParseMode.HTML)

@Client.on_callback_query(filters.regex("^(schedule_post|schedule_del)$"))
async def ask_schedule_time(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    action = query.data
    if user_id not in POST_STATE:
        return await query.answer("❌ No post found in memory!", show_alert=True)
    POST_STATE[user_id]["state"] = f"WAITING_FOR_TIME_{action}"
    text = (
        "<blockquote><b>⏰ Sᴇᴛ Sᴄʜᴇᴅᴜʟᴇ Tɪᴍᴇ</b>\n\n"
        "Send the delay time in minutes. For example:\n"
        "<code>10</code> (For 10 minutes)\n"
        "<code>60</code> (For 1 hour)\n\n"
        "<i>(Send 'cancel' to abort)</i></blockquote>"
    )
    await query.message.edit_text(text, parse_mode=ParseMode.HTML)

@Client.on_message(filters.private & is_owner_or_admin, group=-2)
async def catch_schedule_time(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id not in POST_STATE: return
    state = POST_STATE[user_id].get("state", "")
    if not state.startswith("WAITING_FOR_TIME_"): return
    
    if message.text.lower() == "cancel":
        POST_STATE[user_id]["state"] = "PREVIEW"
        await message.reply("Cancelled schedule.", reply_markup=preview_markup(POST_STATE[user_id]["mode"]))
        return message.stop_propagation()

    try:
        minutes = int(message.text)
        seconds = minutes * 60
    except ValueError:
        await message.reply("❌ Invalid format! Send numbers only (e.g., 10)")
        return message.stop_propagation()

    action = "schedule_post" if "schedule_post" in state else "schedule_del"
    post_data = POST_STATE.pop(user_id) 
    
    if action == "schedule_post":
        await message.reply(f"<blockquote><b>✅ Pᴏsᴛ Sᴄʜᴇᴅᴜʟᴇᴅ!</b>\nIt will be sent automatically after {minutes} minutes.</blockquote>", parse_mode=ParseMode.HTML)
        asyncio.create_task(background_post_sender(client, post_data, seconds))
    else:
        await message.reply(f"<blockquote><b>✅ Aᴜᴛᴏ-Dᴇʟᴇᴛᴇ Sᴄʜᴇᴅᴜʟᴇᴅ!</b>\nPost will be sent now and deleted after {minutes} minutes.</blockquote>", parse_mode=ParseMode.HTML)
        asyncio.create_task(background_post_deleter(client, post_data, seconds))
    message.stop_propagation()

async def background_post_sender(client, post_data, delay_seconds):
    await asyncio.sleep(delay_seconds)
    msg_to_send = post_data["message_obj"]
    buttons = post_data.get("buttons")
    channels = await get_channels()
    for ch_id in channels:
        try: await msg_to_send.copy(chat_id=ch_id, reply_markup=buttons)
        except: pass
        await asyncio.sleep(0.5)

async def background_post_deleter(client, post_data, delay_seconds):
    msg_to_send = post_data["message_obj"]
    buttons = post_data.get("buttons")
    channels = await get_channels()
    sent_messages = []
    for ch_id in channels:
        try:
            m = await msg_to_send.copy(chat_id=ch_id, reply_markup=buttons)
            sent_messages.append(m)
        except: pass
        await asyncio.sleep(0.5)
    await asyncio.sleep(delay_seconds)
    for m in sent_messages:
        try: await m.delete()
        except: pass


# ==========================================
# 4️⃣ CHANNEL PAGINATION & FINAL SENDING
# ==========================================

@Client.on_callback_query(filters.regex("^(ch_list_single|ch_list_multi|ch_page|select_ch|select_all)"))
async def channel_pagination_handler(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in POST_STATE: return await query.answer("❌ Session expired! Restart process.", show_alert=True)
    
    if query.data in ["ch_list_single", "ch_list_multi"]:
        POST_STATE[user_id]["mode"] = "single" if query.data == "ch_list_single" else "multi"
        
    mode = POST_STATE[user_id]["mode"]
    data = query.data.split("_")
    page = 0
    
    if data[0] == "ch" and data[1] == "page":
        page = int(data[2])
    elif data[0] == "select" and data[1] == "ch":
        ch_id = int(data[2])
        page = int(data[3])
        if ch_id in POST_STATE[user_id]["selected_channels"]: POST_STATE[user_id]["selected_channels"].remove(ch_id)
        else: POST_STATE[user_id]["selected_channels"].append(ch_id)
    elif data[0] == "select" and data[1] == "all":
        page = int(data[2])
        POST_STATE[user_id]["selected_channels"] = await get_channels()

    markup = await get_channel_list_markup(client, page, mode, POST_STATE[user_id]["selected_channels"])
    text = "<blockquote><b>📣 Select Channel(s)</b>\n<i>Choose where to send the post.</i>"
    if mode == "multi": text += f"\n\n<b>Selected:</b> {len(POST_STATE[user_id]['selected_channels'])}"
    text += "</blockquote>"
    
    try: await query.message.edit_text(text, reply_markup=markup, parse_mode=ParseMode.HTML)
    except Exception: pass

@Client.on_callback_query(filters.regex("^(send_to_|execute_multi_post)$"))
async def execute_final_post(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in POST_STATE: return await query.answer("❌ Session expired!", show_alert=True)
    
    post_data = POST_STATE[user_id]
    msg_to_send = post_data["message_obj"]
    buttons = post_data.get("buttons")
    mode = post_data["mode"]
    
    target_channels = [int(query.data.split("_")[2])] if query.data.startswith("send_to_") else post_data["selected_channels"]
    if not target_channels: return await query.answer("❌ Select at least 1 channel!", show_alert=True)

    await query.message.edit_text("<blockquote><i>🔄 Broadcasting post... Please wait.</i></blockquote>", parse_mode=ParseMode.HTML)
    
    post_id = str(uuid.uuid4())[:8]
    SAVED_POSTS[post_id] = {"message_obj": msg_to_send, "buttons": buttons}
    
    success, failed = 0, 0
    success_links = []
    
    for ch_id in target_channels:
        try:
            chat = await client.get_chat(ch_id)
            ch_title = chat.title
            ch_link = f"https://t.me/{chat.username}" if chat.username else (chat.invite_link or await client.export_chat_invite_link(ch_id))
            
            await msg_to_send.copy(chat_id=ch_id, reply_markup=buttons)
            if mode == "multi": success_links.append(f"<a href='{ch_link}'>{ch_title}</a>")
            success += 1
        except FloodWait as e: await asyncio.sleep(e.value + 1)
        except Exception: failed += 1
        await asyncio.sleep(0.5) 
            
    del POST_STATE[user_id]
    bot = await client.get_me()
    
    if success_links:
        links_text = "\n".join([f"• {l}" for l in success_links])
        final_text = f"<blockquote><b>✅ Pᴏsᴛ sᴇɴᴛ ᴛᴏ ᴄʜᴀɴɴᴇʟs!</b>\n\n<b>Pᴏsᴛᴇᴅ ɪɴ:</b>\n{links_text}\n\n"
    else:
        final_text = f"<blockquote><b>✅ Pᴏsᴛ sᴇɴᴛ ᴛᴏ ᴄʜᴀɴɴᴇʟ!</b>\n\n"
        
    final_text += (
        "• Press \"Resend post\" to send this post to other channels\n"
        "• Press \"Resend identical post\" to send this post to other channels with the same settings\n"
        f"• Through this link you can make other users use this post: <code>t.me/{bot.username}?start=resend_{post_id}</code></blockquote>"
    )
    
    resend_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Resend post", callback_data=f"resend_menu_{post_id}")],
        [InlineKeyboardButton("🔄 Resend identical post", callback_data=f"resend_menu_{post_id}")]
    ])
    
    await query.message.edit_text(final_text, reply_markup=resend_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


# ==========================================
# 5️⃣ RESEND & DEEP LINK SYSTEM
# ==========================================

@Client.on_message(filters.command("start") & filters.private & is_owner_or_admin, group=2)
async def deep_link_resend(client: Client, message: Message):
    if len(message.command) > 1 and message.command[1].startswith("resend_"):
        post_id = message.command[1].split("_")[1]
        if post_id in SAVED_POSTS:
            markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("➡️ Send to Single Channel", callback_data=f"start_resend_{post_id}_single")],
                [InlineKeyboardButton("📚 Send to Multiple Channels", callback_data=f"start_resend_{post_id}_multi")],
                [InlineKeyboardButton("✖️ Cancel", callback_data="close")]
            ])
            await message.reply("<blockquote><b>🔄 Hᴏᴡ ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ʀᴇsᴇɴᴅ ᴛʜɪs ᴘᴏsᴛ?</b></blockquote>", reply_markup=markup, parse_mode=ParseMode.HTML)
            message.stop_propagation()

@Client.on_callback_query(filters.regex("^resend_menu_"))
async def handle_resend_btns(client: Client, query: CallbackQuery):
    post_id = query.data.split("_")[-1]
    if post_id not in SAVED_POSTS: return await query.answer("❌ Post expired from memory!", show_alert=True)
        
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("➡️ Send to Single Channel", callback_data=f"start_resend_{post_id}_single")],
        [InlineKeyboardButton("📚 Send to Multiple Channels", callback_data=f"start_resend_{post_id}_multi")],
        [InlineKeyboardButton("⬅️ Back", callback_data="start_menu")]
    ])
    await query.message.edit_text("<blockquote><b>🔄 Hᴏᴡ ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ʀᴇsᴇɴᴅ ᴛʜɪs ᴘᴏsᴛ?</b></blockquote>", reply_markup=markup, parse_mode=ParseMode.HTML)
    
@Client.on_callback_query(filters.regex("^start_resend_"))
async def execute_start_resend(client: Client, query: CallbackQuery):
    data = query.data.split("_")
    post_id = data[2]
    mode = data[3]
    
    if post_id not in SAVED_POSTS: return await query.answer("❌ Post expired from memory!", show_alert=True)
        
    user_id = query.from_user.id
    POST_STATE[user_id] = {
        "state": "PREVIEW",
        "mode": mode,
        "message_obj": SAVED_POSTS[post_id]["message_obj"],
        "buttons": SAVED_POSTS[post_id]["buttons"],
        "selected_channels": []
    }
    await query.message.delete()
    await show_preview(client, user_id, query.message.chat.id)
