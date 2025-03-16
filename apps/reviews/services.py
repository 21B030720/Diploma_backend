from rest_framework.generics import get_object_or_404

from apps.reviews.models import ObjectRating


def delete_rating(pk):
    object_rating = get_object_or_404(ObjectRating, pk=pk)
    object_rating.deleted = True
    object_rating.save()
