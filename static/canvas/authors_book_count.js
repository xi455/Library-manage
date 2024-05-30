let ctx = document.getElementById("chart").getContext("2d");

fetch("/api/canvas/authors/")
   .then(response => response.json())
   .then(data => {
      let chart = new Chart(ctx, {
         type: "bar",
         data: {
          labels: Object.keys(data),
          datasets: [
               {
               label: "Number of movies",
               backgroundColor: "#79AEC8",
               borderColor: "#417690",
               data: Object.values(data),
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