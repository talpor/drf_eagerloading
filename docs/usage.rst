.. highlight:: python

=====
Usage
=====
There are 2 steps to use DRF EagerLoading:
    1. In the desired serializer you will need to use the `EagerLoadingSerializerMixin`::

        from drf_eagerloading.mixins import EagerLoadingSerializerMixin
        class MyModelSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
            # Add the prefetch and select related fields
            select_related_fields = ("my_select_field",)
            prefetch_related_fields = ("my_prefetch_field",)

    Note: when to use `select_related_fields` and `prefetch_related_fields`?

    Quick response: same as before!!

    - `select_related_fields`: one_to_one and many_to_many relations
    - `prefetch_related_fields`: many_to_many and one_to_many relations

2. In the desired view you will need to use the `EagerLoadingViewSetMixin`::

    from drf_eagerloading.mixins import EagerLoadingViewSetMixin
    class MyModelViewSet(EagerLoadingViewSetMixin, viewsets.ModelViewSet):
        queryset = MyModel.objects.all()
