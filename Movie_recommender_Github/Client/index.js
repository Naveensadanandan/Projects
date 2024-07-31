document.getElementById('recommend-button').addEventListener('click', async () => {
    const movieName = document.getElementById('movie-input').value;
    const recommendationsContainer = document.getElementById('recommendations');
    recommendationsContainer.innerHTML = ''; // Clear previous recommendations

    if (movieName) {
        try {
            // Fetch movie details and recommendations from Flask server
            const formData = new FormData();
            formData.append('title', movieName);

            const response = await fetch('http://127.0.0.1:5000/recommend', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (data.recommended_movies) {
                displayMovieDetails(movieName);
                displayRecommendations(data.recommended_movies);
            } else {
                recommendationsContainer.innerHTML = '<p>No recommendations found. Try another movie.</p>';
            }
        } catch (error) {
            console.error('Error fetching recommendations:', error);
            recommendationsContainer.innerHTML = '<p>Error fetching recommendations. Please try again later.</p>';
        }
    }
});

function displayMovieDetails(title) {
    // Assuming you want to display the searched movie title
    const detailsDiv = document.createElement('div');
    detailsDiv.innerHTML = `
        <h2>Movie Details</h2>
        <p><strong>Title:</strong> ${title}</p>
    `;
    document.getElementById('recommendations').appendChild(detailsDiv);
}

function displayRecommendations(recommendations) {
    const recommendationsDiv = document.createElement('div');
    recommendationsDiv.innerHTML = '<h2>Recommended Movies</h2>';
    
    recommendations.forEach(movie => {
        const movieDiv = document.createElement('div');
        movieDiv.innerHTML = `
            <p><strong>Title:</strong> ${movie}</p>
        `;
        recommendationsDiv.appendChild(movieDiv);
    });

    document.getElementById('recommendations').appendChild(recommendationsDiv);
}
