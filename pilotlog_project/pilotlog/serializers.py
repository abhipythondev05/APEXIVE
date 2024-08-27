from rest_framework import serializers
from .models import ImagePic


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument
    that controls which fields should be included in the serialized output.
    """
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' argument up to the superclass
        fields = kwargs.pop('fields', None)
        print("****************************************")
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            print("fields",fields)
            # Drop any fields that are not specified in the `fields` argument
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ImagePicSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = ImagePic
        fields = '__all__'  # or specify the fields you want to include
