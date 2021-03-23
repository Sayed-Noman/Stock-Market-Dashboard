from django.shortcuts import render


def dashboard(requeest):
    return render(requeest,'home/dashboard.html', {})
