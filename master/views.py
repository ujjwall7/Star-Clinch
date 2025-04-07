from django.shortcuts import render
from rest_framework.views import APIView
from . serializers import *
from.models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from rest_framework.throttling import UserRateThrottle

from django.contrib.auth import authenticate

class login(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return Response({
                'token' : str(token)
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "No active session found"}, status=status.HTTP_400_BAD_REQUEST)

class RecipeRateThrottle(UserRateThrottle):
    rate = '10/min'  # Recipe API ke liye 10 requests per minute

class RatingRateThrottle(UserRateThrottle):
    rate = '5/hour'  # Rating API ke liye 5 requests per hour


class RecipeApi(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [RecipeRateThrottle]   

    def get(self, request):
        obj = Recipe.objects.all()
        serializer = RecipeSerializer(obj, many=True)
        return Response({
            'data' : serializer.data
        })

    def post(self, request):
        user = request.user
        get_user = User.objects.get(id = user.id)
        if not get_user.user_type == 'seller':
            return Response({
                'msg' : 'customer cannot add recipe',
            })
        serializer = AddUpdateRecipeSerializer(data = request.data)
        if serializer.is_valid():
            try:
                obj = serializer.save(seller=request.user)
                return Response({
                    'msg' : 'Recipe Added Successfully',
                    'success' : True
                })
            except Exception as e:
                return Response({
                'msg' : str(e),
                'success' : False
            })
        else:
            return Response({
                'msg' : serializer.errors,
                'success' : False
            })

    def put(self, request):
        user = request.user
        get_user = User.objects.get(id = user.id)
        if not get_user.user_type == 'seller':
            return Response({
                'msg' : 'customer cannot add recipe',
            })
        
        recipe_id = request.query_params.get("id")
        if not recipe_id:
            return Response({
                'msg': 'Recipe ID is required',
                'success': False
            }, status=400)

        try:
            recipe = Recipe.objects.get(id=recipe_id, seller=request.user)
        except Recipe.DoesNotExist:
            return Response({
                'msg': 'Recipe not found',
                'success': False
            }, status=404)

        serializer = AddUpdateRecipeSerializer(recipe, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'msg': 'Recipe Updated Successfully',
                'success': True
            })
        else:
            return Response({
                'msg': serializer.errors,
                'success': False
            })


    def delete(self, request):
        user = request.user
        get_user = User.objects.get(id = user.id)
        if not get_user.user_type == 'seller':
            return Response({
                'msg' : 'customer cannot add recipe',
            })
        
        recipe_id = request.query_params.get("id")
        if not recipe_id:
            return Response({
                'msg': 'Recipe ID is required',
                'success': False
            }, status=400)

        try:
            recipe = Recipe.objects.get(id=recipe_id, seller=request.user)
            recipe.delete()
            return Response({
                'msg': 'Recipe Deleted Successfully',
                'success': True
            })
        except Recipe.DoesNotExist:
            return Response({
                'msg': 'Recipe not found',
                'success': False
            }, status=404)

class RatingApi(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [RatingRateThrottle]   

    def post(self, request):
        print(f"{request.user = }")
        serializer = RatingSerializer(data = request.data)
        if serializer.is_valid():
            try:
                obj = serializer.save(customer=request.user)
                return Response({
                    'msg' : 'Rating Added Successfully',
                    'success' : True
                })
            except Exception as e:
                return Response({
                'msg' : str(e),
                'success' : False
            })
        else:
            return Response({
                'msg' : serializer.errors,
                'success' : False
            })

# abc
# Learing Reverting


