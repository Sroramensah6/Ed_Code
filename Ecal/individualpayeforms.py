import datetime
from django import forms
from Eformulas.individual_models import ECALAdvance, ECALBasic


class PayeForm (forms.ModelForm):
    class Meta:
        CAR_ELEMENTS = (
            ('0', 'Choice One'),
            ('dvf', 'Driver vehicle Fuel'),
            ('vf', 'Vehicle Fuel'),
            ('fo', 'Fuel Only'),
            ('vo', 'Vehicle Only')
        )
        RENT_ELEMENTS = (
            ('0', 'Choice One'),
            ('af', 'Accommodation with Furnishing'),
            ('af', 'Accommodation Only'),
            ('fo', 'Furnishing Only'),
            ('sa', 'Shared Accommodation')
        )
        EMP_SSF = (
            ('0', 'Choose One'),
            ('yes', 'Yes'),
            ('no', 'No')
        )
        REG_PEN = (
            ('0', 'Choose One'),
            ('yes', 'Yes'),
            ('no', 'No')
        )
        PROV_FUND = (
            ('0', 'Choose One'),
            ('yes', 'Yes'),
            ('no', 'No')
        )
        NR_PROV_FUND = (
            ('0', 'Choose One'),
            ('yes', 'Yes'),
            ('no', 'No')
        )
        NR_REG_PEN = (
            ('0', 'Choose One'),
            ('yes', 'Yes'),
            ('no', 'No')
        )
        MORTGAGE_INT = (
            ('0', 'Choose One'),
            ('yes', 'Yes'),
            ('no', 'No')
        )
        LOAN_AND_INT = (
            ('0', 'Choose One'),
            ('yes', 'Yes'),
            ('no', 'No')
        )
        OTHER_DED = (
            ('0', 'Choose One'),
            ('yes', 'Yes'),
            ('no', 'No')
        )
        model = ECALAdvance
        fields = ('name', 'date', 'basic_sal', 'housing_all', 'transport_all', 'upfront_all', 'other_all', 'clothing_all',
                  'car_elements', 'rent_elements', 'benefit_in_kind', 'emp_ssf', 'reg_pen', 'reg_pen_amt', 'prov_fund', 'prov_fund_amt',
                  'nr_prov_fund', 'nr_prov_fund_amt', 'pf_employer_rate', 'nr_reg_pen', 'nr_reg_pen_amt', 'mortgage_int',
                  'mortgage_int_amt', 'loan_and_int', 'loan_and_int_amt', 'other_ded', 'other_ded_amt',)

        widgets = {
            # 'user': forms.TextInput(attrs={'id': 'user', 'placeholder': 'user name', 'type':'hidden'})
            'car_elements': forms.Select(choices=CAR_ELEMENTS),
            'rent_elements': forms.Select(choices=RENT_ELEMENTS),
            'emp_ssf': forms.Select(choices=EMP_SSF),
            'reg_pen': forms.Select(choices=REG_PEN),
            'prov_fund': forms.Select(choices=PROV_FUND),
            'nr_prov_fund': forms.Select(choices=NR_PROV_FUND),
            'nr_reg_pen': forms.Select(choices=NR_REG_PEN),
            'mortgage_int': forms.Select(choices=MORTGAGE_INT),
            'loan_and_int': forms.Select(choices=LOAN_AND_INT),
            'other_ded': forms.Select(choices=OTHER_DED),
        }


class PayeBasicForm (forms.ModelForm):
    class Meta:
        model = ECALBasic
        fields = ('basic_name', 'basic_date', 'basic_basic_sal', 'basic_housing_all',
                  'basic_transport_all', 'basic_upfront_all', 'basic_other_all', 'clothing_all', 'over_time')
