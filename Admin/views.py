from django.shortcuts import render

from django.views import View


class AdminAddMember(View):
    template_name = 'admin/add_membre.html'
    

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class AdminAddMember_cont(View):
    contenu = 'admin/contenu.html'
    

    def get(self, request):
        context = {}
        return render(request, self.contenu, context)
   

class AdminAddMember_test(View):
    test = 'admin/test.html'
    

    def get(self, request):
        context = {}
        return render(request, self.test, context)