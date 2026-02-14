from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from .models import Students, FeePayment
import pandas as pd
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


@login_required(login_url="login")
def dashboard(request):
    total_students = Students.objects.count()
    return render(request, "dashboard.html", {"total_students": total_students})

def students(request):
    student_list = Students.objects.all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        student_list = student_list.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(mobile__icontains=search_query) |
            Q(standard__icontains=search_query)
        )

    paginator = Paginator(student_list, 10)
    page = request.GET.get('page')

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'students.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })


def excel(request):
    if request.method == "POST":
        excel_file = request.FILES.get('excel_file')
        df = pd.read_excel(excel_file)

        for _, row in df.iterrows():
            student = Students.objects.create(
                first_name=row['first_name'],
                last_name=row['last_name'],
                age=row['age'],
                dob=row['dob'],
                email=row['email'],
                mobile=str(row['mobile']),
                permanent_address=row['permanent_address'],
                temporary_address=row['temporary_address'],
                admission=row['admission'],
                gender=row['gender'],
                standard=row['standard'],
            )

            FeePayment.objects.create(
                student=student,
                total_fees=row['total_fees'],
                amount_paid=row['amount_paid'],
                pending_amount=row['pending_amount'],
                payment_date=row['payment_date'],
                payment_status=row['payment_status'],
                remarks=row['remarks'],
            )

        return redirect('students')
    return render(request, 'excel.html')

def feesrecord(request):
    fees = FeePayment.objects.select_related('student').order_by('-payment_date')
    return render(request, 'feesrecord.html', {'fees': fees})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def add_students(request):
    if request.method == "POST":

        student = Students.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            age=request.POST.get('age'),
            dob=request.POST.get('dob'),
            email=request.POST.get('email'),
            mobile=request.POST.get('mobile'),
            admission=request.POST.get('admission'),
            gender=request.POST.get('gender'),
            permanent_address=request.POST.get('permanent_address'),
            temporary_address=request.POST.get('temporary_address'),
            standard=request.POST.get('standard'),
            photo=request.FILES.get('photo'),
            signature=request.FILES.get('signature'),
            aadhar=request.FILES.get('aadhar'),
            marksheet_10=request.FILES.get('marksheet_10'),
            marksheet_11=request.FILES.get('marksheet_11'),
        )

        FeePayment.objects.create(
            student=student,
            total_fees=request.POST.get('total_fees'),
            amount_paid=request.POST.get('amount_paid'),
            pending_amount=request.POST.get('pending_amount'),
            payment_date=request.POST.get('payment_date'),
            payment_status=request.POST.get('payment_status'),
            remarks=request.POST.get('remarks'),
        )

        if request.POST.get('action') == 'pdf':
            pdf_data = request.POST.copy()
            template = get_template('student_pdf.html')
            html = template.render(pdf_data)

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="student_form.pdf"'
            pisa.CreatePDF(html, dest=response)
            return response

        return redirect('students')
    return render(request, 'add_students.html')

def update_student(request, student_id):
    student = Students.objects.get(id=student_id)
    fee_payment = FeePayment.objects.filter(student=student).first()
    
    if request.method == "POST":
        # Update student details
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.age = request.POST.get('age')
        student.dob = request.POST.get('dob')
        student.email = request.POST.get('email')
        student.mobile = request.POST.get('mobile')
        student.admission = request.POST.get('admission')
        student.gender = request.POST.get('gender')
        student.permanent_address = request.POST.get('permanent_address')
        student.temporary_address = request.POST.get('temporary_address')
        student.standard = request.POST.get('standard')
        
        if request.FILES.get('photo'):
            student.photo = request.FILES.get('photo')
        if request.FILES.get('signature'):
            student.signature = request.FILES.get('signature')
        if request.FILES.get('aadhar'):
            student.aadhar = request.FILES.get('aadhar')
        if request.FILES.get('marksheet_10'):
            student.marksheet_10 = request.FILES.get('marksheet_10')
        if request.FILES.get('marksheet_11'):
            student.marksheet_11 = request.FILES.get('marksheet_11')
        
        student.save()
        
        if fee_payment:
            fee_payment.total_fees = request.POST.get('total_fees')
            fee_payment.amount_paid = request.POST.get('amount_paid')
            fee_payment.pending_amount = request.POST.get('pending_amount')
            fee_payment.payment_date = request.POST.get('payment_date')
            fee_payment.payment_status = request.POST.get('payment_status')
            fee_payment.remarks = request.POST.get('remarks')
            fee_payment.save()
        
        return redirect('students')
    
    context = {
        'student': student,
        'fee_payment': fee_payment
    }
    return render(request, 'update_student.html', context)