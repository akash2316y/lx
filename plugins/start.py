import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait, PeerIdInvalid, UserIsBlocked, InputUserDeactivated
from config import OWNER_ID, START_PIC
from database.database import add_user, full_userbase, is_admin
from helper_func import is_owner_or_admin

# --- GLOBAL BROADCAST CONTROLLER ---
BROADCAST_RUNNING = False

# --- TEXTS (Channel Help UI) ---
CHANNEL_HELP_START = """
👋🏻 Welcome {mantion} to Channel Help!

• Send posts with buttons simultaneously in multiple channels
• Welcome new subscribers
• Create posts that send automatically every minute, hour, or day
• Protect your channel from unwanted users
• Auto-complete: send messages in the channel and the bot will add buttons, signatures, and everything you need
...And much more!

📣 Channel
📄 Privacy policy
"""

HELP_TEXT = """
<b>ℹ️ Guide</b>

To use the Channel Help features in a channel, you need to add @{bot_username} to the channel as an administrator.

⚠️ <b>Warning:</b> If, after adding the bot to the channel, you don't receive any notification from the bot, you need to remove it and add it to the channel again.

Other administrators will also be able to use the bot for that channel.
"""

CREATE_POST_TEXT = """
<b>📨 Create posts • Guide</b>

From this menu you can choose the post settings.

• Press the buttons on the left to know how the various post settings work.
• Press the buttons on the right to change each setting: the chosen option is the one displayed.
"""

# --- KEYBOARDS ---
def start_markup():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📨 Create Post", callback_data="create_post"), 
         InlineKeyboardButton("📚 Multi Post", callback_data="multi_post")],
        [InlineKeyboardButton("ℹ️ Help & Guide", callback_data="help_menu"), 
         InlineKeyboardButton("➕ Add Channel", callback_data="add_channel")],
        [InlineKeyboardButton("🗂 My Posts", callback_data="my_posts"), 
         InlineKeyboardButton("⚙️ Settings", callback_data="settings")],
        [InlineKeyboardButton("👋 Welcome", callback_data="welcome_msg"), 
         InlineKeyboardButton("🚶‍♂️ Leave", callback_data="leave_msg")],
        [InlineKeyboardButton("⏩ Forward Mode", callback_data="forward_mode"), 
         InlineKeyboardButton("🤖 Create Clone", callback_data="clone_bot")],
        [InlineKeyboardButton("✖️ Close", callback_data="close")]
    ])

def back_close_markup(back_data):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Back", callback_data=back_data), 
         InlineKeyboardButton("✖️ Close", callback_data="close")]
    ])

def create_post_markup(notif=True, protect=False):
    notif_btn = "🔔 ON" if notif else "🔕 OFF"
    protect_btn = "🔒 ON" if protect else "🔓 OFF"
    
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➡️ Next Step", callback_data="cp_next")],
        [InlineKeyboardButton("🔔 Notifications", callback_data="cp_help_notif"), 
         InlineKeyboardButton(notif_btn, callback_data=f"cp_toggle_notif_{notif}")],
        [InlineKeyboardButton("🛡 Protection", callback_data="cp_help_protect"), 
         InlineKeyboardButton(protect_btn, callback_data=f"cp_toggle_protect_{protect}")],
        [InlineKeyboardButton("⬅️ Back", callback_data="start_menu"), 
         InlineKeyboardButton("✖️ Close", callback_data="close")]
    ])

# --- COMMAND HANDLERS (ADMIN ONLY VIA `is_owner_or_admin`) ---
@Client.on_message(filters.command("start") & filters.private & is_owner_or_admin)
async def start_command(client: Client, message: Message):
    # Database me user add karna
    await add_user(message.from_user.id)
    
    # Config wale START_PIC ke sath Channel Help ka text
    await message.reply_photo(
        photo=START_PIC,
        caption=CHANNEL_HELP_START,
        reply_markup=start_markup(),
        parse_mode=ParseMode.HTML
    )

@Client.on_message(filters.command("help") & filters.private & is_owner_or_admin)
async def help_command(client: Client, message: Message):
    bot = await client.get_me()
    await message.reply_text(
        text=HELP_TEXT.format(bot_username=bot.username),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➕ Add Channel", url=f"t.me/{bot.username}?startchannel=true")]]),
        parse_mode=ParseMode.HTML
    )

# --- 🚀 PRO BROADCAST SYSTEM (Integrated with MongoDB) ---
async def process_broadcast(client: Client, message: Message, b_type: str, delete_time: int = 0):
    global BROADCAST_RUNNING
    BROADCAST_RUNNING = True
    
    # 🎯 Fetch all users from your exact database structure
    users = await full_userbase() 
    total = len(users)
    success = 0
    failed = 0
    
    status_msg = await message.reply(f"<blockquote><i>🔄 Broadcast Started... (0/{total})</i></blockquote>", parse_mode=ParseMode.HTML)
    
    for i, user_id in enumerate(users):
        if not BROADCAST_RUNNING:
            await status_msg.reply("<blockquote><b>🛑 Broadcast Cancelled by Admin!</b></blockquote>", parse_mode=ParseMode.HTML)
            break
            
        try:
            sent_msg = None
            if b_type == "forward":
                sent_msg = await message.reply_to_message.forward(user_id)
            else:
                sent_msg = await message.reply_to_message.copy(user_id)
                
            if b_type == "pin":
                try: await sent_msg.pin(both_sides=True)
                except: pass
                
            if b_type == "delete" and delete_time > 0:
                # Background auto-delete process
                async def auto_delete(m, t):
                    await asyncio.sleep(t)
                    try: await m.delete()
                    except: pass
                asyncio.create_task(auto_delete(sent_msg, delete_time))
                
            success += 1
            
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
        except (PeerIdInvalid, UserIsBlocked, InputUserDeactivated):
            failed += 1 
        except Exception:
            failed += 1
            
        if (i + 1) % 20 == 0:
            try: await status_msg.edit(f"<blockquote><i>🔄 Broadcasting... ({i+1}/{total})</i></blockquote>", parse_mode=ParseMode.HTML)
            except: pass
            
        await asyncio.sleep(0.1) # Server safety delay
        
    BROADCAST_RUNNING = False
    await status_msg.edit(f"<blockquote><b>✅ Broadcast Completed!</b>\n\nTotal: {total}\nSuccess: {success}\nFailed: {failed}</blockquote>", parse_mode=ParseMode.HTML)


