document.addEventListener("DOMContentLoaded", function() {

    const form = document.getElementById("cashCutForm");
    const button = document.getElementById("calculateBtn");
    const historyButton = document.getElementById("loadHistoryBtn");

    function cargarUtilidadMensual() {
        fetch("http://127.0.0.1:8000/utilidad-mensual")
            .then(response => response.json())
            .then(data => {
                document.getElementById("utilidadMensual").innerText = `Utilidad mensual: $${data.total}`;
            })
            .catch(error => {
                console.error("Error cargando utilidad mensual:", error);
            });
    }

    cargarUtilidadMensual();

    function cargarTotalUtilidad() {
        fetch("http://127.0.0.1:8000/total-utilidad")
            .then(response => response.json())
            .then(data => {
                document.getElementById("totalUtilidad").innerText = `Utilidad total: $${data.total}`;
            })
            .catch(error => {
                console.error("Error cargando utilidad total:", error);
            });
    }

    cargarTotalUtilidad();

    form.addEventListener("submit", function(event) {
        event.preventDefault();
    });

    button.addEventListener("click", function() {

        const fondo = Number(document.getElementById("fondo_inicial").value);
        const venta = Number(document.getElementById("venta_total").value);
        const tarjeta = Number(document.getElementById("total_tarjeta").value);
        const otrosIngresosEfectivo = Number(document.getElementById("otros_ingresos_efectivo").value);
        const gastosEfectivo = Number(document.getElementById("gastos_efectivo").value);
        const gastosTarjeta = Number(document.getElementById("gastos_tarjeta").value);
        const d1000 = Number(document.getElementById("d1000").value);
        const d500 = Number(document.getElementById("d500").value);
        const d200 = Number(document.getElementById("d200").value);
        const d100 = Number(document.getElementById("d100").value);
        const d50 = Number(document.getElementById("d50").value);
        const d20 = Number(document.getElementById("d20").value);
        const d10 = Number(document.getElementById("d10").value);
        const d5 = Number(document.getElementById("d5").value);
        const d2 = Number(document.getElementById("d2").value);
        const d1 = Number(document.getElementById("d1").value);

        const denominaciones = {
            "1000": d1000,
            "500": d500,
            "200": d200,
            "100": d100,
            "50": d50,
            "20": d20,
            "10": d10,
            "5": d5,
            "2": d2,
            "1": d1
     };

    const corte = {
        fondo_inicial: fondo,
        venta_total: venta,
        total_tarjeta: tarjeta,
        otros_ingresos_efectivo: otrosIngresosEfectivo,
        gastos_efectivo: gastosEfectivo,
        gastos_tarjeta: gastosTarjeta,
        denominaciones: denominaciones
    };

    if (venta < tarjeta) {
    alert("El total de tarjeta no puede ser mayor a la venta total");
    return;
    }
    
    fetch("http://127.0.0.1:8000/corte-caja", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(corte)
    })
        .then(response => response.json())
        .then(data => {
            console.log("Respuesta del backend:", data);

            const results = document.getElementById("results");

            results.innerHTML = `
                <div class="result-box">
                    <span>Estado</span>
                    <strong>${data.estado}</strong>
                </div>

                <div class="result-box">
                    <span>Mensaje</span>
                    <strong>${data.mensaje}</strong>
                </div>

                <div class="result-box">
                    <span>Efectivo contado</span>
                    <strong>${data.efectivo_contado}</strong>
                </div>

                <div class="result-box">
                    <span>Efectivo esperado</span>
                    <strong>$${data.efectivo_esperado}</strong>
                </div>

                <div class="result-box">
                    <span>Diferencia</span>
                    <strong>$${data.diff}</strong>
                </div>

                <div class="result-box">
                    <span>Utilidad estimada</span>
                    <strong>$${data.utilidad}</strong>
                </div>

                <div class="result-box">
                    <span>Guardado en base de datos</span>
                    <strong>${data.guardado ? "Sí" : "No"}</strong>
                </div>
            `;  

            cargarUtilidadMensual();
        })
        .catch(error => {
            console.error("Error:", error);
        });

    });

    historyButton.addEventListener("click", function() {
        fetch("http://127.0.0.1:8000/historial")
        .then(response => response.json())
        .then(data => {
            const history = document.getElementById("history");

            if (data.length === 0) {
                history.innerHTML = `
                    <div class="result-box">
                        <span>No hay cortes registrados</span>
                        </div>
                    `;  
                return;
            }

            let historyHTML = "";

            data.forEach(corte => {
                historyHTML += `
                    <div class="result-box">
                        <span>${corte.fecha}</span>
                        <strong>${corte.estado}</strong>
                        <p>venta total: $${corte.venta_total}</p>
                        <p>Utilidad: $${corte.utilidad}</p>
                        <p>Diferencia: $${corte.diff}</p>
                    </div>
                `;
            });

            history.innerHTML = historyHTML;
        })
        .catch(error => {
            console.error("Error cargando historial:", error);
        });

    });

});


