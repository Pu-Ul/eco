window.addEventListener('load', function() {
    // Obtener los resultados del almacenamiento local
    const storedResults = localStorage.getItem('carbonResults');
    if (!storedResults) {
        document.getElementById('total-footprint').textContent = "N/A";
        return; // No hay datos, no hacer nada más
    }
    
    const results = JSON.parse(storedResults);
    
    // Promedios de referencia (toneladas de CO2e/año)
    const japanAverage = 3.7;
    const chileAverage = 4.6;

    // Actualizar el card de la huella total
    document.getElementById('total-footprint').textContent = results.total;

    // Configurar la gráfica de comparación
    const comparisonCtx = document.getElementById('comparison-chart').getContext('2d');
    new Chart(comparisonCtx, {
        type: 'bar',
        data: {
            labels: ['Tu Huella', 'Promedio Japón', 'Promedio Chile'],
            datasets: [{
                label: 'Toneladas de CO₂e por Año',
                data: [results.total, japanAverage, chileAverage],
                backgroundColor: [
                    'rgba(39, 174, 96, 0.7)',  // Verde Primario
                    'rgba(231, 76, 60, 0.7)',   // Rojo (Japón)
                    'rgba(52, 152, 219, 0.7)'  // Azul (Chile)
                ],
                borderColor: [
                    'rgba(39, 174, 96, 1)',
                    'rgba(231, 76, 60, 1)',
                    'rgba(52, 152, 219, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });

    // Configurar la gráfica de desglose
    const breakdownCtx = document.getElementById('breakdown-chart').getContext('2d');
    new Chart(breakdownCtx, {
        type: 'doughnut',
        data: {
            labels: ['Alimentación', 'Transporte', 'Hogar'],
            datasets: [{
                label: 'Desglose de la Huella',
                data: [results.food, results.transport, results.home],
                backgroundColor: [
                    'rgba(241, 196, 15, 0.7)',  // Amarillo
                    'rgba(230, 126, 34, 0.7)', // Naranja
                    'rgba(142, 68, 173, 0.7)'  // Morado
                ]
            }]
        }
    });
    
    // Generar recomendaciones
    const recommendationsList = document.getElementById('recommendations-list');
    recommendationsList.innerHTML = ''; // Limpiar la lista

    if (results.food > 1.0) {
        recommendationsList.innerHTML += '<li class="list-group-item"><i class="fas fa-carrot text-warning"></i> <strong>Alimentación:</strong> Considera reducir el consumo de carne roja. Reemplazarla por pollo, pescado o vegetales una vez por semana puede hacer una gran diferencia.</li>';
    }

    if (results.transport > 1.5) {
        recommendationsList.innerHTML += '<li class="list-group-item"><i class="fas fa-bus text-info"></i> <strong>Transporte:</strong> Intenta usar más el transporte público, la bicicleta o caminar para trayectos cortos. El coche compartido también es una excelente opción.</li>';
    } else if (results.transport > 0.5) {
         recommendationsList.innerHTML += '<li class="list-group-item"><i class="fas fa-motorcycle text-info"></i> <strong>Transporte:</strong> Si usas mucho la motocicleta, asegúrate de que tenga un mantenimiento adecuado para optimizar el consumo de combustible.</li>';
    }

    if (results.home > 1.0) {
        recommendationsList.innerHTML += '<li class="list-group-item"><i class="fas fa-lightbulb text-primary"></i> <strong>Hogar:</strong> Si aún no lo has hecho, cambiar todas tus bombillas a tecnología LED puede reducir significativamente tu consumo eléctrico.</li>';
    }
    
    if (recommendationsList.innerHTML === '') {
        recommendationsList.innerHTML = '<li class="list-group-item"><i class="fas fa-check-circle text-success"></i> ¡Felicidades! Tu huella de carbono es relativamente baja. Sigue así.</li>';
    }
});