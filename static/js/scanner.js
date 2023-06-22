<<<<<<< HEAD


const barcodeInput = document.getElementById("barcode-input");
let scannedBarcodes = []; 

let inventory = {
    
}

barcodeInput.addEventListener("keydown", function(event) {
  // check if the input came from the scanner
  if (event.keyCode === 13) {
    event.preventDefault();
    // get the scanned barcode value
    let rawScannedBarcode = barcodeInput.value; 
    const scannedBarcode = rawScannedBarcode.slice(2);

    fetch('/barcode', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify({scannedBarcode})
    })
    .then(response => {
        console.log(response); 
        barcodeInput.value = ''; 
        barcodeInput.focus(); 
    })
    .catch(error => {
        console.error(error);
        alert('An error has occurred while saving the barcode'); 
    });


    scannedBarcodes.push(scannedBarcode);

    // do something with the scanned barcode, such as display it on the page
    console.log(`Scanned Barcode: ${scannedBarcode}`);

    barcodeInput.value = "";
  }
});
=======
let barcode = ''; 
        let interval; 
        document.addEventListener('keydown', evt =>{
            if(interval){
                clearInterval(interval);
            }
            if(evt.key == "Enter"){
                if(barcode){
                    handleBarcode(barcode);
                }
            barcode = ''; 
            return;
            }
            if(evt.key != 'Shift'){
                barcode += evt.key; 
            }
            interval = setInterval(() => barcode = '', 20);
        });

        function handleBarcode(scanned_barcode){
            document.querySelector('#last-barcode').innerHTML = scanned_barcode;
        }
>>>>>>> parent of 2edb5f1 (Initial commit)
