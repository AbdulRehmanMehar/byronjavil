# -*- coding: utf-8 -*-
# app/server/dbo/research_type.py

from app.models import ResearchType


class ResearchTypeDBO:

    def create(self, _type):

        research_type = ResearchType.create(research_type=_type)

        return research_type

    def read(self, _id):

        research_type = ResearchType.select().where(ResearchType.id==_id).get()

        return research_type

    def read_by_type(self, _type):

        research_type = ResearchType.select().where(ResearchType.research_type==_type).get()

        return research_type

    def read_all(self):

        result = list()

        research_types = ResearchType.select()

        for research_type in research_types:
            result.append(research_type)
        
        return result

    def update(self, _id, _type):

        research_type = self.read(_id)

        research_type.research_type = _type
        research_type.save()

        return True

    def delete(self, _id):

        research_type = self.read(_id)

        research_type.delete_instance()

        return True


