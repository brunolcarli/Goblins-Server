import graphene

import goblins.schema


class Query(goblins.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
