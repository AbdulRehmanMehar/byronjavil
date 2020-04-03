# -*- coding: utf-8 -*-
# app/server/dbo/utils.py

def update_record(record, **kwargs):

    for key, value in kwargs.items():

        try:
            setattr(record, key, value)
        except:
            pass

    record.save()

    return record