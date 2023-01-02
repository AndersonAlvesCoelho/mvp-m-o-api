from flask import Flask, make_response, jsonify, request, json
from scripts.login_check import checkLoginBrands
from scripts.Cal_orcamento import create_plano_mensal

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/script', methods=['GET'])
def get_dados():
    return make_response(jsonify([
        {'key': "nome", 'type': "nome", 'text': "Ordenar nome ASC"},
        {'key': "-nome", 'type': "nome", 'text': "Ordenar nome DESC"},
        {'key': "documento", 'type': "documento", 'text': "Ordenar documento ASC"},
    ]))


@app.route('/login_check', methods=['POST'])
def login_check():
    res = json.loads(request.data)['stepTechnical']['access']
    for x in res:
        checkLoginBrands(x["login"], x["password"], x["brand"])

    return make_response(jsonify({'menssage': 'JSON received'}), 200)


@app.route('/cal_orcamento', methods=['POST'])
def cal_orcamento():
    data = json.loads(request.data)['stepComplementaryData']
    user_pot = float(data['kwp'])
    user_assina = 'GIGAWATT'
    user_height = data['powerPlantType']
    user_address = data['address']
    price_ratio = 1

    if (user_height == 'roof'):
        user_height = int(data['roofHeight'])
    else:
        user_height = 3

    # res = create_plano_mensal(user_pot,user_assina,  user_height, user_address, price_ratio )
    res = create_plano_mensal(user_pot, user_assina, user_height, user_address, price_ratio)
    res = json.loads(res)

    # print(create_plano_mensal(6.8,'GIGAWATT',3,'Rua padre Eustáquio, 1024, padre Eustáquio',1))


    response = app.response_class(
        response=json.dumps(res),
        mimetype='application/json'
    )
    return response

    return make_response(jsonify({'menssage': 'JSON received'}), 200)


if __name__ == '__main__':
    app.run(host="5.161.116.181", port=5000)
