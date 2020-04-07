# -*- coding: utf-8 -*-
# run.py

import sys
import os

from app.server.instance import server


if __name__ == "__main__":

    app = server.get_app()
    
    app.run()