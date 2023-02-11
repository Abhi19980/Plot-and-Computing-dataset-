from rest_framework import serializers
from EmployeeApp.models import Departments, Employees, PitcherResume

class DepartmentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = ('DepartmentId','DepartmentName')

class EmployeesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ('EmployeesId','EmployeesName','Department','DateOfJoining','PhotoFileName')




class PitcherResumeSerializers(serializers.ModelSerializer):
    class Meta:
        model = PitcherResume
        fields = ('pitcher_id','pitcher_pdf_resume',)