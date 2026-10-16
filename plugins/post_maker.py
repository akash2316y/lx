import math
import asyncio
from pyrogram import Client, filters
from pyrogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
)
from pyrogram.enums import ParseMode, ButtonStyle
from pyrogram.errors import FloodWait

from database.database import get_all_channels
from helper_func import is_owner_or_admin

# Memory store for post creation
POST_STATE = {}

def get_preview_markup():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➡️ Next (Choose Channel)", callback_data="pm_choose_channel")],
        [InlineKeyboardButton("🕒 Schedule Post", callback_data="pm_under_dev"), 
         InlineKeyboardButton("📌 Pin Post", callback_data="pm_under_dev")],
        [InlineKeyboardButton("⚙️ Change Button", callback_data="pm_edit_button")],
        [InlineKeyboardButton("📝 Change Caption", callback_data="pm_edit_caption"), 
         InlineKeyboardButton("🖼 Change Media", callback_data="pm_edit_media")],
        [InlineKeyboardButton("⬅️ Back", callback_data="start_menu"), 
         InlineKeyboardButton("🏠 Menu", callback_data="start_menu")]
    ])

# Catch under development for minor buttons so it doesn't crash
@Client.on_callback_query(filters.regex("^pm_under_dev$"))
async def pm_under_dev_alert(client, query):
    await query.answer("This specific feature is coming soon!", show_alert=True)

