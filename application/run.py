import streamlit

import streamlit.web.cli as stcli
import os, sys

# Import the other libraries you need here
import xml.etree.ElementTree as ET
import essential_functions as ef
from datetime import datetime
import pandas as pd


def resolve_path(path):
    resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))
    return resolved_path


if __name__ == "__main__":
    sys.argv = [
        "streamlit",
        "run",
        resolve_path("Welcome.py"),
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())