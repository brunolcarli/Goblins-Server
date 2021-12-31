from ast import literal_eval
from django.contrib.auth import default_app_config
import graphene
from graphene.types.structures import Structure
import redis
from django.conf import settings
from goblins.enums import ChatZone
from goblins.models import Entity
from django.conf import settings
from goblins.util import publish
from goblins.enums import ChatZone
from users.utils import access_required


class ChatMessageType(graphene.ObjectType):
    """
    Define estrutura para uma mensagem enviada ao chat.
    """
    player_name = graphene.String()
    message = graphene.String()
    chat_zone = graphene.String()


class PositionType(graphene.ObjectType):
    """
    Define estrutura para coordenada geografica cartesiana
    """
    x = graphene.Int()
    y = graphene.Int()


class EntityType(graphene.ObjectType):
    name = graphene.String()
    location = graphene.Field(PositionType)
    logged = graphene.Boolean()

    def resolve_name(self, info, **kwargs):
        if not self.name:
            return self.reference
        return self.name


    def resolve_logged(self, info, **kwargs):
        if self.logged:
            return True
        return False

    def resolve_location(self, info, **kwargs):
        if self.location:
            return literal_eval(self.location.decode('utf-8'))
        return {'x': 0, 'y': 0}


class Query:

    version = graphene.String(
        description='Returns service version'
    )

    def resolve_version(self, info, **kwargs):
        return settings.VERSION

    entities = graphene.List(
        EntityType,
        logged=graphene.Boolean()
    )

    @access_required
    def resolve_entities(self, info, **kwargs):
        return Entity.objects.filter(**kwargs)

    position = graphene.Field(
        EntityType,
        reference=graphene.String(required=True),
        description='Get position from a filtered entity'
    )

    @access_required
    def resolve_position(self, info, **kwargs):
        return Entity.objects.get(reference=kwargs['reference'])

    chat_messages = graphene.List(
        ChatMessageType,
        chat_zone=ChatZone(required=True),
        description='Get messages from a chat zone.'
    )

    @access_required
    def resolve_chat_messages(self, info, **kwargs):
        connection = redis.Redis(
            settings.REDIS['host'],
            settings.REDIS['port'],
            decode_responses=True
        )
        chat = connection.get(kwargs['chat_zone'])
        if chat:
            chat = literal_eval(chat)
        else:
            chat = []

        return [ChatMessageType(**i) for i in chat[:25]]


class LocationInput(graphene.InputObjectType):
    x = graphene.Int(required=True)
    y = graphene.Int(required=True)


class CreateEntity(graphene.relay.ClientIDMutation):
    entity = graphene.Field(EntityType)

    class Input:
        name = graphene.String(required=True)
        reference = graphene.String(required=True)
        location = graphene.Argument(LocationInput)

    @access_required
    def mutate_and_get_payload(self, info, **kwargs):
        location = kwargs.get('location', {'x': 0, 'y': 0})
        location = str(location).encode('utf-8')
        name = kwargs.get('name')
        reference = kwargs.get('reference')

        entity = Entity.objects.create(
            name=name,
            reference=reference,
            location=location
        )
        entity.save()
        return CreateEntity(entity)


class UpdatePosition(graphene.relay.ClientIDMutation):
    entity = graphene.Field(EntityType)

    class Input:
        reference = graphene.String(required=True)
        location = graphene.Argument(LocationInput, required=True)

    @access_required
    def mutate_and_get_payload(self, info, **kwargs):
        location = kwargs.get('location')
        x = location.get('x', 0)
        y = location.get('y', 0)
        location = str(location).encode('utf-8')
        reference = kwargs.get('reference')

        entity = Entity.objects.get(
            reference=reference,
        )
        entity.location = location
        entity.save()

        data = {
            'reference': reference,
            'x': x,
            'y': y
        }

        publish(data, 'foo/baz')

        return UpdatePosition(entity)


class SendChatMessage(graphene.relay.ClientIDMutation):
    chat_message = graphene.Field(ChatMessageType)

    class Input:
        player_name = graphene.String(required=True)
        message = graphene.String(required=True)
        chat_zone = ChatZone(required=True)

    @access_required
    def mutate_and_get_payload(self, info, **kwargs):
        connection = redis.Redis(
            settings.REDIS['host'],
            settings.REDIS['port'],
            decode_responses=True
        )
        data = {
            'player_name': kwargs['player_name'],
            'message': kwargs['message'],
            'chat_zone': kwargs['chat_zone']
        }
        chat = connection.get(kwargs['chat_zone'])
        if not chat:
            connection.set(kwargs['chat_zone'], [data])
        else:
            chat = literal_eval(chat)
            chat.append(data)
            connection.set(kwargs['chat_zone'], chat)

        publish(data, f'log/chat/{kwargs["chat_zone"].lower()}')

        return SendChatMessage(data)


class Mutation:
    create_entity = CreateEntity.Field()
    update_position = UpdatePosition.Field()
    send_chat_message = SendChatMessage.Field()
