from django.db import models


class Students(models.Model):
    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100,null=True)
    age = models.CharField(max_length=50,null=True)
    dob = models.DateField(null=True)
    email = models.EmailField(null=True, blank=True)
    permanent_address = models.CharField(max_length=200,null=True)
    temporary_address = models.CharField(max_length=200,null=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    admission = models.DateField(null=True)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('other','other')
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,null=True)
    standard = models.CharField(max_length=5,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    photo = models.ImageField(upload_to="students/photos/", null=True, blank=True)
    signature = models.ImageField(upload_to="students/signatures/", null=True, blank=True)
    aadhar = models.FileField(upload_to="students/aadhar/", null=True, blank=True)
    marksheet_10 = models.FileField(upload_to="students/marksheets/", null=True, blank=True)
    marksheet_11 = models.FileField(upload_to="students/marksheets/", null=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class FeePayment(models.Model):
    student = models.ForeignKey(
        Students,
        on_delete=models.CASCADE,
        related_name="fees"
    )
    total_fees = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    pending_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    payment_date = models.DateField(null=True)
    payment_status = models.CharField(max_length=20,null=True)
    remarks = models.CharField(max_length   =255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f"{self.student.first_name} - ₹{self.amount_paid}"

    
    
