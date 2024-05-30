let ctx = document.getElementById("chart").getContext("2d");
 
fetch(`/api/canvas/book-borrower-count/${book_id}`)
.then(response => response.json())
.then(data => {
    let data_value = Object.values(data)
    
    let chart = new Chart(ctx, {
        type: "line",
        data: {
        labels: Object.keys(data),
        datasets: [
            {
            label: 'My First Dataset',
            data: data_value,
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
            }
        ]
        },
        options: {
        title: {
            text: "Number of movies per genre",
            display: true
        }
        }
    });
})
.catch(error => console.error("Error:", error));