from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

UserModel = get_user_model()


class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
	##
	def check_user(self, clean_data):
		user = authenticate(username=clean_data['email'], password=clean_data['password'])
		if not user:
			raise RuntimeError('user not found')
		return user

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = UserModel
        fields = ['user_id', 'email', 'username', 'password', 'is_doctor', 'is_staff']
        extra_kwargs = {
			'password' : {'write_only' : True}
		}
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance