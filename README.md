# Copy Trading Script

This Python script facilitates copy trading between two MetaTrader 5 accounts. Any trade placed on account 1 will be automatically copied to account 2. Similarly, when a trade is closed on account 1, it will also be closed on account 2.

## Features
- **Trade Mirroring:** Automatically copies trades from account 1 to account 2.
- **Selective Trade Copying:** Trades are only copied if both stop loss and take profit are set.
- **Real-time Synchronization:** Trades are mirrored in real-time, ensuring that account 2 reflects the actions taken on account 1.

## Getting Started

### Prerequisites
- MetaTrader 5 installed
- In MetaTrader 5 => Options => Expert Advisors, only **Allow algorithmic trading** and **Allow DLL imports** should be checked!

### Installation

#### Windows
1. Download and install Python from the [official website](https://www.python.org/downloads/).
2. Add Python to your system PATH during the installation.

#### Linux
1. Install Python using your distribution's package manager. For example, on Ubuntu:
    ```bash
    sudo apt update
    sudo apt install python3 python3-pip
    ```

#### Mac
1. Download and install Python from the [official website](https://www.python.org/downloads/).
2. Alternatively, you can use Homebrew:
    ```bash
    brew install python
    ```

### Required Packages
1. Install MetaTrader 5:
    ```bash
    pip install MetaTrader5
    ```
2. Uninstall numpy and install a compatible version:
    ```bash
    pip uninstall numpy
    pip install numpy==1.26.4
    ```

### Configuration
1. After the first execution of the script, fill in the `accounts.json` file with the credentials of both MetaTrader 5 accounts:
    ```json
    {
      "account_1": {
        "login": "your_login",
        "password": "your_password",
        "server": "your_server"
      },
      "account_2": {
        "login": "your_login",
        "password": "your_password",
        "server": "your_server"
      }
    }
    ```
2. Save the `accounts.json` file.

### Usage
1. Run the script:
    ```bash
    python copy_trading.py
    ```
2. The script will start monitoring trades on account 1 and copy them to account 2, provided that stop loss and take profit are set.

### Important Notes
- Only trades placed after starting the script will be copied. Existing trades will not be mirrored.
- Trades without stop loss and take profit will not be copied.

## Desired Features
- **Stop Loss and Take Profit Synchronization:** Automatically synchronize any changes in stop loss and take profit for copied trades.

## Acknowledgements
- MetaTrader 5
- Python Community

## Contact
For any issues or suggestions, feel free to open an issue or contact the maintainers.
