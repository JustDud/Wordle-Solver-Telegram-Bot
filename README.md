# WordleSolver-TG-Bot

## Overview
WordleSolver-TG-Bot is a Python-based project that combines a Wordle puzzle solver with a Telegram bot interface. The bot efficiently solves Wordle puzzles using advanced algorithms, including entropy-based optimisations, and allows users to interact with it via Telegram using the **aiogram** library.

## Features
- **Wordle Solver Logic:** Utilises entropy calculations to prioritise word guesses, maximising information gain.
- **Telegram Bot Integration:** Allows users to play and solve Wordle puzzles interactively via Telegram.
- **Customisable Gameplay:** Easily modify word lists and adapt solving logic for experimentation.
- **User-Friendly Interface:** Provides clear instructions and real-time feedback through Telegram.

## Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/YourUsername/WordleSolver-TG-Bot.git
   ```
2. **Navigate to the Project Directory:**
   ```bash
   cd WordleSolver-TG-Bot
   ```
3. **Create and Activate a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### Running the Telegram Bot:
1. Obtain a bot token from [BotFather](https://core.telegram.org/bots#botfather).
2. Create a `.env` file in the project directory and add your bot token:
   ```plaintext
   TOKEN=your-bot-token
   ```
3. Start the bot:
   ```bash
   python TGBot.py
   ```
4. Open Telegram and interact with your bot.

## Technologies Used
- **Programming Language:** Python
- **Libraries:** aiogram, python-dotenv
- **Algorithm:** Entropy-based optimisation for solving Wordle puzzles.

## Visual Overview
Below is an example of the bot in action, showcasing its Telegram interface and solving capabilities.

![Wordle Solver Telegram Bot](images/telegram_bot_interface.png)

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your changes.
3. Submit a pull request.

## Contact
For questions or feedback, feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/dmytro-dudarenko/).

---

*Keywords: Wordle Solver, Telegram Bot, Python, aiogram, Entropy Algorithm, Word Game Development*
