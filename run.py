import sys
from dotenv import dotenv_values
config = dotenv_values(".env")


def main():
    type_ = sys.argv[1].lower() if (sys.argv and len(sys.argv) > 1) else False

    if type_ == "discord":
        if "DISCORD_TOKEN" in config and config["TELEGRAM_TOKEN"] != "False":
            import integrations.discord
            integrations.discord.init(config["DISCORD_TOKEN"])
        else:
            print(f"Missing '{str(type_)}' bot token.")
        
    elif type_ == "telegram":
        if "TELEGRAM_TOKEN" in config and config["TELEGRAM_TOKEN"] != "False":
            import integrations.telegram
            integrations.telegram.init(config["TELEGRAM_TOKEN"])
        else:
            print(f"Missing '{str(type_)}' bot token.")

    else:
        print("Expected valid Integration-type at command line argument 1, got " + str(type_), file=sys.stderr)


if __name__ == "__main__":
    main()