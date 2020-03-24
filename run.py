# -*- coding: utf-8 -*-
# run.py

import sys
import os

from app.server.instance import server

app = server.get_app()

if __name__ == "__main__":
    
    app.run()