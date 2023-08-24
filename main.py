import requests
import json
import time
import sqlite3
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


database = os.getenv("DATABASE")
user = os.getenv("USER")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")
getUrl = os.getenv("URL")

try:
    db = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cursor = db.cursor()
except (Exception, psycopg2.Error) as error:
    print("Hata:", error)


for i in range(1,160):
    url = getUrl.format(i)
    print("--------------------------------goto------------------------",url)
    r = requests.get(url, auth=('user', 'pass'))
    time.sleep(4)
    jsonData = json.loads(r.text)

    datas = jsonData.get('data' ,[])

    for data in datas:
        for key,val in data.items():
            if key == "name":
                name = val
            elif key == "desc":
                desc = val
            elif key == "slug":
                slug = val
            elif key == "pricingModel":
                pricingModel = val
            elif key == "toolTags":
                for tag in val:
                    aitag = tag
            elif key == "url":
                siteUrl = val 
            elif key == "imageSrc":
                imageSrc = val
            elif key == "src":
                src = val

        try:
            if  aitag is not None:
                selectQuery1 = f"""
                    select id from aiwebsite_category ac where ac.title = '{aitag}' order by id
                """
                cursor.execute(selectQuery1)
                categoryId =  cursor.fetchone()
                if categoryId[0] is not None:
                    categoryId =  categoryId[0]
                else:
                    categoryId=30
            else:
                categoryId =30
        except Exception:
            categoryId=30

        
        try:
            if pricingModel is not None and pricingModel != " ":
                print("pricingModel",pricingModel)
                selectQuery2 = f"""
                    select id from aiwebsite_pricing ac where ac.title = '{pricingModel}' order by id
                """
                cursor.execute(selectQuery2)
                pricingId =  cursor.fetchone()
                if pricingId is not None:
                    pricingId = pricingId[0]
                else:
                    pricingId=5
            else:
                pricingId = 5
        except Exception:
            pricingId =5
        
        insertQuery = """INSERT INTO public.aiwebsite_product
        (title, description, slug, "pricingModel_id", url, "imageSrc", src, is_active, category_id)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        values = (name, desc, slug, pricingId, siteUrl, imageSrc, src, True, categoryId)

        cursor.execute(insertQuery, values)

        # Değişiklikleri kaydet ve bağlantıyı kapat
        db.commit()


cursor.close()
db.close()