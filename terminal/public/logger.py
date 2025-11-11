import click

def WARNING(msg: str) -> None:
    """打印警告信息

    Args:
        msg (str): 需要打印的字符串
    """
    click.secho(msg, fg="yellow")


def INFO(msg: str) -> None:
    """打印警告信息

    Args:
        msg (str): 需要打印的字符串
    """
    click.secho(msg, fg="blue")


def ERROR(msg: str) -> None:
    """打印警告信息

    Args:
        msg (str): 需要打印的字符串
    """
    click.secho(msg, fg="red")


def SUCCESS(msg: str) -> None:
    """打印警告信息

    Args:
        msg (str): 需要打印的字符串
    """
    click.secho(msg, fg="green")
