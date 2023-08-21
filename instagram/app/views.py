from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Post
import json

# Create your views here.

def post_list(request):
    posts=Post.objects.all()
    return render(request,'app/post_list.html',{'posts':posts})


def create_post(request):
    if request.method == "POST" :
        try :
            post_data=json.loads(request.body)
            username=post_data['username']
            caption = post_data['caption']

            new_post = Post(username=username,caption=caption)
            new_post.save()

            return JsonResponse({'message':"Post Created Successfully"})
        except Exception as e:
            return JsonResponse({'error':str(e)}, status=400)

    else :
        return JsonResponse({'error':'Only POST request are allowed'},status=405)         

def view_post(request):
    if request.method=="GET":
        posts = Post.objects.all().value()

        return JsonResponse({"post":list(posts)})
    else:
        return JsonResponse({'error':"Only Get request allowed"},status=405)
    
def delete_post(request,post_id):
    if request.method=="DELETE":
        try:
            post = Post.objects.get(id=post_id)
            post.delete()
            return JsonResponse({'message':"Post Deleted Successfully"})
        except Post.DoesNotExist:
            return JsonResponse({'error':"Post not Found"},status=404) 

    else: return JsonResponse({'error':"Only Delete request is allowed"},status=405)       