import re


class Filepath:
    @staticmethod
    def safe_filepath(unsafe_filepath: str) -> str:
        """
        Use regex to strip illegal characters from a string filepath

        :param unsafe_filepath: A filepath string containing illegal characters
        :returns: A filepath string without any illegal characters
        """

        return re.sub(
            r"[/\\?%*:;&#<>$`!{}@= |\"\x7F\x00-\x1F]",
            "-",
            unsafe_filepath
        ).replace(
            "'",
            ""
        )
