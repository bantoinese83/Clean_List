// Function to update the analysis display
const updateAnalysis = (analysis) => {
    // Replace newline characters with HTML line breaks for proper display
    const analysisElement = document.getElementById("analysis");
    analysisElement.innerHTML = analysis.replace(/\n/g, '<br>');
}

// Function to handle form submission
const handleFormSubmit = (e) => {
    e.preventDefault();

    // Show the ghost loading progress bar
    const progressElement = document.getElementById('progress');
    progressElement.classList.remove('d-none');

    // Submit the form using AJAX
    const formData = new FormData(e.target);
    fetch(e.target.action, {
        method: e.target.method,
        body: formData
    })
        .then(response => response.json())
        .then(data => {

            // Hide the ghost loading progress bar
            progressElement.classList.add('d-none');

            // Extract the desired content from the response
            const content = data.choices[0].message.content;

            // Update the analysis display
            updateAnalysis(content);
        })
        .catch(error => console.error('Error:', error));
}

// Function to handle file input change
const handleFileInputChange = (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const previewElement = document.getElementById('preview');
            previewElement.src = e.target.result;
            previewElement.style.display = 'block';
        };
        reader.onerror = (error) => console.error('Error:', error);
        reader.readAsDataURL(file);
    }
}

// Add event listeners
document.getElementById('upload-form').addEventListener('submit', handleFormSubmit);
document.getElementById('file-input').addEventListener('change', handleFileInputChange);