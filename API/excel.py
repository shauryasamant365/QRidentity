from openpyxl import Workbook
import openpyxl, os

# Give the location of the file
path = f"{os.getcwd()}\\API\\attendance.xlsx"
 
# To open the workbook
# workbook object is created
wb_obj = openpyxl.load_workbook(path)

workbook = Workbook()
sheet = workbook.active
sheet["A4"] = "1"
sheet["B4"] = "Shaurya Samir Samant"
sheet["C4"] = "789"
workbook.save(path)