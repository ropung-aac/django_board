from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('board:post_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # 회원가입 후 자동 로그인
        return response
    
@login_required
def logout_view(request):
    logout(request)
    return redirect('board:post_list')