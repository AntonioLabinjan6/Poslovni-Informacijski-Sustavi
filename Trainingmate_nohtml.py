#PROVAT INSTALIRAT POSTMAN ZA VIDIT DALI DELA BACKEND DOBRO. FORŠI SMANJIT BROJ FUNKCIJA :)
# STAVIT KOD NA GITHUB I PROSLJEDIT LINK PROFESORICI
#MAKNUT OVE MOJE AUTISTIČNE KOMENTARE

# SADA JE STVARNO SVE OKEJ; JEDINO FALI HTML :)

# U SVAKI APP ROUTE TREBA DODAT ODGOVARAJUĆI HTML TEMPLATE

from flask import Flask, request, make_response, jsonify, render_template, url_for, redirect
from pony import orm
import random

DB = orm.Database()

app = Flask(__name__)

class Exercise(DB.Entity):
    exercise_name = orm.Required(str)
    exercise_calories = orm.Required(float)
    exercise_duration = orm.Required(int)
    exercise_intensity = orm.Required(str)
    
class Meal(DB.Entity):
    meal_name = orm.Required(str)
    meal_calories = orm.Required(str)
    meal_number = orm.Required(int)
    meal_category = orm.Optional(str) #vegetarijanski, veganski, bezglutenski, proteinski...
    meal_location = orm.Optional(str) # posao, kuća, birtija

DB.bind(provider="sqlite", filename="database.sqlite", create_db=True)
DB.generate_mapping(create_tables=True)

@app.route("/", methods=["GET"])   
def home():
     return make_response(render_template("index.html"),200)
#PROBLEM JE U OVOJ RUTI GORE

def add_exercise(json_request):
    try:
        exercise_name = json_request["exercise_name"]
        exercise_calories = json_request["exercise_calories"]
        exercise_duration = json_request["exercise_duration"]
        exercise_intensity = json_request["exercise_intensity", None]
        
        with orm.db_session:
            Exercise(exercise_name=exercise_name, exercise_calories=exercise_calories, exercise_duration=exercise_duration, exercise_intensity=exercise_intensity)
            
        response = {"response": "Success"}
        return response
    except Exception as e:
        return{"response": "Fail","error":str(e)}
    
def get_exercises():
    try:
        with orm.db_session:
            db_querry = orm.select(x for x in Exercise)[:]
            results_list = []
            for r in db_querry:
                results_list.append(r.to_dict())
            response = {"response":"Success", "data":results_list}
            return response
    except Exception as e:
        return{"response":"Fail", "error":str(e)}
    
def get_exercise(querry_string):
    try:
        with orm.db_session:
            result = orm.select(x for x in Exercise if x.exercise_name == querry_string["exercise_name"])[:][0]
            result = result.to_dict()
            response = {"response":"Success", "data":result}
            return response
    except Exception as e:
        return {"response": "Fail", "error":str(e)}

def update_exercise(querry_string, json_request):
    try:
        with orm.db_session:
            to_update = orm.select(x for x in Exercise if x.exercise_name == querry_string["exercise_name"])[:][0]
            to_update.set(**json_request)    
            response={"response":"Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error":str(e)}
    
def delete_exercise(querry_string):
    try:
        with orm.db_session:
            to_delete = orm.select(x for x in Exercise if x.exercise_name == querry_string["exercise"])[:][0]
            to_delete.delete()
            response={"response":"Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error":str(e)}


def add_meal(json_request):
    try: 
        meal_name = json_request["meal_name"]
        meal_calories = json_request["meal_calories"]
        meal_number = json_request["meal_number"]
        meal_category = json_request["meal_category"] #vegetarijanski, veganski, bezglutenski, proteinski...
        meal_location = json_request["meal_location"] # posao, kuća...

        with orm.db_session:
            Meal(meal_name=meal_name, meal_calories=meal_calories, meal_number=meal_number, meal_category=meal_category, meal_location=meal_location)
            response = {"response":"Success"}
            return response
    except Exception as e:
        return {"response":"Fail", "error":str(e)}
    
