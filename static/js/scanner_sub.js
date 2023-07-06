$(document).ready(function() {
    let barcode = '';
    let keyEvents = 0;

    $(document).keypress(function(e) {
        let charCode = (typeof e.which === "number") ? e.which : e.keyCode;
        let charStr = String.fromCharCode(charCode);

        barcode += charStr.toUpperCase();
        keyEvents++;
    });

    setInterval(function() {
        if (keyEvents > 2 && barcode !== '') {
            $.post('/scan_sub', { barcode: barcode }, function(response) {
                console.log(response.message);
                // Handle the response as needed

                // Reload the page
                location.reload();
            });
            barcode = '';
        }
        keyEvents = 0;
    }, 500); 
});