# -*- coding: utf-8 -*-

from .utils import get_field_serializer, prefetch_serializer


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
