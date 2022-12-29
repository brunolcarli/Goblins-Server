from collections import defaultdict

import channels_graphql_ws

from ast import literal_eval
from site import ENABLE_USER_SITE
import graphene
from graphql import GraphQLObjectType
import redis
from django.conf import settings
from goblins.enums import AvailableMaps, ChatZone
from goblins.models import Entity, Character, ServerInstance, MapArea
from django.conf import settings
from goblins.enums import ChatZone, AvailableClasses
from users.utils import access_required
from goblins.goblin_classes import GoblinClasses
from goblins.maps import MapSizes


chats = defaultdict(list)

class Message(  # type: ignore
    graphene.ObjectType, default_resolver=graphene.types.resolver.dict_resolver
):
    """Message GraphQL type."""

    chatroom = graphene.String()
    text = graphene.String()
    sender = graphene.String()



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


class CharacterType(graphene.ObjectType):
    """
    Character attributes.
    """
    name = graphene.String()
    current_hp = graphene.Int()
    current_mp = graphene.Int()
    max_hp = graphene.Int()
    max_mp = graphene.Int()
    strength = graphene.Int()
    defense = graphene.Int()
    magic = graphene.Int()
    spirit = graphene.Int()
    experience = graphene.Int()
    next_lv = graphene.Int()
    lv = graphene.Int()
    max_range = graphene.Int()
    movement = graphene.Int()
    luck = graphene.Int()
    # skills = models.ManyToManyField('goblins.Skill')
    goblin_class = graphene.String()
    logged = graphene.Boolean()
    location = graphene.Field(PositionType)
    map_area = graphene.Field('goblins.schema.MapAreaType')
    sprite = graphene.String(description="Sprite image url")

    def resolve_sprite(self, info, **kwargs):
        return GoblinClasses.get_class(self.goblin_class)['sprite']

    def resolve_map_area(self, info, **kwargs):
        try:
            zone = MapArea.objects.get(
                reference=self.map_area,
                server_instance__reference=self.server_instance
            )
        except MapArea.DoesNotExist:
            return None
        else:
            return zone

    def resolve_logged(self, info, **kwargs):
        if self.logged:
            return True
        return False

    def resolve_location(self, info, **kwargs):
        if self.location:
            return literal_eval(self.location.decode('utf-8'))
        return {'x': 0, 'y': 0}


class MapAreaType(graphene.ObjectType):
    """
    Define available map scenarios to play
    """
    reference = graphene.String()
    online_count = graphene.Int()
    area_dimension = graphene.List(
        graphene.Int,
        description='Sizes XxY of the map.'
    )

    def resolve_area_dimension(self, info, **kwargs):
        return MapSizes.get_map_size(self.reference)

    def resolve_online_count(self, info, **kwargs):
        return Character.objects.filter(
            logged=True,
            server_instance=self.server_instance.reference,
            map_area=self.reference
        ).count()


class ServerInstanceType(graphene.ObjectType):
    """
    Define available server instances.
    """
    reference = graphene.String(description='Server reference.')
    map_areas = graphene.List(MapAreaType)
    online_count = graphene.Int()

    def resolve_map_areas(self, info, **kwargs):
        return MapArea.objects.filter(server_instance__id=self.id)

    def resolve_online_count(self, info, **kwargs):
        return Character.objects.filter(
            logged=True,
            server_instance=self.reference
        ).count()


class LogStatus(graphene.ObjectType):
    """ User current status """
    username = graphene.String()
    online_characters = graphene.List(
        CharacterType
    )
    active_server = graphene.String()
    irregular = graphene.Boolean()
    logged = graphene.Boolean()


##########################
# Query
##########################
class Query:

    version = graphene.String(
        description='Returns service version'
    )

    def resolve_version(self, info, **kwargs):
        return settings.VERSION

    history = graphene.List(Message, chatroom=graphene.String())
    def resolve_history(self, info, chatroom):
        """Return chat history."""
        del info
        return chats[chatroom] if chatroom in chats else []



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

    user_characters = graphene.List(
        CharacterType
    )

    @access_required
    def resolve_user_characters(self, info, **kwargs):
        if not kwargs.get('user'):
            raise Exception('Invalid user.')

        return Character.objects.filter(user=kwargs['user'])

    characters = graphene.List(
        CharacterType,
        logged=graphene.Boolean(),
        map_area=AvailableMaps()
    )

    @access_required
    def resolve_characters(self, info, **kwargs):
        return Character.objects.filter(**kwargs)

    # servers
    server_instances = graphene.List(
        ServerInstanceType,
        reference=graphene.String()
    )

    @access_required
    def resolve_server_instances(self, info, **kwargs):
        user = kwargs.pop('user')
        return ServerInstance.objects.filter(**kwargs)