def get_meals():
    try:
        with orm.db_session:
            db_querry = orm.select(x for x in Meal)[:]
            results_list = []
            for r in db_querry:
             results_list.append(r.to_dict())
            response = {"response":"Success", "data":results_list}
            return response
    except Exception as e:
        return {"response":"Fail", "error":str(e)}

    
def get_meal(querry_string):
    try:
        with orm.db_session:
            result = orm.select(x for x in Meal if x.meal_name == querry_string["meal"])[:][0]
            result = result.to_dict()
            response = {"response":"Success", "data": result}
            return response
    except Exception as e:
        return {"response": "Fail", "error":str(e)}
    
def update_meal(querry_string, json_request):
    try:
        with orm.db_session:
            to_update = orm.select(x for x in Meal if x.meal_name == querry_string["meal_name"])[:][0]
            to_update.set(**json_request)
            response= {"response":"Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error":str(e)}
    
def delete_meal(querry_string):
    try:
        with orm.db_session:
            to_delete = orm.select(x for x in Meal if x.meal_name == querry_string["mealName"])[:][0]
            to_delete.delete()
            response= {"response": "Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error":str(e)}
    

@app.route("/exercise/dodaj", methods=["POST"])
def dodaj_vjezbu():
    if request.method == "POST":
        try:
            json_request = request.get_json()
            if json_request is None:
                raise ValueError("Invalid JSON data")

            for key, value in json_request.items():
                if value == "":
                    json_request[key] = None

            response = add_exercise(json_request)

            if response["response"] == "Success":
                return make_response(render_template("dodaj_vjezbu.html"), 200) 
        except Exception as e:
            response = {"response": str(e)}
            return make_response(jsonify(response), 400)

@app.route("/exercise/vrati", methods=["GET"])
def vrati_vjezbu():
    response = get_exercises()
    if response["response"] == "Success":
        return make_response(render_template("vrati_vjezbu.html", data=response["data"]), 200)
    else:
        return make_response(jsonify(response), 400)
@app.route("/exercise/obrisi", methods=["DELETE"])
def obrisi_vjezbu():
    if request.args:
        response = delete_exercise(request.args)
        if response["response"]== "Success":
            return make_response(jsonify(response),200)
        return make_response(jsonify(response),400)
    else:
        response={"response":"Querry string missing"}
        return make_response(jsonify(response),400)
    
@app.route("/exercise/izmjeni", methods=["PATCH"])
def izmjeni_vjezbu():
    try:
        json_request = request.get_json()
        if json_request is None:
            raise ValueError("Invalid JSON data")
    except Exception as e:
        response = {"response": str(e)}
        return make_response(jsonify(response), 400)

    if json_request:
        response = update_exercise(request.args, json_request)
        if response["response"] == "Success":
            return make_response(render_template("izmjeni_vjezbu.html", success=True), 200)
        else:
            return make_response(render_template("izmjeni_vjezbu.html", error=True), 400)
    else:
        response = {"response": "JSON data missing"}
        return make_response(jsonify(response), 400)
        
@app.route("/meal/dodaj", methods=["POST"])
def dodaj_obrok():
    if request.method == "POST":
        try:
            json_request = request.get_json()
            if json_request is None:
                raise ValueError("Invalid JSON data")

            for key, value in json_request.items():
                if value == "":
                    json_request[key] = None
        except Exception as e:
            response = {"response": str(e)}
            return make_response(jsonify(response), 400)

        response = add_meal(json_request)

        if response["response"] == "Success":
            return make_response(render_template("dodaj_obrok.html"), 200)
        else:
            return make_response(jsonify(response), 400)
    else:
        return make_response(render_template("dodaj_obrok.html"), 200)

@app.route("/meal/vrati", methods=["GET"])
def vrati_obrok():
    response = get_meals()
    if response["response"] == "Success":
        return make_response(render_template("vrati_obrok.html", data=response["data"]),200)
    else:
        return make_response(jsonify(response),400)

@app.route("/meal/obrisi", methods=["DELETE"])
def obrisi_obrok():
    if request.args:
        response = delete_meal(request.args)
        if response["response"]== "Success":
            return make_response(jsonify(response),200)
        return make_response(jsonify(response),400)
    else:
        response={"response": "Querry string missing"}
        return make_response(jsonify(response),400)

