<p align="center">
  <img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" />
</p>

<div align="center">
  <table>
    <tr>
      <td align="center">
        <img src="https://telegra.ph/file/64d61b1f3933fbc18925e-4ba9274225dadacc17.jpg" width="90px" style="border-radius: 50%;" />
      </td>
      <td>
        <img src="https://readme-typing-svg.herokuapp.com?color=00BFFF&width=600&lines=Hey+There,+This+is+ChannelPostBot+%F0%9F%A5%80+%E2%9D%97%EF%B8%8F" />
      </td>
    </tr>
  </table>
</div>

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=ChannelPostBot&style=flat-square" />
</p>

<h1 align="center">
  <img src="https://readme-typing-svg.herokuapp.com?color=FF69B4&width=500&lines=Welcome+to+PostBot;Your+Ultimate+Channel+Manager" />
</h1>

<p align="center">
  <a href="https://t.me/i_killed_my_clan">
    <img src="https://telegra.ph/file/86ee10d05289af41720e9-51ee4d6108f7131e02.jpg" width="600">
  </a>
</p>

<p align="center">
  <a href="https://t.me/i_killed_my_clan"><img src="https://img.shields.io/badge/Try%20Bot-@postyflix-blue?style=for-the-badge&logo=telegram"/></a>
</p>

<p align="center">
  <a href="https://github.com/yourusername/ChannelPostBot/stargazers"><img src="https://img.shields.io/github/stars/yourusername/ChannelPostBot?style=flat-square"/></a>
  <a href="https://github.com/yourusername/ChannelPostBot/network/members"><img src="https://img.shields.io/github/forks/yourusername/ChannelPostBot?style=flat-square"/></a>
  <a href="https://github.com/yourusername/ChannelPostBot/issues"><img src="https://img.shields.io/github/issues/yourusername/ChannelPostBot?style=flat-square"/></a>
  <a href="https://github.com/yourusername/ChannelPostBot/commits/main"><img src="https://img.shields.io/github/last-commit/yourusername/ChannelPostBot?style=flat-square"/></a>
  <a href="https://img.shields.io/badge/CI-Status-grey?style=flat-square"><img src="https://img.shields.io/badge/CI-Status-grey?style=flat-square"/></a>
</p>

## 🌟 What is Channel Post Bot?

**Channel Post Bot** is an advanced, professional Telegram bot engineered to handle all your channel management and automated posting needs. 

Built with scalability in mind, it provides a powerful experience for admins to schedule posts, manage multiple networks, and execute bulk broadcasting with robust queue systems. Features include multi-media support, auto-deletion, watermarking, and comprehensive admin statistics.

## 🚀 Features

<table>
<tr>
<td>
  <img src="https://telegra.ph/file/6478c4b60d9164beb39d2-14a358dcdc0a18b5a5.jpg" width="300" />
</td>
<td>

| 🌟 Feature                | 🔎 Description                              |
| ------------------------- | ------------------------------------------- |
| 📢 Channel Management     | Add, remove, and monitor unlimited channels |
| ⏰ Auto Post Scheduler    | Daily, weekly, monthly & custom time posting|
| 📦 Bulk Broadcasting      | Send media/text to all channels in one click|
| 📂 Universal Media        | Text, Photo, Video, GIF, Audio, Document    |
| 🔒 Post Settings          | Pin, Auto-Delete, Silent Post, Protect Content|
| 🔄 Robust Queue System    | Delay between posts, auto-retry on failure  |
| ⚙️ Automation Tools      | Auto-caption, Auto-hashtag, URL shortener   |
| 📊 Admin Dashboard        | Real-time logs, stats, and storage usage    |

</td>
</tr>
</table>

## 🛠️ Commands

### 📝 Post & Schedule Management
- <b>`/schedule`</b> — Schedule a new post
- <b>`/bulkpost`</b> — Start bulk broadcasting to all networks
- <b>`/queue`</b> — Check the current active posting queue
- <b>`/broadcast`</b> — Send a broadcast to bot users

### 📢 Channel Management (Admins)
- <b>`/addchannel`</b> — Connect a new channel to the bot
- <b>`/removechannel`</b> — Disconnect a channel
- <b>`/channels`</b> — List all connected channels and their details
- <b>`/settings`</b> — Configure post settings (auto-delete, notifications)

### 🎛️ Admin Commands (Owner)
- <b>`/start`</b> — Initialize the bot
- <b>`/admins`</b> — Manage bot administrators and permissions
- <b>`/logs`</b> — View success/failure posting logs
- <b>`/stats`</b> — Show bot performance and uptime statistics
- <b>`/cancel`</b> — Cancel any current ongoing operation

## 🔑 Environment Variables

Below are the required environment variables for deployment.

