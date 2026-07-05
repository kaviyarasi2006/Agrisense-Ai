document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");

    if(form){

        form.addEventListener("submit", function(e){

            const farmer = document.querySelector("[name='farmerName']").value.trim();
            const crop = document.querySelector("[name='cropName']").value.trim();
            const problem = document.querySelector("[name='problemDescription']").value.trim();

            // Empty validation
            if(farmer === "" || crop === "" || problem === ""){
                alert("⚠ Please fill all the fields.");
                e.preventDefault();
                return;
            }

            // Confirmation
            const confirmSubmit = confirm("Are you sure you want to analyze this crop?");

            if(!confirmSubmit){
                e.preventDefault();
                return;
            }

            // Success Message
            alert("✅ Crop analysis submitted successfully!\nAI is analyzing your crop...");
        });

    }

});