from difflib import restore
from fastapi import FastAPI

app = FastAPI()



add_city_country = []
#Utilizaremos metodos HTTP
#EndPoint para saber que la API esta activa
@app.get("/")
def health():
    return{
        "Status": 200,
        "description": "Todo ok",
        "body": {}
    }

def all_countries(countries):
    for country in range(len(countries)):
        countries[country] = countries[country].replace("\n", "")
    return countries

#EndPoint que devuelve todas las ciudades de nuesta DB
@app.get('/city')
def city():
    with open("database.txt", "r") as file:
        countries = file.readlines()
        file.close()

    all_countries(countries)

    array = []
    for country in countries:
        
        country = country.split(",")
        
        array.append({
            "id": country[0].strip(),
            "country": country[1].strip(),
            "city": country[2].strip()
        })


    array_all_countries = []
    for i in array:
        array_all_countries.append(i["city"])


    try:
        response = array_all_countries
        status = 200
        description = ""
    except:
        response= ""
        status = 400
        description = "No existe esta base de datos."


    return {
        "Status": status,
        "Description": description,
        "body" : {
            "Country" : response
        }
    }

#EndPoint en el que pasamos por parametro la ciudad y devuelve el pais.
@app.get('/oneCountry')
def oneCountry(city: str):
    with open("database.txt", "r") as file:
        countries = file.readlines()
        file.close()

    all_countries(countries)
    array = []
    for country in countries:
        
        country = country.split(",")
        
        array.append({
            "id": country[0].strip(),
            "country": country[1].strip(),
            "city": country[2].strip().lower()
        })

    for i,item in enumerate(array):
        if item["city"] == city.lower():
            array_one_country = []
            array_one_country.append(array[i]["country"])
              
        
    try:
        response = array_one_country
        status = 200
        description = ""
    except:
        response = "La ciudad no existe"
        status = 400
        description = ""

    return {
        "status": status,
        "description": description, 
        "Body": {
            "Country" : response
        }
    }

#EndPoint en el que pasamos por parametro el ID y nos retorna la ciudad y el pais.
@app.get('/oneCountryByID')
def oneCountry(id: int):
    with open("database.txt", "r") as file:
        countries = file.readlines()
        file.close()

    all_countries(countries)
    array = []
    for country in countries:
        
        country = country.split(",")
        
        array.append({
            "id": country[0],
            "country": country[1],
            "city": country[2]
        })


    for i,item in enumerate(array):
        if item["id"] == str(id):
            array_city_country = []
            array_city_country.append({
                "city": array[i]["city"],
                "country":  array[i]["country"]
                })
            break
        
        

    try:
        response = array_city_country
        status = 200
        description = ""
    except:
        response = "El ID no existe"
        status = 400
        description = ""

    return {
        "status": status,
        "description": description,
        "Body":    response
    }


#EndPoint para agregar ciudad y pais
@app.post('/addCityCountry')
def addCityCountry(city: str, country:str):
    with open("database.txt", "r") as file:
        countries = file.readlines()
        file.close()

    size_country = len(countries) + 1

    addCountry = f"{str(size_country)},{country},{city}"

    with open("database.txt", "a") as file:
        file.write(addCountry + "\n")
        file.close()

    
    try:
        status = 200
        description = "Nuevo pais y Ciudad agregados"
        addCountry = countries[0:size_country]
    except:
        status = 400
        description = "Algo salio mal"
        addCountry = "Fail"

    return {
        "status": status,
        "descripcion": description,
        "body": f"Se agrego el registo {[city, country]}"
    }

#EndPoint para eliminar 
@app.delete("/deleteCityCountry")
def deleteCityCountry(id: int):
    with open('database.txt', 'r') as file:
        countries = file.readlines()
          
        ptr = 1
        with open('database.txt', 'w') as fw:
            for line in countries:
                if ptr != (id):
                    fw.write(line)
                ptr += 1



    try:
        status = 200
        description = "Registro eliminado satisfactoriamente"
    except:
        status = 200
        description = "El id no extiste"

    return {
        "status": status,
        "description": description,
        "body": {}
    }

            
