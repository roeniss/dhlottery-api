# Unofficial DH Lottery API

[![PyPI version](https://badge.fury.io/py/dhapi.svg)](https://badge.fury.io/py/dhapi)

A command line wrapper around the [DH Lottery](https://dhlottery.co.kr/) website.

https://github.com/user-attachments/assets/0be65454-8025-4fff-aa29-f88bc5948b43

### Installation & Usage

Python 3.9 or higher is required.

```sh
pip install dhapi --upgrade  # pip install --upgrade pip is recommended
# When using [uv](https://github.com/astral-sh/uv)
uv pip install dhapi --upgrade
dhapi --help                  # Show basic help
dhapi buy-lotto645 --help     # Help for buying Lotto 6/45
dhapi buy-lotto645 -y         # Purchase 5 automatic tickets and skip prompts
```

### Using without installation

```sh
uvx dhapi --help
uvx dhapi buy-lotto645 --help
uvx dhapi buy-lotto645 -y
```

## Features

- [Buy Lotto 6/45](https://dhlottery.co.kr/gameInfo.do?method=gameMethod&wiselog=H_B_1_1) (`buy-lotto645`)
    - Supports automatic, manual, and semi-automatic purchase modes.
    - Up to 5 tickets can be purchased at once.
    - A maximum of 5 tickets can be purchased each week (per the DH Lottery online policy).
- [Check balance](https://dhlottery.co.kr/userSsl.do?method=myPage) (`show-balance`)
    - View your current deposit balance.
- [Set up a virtual account](https://dhlottery.co.kr/userSsl.do?method=myPage) (`assign-virtual-account`)
    - The site allows you to charge funds by transferring to a personal virtual account. This command selects the desired deposit amount for you.
    - The actual transfer must be done manually.
    - Quick charge is not implemented.

### Utility Commands

- Multiple profile support
    - You can define more than one profile. See the advanced configuration section.
- List profiles (`show-profiles`)
    - Display the names of configured profiles.

## Advanced Configuration

### Profile (account) settings

> **Note**: The first time you run the program, you will be prompted to create a profile. This section explains how to edit the profile file manually.

You can edit or add profiles in the `~/.dhapi/credentials` file. It uses TOML format as shown below.

```toml
[default]
username = "dhlotter_id"
password = "****"
[another_profile]
username = "dhlotter_second_id"
password = "****"
```

Afterward, select a profile with the `-p` flag when running commands.

## Support This Project

If you hit the jackpot using this program, please consider donating 10,000,000 KRW to me!

Even if you don't win, you can still buy me a coffee.

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png)](https://www.buymeacoffee.com/roeniss)

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](/docs/CONTRIBUTING.md).

