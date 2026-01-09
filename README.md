# DuelDuck Auto Bot

🦆 **[Join DuelDuck Now!](https://duelduck.com?referral_token=2E3ZltyT)** 🦆

An automated bot for DuelDuck platform that helps you participate in duels automatically with intelligent decision-making based on majority votes.

## 🌟 Features

- ✅ **Automatic Login** - Secure wallet-based authentication with Solana keypair
- ✅ **Smart Decision Making** - Follows majority votes or random selection when tied
- ✅ **Captcha Solving** - Integrated 2Captcha support for seamless automation
- ✅ **Multi-Account Support** - Run multiple accounts simultaneously
- ✅ **Proxy Support** - Optional proxy configuration for enhanced privacy
- ✅ **Rate Limit Handling** - Automatic retry mechanism for rate-limited requests
- ✅ **Cycle-Based Operation** - Continuous operation with configurable intervals
- ✅ **Detailed Logging** - Color-coded console output with timestamps

## 📋 Requirements

- Python 3.8 or higher
- 2Captcha API key
- Solana wallet private keys

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/febriyan9346/DuelDuck-Auto-Bot.git
cd DuelDuck-Auto-Bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Create configuration files**

Create the following files in the root directory:

- `accounts.txt` - Your Solana private keys (one per line)
- `proxy.txt` - Your proxies in format `http://user:pass@ip:port` (one per line, optional)
- `2captcha.txt` - Your 2Captcha API key (one line)

## 📝 Configuration Files

### accounts.txt
```
your_solana_private_key_1
your_solana_private_key_2
your_solana_private_key_3
```

### proxy.txt (Optional)
```
http://username:password@proxy1.com:8080
http://username:password@proxy2.com:8080
```

### 2captcha.txt
```
your_2captcha_api_key
```

## 🚀 Usage

Run the bot:
```bash
python bot.py
```

You'll be presented with a menu:
```
1. Run with proxy
2. Run without proxy
```

Select your preferred mode and the bot will start automatically.

## 🎯 How It Works

1. **Login**: The bot authenticates using your Solana wallet private key
2. **Fetch Duels**: Retrieves available duels from the platform
3. **Smart Decision**: 
   - If YES votes > NO votes → Vote YES
   - If NO votes > YES votes → Vote NO
   - If votes are equal → Random selection
4. **Join Duels**: Automatically joins up to 10 duels per cycle
5. **Repeat**: Waits 24 hours before starting the next cycle

## ⚙️ Configuration

The bot includes several configurable parameters:

- **Delay between actions**: 8-15 seconds (randomized)
- **Delay between accounts**: 3 seconds
- **Duels per cycle**: 10 maximum
- **Cycle interval**: 24 hours (86400 seconds)
- **Pages to fetch**: 3 pages (up to 150 duels)

## 🛡️ Security Notes

- Never share your private keys
- Use proxies for enhanced privacy
- Keep your 2Captcha API key secure
- The bot censors wallet addresses in logs (shows only first/last 5 characters)

## 📊 Sample Output

```
[12:34:56] [INFO] Loaded 3 accounts
[12:34:56] [INFO] Running without proxy
[12:34:57] [CYCLE] Cycle #1 Started
[12:34:57] [INFO] Account #1/3
[12:34:57] [INFO] Wallet: 9XgbP***Xki
[12:34:58] [INFO] Solving Captcha...
[12:35:02] [SUCCESS] Captcha Solved
[12:35:03] [SUCCESS] Login Successful
[12:35:05] [INFO] Total found 47 available duels
[12:35:06] [SUCCESS] Join Success! | Answer: Yes | Following Majority (Yes: 156 vs No: 89)
```

## 🐛 Troubleshooting

**Bot fails to login:**
- Check your private key format
- Verify your internet connection
- Ensure 2Captcha has sufficient balance

**No duels available:**
- Wait for new duels to be created
- Check if you've already joined recent duels

**Rate limit errors:**
- The bot automatically waits and retries
- Consider using proxies to avoid rate limits

## 📄 Requirements File

Create a `requirements.txt` file:
```
requests
colorama
solders
PyNaCl
pytz
```

## ⚠️ Disclaimer

This bot is for educational purposes only. Use at your own risk. The developer is not responsible for:
- Loss of funds
- Account bans
- Any other consequences of using this bot

Always comply with DuelDuck's Terms of Service.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Developer

**FEBRIYAN**

## 🔗 Links

- [DuelDuck Platform](https://duelduck.com?referral_token=2E3ZltyT)
- [2Captcha Service](https://2captcha.com)

---

## 💰 Support Us with Cryptocurrency

You can make a contribution using any of the following blockchain networks:

| Network | Wallet Address |
|---------|----------------|
| **EVM** | `0x216e9b3a5428543c31e659eb8fea3b4bf770bdfd` |
| **TON** | `UQCEzXLDalfKKySAHuCtBZBARCYnMc0QsTYwN4qda3fE6tto` |
| **SOL** | `9XgbPg8fndBquuYXkGpNYKHHhymdmVhmF6nMkPxhXTki` |
| **SUI** | `0x8c3632ddd46c984571bf28f784f7c7aeca3b8371f146c4024f01add025f993bf` |

---

⭐ If you find this bot helpful, please consider giving it a star on GitHub!