@app.route("/meal/izmjeni", methods=["PATCH"])
def izmjeni_obrok():
    try:
        json_request = request.get_json()
        if json_request is None:
            raise ValueError("Invalid JSON data")
    except Exception as e:
        response = {"response": str(e)}
        return make_response(jsonify(response), 400)

    if json_request:
        response = update_meal(request.args, json_request)
        if response["response"] == "Success":
            return make_response(render_template("izmjeni_obrok.html", success=True), 200)
        else:
            return make_response(render_template("izmjeni_obrok.html", error=True), 400)
    else:
        response = {"response": "JSON data missing"}
        return make_response(jsonify(response), 400)

                                                                #BONUS FUNKCIJE

#OVO SLUŽI DA IZRAČUNAMO UKUPNE POTROŠENE KALORIJE
@app.route("/exercise/ukupno-kalorija", methods=["GET"])
def calculate_total_calories_burnt():
    exercises = Exercise.select()
    burnt_calories = sum(exercise.exercise_calories for exercise in exercises)

    return jsonify({'total_calories': burnt_calories})

#OVO SLUŽI DA IZRAČUNAMO UKUPNO TRAJANJE SVIH VJEŽBI
@app.route("/exercise/ukupno-trajanje", methods=["GET"])
def calculate_total_duration():
    exercises = Exercise.select()
    total_duration = sum(exercise.exercise_duration for exercise in exercises)

    return jsonify({'total_duration': total_duration})

#OVO SLUŽI DA IZRAČUNAMO UKUPNE UNESENE KALORIJE
@app.route("/meal/ukupne-unesene-kalorije", methods=["GET"])
def calculate_total_calories_consumed():
    meals = Meal.select()
    consumed_calories = sum(meal.meal_calories for meal in meals)

    return jsonify({'total_calories': consumed_calories})

#OVO SLUŽI DA IZRAČUNAMO JE LI OSOBA U BALANSU KALORIJA
@app.route("/balans-kalorija")
def calculate_caloric_balance():
    meals_calories = DB.session.query(DB.func.sum(Meal.meal_calories)).scalar() or 0
    exercises_calories = DB.session.query(DB.func.sum(Exercise.exercise_calories)).scalar() or 0
    caloric_balance = meals_calories - exercises_calories

    if caloric_balance > 0:
        return "Osoba je u plusu"
    elif caloric_balance < 0:
        return "Osoba je u minusu"
    else:
        return "Osoba je u balansu"

#OVO SLUŽI DA ISPIŠEMO PROSJEK KALORIJA PO OBROKU    
@app.route("/meal/prosjek-kalorija-po-obroku", methods=["GET"])
def calculate_average_calories_per_meal():
    def average_calories_per_meal():
        meals = Meal.select()
        total_calories = sum(meal.meal_calories for meal in meals)
        total_meals = len(meals)
        
        if total_meals > 0:
            average_calories = total_calories / total_meals
        else:
            average_calories = 0
        
        return jsonify({'average_calories': average_calories})
    
    return average_calories_per_meal()

#OVO SLUŽI DA ISPIŠEMO PROSJEČNE KALORIJE PO VJEŽBI
@app.route("/exercise/prosjek-kalorija-po-vjezbi", methods=["GET"])
def calculate_average_calories_per_exercise():
    def average_calories_per_exercise():
        exercises = Exercise.select()
        total_calories = sum(exercise.exercise_calories for exercise in exercises)
        total_exercises = len(exercises)
        
        if total_exercises > 0:
            average_calories = total_calories / total_exercises
        else:
            average_calories = 0
        
        return jsonify({'average_calories': average_calories})
    
    return average_calories_per_exercise()

#OVO SLUŽI DA FILTIRAMO VJEŽBE KOJE TROŠE VIŠE KALORIJA OD PROSJEKA
@app.route("/exercise/filter-by-calories", methods=["GET"])
def filter_exercises_by_calories():
    total_calories = sum(exercise.exercise_calories for exercise in Exercise.select())
    total_exercises = len(Exercise.select())
    average_calories = total_calories / total_exercises if total_exercises > 0 else 0

    filtered_exercises = [exercise for exercise in Exercise.select() if exercise.exercise_calories > average_calories]

    filtered_exercises_dict = [exercise.to_dict() for exercise in filtered_exercises]

    return jsonify({'filtered_exercises': filtered_exercises_dict})

