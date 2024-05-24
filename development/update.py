from veritasai.firebase import get_db


def firestore_create(field_name: str, data: dict):
    """
    Create a new article in Firestore with a single field (for now).

    :param field_name: string representing document field name
    :data: a dictionary with analysis data
    """
    # Add a new document with a random id and grab a reference to it
    _, doc_ref = get_db().collection("articles").add({})
    match field_name:
        case "tone":
            doc_ref.update({"tone": data})
        case "bias":
            doc_ref.update({"bias": data})
