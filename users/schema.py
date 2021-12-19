"""
Schema contendo objetos de usuário para o sistema.
Neste módulo ficarão:
    - Objetos graphql;
    - Queries (consultas) relacionadas a usuários;
    - Mutations:
        + Para cadastro;
        + LogOut do sistema

By Beelzebruno <brunolcarli@gmail.com>
"""
from ast import literal_eval
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from goblins.util import publish
from users.utils import access_required
from users.models import TokenBlackList
from goblins.models import Entity
import graphql_jwt


class UserType(DjangoObjectType):
    """
    Modelo de usuário padrão do django
    """ 
    class Meta:
        model = get_user_model()
        interfaces = (graphene.relay.Node,)


class UserConnection(graphene.relay.Connection):
    """Implementa o relay no objeto User."""
    class Meta:
        node = UserType


class Query(object):
    """
    Consultas GraphQL delimitando-se ao escopo
    de usuários.
    """
    users = graphene.relay.ConnectionField(UserConnection)

    @access_required
    def resolve_users(self, info, **kwargs):
        """
        Retorna uma lista de todos os usuários registrados no sistema.
        """
        return get_user_model().objects.all()


class CreateUser(graphene.relay.ClientIDMutation):
    """
    Cadastra um novo usuário no sistema.
    """
    user = graphene.Field(
        UserType,
        description='The response is a User Object.'
    )

    class Input:
        """inputs"""
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate_and_get_payload(self, info, **_input):

        username = _input.get('username')
        password = _input.get('password')
        email = _input.get('email')

        try:
            user = get_user_model()(
                username=username,
                email=email
            )
            user.set_password(password)
            user.save()
        except:
            raise Exception(
                'Username already registered. Please choose another username!'
            )
        return CreateUser(user=user)


class LogOut(graphene.relay.ClientIDMutation):
    """
    Desloga do sistema.
    """
    response = graphene.String()

    class Input:
        username = graphene.String(required=True)

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        username = _input['username']
        meta_info = info.context.META
        user_token = meta_info.get('HTTP_AUTHORIZATION').split(' ')[1]
        token_metadata = graphql_jwt.utils.jwt_decode(user_token)


        if username != token_metadata['username']:
            raise Exception('Invalid credentials')

        ents = Entity.objects.filter(reference=username)
        for ent in ents:
            ent.logged = False
            ent.save()

        # Publish logged playerd to the interfaces
        data = {'data': {'entities': []}}
        for entity in Entity.objects.filter(logged=True):
            user_data = {}
            try:
                location = literal_eval(entity.location.decode('utf-8'))
            except:
                continue
            
            user_data['name'] = entity.reference
            user_data['location'] = location
            user_data['logged'] = entity.logged
            data['data']['entities'].append(user_data)
        publish(data, 'system/logged_players')

        return LogOut("Bye Bye")

        revoke = TokenBlackList.objects.create(token=user_token)
        revoke.save()

        return LogOut("Bye Bye")

    def mutate_and_get_payload(self, info, **kwargs):
        session = graphql_jwt.ObtainJSONWebToken.mutate(
            self,
            info,
            username=kwargs['username'],
            password=kwargs['password']
        )
        token = session.token
        entity = Entity.objects.get(reference=kwargs['username'])
        entity.logged = True
        entity.save()

        # Publish logged playerd to the interfaces
        data = {'data': {'entities': []}}
        for entity in Entity.objects.filter(logged=True):
            user_data = {}
            try:
                location = literal_eval(entity.location.decode('utf-8'))
            except:
                continue
            
            user_data['name'] = entity.reference
            user_data['location'] = location
            user_data['logged'] = entity.logged
            data['data']['entities'].append(user_data)
        publish(data, 'system/logged_players')

        return LogIn(token)

class LogIn(graphene.relay.ClientIDMutation):
    token = graphene.String()

    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate_and_get_payload(self, info, **kwargs):
        session = graphql_jwt.ObtainJSONWebToken.mutate(
            self,
            info,
            username=kwargs['username'],
            password=kwargs['password']
        )
        token = session.token
        entity = Entity.objects.get(reference=kwargs['username'])
        entity.logged = True
        entity.save()

        # Publish logged playerd to the interfaces
        data = {'data': {'entities': []}}
        for entity in Entity.objects.filter(logged=True):
            user_data = {}
            try:
                location = literal_eval(entity.location.decode('utf-8'))
            except:
                continue
            
            user_data['name'] = entity.reference
            user_data['location'] = location
            data['data']['entities'].append(user_data)
        publish(data, 'system/logged_players')

        return LogIn(token)

class Mutation(object):
    sign_up = CreateUser.Field()
    log_out = LogOut.Field()
    log_in = LogIn.Field()
