from playwright.sync_api import sync_playwright
from time import sleep as s
import pandas as  pd

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)    
   
    context = browser.new_context(
        geolocation={"longitude": -22.06355585266077, "latitude": -47.878786595982284},
        permissions=["geolocation"]        
    )

    page2 = context.new_page()
  
    def login():
        
        # //div/div[2]/div/div/form/div/div/div/div/div[2]/div[2]/span/div/div/div/div/div/div/div/div/div/div/div/a[2]/div
        agenciaBT = 'Soy/Sou AGENCIA'
        userName  = '//div[2]/div/div[2]/form/div/div/div/div[1]/div[2]/div[2]/span/div/div/div/div/div/div/div/div/div/div/div[1]/div/input'   
        userPass  = '//div[2]/div/div[2]/form/div/div/div/div[1]/div[2]/div[2]/span/div/div/div/div/div/div/div/div/div/div/div[2]/div[1]/div/input'

        page1 = context.new_page()
        page1.bring_to_front()
        page1.goto("https://envios.adminml.com/logistics/service-center/inventory")
    
        page1.get_by_text(agenciaBT).click()
        s(2)
        page1.locator(userName).fill("ext_balua")    
        s(1)
        page1.locator(userPass).fill("Ceva@2025###")
        s(1)
        page1.locator(userPass).press("Enter")

    
   
   
   


    s(10)  

    
    context.close()
    browser.close()


