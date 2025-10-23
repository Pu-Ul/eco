document.getElementById('carbon-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita que la página se recargue

    // Factores de emisión (toneladas de CO2e)
    const MEAT_FACTORS = [0.6, 1.5, 2.5, 3.3]; // Anual, por categoría de frecuencia
    const CAR_FACTOR_PER_KM = 0.17; // Por km
    const MOTO_FACTOR_PER_KM = 0.09; // Por km
    const PUBLIC_FACTOR_PER_KM = 0.04; // Por km
    const LED_SAVINGS = 0.4; // Ahorro anual si se usan LEDs

    // 1. Obtener valores del formulario
    const meatConsumption = parseInt(document.getElementById('meat-consumption').value);
    const kmCar = parseFloat(document.getElementById('km-car').value) || 0;
    const kmMoto = parseFloat(document.getElementById('km-moto').value) || 0;
    const kmPublic = parseFloat(document.getElementById('km-public').value) || 0;
    const ledUsage = document.querySelector('input[name="led-usage"]:checked').value;

    // 2. Calcular huella por categoría
    // Alimentación (anual)
    const foodFootprint = MEAT_FACTORS[meatConsumption];

    // Transporte (convertir km/semana a km/año y multiplicar por factor)
    const transportFootprint = ((kmCar * CAR_FACTOR_PER_KM) + (kmMoto * MOTO_FACTOR_PER_KM) + (kmPublic * PUBLIC_FACTOR_PER_KM)) * 52;

    // Hogar (se añade una base y se resta si usan LED)
    let homeFootprint = 1.2; // Huella base promedio por consumo eléctrico sin LEDs
    if (ledUsage === "1") {
        homeFootprint -= LED_SAVINGS;
    }

    // 3. Calcular el total
    const totalFootprint = foodFootprint + transportFootprint + homeFootprint;
    
    // 4. Guardar resultados en el almacenamiento local del navegador
    const results = {
        total: totalFootprint.toFixed(2),
        food: foodFootprint.toFixed(2),
        transport: transportFootprint.toFixed(2),
        home: homeFootprint.toFixed(2)
    };

    localStorage.setItem('carbonResults', JSON.stringify(results));
    
    // 5. Redirigir al dashboard
    window.location.href = 'dashboard.html';
});