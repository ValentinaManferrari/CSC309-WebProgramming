from rest_framework.serializers import ModelSerializer
from django.core.exceptions import ValidationError
from accounts.models import OurUser
from django.contrib.auth.hashers import check_password

class UserSerializer(ModelSerializer):
    # inspiration: https://stackoverflow.com/questions/38845051/how-to-update-user-password-in-django-rest-framework
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password': 
                old_password = self.initial_data.get("old_password", None)
                password2 = self.initial_data.get("password2", None)
                if old_password == None:
                  raise ValidationError({"old_password":"Must provide the old password too"})
                if not check_password(old_password, instance.password):
                  raise ValidationError({"old_password":"Old Password is incorrect"})
                if password2 == None or password2 != value:
                  raise ValidationError({"password2":"Passwords don't not match"})
                    
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
    class Meta:
      model = OurUser
      fields = ['username', 'password', 'first_name', 'last_name', 'email', 'phone', 'avatar'] 
      

       