document.getElementById('date').addEventListener('change', function() {
    const selectedDate = this.value;
    fetch(`/matches/${selectedDate}`)
        .then(response => response.json())
        .then(data => {
            const dropdown = document.getElementById('dropdown');
            // Vider les options existantes
            dropdown.innerHTML = '<option value="" disabled selected>Choose the day match...</option>'; // Réintroduire le placeholder
            // Ajouter les nouvelles options pour les matchs
            data.matches.forEach(match => {
                const option = document.createElement('option');
                option.value = match;
                option.textContent = match;
                dropdown.appendChild(option);
            });
        });
});

function matchSelected() {
    var dropdown = document.getElementById('dropdown');
    var teamSelection = document.getElementById('teamSelection');
    
    if(dropdown.value !== "") {
        teamSelection.style.display = "block";
    } else {
        teamSelection.style.display = "none";
    }
}

function loadStreamlit() {
    var iframe = document.getElementById('streamlitFrame');
    iframe.src = "http://localhost:8501";
    iframe.style.display = "block";
}

document.getElementById('dropdown').addEventListener('change', matchSelected);

