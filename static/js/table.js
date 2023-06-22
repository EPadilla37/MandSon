class BarcodeTable {
    constructor(tableId) {
      this.tableId = tableId;
      this.tableElement = document.getElementById(tableId);
      this.fetchBarcodes();
    }
  
    fetchBarcodes() {
      fetch('/barcodes')
        .then(response => response.json())
        .then(data => {
          console.log(data);
          this.populateTable(data);
        })
        .catch(error => {
          console.error(error);
          alert('An error has occurred while fetching the barcodes');
        });
    }
  
    populateTable(barcodes) {
      // Create the table rows
      let rows = '';
      for (let i = 0; i < barcodes.length; i++) {
        const barcode = barcodes[i];
        rows += `
          <tr>
            <td>${barcode.id}</td>
            <td>${barcode.barcode}</td>
            <td>${barcode.timestamp}</td>
          </tr>
        `;
      }
  
      // Add the rows to the table
      const tbody = this.tableElement.querySelector('tbody');
      tbody.innerHTML = rows;
    }
  }
  
  window.addEventListener('DOMContentLoaded', () => {
    const barcodeTable = new BarcodeTable('barcode-table');
  });
  