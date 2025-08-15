from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

# hardcoded fin year due to data overload. 
# Initial plan was to create a list of all existing fin years for which work was done
# Use the list and run through the loop to collect HTML files
fin_year = "2024-2025"
# Papa only works under this district hence hardcoded
district = "MADHUBANI"

driver = webdriver.Chrome()

driver.get("https://nregastrep.nic.in/netnrega/loginframegp.aspx?salogin=Y&state_code=05")

# dict for block-panchayat list
blocks_dict = {}

# wait for page to load
time.sleep(2)

# Select state (if needed, here it's a span so no interaction)
state_text = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_lblstate").text
print("State:", state_text)

# Select Financial Year
fin_year_dropdown = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlFin"))
fin_year_dropdown.select_by_visible_text(fin_year)
time.sleep(2)

# Select District
district_dropdown = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlDistrict"))
# Madhubani is the only district we operate in
district_dropdown.select_by_visible_text(district) 
time.sleep(2)

# Gather Block names
block_dropdown = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlBlock"))
block_list = [optionblock.text for optionblock in block_dropdown.options if optionblock.text.strip() and optionblock.text.strip() != "Select Block"]
print(block_list)

# Gather panchayat list for each block
for block in block_list:
    
    block_dropdown = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlBlock"))
    block_dropdown.select_by_visible_text(block)
    time.sleep(1)

    panchayat_dropdown = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlPanchayat"))
    panchayat_list = [optionpan.text for optionpan in panchayat_dropdown.options if optionpan.text.strip() and optionpan.text.strip() != "Select Panchayat"]
    blocks_dict[block] = panchayat_list
    time.sleep(1)


"""

    block_list = ["BLOCK_1", "BLOCK_2", ... ]

    blocks_ dict = {
        "BLOCK_1": ["P1", "P2"...],      
        "BLOCK_2": ["P1", "P2"...],      
        "BLOCK_3": ["P1", "P2"...],      
    }
"""

# retrieving data
for block in block_list:
    
    #if block == block_list[5]:
    #    break
        
    for panchayat in blocks_dict[block]:
        #if panchayat == panchayat_list[5]:
            #break

        print(block,panchayat)    
        # visit again
        driver.get("https://nregastrep.nic.in/netnrega/loginframegp.aspx?salogin=Y&state_code=05")
        time.sleep(2)
        
        # select financial year
        fin_year_dropdown = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlFin"))
        fin_year_dropdown.select_by_visible_text(fin_year)
        time.sleep(2)
        
        # select district
        district_dropdown = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlDistrict"))
        district_dropdown.select_by_visible_text(district)  # This remains constant: Madhubani
        time.sleep(2)
        
        # select block 
        block_dropdown = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlBlock"))
        block_dropdown.select_by_visible_text(block)
        time.sleep(2)

        # select panchayat
        panchayat_dropdown = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlPanchayat"))
        panchayat_dropdown.select_by_visible_text(panchayat)
        time.sleep(2)
        
        # Click Proceed Button
        proceed_button = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btProceed")
        proceed_button.click()
        time.sleep(2)
        

        # on the next page - find the link and click        
        link = driver.find_element(By.LINK_TEXT, "Material Procured Report")
        link.click()
        time.sleep(5)

        # save html 
        html_content = driver.page_source

        vendor_names = ['navita enterprises', 'mithila tool kits hardware and nursery',
                'navita enterprises and nursery',
                'pallavi enterprises and nursery']
        
        # to avoid case sensitivity
        html_lower = html_content.lower()
        if any(vendor in html_lower for vendor in vendor_names):
            # Save it to a local file
            # dont have to explicitly close the file if you use with open(...) function
            with open(f"reports/{fin_year}-{block}-{panchayat}-report.html", "w", encoding="utf-8") as f:
                f.write(html_content)
            print("HTML saved successfully.")

driver.quit()