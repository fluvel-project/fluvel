from pathlib import Path

# Expect handler
from fluvel.core.exceptions.expect_handler import expect

@expect.FileNotFound(stop=False, default_value="")
def load_style_sheet(file_path: str | Path) -> str:
    """
    Loads and returns the contents of a QSS stylesheet file.
    
    This function reads the contents of a specified stylesheet file (QSS)
    and returns it as a string. If the file is not found,
    the function does not stop execution (``stop=False``) and
    returns an empty string (``default_value=""``) due to the decorator
    :py:meth:`expect.FileNotFound`.

    :param file_path: Path to the QSS file. This can be a string or a Path object.
    :type file_path: str or :py:class:`pathlib.Path`
    :returns: Contents of the QSS file as a string.
    :rtype: str
    """

    with open(file_path, "r", encoding="utf-8") as f:
        style_content = f.read()

    return style_content


def load_theme(folder: Path, theme_name: str) -> str:
    """
    Loads and concatenates the contents of all QSS files for a theme.

    This function recursively scans a specific theme folder
    within the base directory (``folder``) for all files
    with the `.qss` extension and concatenates their contents into a single string.

    :param folder: Base directory where the theme folders are located.
    :type folder: :py:class:`pathlib.Path`
    :param theme_name: Name of the subfolder containing the theme's QSS files.
    :type theme_name: str
    :returns: Text string containing the combined QSS of all the theme's files.
    :rtype: str
    """

    qss_files = Path(folder/theme_name).rglob("*.qss")
    
    qss_content: str = ""

    # Iterating and concatenating the QSS content of the files
    for qss_file in qss_files:

        qss_content += load_style_sheet(qss_file)

    return qss_content  

