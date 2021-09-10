import json
from ast import literal_eval
import graphene
from goblins.models import Entity
from django.conf import settings
from goblins.util import publish
from users.utils import access_required


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

    @access_required
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

        publish(data)

        return UpdatePosition(entity)


class Mutation:
    create_entity = CreateEntity.Field()
    update_position = UpdatePosition.Field()
