# Network Monitor Telegram Bot

This project is a **Telegram bot** designed to monitor network activity and notify users about network status, outages, or performance issues.

## Features

- **Real-time Monitoring**: Tracks network status and performance.
- **Telegram Notifications**: Sends alerts directly to your Telegram account.
- **Customizable Alerts**: Configure thresholds for notifications.
- **Multi-Platform Support**: Works on Linux, macOS, and Windows.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/network-monitor-telegram.git
    cd network-monitor-telegram
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your Telegram bot:
    - Create a bot using [BotFather](https://core.telegram.org/bots#botfather).
    - Obtain the bot token and update the configuration file.

4. Run the bot:
    ```bash
    python bot.py
    ```

## Configuration

Edit the `config.json` file to set:
- Telegram bot token
- Chat ID for notifications
- Network monitoring parameters

## Usage

- Start the bot and let it monitor your network.
- Receive alerts on Telegram when issues are detected.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For questions or support, contact [ewertontertuliano@gmail.com](mailto:ewertontertuliano@gmail.com).