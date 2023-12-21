from dotenv import dotenv_values
config = dotenv_values(".env")


def main():
    if config["TOKEN"] == "False":
        print(f"Missing bot token.")
        return

    if config["INTEGRATION"] == "discord":
        import integrations.discord
        integrations.discord.init(config["TOKEN"])
        
    elif config["INTEGRATION"] == "telegram":
        import integrations.telegram
        integrations.telegram.init(config["TOKEN"])

    else:
        print("Expected valid Integration-type at command line argument 1, got " + str(config["INTEGRATION"]))


if __name__ == "__main__":
    main()
