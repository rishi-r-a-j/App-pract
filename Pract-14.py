
import logging
import logging.config
import logging.handlers
import os
import tempfile

LOG_DIR = tempfile.mkdtemp(prefix="logdemo_")


def section(title):
    print(f"\n{'=' * 8} {title} {'=' * 8}")


# 1. Logging Levels
def demo_levels():
    section("1. Logging Levels")

    log = logging.getLogger("levels")
    log.setLevel(logging.DEBUG)

    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))

    log.addHandler(h)
    log.propagate = False

    log.debug("Detailed developer information")
    log.info("Normal information")
    log.warning("Something unexpected")
    log.error("An error occurred")
    log.critical("Critical error")

    log.setLevel(logging.WARNING)
    log.info("This message will be hidden")
    log.warning("This warning will be displayed")


# 2. Formatters
def demo_formatter():
    section("2. Formatters")

    log = logging.getLogger("format")
    log.setLevel(logging.INFO)

    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    ))

    log.addHandler(h)
    log.propagate = False

    log.info("Formatted log message")


# 3. Logging Handlers
def demo_handlers():
    section("3. Logging Handlers")

    path = os.path.join(LOG_DIR, "app.log")

    log = logging.getLogger("handlers")
    log.setLevel(logging.DEBUG)
    log.propagate = False

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(
        "CONSOLE %(levelname)s - %(message)s"
    ))

    file_handler = logging.FileHandler(path)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s"
    ))

    log.addHandler(console)
    log.addHandler(file_handler)

    log.debug("Debug message")
    log.info("Information message")
    log.warning("Warning message")
    log.error("Error message")

    file_handler.flush()

    print("\nFile Contents:")
    with open(path, "r") as f:
        print(f.read())


# 4. Rotating File Handler
def demo_rotation():
    section("4. Rotating File Handler")

    path = os.path.join(LOG_DIR, "rotate.log")

    log = logging.getLogger("rotate")
    log.setLevel(logging.INFO)
    log.propagate = False

    h = logging.handlers.RotatingFileHandler(
        path, maxBytes=200, backupCount=2
    )

    log.addHandler(h)

    for i in range(1, 21):
        log.info("Rotating entry number %d", i)

    h.close()

    print("Files created:",
          sorted(f for f in os.listdir(LOG_DIR)
                 if f.startswith("rotate")))


# 5. Logger Hierarchy
def demo_hierarchy():
    section("5. Logger Hierarchy")

    parent = logging.getLogger("shop")
    parent.setLevel(logging.INFO)
    parent.propagate = False

    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter(
        "[%(name)s] %(message)s"
    ))

    parent.addHandler(h)

    logging.getLogger("shop.cart").info("Item added to cart")
    logging.getLogger("shop.pay").info("Payment accepted")
    logging.getLogger("shop.pay").debug("Hidden message")


# 6. Exception Logging
def demo_exception():
    section("6. Exception Logging")

    log = logging.getLogger("errors")
    log.setLevel(logging.ERROR)
    log.propagate = False

    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter(
        "%(levelname)s - %(message)s"
    ))

    log.addHandler(h)

    try:
        result = 10 / 0
    except ZeroDivisionError:
        log.exception("Division failed")


# 7. Logging Filters
class HideSecrets(logging.Filter):

    def filter(self, record):
        return "password" not in record.getMessage().lower()


def demo_filter():
    section("7. Logging Filters")

    log = logging.getLogger("secure")
    log.setLevel(logging.INFO)
    log.propagate = False

    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter(
        "%(levelname)s - %(message)s"
    ))

    h.addFilter(HideSecrets())
    log.addHandler(h)

    log.info("User logged in")
    log.info("Password is 1234")
    log.info("User opened dashboard")


# 8. Lazy Formatting and Extra Fields
def demo_lazy_and_extra():
    section("8. Lazy Formatting and Extra Fields")

    log = logging.getLogger("extras")
    log.setLevel(logging.INFO)
    log.propagate = False

    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter(
        "%(levelname)s user=%(user)s %(message)s"
    ))

    log.addHandler(h)

    log.info(
        "Order %d placed, total Rs. %.2f",
        42, 1999.5,
        extra={"user": "Rahul"}
    )


# 9. Dictionary Configuration
def demo_dictconfig():
    section("9. Dictionary Configuration")

    config = {
        "version": 1,
        "disable_existing_loggers": False,

        "formatters": {
            "short": {
                "format": "%(levelname)s:%(name)s:%(message)s"
            }
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "short",
                "level": "INFO"
            }
        },

        "loggers": {
            "configured": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False
            }
        }
    }

    logging.config.dictConfig(config)

    logging.getLogger("configured").info(
        "Configured using dictionary"
    )


# Main Program
if __name__ == "__main__":

    demo_levels()
    demo_formatter()
    demo_handlers()
    demo_rotation()
    demo_hierarchy()
    demo_exception()
    demo_filter()
    demo_lazy_and_extra()
    demo_dictconfig()

    print("\nLog files saved in:", LOG_DIR)
