import dotenv
config = dotenv.dotenv_values(".env")


def main():
    if config["TOKEN"] == "False":
        print(f"Missing bot token.")
        return

    if config["INTEGRATION"] == "discord":
        import classes.integrations.discord as DiscordIntegration
        DiscordIntegration.init(config["TOKEN"])
        
    elif config["INTEGRATION"] == "telegram":
        import classes.integrations.telegram as TelegramIntegration
        TelegramIntegration.init(config["TOKEN"])

    else:
        print("Expected valid Integration-type at command line argument 1, got " + str(config["INTEGRATION"]))


if __name__ == "__main__":
    main()