@Client.on_message(filters.command(["broadcast", "fcast", "pbroadcast", "dbroadcast"]) & filters.private & is_owner_or_admin)
async def broadcast_handler(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply("<blockquote><b>❌ Reply to a message to broadcast!</b></blockquote>", parse_mode=ParseMode.HTML)
        
    global BROADCAST_RUNNING
    if BROADCAST_RUNNING:
        return await message.reply("<blockquote><b>⚠️ A broadcast is already running!</b> Use /bcancel to stop it.</blockquote>", parse_mode=ParseMode.HTML)

    cmd = message.command[0].lower()
    
    if cmd == "broadcast":
        asyncio.create_task(process_broadcast(client, message, "copy"))
    elif cmd == "fcast":
        asyncio.create_task(process_broadcast(client, message, "forward"))
    elif cmd == "pbroadcast":
        asyncio.create_task(process_broadcast(client, message, "pin"))
    elif cmd == "dbroadcast":
        try:
            delete_time = int(message.command[1]) * 60 
            asyncio.create_task(process_broadcast(client, message, "delete", delete_time))
        except (IndexError, ValueError):
            await message.reply("<blockquote><b>❌ Invalid Format!</b>\nUse: <code>/dbroadcast [time_in_minutes]</code> (Reply to message)</blockquote>", parse_mode=ParseMode.HTML)

@Client.on_message(filters.command("bcancel") & filters.private & is_owner_or_admin)
async def cancel_broadcast(client: Client, message: Message):
    global BROADCAST_RUNNING
    if not BROADCAST_RUNNING:
        return await message.reply("<blockquote><b>ℹ️ No broadcast is currently running.</b></blockquote>", parse_mode=ParseMode.HTML)
        
    BROADCAST_RUNNING = False
    await message.reply("<blockquote><b>🛑 Broadcast cancellation initiated. It will stop in a few seconds.</b></blockquote>", parse_mode=ParseMode.HTML)

# --- CALLBACK QUERIES (NAVIGATION) ---
@Client.on_callback_query()
async def callback_handler(client: Client, query: CallbackQuery):
    # Check Admin via your DB
    user_id = query.from_user.id
    if user_id != OWNER_ID and not await is_admin(user_id):
        return await query.answer("You are not an Admin!", show_alert=True)
        
    data = query.data
    bot = await client.get_me()

    if data == "close":
        await query.message.delete()

    elif data == "start_menu":
        await query.message.edit_media(
            media=START_PIC,
            reply_markup=start_markup()
        )
        await query.message.edit_caption(
            caption=CHANNEL_HELP_START,
            reply_markup=start_markup()
        )

    elif data == "help_menu":
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Channel", callback_data="add_channel")],
            [InlineKeyboardButton("⬅️ Back", callback_data="start_menu"), InlineKeyboardButton("✖️ Close", callback_data="close")]
        ])
        # Removing image for text-only help menu
        await query.message.edit_caption(HELP_TEXT.format(bot_username=bot.username), reply_markup=markup)

    elif data == "add_channel":
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Bot to Channel", url=f"t.me/{bot.username}?startchannel=true")],
            [InlineKeyboardButton("⬅️ Back", callback_data="start_menu"), InlineKeyboardButton("✖️ Close", callback_data="close")]
        ])
        await query.message.edit_caption(HELP_TEXT.format(bot_username=bot.username), reply_markup=markup)

    elif data == "create_post":
        await query.message.edit_caption(CREATE_POST_TEXT, reply_markup=create_post_markup(notif=True, protect=False))

    elif data.startswith("cp_toggle_notif_"):
        current_state = data.split("_")[-1] == "True"
        await query.message.edit_reply_markup(create_post_markup(notif=not current_state, protect=True)) 

    elif data.startswith("cp_toggle_protect_"):
        current_state = data.split("_")[-1] == "True"
        await query.message.edit_reply_markup(create_post_markup(notif=True, protect=not current_state)) 

    elif data == "cp_next":
        next_text = """
<b>Send the post message or media</b>
Allowed media: photos, videos, albums, files, stickers, GIFs, audio, voice messages, round videos.

💡 To attach a media under the post, send it here.
"""
        await query.message.edit_caption(next_text, reply_markup=back_close_markup("create_post"))

    elif data == "settings":
        settings_text = "<b>⚙️ Settings</b>\n\nConfigure your favourite buttons and default reactions here."
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("⭐ Favourite Buttons", callback_data="fav_buttons")],
            [InlineKeyboardButton("🎭 Default Reactions", callback_data="def_reactions")],
            [InlineKeyboardButton("⬅️ Back", callback_data="start_menu"), InlineKeyboardButton("✖️ Close", callback_data="close")]
        ])
        await query.message.edit_caption(settings_text, reply_markup=markup)

    else:
        await query.answer("This module is under development for the client!", show_alert=True)
        
