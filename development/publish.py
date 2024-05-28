import json
from base64 import b64encode
from datetime import datetime, timezone

import click
import cloup
import requests
from cloup.constraints import mutually_exclusive
from veritasai.articles import Article


@cloup.command()
@cloup.option_group(
    "Sources",
    cloup.option("--content", "-c", help="The content to send to", type=cloup.STRING),
    cloup.option(
        "--file", "-f", help="The file containing the content to send", type=cloup.File("r")
    ),
    cloup.option(
        "--id", "-i", "article_id", help="The article ID to send", metavar="ID", type=cloup.STRING
    ),
    constraint=mutually_exclusive,
)
@cloup.option_group(
    "Article metadata",
    cloup.option(
        "--author",
        help="The name of the article's author",
        metavar="AUTHOR",
        type=cloup.STRING,
    ),
    cloup.option(
        "--publisher",
        help="The name of the article's publisher",
        metavar="PUBLISHER",
        type=cloup.STRING,
    ),
    cloup.option(
        "--url",
        help="The URL where the article can be found",
        metavar="URL",
        type=cloup.STRING,
    ),
)
@cloup.option_group(
    "Development server",
    cloup.option(
        "--address",
        "-a",
        help="The address the development server is running on",
        default="127.0.0.1",
        metavar="ADDRESS",
        type=cloup.STRING,
        show_default=True,
    ),
    cloup.option(
        "--port",
        "-p",
        help="The port the development server is running on",
        default=5000,
        metavar="PORT",
        type=cloup.INT,
        show_default=True,
    ),
)
def publish(
    address: str,
    port: int,
    content: str | None = None,
    file: cloup.File | None = None,
    article_id: str | None = None,
    author: str | None = None,
    publisher: str | None = None,
    url: str | None = None,
):
    """
    Mock a Pub/Sub publish operation for analysis requests.

    The article content can be provided as a string, a file, or an already existing article ID.
    """

    if file is not None:
        content = file.read()
    if content is not None:
        article = Article.from_input(content, author=author, publisher=publisher, url=url)
    else:
        article = Article(id=article_id, author=author, publisher=publisher, url=url)

    serialized = json.dumps(article.to_dict()).encode("utf-8")
    encoded = b64encode(serialized).decode()

    response = requests.post(
        f"http://{address}:{port}/",
        json={
            "message": {
                "data": encoded,
            }
        },
        headers={
            "Content-Type": "application/json",
            "ce-id": "123451234512345",
            "ce-specversion": "1.0",
            "ce-time": datetime.now(timezone.utc).isoformat(),
            "ce-type": "google.cloud.pubsub.topic.v1.messagePublished",
            "ce-source": "//pubsub.googleapis.com/projects//topics//",
        },
    )

    click.secho("Status: ", fg="yellow", nl=False)

    if response.ok:
        click.secho("OK", fg="green")
    else:
        click.secho("ERROR", fg="red")

        click.secho("Status code: ", fg="yellow", nl=False)
        click.secho(str(response.status_code), fg="red")

        click.secho("Response:", fg="yellow")
        click.echo(response.text)


if __name__ == "__main__":
    publish()
