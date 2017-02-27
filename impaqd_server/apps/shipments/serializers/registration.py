# from rest_framework import serializers
# from .generics import GenericCompanySerializer
# from ..models.generic_company import GenericCompany
# from ..models.generic_user import GenericUser
# 
# 
# class CompanyRegistrationSerializer(serializers.ModelSerializer):
#     company = GenericCompanySerializer()
# 
#     class Meta:
#         model = GenericUser
# 
#     def create(self, validated_data):
#         company = GenericCompany.objects.create(
#             **validated_data.pop('company', {}))
# 
#         return GenericUser.objects.create(
#             company=company, **validated_data)
