### 4주차   

## 1️⃣ 데이터 삽입

- `ORM 쿼리`를 통해 `Post 모델`에 데이터 3개 삽입

![orm](https://user-images.githubusercontent.com/80563849/138105662-921d1b7b-3053-4f19-b11b-bc7c6a6afb95.PNG)

- 모델 선택 및 데이터 삽입

  ```python
  class Post(models.Model):
      post_author = models.ForeignKey(User, on_delete=models.CASCADE)
      location = models.TextField()
      post_content = models.TextField()
      is_comment = models.BooleanField()
      upload_time = models.DateTimeField(auto_now=True)
  
      def publish(self):
          self.upload_time = timezone.now()
          self.save()
  
      def __str__(self):
          return self.post_content
  
      class Meta:
          managed = True
          verbose_name = 'Post'
          verbose_name_plural = 'Posts'
          
          
  class User(AbstractBaseUser):
      username = models.CharField(max_length=100, unique=True)
      USERNAME_FIELD = 'username'
      instagram_id = models.CharField(max_length=100, unique=True)
      is_professional = models.BooleanField(default=False)
  
      objects = UserManager()
  
      class Meta:
          managed = True
          verbose_name = 'User'
          verbose_name_plural = 'Users'
  ```

  ![저장](https://user-images.githubusercontent.com/80563849/138125025-7c183c7a-cf45-4118-a872-88629275788a.PNG)

## 2️⃣ 모든 데이터를 가져오는 API 만들기

- 모든 'Post'의 list를 가져오는 API 요청 결과: `GET`  `api/posts`

![image](https://user-images.githubusercontent.com/80563849/138129310-d1e205e7-0b74-434c-b6f0-edcdbc75a96b.png)



## 3️⃣ 새로운 데이터를 create하도록 요청하는 API 만들기

- Post를 추가하는 API 요청 결과: `POST` `api/posts/` 

- Body: `{"post_content" : "happy", "location" : "Namyangju"}`

  ![image](https://user-images.githubusercontent.com/80563849/138139771-7500ec46-71c2-4fb7-b55d-6dfb525704cb.png)



## 4️⃣ 회고

가장 오래 걸렸던 과제였던 것 같다. 아직 완벽하게 이해가 된 것 같지 않아서 날 잡고 열심히 공부해야겠다..😥 erd와 변경된 model을 3주차 README에 반영해야겠다.



## ☑ 참고

- `django.db.utils.IntegrityError` 에러가 발생한 경우: 에러가 발생한 **필드가 null 값이 되지 않도록 값 필수로 설정**

- POSTMAN으로 POST api 작성 방법: [POST api - Body->raw](https://meetup.toast.com/posts/107) (param으로 값을 입력해서 호출한 경우, 

  `rest_framework.exceptions.parseerror: json parse error - expecting value: line 1 column 1 (char 0)` 에러가 발생했음)

- `'manager' object has no attribute 'get_by_natural_key'` 에러가 발생한 경우: User 클래스에 `objects = UserManager()` 추가 (**AbstractBaseUser로 custom user를 생성한 경우** **UserManager 필수**로 선언, 추가)

- [verbose name이란](https://djangojeng-e.github.io/2020/08/02/Django-Models-6%ED%8E%B8-Fields-verbose-field-names/)


## 5주차 과제

기존에 작성했던 views.py 를 **CBV인 API View**로 변경할 것이다.



### READ API (`GET`)

#### 1. views.py 작성하기

```python
# views.py
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import PostSerializer


class PostList(APIView):
    def get(self, request, format=None):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)
```

`PostList`의 `get` 함수는 **모든 Post의 list를 가져오는 함수**이다.  

`queryset`에 모든 `Post` 데이터를 저장한 후 `PostSerializer`에 queryset을 `many=True`로 삽입하여 **serializer에 담긴 data를 반환**하는 형식이다.

```python
class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        post = self.get_object(pk)    # get_object로 error check
        serializer = PostSerializer(post)
        return Response(serializer.data)
```

`PostDetail`의 `get` 함수는 특정 `id` (=pk)를 받아 **그 id값을 지닌 Post를 가져오는 함수**이다.

`get_object`는 **Error catch를 위한 함수**로, 요청을 보낸 id가 존재하지 않는 경우엔 `Http404`에러를 발생시킨다.

#### 2. urls.py 작성하기

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('posts', views.PostList.as_view()),
    path('posts/<int:pk>', views.PostDetail.as_view())
]
```

view.py를 작성한 후 urls.py를 작성한다.



#### 결과

**1️⃣ 모든 데이터를 가져오는 API**

- URL: `api/posts`
- Method: `GET`

![모든포스트가져오기](https://user-images.githubusercontent.com/80563849/141237418-2afff7e9-e32e-4fb6-bb0a-1c2c259db18d.PNG)

**2️⃣ 특정 데이터를 가져오는 API**

- URL: `api/posts/\<int:pk>` (`api/posts/2`)
- Method: `GET`

![특정포스트가져오기](https://user-images.githubusercontent.com/80563849/141237490-a52ed993-ae7f-49dc-aa3b-36c1a114dbb8.PNG)

### CREATE API (`POST`)

#### views.py 작성하기

```python
# views.py

class PostList(APIView):
	def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
```

`PostList`의 `post` 함수는 **새 Post를 create하는 함수**이다. 

serializer의 값이 `valid` 하면, 즉 요청한 값이 `valid`하면 `Http201`을, `invalid`하다면 `Http400` error를 반환한다.   



#### 결과

**3️⃣ 새로운 데이터를 create하는 API** 

- URL: `api/posts`
- Method: `POST`
- Body: `{"필드명": 필드값, ... }`

![새로운데이터생성하기](https://user-images.githubusercontent.com/80563849/141237547-164620a5-b15c-47eb-80e7-e6a96fb6015e.PNG)



### UPDATE API (`PUT`)

#### views.py 작성하기

```python
# views.py

class PostDetail(APIView):
    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

`PostDetail`의 `put` 함수는 특정 `id`(=pk)를 받아 **그 id값을 지닌 Post의 내용을 변경하는 함수**이다.

요청한 값이 `valid`하면 **변경된 값을 보여주고**, `invalid`하면 `Http400` error를 발생시킨다.

### 

#### 결과

**4️⃣ 특정 데이터를 업데이트하는 API**

- URL: `api/posts/<int:pk>` (`api/posts/3`)
- Method: `PUT`
- Body: `{"필드명": 업데이트 할 필드값, ... }` (`{"location": "Songdo"}`)

  ![특정데이터업데이트하기](https://user-images.githubusercontent.com/80563849/141237595-a49712c2-93f0-4bff-856f-e4f8548012db.PNG)



### DELETE API (`DELETE`)

#### views.py 작성하기

```python
class PostDetail(APIView):
	def delete(self, request, pk):
    	post = self.get_object(pk)
    	post.delete()
    	return Response(status=status.HTTP_204_NO_CONTENT)
```

`PostDetail`의 `delete` 함수는 특정 `id`(=pk)의 **Post를 삭제하는 함수**이다.

delete() 함수로 삭제를 한 후, `Http204`로 삭제가 완료되었음을 보여준다.



#### 결과

**5️⃣ 특정 데이터를 삭제하는 API**

- URL: `api/posts/\<int:pk>`
- Method: `DELETE`

아래 사진처럼 삭제 요청을 보내고,

![삭제요청보내기](https://user-images.githubusercontent.com/80563849/141237632-3de6d0cf-eadd-404a-8d8d-f19ca537d6b4.PNG)

요청을 보낸 후, GET api/post/3 으로 3번째 Post를 조회하면, 

![삭제하고다시조회하기](https://user-images.githubusercontent.com/80563849/141237654-b0dc8d41-3e64-4359-b1f2-2b274bb5acae.PNG)



### 간단한 회고

- 새로운 데이터를 생성하는 POST 함수에서 계속 에러가 난다. ForeignKey로 post_author의 id를 생성하면서 `IntegrityError` 가 떠서 해결을.. 얼른... 해야겠다..
- 확실히 지난주에 만들었던 view 보다 API view를 사용하는 것이 코드가 깔끔해보여서 좋았다.
