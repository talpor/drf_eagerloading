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


def get_select_related(queryset, serializer, field, prefix):
    queryset = queryset.select_related(f"{prefix}{field}")
    if hasattr(serializer, "setup_eager_loading"):
        queryset = serializer.setup_eager_loading(queryset, prefix=f"{prefix}{field}__")

    return queryset


def get_prefetch_related(queryset, serializer, field, field_queryset, prefix):
    kwargs = {}

    if hasattr(serializer, "setup_eager_loading"):
        if field_queryset is None:
            field_queryset = serializer.Meta.model.objects.all()

        kwargs["queryset"] = serializer.setup_eager_loading(field_queryset)

    return queryset.prefetch_related(Prefetch(f"{prefix}{field}", **kwargs))


def prefetch_serializer(
    queryset, serializer, field, field_queryset=None, select_related=False, prefix=""
):
    return (
        get_select_related(queryset, serializer, field, prefix)
        if select_related
        else get_prefetch_related(queryset, serializer, field, field_queryset, prefix)
    )


class EagerLoadingViewSetMixin(object):
    def get_queryset(self):
        queryset = super(EagerLoadingViewSetMixin, self).get_queryset()
        serializer_class = self.get_serializer_class()

        if hasattr(serializer_class, "setup_eager_loading"):
            queryset = serializer_class.setup_eager_loading(queryset, self.request.user)

        return queryset


class EagerLoadingSerializerMixin(object):
    @classmethod
    def setup_eager_loading(cls, queryset, *args, **kwargs):
        prefix = kwargs.get("prefix", "")
        if hasattr(cls, "Meta"):
            for field_type in ("select_related_fields", "prefetch_related_fields"):
                for field_name in getattr(cls.Meta, field_type, []):
                    queryset = prefetch_serializer(
                        queryset,
                        get_field_serializer(cls, field_name),
                        f"{prefix}{field_name}",
                        select_related=(field_type == "select_related_fields"),
                    )

        return queryset
