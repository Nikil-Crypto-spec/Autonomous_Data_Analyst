import os


def create_folder(path):

    os.makedirs(
        path,
        exist_ok=True
    )


def list_html_reports(path):

    if not os.path.exists(path):

        return []

    return [

        file

        for file in os.listdir(path)

        if file.endswith(".html")

    ]