from time import sleep

from configurations import Configurations
from view import build_item_sales_record


def main():
    sleep(Configurations.wait_second)
    build_item_sales_record()


if __name__ == "__main__":
    main()
