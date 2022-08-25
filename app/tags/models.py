from django.db import models
from django.utils.translation import gettext_lazy as _

# from taggit.models import TagBase, GenericTaggedItemBase, TaggedItemBase


# class Tag(TagBase):
#     test = models.CharField("",max_length=10)

#     class Meta:
#         verbose_name = _("Tag")
#         verbose_name_plural = _("Tags")

#     # ... methods (if any) here

# class TaggedPost(TaggedItemBase):
#     post = models.ForeignKey('content.Post', on_delete=models.CASCADE)

#     tag = models.ForeignKey(
#         Tag,
#         on_delete=models.CASCADE,
#         related_name="%(app_label)s_%(class)s_items",
#     )



# class TaggedWhatever(GenericTaggedItemBase):
#     # TaggedWhatever can also extend TaggedItemBase or a combination of
#     # both TaggedItemBase and GenericTaggedItemBase. GenericTaggedItemBase
#     # allows using the same tag for different kinds of objects, in this
#     # example Food and Drink.

#     # Here is where you provide your custom Tag class.
#     tag = models.ForeignKey(
#         Tag,
#         on_delete=models.CASCADE,
#         related_name="%(app_label)s_%(class)s_items",
#     )