function sortTable() {
  var sortOption = document.getElementById("sort").value;
  var table = document.querySelector(".table"); 
  var rows, switching, i, x, y, shouldSwitch;
  switching = true;

  while (switching) {
    switching = false;
    rows = table.getElementsByClassName("table-row"); 
    for (i = 0; i < rows.length - 1; i++) {
      shouldSwitch = false;
      x = rows[i].querySelector("td").textContent.toLowerCase(); 
      y = rows[i + 1].querySelector("td").textContent.toLowerCase(); 

      if (
        (sortOption === "name_asc" && x > y) ||
        (sortOption === "name_desc" && x < y) ||
        (sortOption === "quantity_asc" &&
          parseInt(rows[i].querySelectorAll("td")[1].textContent) >
            parseInt(rows[i + 1].querySelectorAll("td")[1].textContent)) ||
        (sortOption === "quantity_desc" &&
          parseInt(rows[i].querySelectorAll("td")[1].textContent) <
            parseInt(rows[i + 1].querySelectorAll("td")[1].textContent))
      ) {
        shouldSwitch = true;
        break;
      }
    }

    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}
