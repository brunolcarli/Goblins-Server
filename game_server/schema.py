import graphene
import graphql_jwt

import users.schema as users
import goblins.schema as goblins

queries = (
    graphene.ObjectType,
    users.Query,
    goblins.Query,
)

mutations = (
    graphene.ObjectType,
    users.Mutation,
    goblins.Mutation,
)

class Query(*queries):
    pass


class Mutation(*mutations):
    # log_in = graphql_jwt.ObtainJSONWebToken.Field()
    validate_user_token = graphql_jwt.Verify.Field()
    refresh_user_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
