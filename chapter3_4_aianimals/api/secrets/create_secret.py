from cryptography.fernet import Fernet


def main():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as f:
        f.write(key)


if __name__ == "__main__":
    main()
