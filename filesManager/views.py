from xmlrpc.client import Boolean
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views import View
from filesManager.forms import FileForm

from rest_framework import  mixins, generics, viewsets

from filesManager.models import Files, FileSetup
from filesManager.serializers import FileManagerSerializer
from users.models import Plan


class FileViewSet(viewsets.GenericViewSet):
    queryset= Files.objects.all()
    serializer_class = FileManagerSerializer

class FileListview(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset= Files.objects.all()
    serializer_class = FileManagerSerializer

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        fileName= request.FILES['file'].name
        fileSize= request.FILES['file'].size
        return self.create(request, *args, **kwargs)


class FileDetailview(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):

    queryset= Files.objects.all()
    serializer_class = FileManagerSerializer

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class Upload(View):
    form_class=FileForm
    template_name = 'users/videos_upload.html'
   
    def get(self, request, *args, **kwargs):       
        form = self.form_class()
        if self.check_plan(request, 0):
            return redirect('payment')
        return render(request, 'users/videos_upload.html', {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class()
        file_size = request.FILES['file'].size
        if self.check_plan(request, file_size):
            return redirect('payment')
        form=self.form_class(data=request.POST,files=request.FILES)
        if form.is_valid():
            files = Files(user = request.user, file=request.FILES['file'], file_name=request.POST['file_name'], file_size=file_size)
            files.save()
            return redirect('profile')
    
    def check_plan(self, request, upload_file_size)-> Boolean:
        try:
            file_setup = FileSetup.objects.get(pk=1)
        except(ObjectDoesNotExist):
            raise 'File Setup not found'
        user = request.user  
        userCurrentPlan = False
        try:  
            userCurrentPlan = Plan.objects.get(user=user, current=True)
        except:
            pass
        totalFileSize = sum([file.file_size for file in Files.objects.filter(user=user)])+upload_file_size
        totalFileSize = totalFileSize / (1000**3)
        fileCount = Files.objects.filter(user=user).count()
        print('file size: {}'.format(totalFileSize), '\nfile count: {}'.format(fileCount), '\nMaximum no of files: {}'.format(file_setup.max_no_of_free_files))
        if not userCurrentPlan:
            match file_setup.free_plan_restriction:
                case 0:
                    if fileCount >= file_setup.max_no_of_free_files:
                        return True
                case 1:
                    if totalFileSize >= file_setup.max_of_free_file_size:
                        return True
                case 2:
                    if totalFileSize >= file_setup.max_of_free_file_size or fileCount >= self.file_setup.max_no_of_free_files:
                        return True
        else:
            userCurrentPlan.expired = userCurrentPlan.is_expired()
            if totalFileSize >= userCurrentPlan.storage_size:
                return True
