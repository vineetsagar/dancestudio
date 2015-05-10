from rest_framework import serializers
from sway.models import Lead, LeadFollowUp,StudioUser
from django.shortcuts import get_object_or_404
    
class FollowUpSerializer(serializers.ModelSerializer):
    followed_by_name=serializers.SerializerMethodField()
    class Meta:
        model=LeadFollowUp
        field=('id','lead','notes','follwed_by','followed_date')
            
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
    
           