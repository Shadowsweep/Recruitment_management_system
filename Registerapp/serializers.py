from rest_framework import serializers
from .models import  Profile ,Blog ,Appointment,Student,Admin,PlacementDrive
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
    
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
        
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        
        
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['enrollment_id', 'name', 'resume', 'profile_picture', 'email', 'gender', 'city', 'state', 'tenth_grade', 'twelth_grade','applied']

class AdminSerializer(serializers.ModelSerializer):
    enrollment_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())

    class Meta:
        model = Admin
        fields = ['admin_id', 'enrollment_id','name','email','password']
        
class PlacementDriveSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlacementDrive
        fields = '__all__'