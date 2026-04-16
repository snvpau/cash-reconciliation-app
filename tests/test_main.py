from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)

def test_corte():
    response = client.post (
        "/corte-caja",
        json = {
            "fondo_inicial" : 1000,
            "venta_total" : 8000,
            "total_tarjeta" : 3000,
            "otros_ingresos_efectivo" : 200,
            "gastos_efectivo" : 500,
            "gastos_tarjeta" : 300,
            "denominaciones" : {
                "1000" : 2,
                "500" : 1,
                "200" : 3  ,
                "100" : 4
            }
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["estado"] == "Faltante"

def test_corteinvalido_tarjetamayor():
    response = client.post(
        "/corte-caja",
        json={
            "fondo_inicial": 1000,
            "venta_total": 2000,
            "total_tarjeta": 3000,
            "otros_ingresos_efectivo": 200,
            "gastos_efectivo": 500,
            "gastos_tarjeta": 300,
            "denominaciones": {
                "1000": 2
            }
        }
    )

    assert response.status_code == 400

    data = response.json()
    assert data["detail"] == "Total tarjeta no puede ser mayor que venta total"
    