##########################
# Mutation
##########################
class SendChatMessage(graphene.Mutation, name="SendChatMessagePayload"):  # type: ignore
    """Send chat message."""

    ok = graphene.Boolean()

    class Arguments:
        """Mutation arguments."""

        chatroom = graphene.String()
        text = graphene.String()

    def mutate(self, info, chatroom, text):
        """Mutation "resolver" - store and broadcast a message."""

        # Use the username from the connection scope if authorized.
        username = (
            info.context.user.username
            if info.context.user.is_authenticated
            else "Anonymous"
        )

        # Store a message.
        chats[chatroom].append({"chatroom": chatroom, "text": text, "sender": username})

        # Notify subscribers.
        OnNewChatMessage.new_chat_message(chatroom=chatroom, text=text, sender=username)

        return SendChatMessage(ok=True)


class CreateCharacter(graphene.relay.ClientIDMutation):
    """
    Creates an unique Character.
    """
    character = graphene.Field(CharacterType)

    class Input:
        name = graphene.String(required=True)
        goblin_class = AvailableClasses(required=True)

    @access_required
    def mutate_and_get_payload(self, info, **kwargs):
        user = kwargs['user']
        class_bonus = GoblinClasses.get_class(kwargs['goblin_class']).copy()
        # remove sprite from bonuses
        class_bonus.pop('sprite')

        if not user:
            raise Exception('Not a valid user.')

        if user.character_set.count() > 2:
            raise Exception('Max characters reached.')

        character = Character.objects.create(
            name=kwargs['name'],
            goblin_class=kwargs['goblin_class'],
            user=user,
            **class_bonus

        )
        character.save()
        return CreateCharacter(character)


class DeleteCharacter(graphene.relay.ClientIDMutation):
    character = graphene.Field(CharacterType)

    class Input:
        name = graphene.String(required=True)

    @access_required
    def mutate_and_get_payload(self, info, **kwargs):
        user = kwargs.get('user')

        if not user:
            raise Exception('Invalid user')

        try:
            char = Character.objects.get(name=kwargs['name'], user__id=user.id)
            char.delete()
        except Character.DoesNotExist:
            raise Exception('Not found')
        else:
            return DeleteCharacter(char)


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

        OnCharacterMovement.character_movement(reference=reference, x=x, y=y)

        return UpdatePosition(entity)


# class SendChatMessage(graphene.relay.ClientIDMutation):
#     chat_message = graphene.Field(ChatMessageType)

#     class Input:
#         player_name = graphene.String(required=True)
#         message = graphene.String(required=True)
#         chat_zone = ChatZone(required=True)

#     @access_required
#     def mutate_and_get_payload(self, info, **kwargs):
#         connection = redis.Redis(
#             settings.REDIS['host'],
#             settings.REDIS['port'],
#             decode_responses=True
#         )
#         data = {
#             'player_name': kwargs['player_name'],
#             'message': kwargs['message'],
#             'chat_zone': kwargs['chat_zone']
#         }
#         chat = connection.get(kwargs['chat_zone'])
#         if not chat:
#             connection.set(kwargs['chat_zone'], [data])
#         else:
#             chat = literal_eval(chat)
#             chat.append(data)
#             connection.set(kwargs['chat_zone'], chat)

#         publish(data, f'log/chat/{kwargs["chat_zone"].lower()}')

#         return SendChatMessage(data)


class CharacterLogIn(graphene.relay.ClientIDMutation):
    """Enters the game with a selected character"""
    
    log_status = graphene.Field(LogStatus)

    class Input:
        character_name = graphene.String(required=True)
        map_area = AvailableMaps(required=True)
        server_reference = graphene.String(required=True)

    @access_required
    def mutate_and_get_payload(self, info, **kwargs):
        user = kwargs.get('user')
        if not user:
            raise Exception('Unauthorized!')

        # Try recover the Map Area
        try:
            zone = MapArea.objects.get(
                reference=kwargs['map_area'],
                server_instance__reference=kwargs['server_reference']
            )
        except MapArea.DoesNotExist:
            raise Exception('Invalid Server or Map area.')

        # Try recover the Character
        try:
            char = Character.objects.get(
                user=user,
                name=kwargs['character_name']
            )
        except Character.DoesNotExist:
            raise Exception('Invalid character!')

        # Good to go
        char.logged = True
        char.map_area = zone.reference
        char.server_instance = zone.server_instance.reference
        char.save()

        # Broadcast character login
        position = literal_eval(char.location.decode('utf-8'))
        OnCharacterLogIn.character_login(
            reference=char.name,
            x=position['x'],
            y=position['y']
        )

        # API response
        response = {
            'username': user.username,
            'online_characters': user.character_set.filter(logged=True),
            'active_server': char.server_instance,
            'irregular': False,
            'logged': True
        }
        return CharacterLogIn(response)


