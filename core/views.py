from django.shortcuts import render
from .models import *
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.conf import settings

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page after login
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


def home(request):
    return render(request,'cement.html')
def home2(request):
    return render(request,'checkstatus.html')
def home3(request):
    return render(request,'contact.html')
def hola(request):
    return render(request,'main.html')

def main(request):
    if request.method == 'POST':
        mob = request.POST.get("mobile")
        try:
            # First, try to find the client by phone number
            ven = Client.objects.get(phone_number=mob)
            
            # If found, check their status and return appropriate message
            if ven.status == 'pending':
                message = "Currently Your Application is Pending."
            elif ven.status == 'accepted':
                message = "Congratulations! Your Application is Approved!"
            else:
                message = "Sorry! Your Application has been Rejected."
            
            return render(request, 'index.html', {'message': message, 'ven': ven})
        
        except Client.DoesNotExist:
            try:
                # If client not found by phone number, try to find by vendor code
                ven = Client.objects.get(vendor_code=mob)
                
                # Check status and return appropriate message
                if ven.status == 'pending':
                    message = "Currently Your Application is Pending."
                elif ven.status == 'accepted':
                    message = "Congratulations! Your Application is Approved!"
                else:
                    message = "Sorry! Your Application has been Rejected."
                
                return render(request, 'index.html', {'message': message, 'ven': ven})
            
            except Client.DoesNotExist:
                # If client not found by either phone number or vendor code, show appropriate message
                message = "Client with provided mobile number or vendor code does not exist."
                return render(request, 'index.html', {'message': message})        
    # return render(request,'index.html' ,{'ven':ven})


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact = Contact(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        contact.save()

        return render(request, 'cement.html')

    else:
        return render(request, 'contact.html')



from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Frame, PageTemplate,Spacer
from reportlab.platypus import Image
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Assuming you have defined styles somewhere
styles = getSampleStyleSheet()
from django.http import HttpResponse
import datetime 

def generate_pdf(request):
    if request.method == 'POST':
        vendor_code = request.POST.get('vendor_code')
        client = Client.objects.get(vendor_code=vendor_code)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{vendor_code}_details.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)

        # Adjusted the coordinates to position the logo at the top-left corner
        top_left_frame = Frame(
            1,  # Left coordinate
            letter[1],  # Bottom coordinate (from top)
            2 * inch,  # Width
            2 * inch,  # Height
            id='top_left_frame'
        )
        template = PageTemplate(id='template', frames=[top_left_frame])
        doc.addPageTemplates([template])
        elements = []

        logo_path = f"C:\\CivilVendor\\media\\core\\logo\\{client.company.logo.url.split('logo/', 1)[1]}"
        logo = Image(logo_path, width=2 * inch, height=2 * inch)
        elements.append(logo)

        elements.append(Spacer(1, 0.3 * inch))  # Adding space of 0.3 inch

        current_date = datetime.date.today()
        main = str(current_date)
        date_paragraph = Paragraph(f"Date: {main}", style=styles['Normal'])
        elements.append(date_paragraph)

        approval_text = f"Congratulations {client.name}"
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph(approval_text, style=styles['Normal']))

        ab = f"Your vendor code application is approved by {client.company.name}"
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph(ab, style=styles['Normal']))

        abc = f"Your Vendor Code is {client.vendor_code}."
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph(abc, style=styles['Normal']))

        abs = f"We received your details as:"
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph(abs, style=styles['Normal']))
        elements.append(Spacer(1, 0.2 * inch))

        client_data = {
            "Phone Number": client.phone_number,
            "Email": client.email,
            "Agency Name": client.agency_name,
            "GST Number": client.GST_number,
            "Aadhar": client.Aadhar,
            "PAN Number": client.PAN_number,
            "Address": client.address,
            "Vendor Code": client.vendor_code,
        }

        for key, value in client_data.items():
            paragraph = Paragraph(f"{key}: {value}", style=styles['Normal'])
            elements.append(paragraph)
            elements.append(Spacer(1, 0.05 * inch))

        # Adding company bank details
        bank_details = (
            "Company Bank Details:-",
            "Account Number :- 60478986115",
            "IFSC Code :- MAHB0000311",
            "Holder Name :- Ultratech Cement Limited",
            "Branch Name :- Andheri East Mumbai",
        )

        for detail in bank_details:
            elements.append(Paragraph(detail, style=styles['Normal']))
            elements.append(Spacer(1, 0.05 * inch))

        elements.append(Spacer(1, 0.3 * inch))
        abq = f"Kind Regards,"
        elements.append(Paragraph(abq, style=styles['Normal']))
        abu = f"{client.company.name}"
        elements.append(Spacer(1, 0.3 * inch))
        elements.append(Paragraph(abu, style=styles['Normal']))

        doc.build(elements)

        return response

