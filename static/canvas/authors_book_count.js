function ColorData() {
   let backgroundColor = [
      'rgba(255, 99, 132, 0.2)',
      'rgba(255, 159, 64, 0.2)',
      'rgba(255, 205, 86, 0.2)',
      'rgba(75, 192, 192, 0.2)',
      'rgba(54, 162, 235, 0.2)',
      'rgba(153, 102, 255, 0.2)',
      'rgba(201, 203, 207, 0.2)'
   ]

   let borderColor = [
      'rgb(255, 99, 132)',
      'rgb(255, 159, 64)',
      'rgb(255, 205, 86)',
      'rgb(75, 192, 192)',
      'rgb(54, 162, 235)',
      'rgb(153, 102, 255)',
      'rgb(201, 203, 207)'
   ]

   return [backgroundColor, borderColor]
}

let ctx = document.getElementById("chart").getContext("2d");

fetch("/api/canvas/authors/")
   .then(response => response.json())
   .then(data => {
      let [backgroundColor, borderColor] = ColorData()
      let data_value = Object.values(data)
      let backgroundColors = data_value.map((_, i) => backgroundColor[i % backgroundColor.length])
      let borderColors = data_value.map((_, i) => borderColor[i % borderColor.length])
      
      let chart = new Chart(ctx, {
         type: "bar",
         data: {
          labels: Object.keys(data),
          datasets: [
               {
               data: data,
               label: "Number of movies",
               backgroundColor: backgroundColors,
               borderColor: borderColors,
               borderWidth: 1
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