''' env
API_ID=              # Required - Get from [https://my.telegram.org](https://my.telegram.org)
API_HASH=            # Required - From [https://my.telegram.org](https://my.telegram.org)
BOT_TOKEN=           # Required - Get from @BotFather
OWNER_ID=            # Required - Your Telegram user ID
ADMINS=              # Optional - Admin user IDs (space separated)
DB_URL=              # Required - PostgreSQL/MongoDB connection string
TIMEZONE=            # Optional - E.g., Asia/Kolkata (Default: UTC) '''

⚠️ Never expose raw credentials or tokens in public repos. Use safe paste services like Pastebin.

<details>
<summary><b>Where do I get each key?</b></summary>


<table>
<thead>
<tr>
<th>Key</th>
<th>Where to Get It</th>
<th>Notes</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>API_ID</code> & <code>API_HASH</code></td>
<td><a href="https://my.telegram.org" target="_blank">my.telegram.org</a></td>
<td>Needed for the core client connection.</td>
</tr>
<tr>
<td><code>BOT_TOKEN</code></td>
<td><a href="https://t.me/BotFather" target="_blank">@BotFather</a></td>
<td>Keep private. Used to authenticate the bot.</td>
</tr>
<tr>
<td><code>OWNER_ID</code></td>
<td><b>@userinfobot</b> or <b>@getmyid_bot</b></td>
<td>Required for owner-only commands.</td>
</tr>
<tr>
<td><code>DB_URL</code></td>
<td><a href="https://www.mongodb.com/" target="_blank">MongoDB</a> / Supabase</td>
<td>Required for saving scheduled posts and channel data.</td>
</tr>
</tbody>
</table>


</details>

☕ VPS Setup Guide (Ubuntu/Debian)
<img src="https://img.shields.io/badge/Show%20/Hide-VPS%20Steps-0ea5e9?style=for-the-badge" alt="Toggle VPS Steps"/>
<div align="left">
<details>
🎵 Deploy PostBot on VPS

# Step 1: Update & Install Dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl python3-pip python3-venv tmux

# Step 2: Clone & Setup
git clone [https://github.com/yourusername/professional-telegram-post-bot.git](https://github.com/yourusername/professional-telegram-post-bot.git)
cd professional-telegram-post-bot
tmux new -s postbot

# Inside tmux:
python3 -m venv venv
source venv/bin/activate
pip install -U pip && pip install -r requirements.txt

# Create .env file with your environment variables
nano .env

# Run the bot
python3 main.py

### Useful Commands
tmux detach                      # Use Ctrl+B, then D (Leaves bot running in background)
tmux attach-session -t postbot   # Reattach to check logs
tmux kill-session -t postbot     # Stop the bot

</details>
</div>

🐳 Docker Deployment
<img src="https://img.shields.io/badge/Show%20/Hide-Docker%20Steps-10b981?style=for-the-badge" alt="Toggle Docker Steps"/>
<div align="left">
<details>
### Step 1: Clone Repo
git clone [https://github.com/yourusername/professional-telegram-post-bot.git](https://github.com/yourusername/professional-telegram-post-bot.git)
cd professional-telegram-post-bot

### Step 2: Setup Environment
nano .env

### Step 3: Use Docker Compose
docker-compose up -d --build

### Step 4: Manage Container
docker-compose logs -f           # View real-time logs
docker-compose stop              # Stop the bot
docker-compose start             # Start the bot
docker-compose down              # Remove containers entirely

</details>
</div>

☁️ Quick Deploy
| Platform | Deploy Link |
|---|---|
| 🌍 Heroku Deploy | <a href="http://dashboard.heroku.com/new?template=https://github.com/codeflix-bots/ChannelPostBot"><img src="https://img.shields.io/badge/Deploy%20to-Heroku-purple?style=for-the-badge&logo=heroku"/></a> |
| 🚂 Railway Deploy | <a href="https://railway.app/new"><img src="https://img.shields.io/badge/Deploy%20to-Railway-black?style=for-the-badge&logo=railway"/></a> |
| ☁️ Render Deploy | <a href="https://render.com/deploy"><img src="https://img.shields.io/badge/Deploy%20to-Render-46E3B7?style=for-the-badge&logo=render"/></a> |
💬 Community & Support
<p align="center">
<a href="https://t.me/codeflixsupport">
<img src="https://img.shields.io/badge/Support_Group-Telegram-0088cc?style=for-the-badge&logo=telegram&logoColor=white" />
</a>
<a href="https://t.me/codeflix_bots">
<img src="https://img.shields.io/badge/Updates_Channel-Telegram-6A5ACD?style=for-the-badge&logo=telegram&logoColor=white" />
</a>
</p>

🔖 Credits
 * <b> ᴄʀᴀғᴛᴇᴅ ᴡɪᴛʜ ᴘᴀssɪᴏɴ ʙʏ ᴏʙɪᴛᴏ & ᴄᴏᴅᴇғʟɪx </b>