#OVO SLUŽI DA FILTRIRAMO OBROKE KOJI IMAJU MANJE KALORIJA OD PROSJEKA
@app.route("/meal/filter-by-calories", methods = ["GET"])
def filter_meals_by_calories():
    total_calories = sum(meal.meal_calories for meal in Meal.select())
    total_meals = len(Meal.select())
    average_calories = total_calories / total_meals if total_meals > 0 else 0

    filtered_meals = [meal for meal in Meal.select() if meal.meal_calories < average_calories]

    filtered_meals_dict = [meal.to_dict() for meal in filtered_meals]

    return jsonify({'filtered_meals': filtered_meals_dict})

#OVO SLUŽI ZA DOHVAĆANJE UKUPNOG BROJA VJEŽBI
@app.route("/exercise/ukupan-broj-vjezbi", methods=["GET"])
@orm.db_session
def get_total_exercises():
    try:
        total_exercises = orm.select(orm.count() for x in Exercise)[:]
        response = {"response": "Success", "total_exercises": total_exercises[0]}
        return make_response(jsonify(response), 200)
    except Exception as e:
        response = {"response": "Fail", "error": str(e)}
        return make_response(jsonify(response), 400)

#OVO SLUŽI ZA DOHVAĆANJE UKUPNOG BROJA OBROKA

@app.route("/exercise/ukupan-broj-obroka", methods=["GET"])
@orm.db_session
def get_total_meals():
    try:
        total_meals = orm.select(orm.count() for x in Meal)[:]
        response = {"response": "Success", "total_meals": total_meals[0]}
        return make_response(jsonify(response), 200)
    except Exception as e:
        response = {"response": "Fail", "error": str(e)}
        return make_response(jsonify(response), 400)

#OVO SLUŽI ZA DOHVAĆANJE NASUMIČNE VJEŽBE
@app.route("/exercise/random", methods=["GET"])
def get_random_exercise():
    try:
        with orm.db_session:
            exercises = orm.select(x for x in Exercise)[:]
            if exercises:
                random_exercise = random.choice(exercises).to_dict()
                response = {"response": "Success", "data": random_exercise}
            else:
                response = {"response": "No exercises found"}
            return make_response(jsonify(response), 200)
    except Exception as e:
        response = {"response": "Fail", "error": str(e)}
        return make_response(jsonify(response), 400)

#OVO SLUŽI ZA DOHVAĆANJE NASUMIČNOG OBROKA
@app.route("/meal/random", methods=["GET"])
def get_random_meal():
    try:
        with orm.db_session:
            meals = orm.select(x for x in Meal)[:]
            if meals:
                random_meal = random.choice(meals).to_dict()
                response = {"response": "Success", "data": random_meal}
            else:
                response = {"response": "No meals found"}
            return make_response(jsonify(response), 200)
    except Exception as e:
        response = {"response": "Fail", "error": str(e)}
        return make_response(jsonify(response), 400)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

#TREBA NAN HTML ZA DELETE I UPDATE
##ZA DELETE FUNKCIONALNOSTI NE BI BILO LOŠE NAPRAVIT NEKU PORUKU POTVRDE, TIPA: "ŽELITE LI SIGURNO OBRISATI VJEŽBU?"
# ZA OVE NEKE NAPREDNE STVARI ĆE TRIBAT UBACIT MALO JS-a :)
# DA BI SE TO SVE LIPO VIDILO, TRIBAT ĆE UBACIT RENDERIRANJE TEMPLATE-a U KOD, ALI TO NI PREVELIKI PROBLEM 
# PASALO JE PO NOĆI. NE DA MI SE VIŠE PISAT PIS. GREN SE VADIT BAZE I SPA

# GRAFOVI S CHART.JS-on SE DELAJU NA FRONTENDU!!!!!!!!!!