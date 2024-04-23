from rest_framework import mixins, viewsets


class GetCreateDelete(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass
