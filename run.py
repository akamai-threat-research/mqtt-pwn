from mqtt_pwn import cli, db
from mqtt_pwn.database import create_all_tables
from mqtt_pwn.utils import clear_screen


if __name__ == '__main__':
    """Main driver for this application"""

    create_all_tables(db)
    clear_screen()
    cli.cmdloop()
