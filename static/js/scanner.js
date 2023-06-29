$(document).ready(function() {
    var barcode = '';
    var keyEvents = 0;

    $(document).keypress(function(e) {
        var charCode = (typeof e.which === "number") ? e.which : e.keyCode;
        var charStr = String.fromCharCode(charCode);

        barcode += charStr;
        keyEvents++;
    });

    setInterval(function() {
        if (keyEvents > 2 && barcode !== '') {
            $.post('/scan', { barcode: barcode }, function(response) {
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
