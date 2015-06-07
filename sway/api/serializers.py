from rest_framework import serializers
from sway.models import Lead, LeadFollowUp,StudioUser,Studio
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
    
class FollowUpSerializer(serializers.ModelSerializer):
    followed_by_name=serializers.SerializerMethodField('get_followed_by_name')
    class Meta:
        model=LeadFollowUp
        field=('id','lead','notes','follwed_by','followed_date', 'followed_by_name')
            
    def get_followed_by_name(self,obj):
        return obj.followed_by.username

class LeadSerializer(serializers.ModelSerializer):
    followups = FollowUpSerializer(many=True,required=False)
    class Meta:
        model = Lead
        fields=('id','name','contact_detail','email','mobile' ,'nextFollowUpDate' ,'inquiryFor','studio','followups')
        #fields=('id','name','contact_detail','email','mobile' ,'nextFollowUpDate' ,'inquiryFor','followups')
        
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Lead.objects.create(**validated_data) 


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'email', 'first_name', 'last_name', 'username', 'id')
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ('name', 'mobile', 'email', 'email_port', 'id')
    def create(self, validated_data):
        studio = Studio.objects.create(**validated_data)
        studio.save()
        return studio

class StudioUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudioUser
        field = ('user', 'studio_id')
    def create(self, validated_data):
        print "inside create studio user"
        studioUser = StudioUser.objects.create(**validated_data)
        studioUser.save()
        return studioUser 
    
           