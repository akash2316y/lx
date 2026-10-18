import asyncio
from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ChatMemberStatus, ParseMode
from database.database import get_channels
from helper_func import is_owner_or_admin

WELCOME_SETTINGS = {
    "welcome": True,
    "leave": True,
    "welcome_text": "<blockquote><b>👋 Wᴇʟᴄᴏᴍᴇ {mention} ᴛᴏ {title}!</b></blockquote>",
    "leave_text": "<blockquote><b>😢 {mention} ʟᴇғᴛ {title}. ᴡᴇ ᴡɪʟʟ ᴍɪss ʏᴏᴜ!</b></blockquote>"
}

@Client.on_callback_query(filters.regex("^(Welcome|Leave)$") & is_owner_or_admin)
async def welcome_leave_ui(client: Client, query: CallbackQuery):
    mode = query.data.lower()
    is_active = WELCOME_SETTINGS[mode]
    
    status_text = "🟢 ON" if is_active else "🔴 OFF"
    text = f"<blockquote><b>⚙️ {query.data} Mᴇssᴀɢᴇ Sᴇᴛᴛɪɴɢs</b>\n\nCurrent Status: <b>{status_text}</b>\n<i>Toggle below to turn it on or off for all connected channels.</i></blockquote>"
    
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"Turn {query.data} {'OFF' if is_active else 'ON'}", callback_data=f"wl_toggle_{mode}")],
        [InlineKeyboardButton("⬅️ Back to Menu", callback_data="start_menu")]
    ])
    try:
        await query.message.edit_caption(text, reply_markup=markup, parse_mode=ParseMode.HTML)
    except:
        await query.message.edit_text(text, reply_markup=markup, parse_mode=ParseMode.HTML)

@Client.on_callback_query(filters.regex("^wl_toggle_") & is_owner_or_admin)
async def toggle_wl_settings(client: Client, query: CallbackQuery):
    mode = query.data.split("_")[2]
    WELCOME_SETTINGS[mode] = not WELCOME_SETTINGS[mode]
    await query.answer(f"{mode.capitalize()} message is now {'ON' if WELCOME_SETTINGS[mode] else 'OFF'}!", show_alert=False)
    query.data = mode.capitalize()
    await welcome_leave_ui(client, query)

@Client.on_chat_member_updated(filters.channel, group=6)
async def handle_channel_members(client: Client, update: ChatMemberUpdated):
    ch_ids = await get_channels()
    ch_ids = [ch["id"] for ch in channels]
    chat_id = update.chat.id
    
    if chat_id not in ch_ids:
        return
        
    new_member = update.new_chat_member
    old_member = update.old_chat_member
    user = (new_member.user if new_member else old_member.user) if (new_member or old_member) else None
    
    if not user or user.is_bot:
        return
        
    user_mention = user.mention
    chat_title = update.chat.title

    try:
        if new_member and new_member.status == ChatMemberStatus.MEMBER and (not old_member or old_member.status == ChatMemberStatus.LEFT):
            if WELCOME_SETTINGS["welcome"]:
                text = WELCOME_SETTINGS["welcome_text"].format(mention=user_mention, title=chat_title)
                msg = await client.send_message(chat_id, text, parse_mode=ParseMode.HTML)
                asyncio.create_task(auto_delete(msg, 60))
                
        elif new_member and new_member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]:
            if WELCOME_SETTINGS["leave"]:
                text = WELCOME_SETTINGS["leave_text"].format(mention=user_mention, title=chat_title)
                msg = await client.send_message(chat_id, text, parse_mode=ParseMode.HTML)
                asyncio.create_task(auto_delete(msg, 60))
    except Exception:
        pass

async def auto_delete(msg, delay):
    await asyncio.sleep(delay)
    try:
        await msg.delete()
    except:
        pass
      
