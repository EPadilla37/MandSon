function updateRowClass() {
    var rows = document.getElementsByTagName('tr');
    for (var i = 0; i < rows.length; i++) {
      var quantityCell = rows[i].getElementsByTagName('td')[1];
      var quantity = parseInt(quantityCell.textContent);
      
      rows[i].classList.remove('warning'); // Remove existing classes
      rows[i].classList.remove('danger');
      
      if (quantity >= 1 && quantity <= 5) {
        rows[i].classList.add('warning'); // Add the appropriate class
      } else if (quantity <= 0) {
        rows[i].classList.add('danger');
      }
    }
  }
  
  updateRowClass();
  