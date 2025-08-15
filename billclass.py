
class BillData:
    bill_no = None
    bill_amt = None
    bill_date = None
    bill_dop = None

    def __init__(self, bill_row):
        self.set_bill_data(bill_row)

    def set_bill_data(self, bill_row):
        columns   = bill_row.find_all('td')
        self.set_bill_no(columns[0].get_text().strip())
        self.set_bill_amt(columns[1].get_text().strip())
        self.set_bill_date(columns[2].get_text().strip())
        self.set_bill_dop(columns[3].get_text().strip())

    def get_bill_data_dict(self):
        return {
            "bill_no": self.bill_no,
            "bill_amt": self.bill_amt,
            "bill_date": self.bill_date,
            "bill_dop": self.bill_dop
        }

    def set_bill_no(self, bill_no):
        self.bill_no =  bill_no.replace("Bill No.", "").replace("\n", "").replace(":", "").strip()

    def set_bill_amt(self, bill_amt):
        self.bill_amt = bill_amt.replace("Bill Amount", "").replace("\n", "").replace(":", "").strip()

    def set_bill_date(self, bill_date):
        self.bill_date = bill_date.replace("Bill Date", "").replace("\n", "").replace(":", "").strip()

    def set_bill_dop(self, bill_dop):
        self.bill_dop = bill_dop.replace("Date of Payment", "").replace("\n", "").replace(":", "").strip()


class MaterialData:
    material = None
    unit_price = None
    quantity = None
    amount = None

    def __init__(self, material_value_row):
        self.set_material_data(material_value_row)

    def set_material_data(self, material_value_row):
        columns = material_value_row.find_all('td')
        self.material = columns[0].get_text().strip()
        self.unit_price = columns[1].get_text().strip()
        self.quantity = columns[2].get_text().strip()
        self.amount = columns[3].get_text().strip()

    def get_material_data_dict(self):
        return {
            "material": self.material,
            "unit_price": self.unit_price,
            "quantity": self.quantity,
            "amount": self.amount
        }


class VendorData(BillData, MaterialData):

    vendor_name = None
    fin_year = None

    def __init__(self, vname, vendor_row, bill_row, material_value_row):
        self.set_vendor_data(vname, vendor_row, bill_row, material_value_row)


    def set_fin_year(self, vendor_row):
        columns = vendor_row.find_all('td')
        fyear = columns[1].get_text().strip()
        fy = fyear.replace("Financial Year", "").replace("\n", "").replace(":", "").strip()
        self.fin_year = fy


    def set_vendor_data(self, vname, vendor_row, bill_row, material_value_row):
        self.vendor_name = vname
        self.set_fin_year(vendor_row)
        self.set_bill_data(bill_row)
        self.set_material_data(material_value_row)


    def get_data_dict(self):
        data_dict = {
            "vendor_name": self.vendor_name,
            "fin_year": self.fin_year
        }
        data_dict.update(self.get_bill_data_dict())
        data_dict.update(self.get_material_data_dict())
        return data_dict
