from flask import render_template


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s

    return render_template("pages/apology.html", top=code,
                           bottom=escape(message)), code


def format_float(value):
    """Format value as float with 2 decimals point"""
    return float("{:.2f}".format(value))


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"
