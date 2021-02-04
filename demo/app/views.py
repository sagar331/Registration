from django.shortcuts import render
from app.models import *
from rest_framework.response import Response
from rest_framework import viewsets,status
from django.contrib.auth import authenticate
import traceback
from django.utils.timezone import now, timedelta
from oauth2_provider.settings import oauth2_settings
from oauthlib.common import generate_token
from oauth2_provider.models import AccessToken, Application, RefreshToken
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope



class RegisterView(viewsets.ViewSet):
    def create(self,request):
        try:
            email=request.data.get('email')
            user_email=MyUser.objects.filter(email=email)
            if  user_email:
                return Response('already register email')

            myuser=MyUser()
            myuser.email=request.data.get('email')
            myuser.username=request.data.get('username')
            myuser.set_password(request.data.get('password'))
            myuser.mobile=request.data.get('mobile')
            myuser.is_active=True
            myuser.save()
            app = Application.objects.create(user=myuser)
            token = generate_token()
            refresh_token = generate_token()
            expires = now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
            scope = "read write"
            access_token = AccessToken.objects.create(user=myuser,
                                                application=app,
                                                expires=expires,
                                                token=token,
                                                scope=scope,
                                                )
            print("access token ------->", access_token)
            RefreshToken.objects.create(user=myuser,
                                        application=app,
                                        token=refresh_token,
                                        access_token=access_token
                                        )
            response = {
                'access_token': access_token.token,
                'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
                'token_type': 'Bearer',
                'refresh_token': access_token.refresh_token.token,
                'client_id': app.client_id,
                'client_secret': app.client_secret
                }
            
            return Response({'response':'you are sign up successfull ','message':True,'status':status.HTTP_200_OK})
        except Exception as error:
            traceback.print_exc()
            return Response({'response':str(error),'message':False,'status':status.HTTP_200_OK})
  


class LoginView(viewsets.ViewSet):
    # permission_classes = [TokenHasReadWriteScope]
    def create(self,request):
        try:
            email=request.data.get('email')
            password=request.data.get('password')

            user=authenticate(email=email,password=password)

            if user is not None:
                app = Application.objects.get(user=user)  
                # token = get_access_token(user)
                token = generate_token()
                refresh_token = generate_token()
                expires = now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
                scope = "read write"
                access_token = AccessToken.objects.create(user=user,
                                                        application=app,
                                                        expires=expires,
                                                        token=token,
                                                        scope=scope,
                                                        )
                    
                RefreshToken.objects.create(user=user,
                                        application=app,
                                        token=refresh_token,
                                        access_token=access_token
                                        )
                response = {
                    'name':user.username,
                    'access_token': access_token.token,
                    'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,                    'token_type': 'Bearer',
                    'refresh_token': access_token.refresh_token.token,
                    'client_id': app.client_id,
                    'client_secret': app.client_secret
                    }
                
                return Response({'response':response,'message':True,'status':status.HTTP_200_OK})

            else:
                email=MyUser.objects.filter(email=email)
                if not email:
                    return Response({'response':'email is not valid plz enter valid email id','message':False,'status':status.HTTP_200_OK})
                password=MyUser.objects.filter(password=password)
                if not password:
                    return Response({'response':'password is not valid plz enter valid paasword id','message':False,'status':status.HTTP_200_OK})
        except Exception as error:
            traceback.print_exc()
            return Response({'response':str(error),'message':False,'status':status.HTTP_200_OK})
  


class LogOutView(viewsets.ViewSet):
    permission_classes = [TokenHasReadWriteScope]
    def list(self,request):
        try:
            user_token=request.auth
        
       
            refresh_token_gen=RefreshToken.objects.filter(access_token=user_token)
            refresh_token_gen.delete()
            user_token.delete()
            return Response({'response':'you are logout successfull','message':True,'status':status.HTTP_200_OK})

        except Exception as error:
            traceback.print_exc()
            return Response({'response':str(error),'message':False,'status':status.HTTP_200_OK})



class DetailViewSet(viewsets.ViewSet):
    def list(self,request):
        detaillist = Detail.objects.all()
        data=[]
        for detaillists in detaillist:
            data.append({
        
                'id':detaillists.id,
                'image':str(detaillists.image)
            })
        return Response({'data list':data})
    def retrieve(self, request, pk=None):
        detail_retrive=Detail.objects.get(id=pk) 
        datad=[{
            'image':str(detail_retrive.image)
        }]
        return Response({'detail retrive':datad})
    def destroy(self, request, pk=None):
        detail_destroy=Detail.objects.filter(id=pk).delete()
        return Response({'Successfully data delete'})
    def update(self,request,pk=None):
        detail_Object=Detail.objects.get(id=pk)
        image=request.data.get('image')
        detail_Object.image = image
        detail_Object.save() 
        return Response({"response":'Create Data'})        
    def create(self,request):
        detail_id=request.data.get('detail_id')
        detail_create=MyUser.objects.get(id=detail_id)
        print(detail_create,detail_create)
        detail_Object=Detail()
        detail_Object.userfor=detail_create
        detail_Object.image = request.data.get('image')
        detail_Object.save()
        return Response({"response":'Create Data'})




