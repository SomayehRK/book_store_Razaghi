from django.utils.text import slugify


class Text:

    def slugify_unique(self, model, title):
        """
        Given a DB model and a title, return a unique slug
        that is unique to all other slug fields of the given DB model.

        Arguments
        model - Must be a Django database model that has a slug field called "slug".
        title - The string used to create the slug.

        Returns - A slug that is unique across all instances of the model.
        """

        slug = slugify(title)
        existing_slugs = []
        try:
            [existing_slugs.append(str(i.slug)) for i in model.objects.all()]
        except:
            print("There was no slug field found for {}".format(model))
            return slug
        if slug in existing_slugs:
            date_slug = slug + "-" + timezone.now().strftime("%Y%m%d")
            if date_slug in existing_slugs:
                long_slug = date_slug + timezone.now().strftime("%m%s")
                return long_slug
            else:
                return date_slug
        else:
            return slug