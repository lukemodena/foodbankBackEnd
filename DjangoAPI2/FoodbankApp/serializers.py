from rest_framework import serializers
from FoodbankApp.models import Donor, Collection, Wholesale, Participation

class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = ('DonorID',
                  'FullName',
                  'FirstName',
                  'LastName',
                  'Email',
                  'Address1',
                  'Address2',
                  'Address3',
                  'PostCode',
                  'DonorType',
                  'Notes',
                  'Phone',
                  'InvolveNo')

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('CollectionID',
                  'CollectionDate',
                  'Type',
                  'TotalWeight',
                  'TotalCost',
                  'CollectionPhoto',
                  'CollectionSpreadsheet',
                  'CollectionStatus')

class WholesaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wholesale
        fields = ('WholesaleID',
                  'TotalDonated',
                  'TotalSpent',
                  'Remainder',
                  'WholesaleReceipt',
                  'Notes',
                  'CollectionID')

class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = ('ParticipationID',
                  'PaymentRecieved',
                  'DonationType',
                  'TotalDonated',
                  'DropOffTime',
                  'Notes',
                  'DonorID',
                  'CollectionID',
                  'WholesaleID')

class ParticipationListSerializer(serializers.ModelSerializer):

    DonorID = DonorSerializer()

    class Meta:
        model = Participation
        fields = ('ParticipationID',
                  'PaymentRecieved',
                  'DonationType',
                  'TotalDonated',
                  'DropOffTime',
                  'Notes',
                  'DonorID',
                  'CollectionID',
                  'WholesaleID')
