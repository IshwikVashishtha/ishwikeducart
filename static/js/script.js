document.getElementById('suggestion-box').addEventListener('submit', function(event) {
  event.preventDefault();

  const suggestion = document.getElementById('suggestion').value;

  if (suggestion.trim() === '') {
    alert('Please enter a suggestion.');
    return;
  }


  alert('Thank you for your suggestion!');
});