class CharacterLogOut(graphene.relay.ClientIDMutation):
    """Leaves the game with current character"""
    
    log_status = graphene.Field(LogStatus)

    class Input:
        character_name = graphene.String(required=True)

    @access_required
    def mutate_and_get_payload(self, info, **kwargs):
        user = kwargs.get('user')
        if not user:
            raise Exception('Unauthorized!')

        # Try recover the Character
        try:
            char = Character.objects.get(
                user=user,
                name=kwargs['character_name']
            )
        except Character.DoesNotExist:
            raise Exception('Invalid character!')

        # Good to go
        char.logged = False
        char.save()

        # Broadcast character logout
        OnCharacterLogOut.character_logout(reference=char.name)

        # API response
        response = {
            'username': user.username,
            'online_characters': user.character_set.filter(logged=True),
            'active_server': char.server_instance,
            'irregular': False,
            'logged': True
        }
        return CharacterLogIn(response)


class Mutation:
    create_character = CreateCharacter.Field()
    delete_character = DeleteCharacter.Field()
    create_entity = CreateEntity.Field()
    update_position = UpdatePosition.Field()
    send_chat_message = SendChatMessage.Field()
    character_login = CharacterLogIn.Field()
    character_logout = CharacterLogOut.Field()



#################
# SUBSCRIPTIONS
#################


class OnNewChatMessage(channels_graphql_ws.Subscription):
    """Subscription triggers on a new chat message."""

    sender = graphene.String()
    chatroom = graphene.String()
    text = graphene.String()

    class Arguments:
        """Subscription arguments."""

        chatroom = graphene.String()

    def subscribe(self, info, chatroom=None):
        """Client subscription handler."""
        del info
        # Specify the subscription group client subscribes to.
        return [chatroom] if chatroom is not None else None

    def publish(self, info, chatroom=None):
        """Called to prepare the subscription notification message."""

        # The `self` contains payload delivered from the `broadcast()`.
        new_msg_chatroom = self["chatroom"]
        new_msg_text = self["text"]
        new_msg_sender = self["sender"]

        # Method is called only for events on which client explicitly
        # subscribed, by returning proper subscription groups from the
        # `subscribe` method. So he either subscribed for all events or
        # to particular chatroom.
        assert chatroom is None or chatroom == new_msg_chatroom

        # Avoid self-notifications.
        if (
            info.context.user.is_authenticated
            and new_msg_sender == info.context.user.username
        ):
            return OnNewChatMessage.SKIP

        return OnNewChatMessage(
            chatroom=chatroom, text=new_msg_text, sender=new_msg_sender
        )

    @classmethod
    def new_chat_message(cls, chatroom, text, sender):
        """Auxiliary function to send subscription notifications.
        It is generally a good idea to encapsulate broadcast invocation
        inside auxiliary class methods inside the subscription class.
        That allows to consider a structure of the `payload` as an
        implementation details.
        """
        cls.broadcast(
            group=chatroom,
            payload={"chatroom": chatroom, "text": text, "sender": sender},
        )


class OnCharacterMovement(channels_graphql_ws.Subscription):
    reference = graphene.String()
    x = graphene.Int()
    y = graphene.Int()


    def subscribe(self, info, **kwargs):
        del info
        return ['movement']

    def publish(self, info, **kwargs):
        reference = self["reference"]
        new_x = self["x"]
        new_y = self["y"]

        return OnCharacterMovement(
            reference=reference, x=new_x, y=new_y
        )

    @classmethod
    def character_movement(cls, reference, x, y):
        cls.broadcast(
            group='movement',
            payload={"reference": reference, "x": x, "y": y},
        )


class OnCharacterLogOut(channels_graphql_ws.Subscription):
    reference = graphene.String()

    def subscribe(self, info, **kwargs):
        del info
        return ['logout']

    def publish(self, info, **kwargs):
        reference = self["reference"]

        return OnCharacterLogOut(reference=reference)

    @classmethod
    def character_logout(cls, reference):
        cls.broadcast(
            group='logout',
            payload={"reference": reference}
        )


class OnCharacterLogIn(channels_graphql_ws.Subscription):
    reference = graphene.String()
    x = graphene.Int()
    y = graphene.Int()

    def subscribe(self, info, **kwargs):
        del info
        return ['login']

    def publish(self, info, **kwargs):
        reference = self["reference"]
        x = self["x"]
        y = self["y"]

        return OnCharacterLogIn(reference=reference, x=x, y=y)

    @classmethod
    def character_login(cls, reference, x, y):
        cls.broadcast(
            group='login',
            payload={"reference": reference, "x": x, "y": y}
        )


class Subscription(graphene.ObjectType):
    """GraphQL subscriptions."""

    on_new_chat_message = OnNewChatMessage.Field()
    on_character_movement = OnCharacterMovement.Field()
    on_character_login = OnCharacterLogIn.Field()
    on_character_logout = OnCharacterLogOut.Field()
