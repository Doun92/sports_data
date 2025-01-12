// Téléchargement des données
const résumé_jeux = d3.csv("/data/jeux_olympiques_résumé.csv");
const résultats = d3.csv("/data/résultats.csv");
// console.log(résultats)

résultats.then(function (data) {
    // On va d'abord retirer les duplicats
    const uniqueDisciplines = Array.from(
        d3.group(data, d => `${d.discipline}`).values()
    ).map(group => group[0]);

    const disciplineCount = d3.rollup(
        uniqueDisciplines,
        group => group.length,
        d => d.discipline
    );

    // Convert the Map to an array for visualization
    const processedData = Array.from(disciplineCount, ([country, count]) => ({ country, count }));
    console.log(processedData)
    // Visualize the result
    // createBarChart(processedData);
})

// résultats.then(function(data){
//     // On va d'abord retirer les duplicats
//     const uniqueAthletes = Array.from(
//         d3.group(data, d => `${d.athlète}-${d.pays}`).values()
//     ).map(group => group[0]);

//     const countryCounts = d3.rollup(
//         uniqueAthletes,
//         group => group.length,
//         d => d.pays
//     );

//     // Convert the Map to an array for visualization
//     const processedData = Array.from(countryCounts, ([country, count]) => ({ country, count }));
//     console.log(processedData)
//     // Visualize the result
//     // createBarChart(processedData);
// })

// Création du barplot
// function createBarChart(data) {
//     const width = 800;
//     const height = 400;
//     const margin = { top: 20, right: 30, bottom: 50, left: 40 };

//     const svg = d3.select("body")
//         .append("svg")
//         .attr("width", width + margin.left + margin.right)
//         .attr("height", height + margin.top + margin.bottom)
//         .append("g")
//         .attr("transform", `translate(${margin.left},${margin.top})`);

//     // Scales
//     const x = d3.scaleBand()
//         .domain(data.map(d => d.country))
//         .range([0, width])
//         .padding(0.1);

//     const y = d3.scaleLinear()
//         .domain([0, d3.max(data, d => d.count)])
//         .nice()
//         .range([height, 0]);

//     // Axes
//     svg.append("g")
//         .attr("transform", `translate(0,${height})`)
//         .call(d3.axisBottom(x))
//         .selectAll("text")
//         .attr("transform", "rotate(-45)")
//         .style("text-anchor", "end");

//     svg.append("g")
//         .call(d3.axisLeft(y));

//     // Bars
//     svg.selectAll(".bar")
//         .data(data)
//         .enter()
//         .append("rect")
//         .attr("class", "bar")
//         .attr("x", d => x(d.country))
//         .attr("y", d => y(d.count))
//         .attr("width", x.bandwidth())
//         .attr("height", d => height - y(d.count))
//         .style("fill", "steelblue");
// }