@Client.on_callback_query(filters.regex("^(Create Post|Multi Post)$") & is_owner_or_admin)
async def start_post_creator(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    mode = "single" if query.data == "Create Post" else "multi"
    POST_STATE[user_id] = {"state": "WAITING_FOR_MESSAGE", "mode": mode, "selected_channels": []}
    
    text = "<blockquote><b>Send the post message or media</b>\n💡 To attach a media under the post, send it here.</blockquote>"
    try:
        await query.message.edit_caption(text, parse_mode=ParseMode.HTML)
    except:
        await query.message.edit_text(text, parse_mode=ParseMode.HTML)

@Client.on_message(filters.private & is_owner_or_admin, group=-1)
async def catch_post_content(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id not in POST_STATE:
        return
    state = POST_STATE[user_id].get("state")
    
    if state in ["WAITING_FOR_MESSAGE", "EDIT_MEDIA", "EDIT_CAPTION"]:
        if state == "WAITING_FOR_MESSAGE":
            POST_STATE[user_id]["is_media"] = bool(message.media)
            POST_STATE[user_id]["message_obj"] = message
            POST_STATE[user_id]["caption"] = message.caption.html if message.caption else (message.text.html if message.text else "")
            POST_STATE[user_id]["state"] = "WAITING_FOR_BUTTONS"
            
            button_text = "<blockquote><b>⚙️ Sᴇᴛ ᴛʜᴇ Iɴʟɪɴᴇ Bᴜᴛᴛᴏɴs</b>\n\n• <b>Standard:</b> <code>Button - Link</code>\n• <b>Colored:</b> <code>#g Green - Link</code>\n\n<i>(Send 'skip' if you don't want any buttons)</i></blockquote>"
            await message.reply(button_text, parse_mode=ParseMode.HTML)
            
        elif state == "EDIT_CAPTION":
            POST_STATE[user_id]["caption"] = message.text.html if message.text else (message.caption.html if message.caption else "")
            POST_STATE[user_id]["state"] = "PREVIEW"
            await show_preview(client, user_id, message.chat.id)
            
        elif state == "EDIT_MEDIA":
            if not message.media:
                return await message.reply("❌ Please send valid media.")
            POST_STATE[user_id]["message_obj"] = message
            POST_STATE[user_id]["is_media"] = True
            POST_STATE[user_id]["state"] = "PREVIEW"
            await show_preview(client, user_id, message.chat.id)
            
        message.stop_propagation()

    elif state in ["WAITING_FOR_BUTTONS", "EDIT_BUTTON"]:
        if not message.text:
            return await message.reply("❌ Send text or 'skip'.")
        if message.text.lower() == "skip":
            POST_STATE[user_id]["buttons"] = None
        else:
            buttons = []
            try:
                for row in message.text.split('\n'):
                    row_buttons = []
                    for btn in row.split('&&'):
                        name, link = btn.split('-', 1)
                        name, link = name.strip(), link.strip()
                        btn_style = None
                        if name.lower().startswith("#g"): btn_style, name = ButtonStyle.SUCCESS, name[2:].strip()
                        elif name.lower().startswith("#r"): btn_style, name = ButtonStyle.DANGER, name[2:].strip()
                        elif name.lower().startswith("#b"): btn_style, name = ButtonStyle.PRIMARY, name[2:].strip()
                        
                        row_buttons.append(InlineKeyboardButton(name, url=link, style=btn_style) if btn_style else InlineKeyboardButton(name, url=link))
                    buttons.append(row_buttons)
                POST_STATE[user_id]["buttons"] = InlineKeyboardMarkup(buttons)
            except Exception:
                return await message.reply("❌ Invalid format! Try again or type 'skip'.")
                
        POST_STATE[user_id]["state"] = "PREVIEW"
        await show_preview(client, user_id, message.chat.id)
        message.stop_propagation()

async def show_preview(client, user_id, chat_id):
    data = POST_STATE[user_id]
    msg = data["message_obj"]
    markup = data.get("buttons")
    caption = data.get("caption", "")
    
    if data.get("is_media"):
        await msg.copy(chat_id, caption=caption, reply_markup=markup, parse_mode=ParseMode.HTML)
    else:
        await client.send_message(chat_id, text=caption, reply_markup=markup, parse_mode=ParseMode.HTML)
        
    await client.send_message(chat_id, "<blockquote><b>👀 Post Preview Ready!</b>\nWhat do you want to do next?</blockquote>", reply_markup=get_preview_markup(), parse_mode=ParseMode.HTML)

@Client.on_callback_query(filters.regex("^pm_edit_") & is_owner_or_admin)
async def edit_post_callbacks(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in POST_STATE:
        return await query.answer("❌ Session expired!", show_alert=True)
    
    if query.data == "pm_edit_button":
        POST_STATE[user_id]["state"] = "EDIT_BUTTON"
        await query.message.edit_text("Send the new button format (or 'skip'):")
    elif query.data == "pm_edit_caption":
        POST_STATE[user_id]["state"] = "EDIT_CAPTION"
        await query.message.edit_text("Send the new caption:")
    elif query.data == "pm_edit_media":
        POST_STATE[user_id]["state"] = "EDIT_MEDIA"
        await query.message.edit_text("Send the new media:")

# --- CHANNEL SELECTION & FINAL POSTING ---
@Client.on_callback_query(filters.regex("^pm_choose_channel$") & is_owner_or_admin)
async def open_channel_selector(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in POST_STATE:
        return await query.answer("❌ Session expired!", show_alert=True)
    
    channels = await get_all_channels()
    if not channels:
        return await query.answer("❌ No channels found in Database!", show_alert=True)
    
    # Select all channels by default for Multi Post
    POST_STATE[user_id]["selected_channels"] = [ch["id"] for ch in channels]
    
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Media DB (Example)", callback_data="dummy"), InlineKeyboardButton("POST", callback_data="pm_execute_final_post")],
        [InlineKeyboardButton("⬅️ Back to Preview", callback_data="pm_back_preview")]
    ])
    await query.message.edit_text("<blockquote><b>📣 Select Channel(s)</b>\n<i>Choose where to send the post.</i></blockquote>", reply_markup=markup, parse_mode=ParseMode.HTML)

@Client.on_callback_query(filters.regex("^pm_back_preview$") & is_owner_or_admin)
async def back_to_preview(client: Client, query: CallbackQuery):
    await query.message.delete()
    await show_preview(client, query.from_user.id, query.message.chat.id)

# 🛑 YAHAN HOGA FINAL POST! (Jo tere video mein fail ho raha tha)
@Client.on_callback_query(filters.regex("^(POST|pm_execute_final_post)$") & is_owner_or_admin)
async def execute_final_posting(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in POST_STATE:
        return await query.answer("❌ Session expired! Create post again.", show_alert=True)
        
    data = POST_STATE[user_id]
    msg = data["message_obj"]
    targets = data.get("selected_channels", [])
    
    if not targets:
        return await query.answer("❌ No channels selected!", show_alert=True)

    await query.message.edit_text("<blockquote><i>🔄 Broadcasting post... Please wait.</i></blockquote>", parse_mode=ParseMode.HTML)
    
    success, failed = 0, 0
    for t_id in targets:
        try:
            if data.get("is_media"):
                await msg.copy(t_id, caption=data["caption"], reply_markup=data["buttons"], parse_mode=ParseMode.HTML)
            else:
                await client.send_message(t_id, text=data["caption"], reply_markup=data["buttons"], parse_mode=ParseMode.HTML)
            success += 1
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
        except Exception:
            failed += 1
        await asyncio.sleep(0.3)
        
    del POST_STATE[user_id]
    await query.message.edit_text(f"<blockquote><b>✅ Pᴏsᴛ Dᴇʟɪᴠᴇʀᴇᴅ!</b>\n\n• <b>Success:</b> <code>{success}</code>\n• <b>Failed:</b> <code>{failed}</code></blockquote>", parse_mode=ParseMode.HTML)
      
