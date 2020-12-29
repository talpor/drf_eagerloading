# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.db.models import Prefetch


def get_field_serializer(cls, field_name):
    field = cls._declared_fields.get(field_name)
    if field:
        serializer = field.serializer if hasattr(field, "serializer") else field
        if isinstance(serializer, serializers.ListSerializer):
            serializer = serializer.child

        return serializer


def get_select_related(queryset, serializer, field, prefix, *args):
    queryset = queryset.select_related(f"{prefix}{field}")
    if hasattr(serializer, "setup_eager_loading"):
        queryset = serializer.setup_eager_loading(queryset, *args, prefix=f"{prefix}{field}__")

    return queryset


def get_prefetch_related(queryset, serializer, field, field_queryset, prefix, *args):
    kwargs = {}

    if hasattr(serializer, "setup_eager_loading"):
        if field_queryset is None:
            field_queryset = serializer.Meta.model.objects.all()

        kwargs["queryset"] = serializer.setup_eager_loading(field_queryset, *args)

    return queryset.prefetch_related(Prefetch(f"{prefix}{field}", **kwargs))


def prefetch_serializer(
    queryset, serializer, field, *args, field_queryset=None, select_related=False, prefix=""
):
    return (
        get_select_related(queryset, serializer, field, prefix, *args)
        if select_related
        else get_prefetch_related(queryset, serializer, field, field_queryset, prefix, *args)
    )
