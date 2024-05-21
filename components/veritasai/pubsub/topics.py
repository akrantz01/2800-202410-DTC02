from os import environ


def topic_name_from_environment(name: str, default: str | None = None) -> str:
    """
    Get the topic name from the environment.

    :param name: The name of the environment variable.
    """
    topic = environ.get(name, default)
    if topic is None or len(topic.strip()) == 0:
        raise ValueError(f"missing topic name for {name}")

    return topic.strip()


analysis_requests = topic_name_from_environment("ANALYSIS_REQUESTS_TOPIC", "analysis-requests")
