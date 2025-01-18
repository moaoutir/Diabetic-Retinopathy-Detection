document.addEventListener('DOMContentLoaded', function() {
    const uploadZone = document.getElementById('upload-zone');
    const fileInput = document.getElementById('fileInput');
    
    document.getElementById('error').style.display = 'none';
    document.getElementById('resultHolder').style.display = 'none';
    document.getElementById('divClassTable').style.display = 'none';

    uploadZone.addEventListener('click', () => {
        fileInput.click();
    });

    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });

    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('dragover');
    });

    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
    });


    fileInput.addEventListener('change', (e) => {
        const files = e.target.files;
        const formData = new FormData();

        formData.append('image', files[0]); 
        sendDataToServer(formData);
    });


    function sendDataToServer(image){
        console.log('Sending data to server:');
        var url = "http://127.0.0.1:8000/poly";
        $.ajax({
            url: url,
            type: 'POST',
            data: image,
            processData: false, 
            contentType: false,
            success: function(data) {

                if(!data || data.length==0){
                    $("#error").show();
                    $("#resultHolder").hide();
                    $("#divClassTable").hide();
                    return;
                }
                let match = null;
                let bestScore = -1;
                for (let i=0;i<data.length;++i) {
                    let maxScoreForThisClass = Math.max(...data[i].class_probability);
                    console.log('Max score for class:', data, maxScoreForThisClass);
                    if(maxScoreForThisClass>bestScore) {
                        match = data[i];
                        bestScore = maxScoreForThisClass;
                    }
                }
                
                if (match) {
                    $("#error").hide();
                    $("#resultHolder").show();
                    $("#divClassTable").show();
                    const playerBlock = document.getElementById(`${match.class}`);
                    if (playerBlock) {
                        const clone = playerBlock.cloneNode(true);
                        const cloneContainer = document.getElementById('resultHolder');
                        cloneContainer.innerHTML = '';
                        cloneContainer.appendChild(clone);
                    }else {
                        console.error('Aucun élément trouvé avec l\'identifiant:', match.class);
                    }
                    
     
                    let classDictionary = match.class_dictionary;
                    for(let personName in classDictionary) {
                        let index = classDictionary[personName];
                        let proabilityScore = match.class_probability[index];
                        let elementName = "score_" + personName;
                        const scoreCell = document.getElementById(`${elementName}`);
                        scoreCell.textContent = proabilityScore
                        
                    }
                }
                
                console.log('Response:', data);
            },
            error: function(xhr, status, error) {
                console.error('Error:', status, error);
            }
        });
    }

});