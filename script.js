document.getElementById('suggestion-box').addEventListener('submit', function(event) {
  event.preventDefault();

  const suggestion = document.getElementById('suggestion').value;

  if (suggestion.trim() === '') {
    alert('Please enter a suggestion.');
    return;
  }

  // You can add your code here to handle the form submission.
  // For example, you could send the suggestion to a server.
  alert('Thank you for your suggestion!');
});

