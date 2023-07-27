from rest_framework import serializers
from watchlist_app.models import WatchList , StreamPlatform ,Review
#model serilaizer


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude = ('watchlist',)
        

class WatchListSerializer(serializers.ModelSerializer):
    
    # reviews =ReviewSerializer(many=True , read_only=True)
    platform = serializers.CharField(source='platform.name')
    class Meta:
        model = WatchList
        fields = '__all__'
    
 

class StreamPlatformSerializer(serializers.ModelSerializer):
    # ->complete watchlist data
    watchlist = WatchListSerializer(many=True , read_only=True)
    # -> str method of watchlist
    # watchlist = serializers.StringRelatedField(many=True)
    # -> primary key of watchlist
    # watchlist = serializers.PrimaryKeyRelatedField(many=True , read_only=True)
    #hyper link related field
    # watchlist = serializers.HyperlinkedRelatedField( many=True , read_only=True , view_name='movie-item')
    
    class Meta:
        model = StreamPlatform
        fields = '__all__'   




# class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
#     # ->complete watchlist data
#     watchlist = WatchListSerializer(many=True , read_only=True)
#     # -> str method of watchlist
#     # watchlist = serializers.StringRelatedField(many=True)
#     # -> primary key of watchlist
#     # watchlist = serializers.PrimaryKeyRelatedField(many=True , read_only=True)
#     #hyper link related field
#     # watchlist = serializers.HyperlinkedRelatedField( many=True , read_only=True , view_name='movie-item')
    
#     class Meta:
#         model = StreamPlatform
#         fields = '__all__'      


       
        
  
  
  
  
  
  
  
  
  
  
  
  
  
  
# -------------------------
# class MovieSerializer(serializers.ModelSerializer):
#     len_name = serializers.SerializerMethodField()  
#     class Meta:
#         model = Movie
#         fields = '__all__'
#         # fields = ['id' , 'name' , 'description' ]
#         # exclude = ['active']
        
#     def get_len_name(self , object):
#         length = len(object.name)
#         return length
      
#     def validate(self , data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Name and description should be different")
#         return data
#     def validate_name(self , value):
#         if len(value) < 2:
#             raise serializers.ValidationError("Name is too short")
#         else:
#             return value


#normal serilaier 
# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too short")
#     else:
#         return value

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=100 ,  validators =[name_length])
#     description = serializers.CharField(max_length=1000)
#     active = serializers.BooleanField(default=True)
    
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update (self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description' , instance.description)
#         instance.active = validated_data.get('active' , instance.active)
#         instance.save()
#         return instance
# # field level validation
#     # def validate_name(self , value):
#     #     if len(value) < 2:
#     #         raise serializers.ValidationError("Name is too short")
#     #     else:
#     #         return value
        
# #object level validation
#     def validate(self , data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Name and description should be different")
#         return data
    
    