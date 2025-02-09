from rest_framework import serializers
from django.contrib.auth.models import User
from user_register.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    print('profile serializer called')
    class Meta:
        model = Profile
        fields = '__all__'
    
    def validate_phone(self, value):
        """Ensure phone number is not taken by another user except the current one."""
        user = self.instance.user if self.instance else None

        # Check if phone number exists for another user
        if Profile.objects.filter(phone=value).exclude(user=user).exists():
            raise serializers.ValidationError("Phone number already exists for another user.")
        
        return value

    def update(self, instance, validated_data):
        print('profile update method called')
        # Check if the phone number is being updated
        new_phone = validated_data.get('phone', instance.phone)

        # Ensure the phone number is not assigned to another profile
        if Profile.objects.filter(phone=new_phone).exclude(id=instance.id).exists():
            raise serializers.ValidationError({"phone": ["This phone number is already in use."]})

        # Update the profile with new validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    print('user serializer called')
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile', 'first_name', 'last_name', 'is_staff', 'is_active', 
                  'date_joined', 'last_login', 'groups', 'user_permissions']
        
    def update(self, instance, validated_data):
        print('user update method calle')
        profile_data = validated_data.pop('profile', None)  # Extract 'profile' data if present

         # Update only the fields provided in validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)  # Dynamically update only changed fields
        instance.save()  # Save the updated User fields

        # Update Profile fields if provided
        if profile_data:
        #     profile_instance, _ = Profile.objects.get_or_create(user=instance)  # Ensure Profile exists
        #     for attr, value in profile_data.items():
        #         setattr(profile_instance, attr, value)
        #     profile_instance.save()
        # user profile serializer to update the profile
            profile_instance = instance.profile
            profile_serializer = ProfileSerializer(profile_instance, data=profile_data)
            if profile_serializer.is_valid():
                profile_serializer.save()
            else:
                raise serializers.ValidationError(profile_serializer.errors)

        return instance