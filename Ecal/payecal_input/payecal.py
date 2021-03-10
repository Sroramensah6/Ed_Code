from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from Eformulas.payecal.models.payecal_models import PayeCalModels


class PayeCal:
    def __init__(self, request):
        self.request = request

    def input(self):
        request = self.request
        if request.method == 'POST':
            print('Start....')
            if request.POST.get("full_name"):
                payecal = PayeCalModels()
                payecal.name = request.POST.get("full_name")
                payecal.date = request.POST.get('date')
                payecal.basic_sal = request.POST.get('basic_sal')
                # if(len(names) == 0):
                #     print("Yes")
                # else:
                #     print("No")
                payecal.housing_all = request.POST.get('housing_all')
                # if bool(payecal.housing_all):
                #     print('Has a value')
                # else:
                #     print("Has no value nice")
                # print(payecal.housing_all)
                payecal.transport_all = request.POST.get(
                    'transport_all')
                payecal.upfront_all = request.POST.get('upfront_all')
                payecal.other_all = request.POST.get('other_all')
                payecal.clothing_all = request.POST.get('clothing_all')
                payecal.over_time = request.POST.get('over_time')
                payecal.car_elements = request.POST.get('car_elements')
                payecal.rent_elements = request.POST.get(
                    'rent_elements')
                payecal.emp_ssf = request.POST.get('emp_ssf')
                payecal.reg_pen = request.POST.get('reg_pen')
                payecal.reg_pen_amt = request.POST.get('reg_pen_amt')
                payecal.prov_fund = request.POST.get('prov_fund')
                payecal.prov_fund_amt = request.POST.get(
                    'prov_fund_amt')
                payecal.pf_employer_rate = request.POST.get(
                    'pf_employer_rate')
                payecal.nr_prov_fund = request.POST.get('nr_prov_fund')
                payecal.nr_prov_fund_amt = request.POST.get(
                    'nr_prov_fund_amt')
                payecal.nr_reg_pen = request.POST.get('nr_reg_pen')
                payecal.nr_reg_pen_amt = request.POST.get(
                    'nr_reg_pen_amt')
                payecal.mortgage_int = request.POST.get('mortgage_int')
                payecal.mortgage_int_amt = request.POST.get(
                    'mortgage_int_amt')
                payecal.loan_and_int = request.POST.get('loan_and_int')
                nae = request.POST.get('prov_fund')
                if nae is None:
                    print("True")
                else:
                    print('nice', nae)

                payecal.loan_and_int_amt = request.POST.get(
                    'loan_and_int_amt')
                payecal.other_ded = request.POST.get('other_ded')
                payecal.other_ded_amt = request.POST.get(
                    'other_ded_amt')
                print('name', payecal.name)
                print('pay', request.POST.get('loan_and_int_amt'))
                print('payecal.emp_ssf', payecal.emp_ssf)
                print('payecal.reg_pen', payecal.reg_pen)
                print('payecal.reg_pen_amt', payecal.reg_pen_amt)
                print('payecal.prov_fund', payecal.prov_fund)
                print('payecal.other_ded_amt', payecal.other_ded_amt)
                print("END")
                # return HttpResponseRedirect(reverse("Home:about"))

        return render(request, 'Ecal/payecal/payecal.html', {
            "title": "Paye Calculator",
            "discription": "Paye Calculator"
        })
