from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin,\
    LoginRequiredMixin
from complaint.models import Complaint
from CholitoProject.userManager import get_user_index
import datetime




class IndexView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'municipality.municipality_user_access'
    template_name = 'muni_complaints_main.html'
    context = {}

    def getComplaintStats(self, complaints, inicio, fin):
        stats_complaint = {}
        status_parser = dict(Complaint().COMPLAINT_STATUS)

        for key, value in status_parser.items():
            stats_complaint[value] = 0

        for complaint in list(complaints):
            temp_status = status_parser.get(complaint.status)
            if (datetime.date.today() > inicio and datetime.date.today() < fin):
                stats_complaint[temp_status] += 1

        return stats_complaint

    def get(self, request, **kwargs):
        user = get_user_index(request.user)
        complaints = Complaint.objects.filter(
            municipality=user.municipality)

        self.context['complaints'] = complaints
        self.context['c_user'] = user
        self.context['stats'] = self.getComplaintStats(complaints,datetime.date.today() - datetime.timedelta(365/12),datetime.date.today())
        return render(request, self.template_name, context=self.context)


class StatisticsView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'municipality.municipality_user_access'
    template_name = 'muni_statistics.html'
    context = {}

    def getComplaintType(self, complaints):
        type_complaint = {}
        type_parser = dict(Complaint().COMPLAINT_OPTIONS)

        for key, value in type_parser.items():
            type_complaint[value] = 0

        for complaint in list(complaints):
            temp_status = type_parser.get(complaint.case)
            type_complaint[temp_status] += 1


        return type_complaint


    def get(self, request, **kwargs):
        user = get_user_index(request.user)
        complaints = Complaint.objects.filter(
            municipality=user.municipality)

        self.context['complaints'] = complaints
        self.context['c_user'] = user
        self.context['type'] = self.getComplaintType(complaints)
        return render(request, self.template_name, context=self.context)


class UserDetail(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'municipality.municipality_user_access'

    def post(self, request, **kwargs):
        c_user = get_user_index(request.user)
        if 'avatar' in request.FILES:
            c_user.municipality.avatar = request.FILES['avatar']
            c_user.municipality.save()
        return redirect('/')
