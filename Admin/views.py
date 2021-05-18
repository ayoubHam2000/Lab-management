from django.shortcuts import render

from django.views import View


class AdminAddMember(View):
    template_name = 'admin/add_membre.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)        

