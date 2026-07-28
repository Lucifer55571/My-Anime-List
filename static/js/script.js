function confirmDelete() {

    let confirmAction = confirm(
        "Apakah kamu yakin ingin menghapus anime ini?"
    );

    return confirmAction;
}

document.addEventListener(
    "DOMContentLoaded",
    function(){

        let alerts = document.querySelectorAll(".alert");

        alerts.forEach(function(alert){

            setTimeout(function(){

                alert.style.transition = "0.5s";
                alert.style.opacity = "0";

                setTimeout(function(){
                    alert.remove();
                },500);

            },3000);

        });

    }
);

function previewImage(){

    let imageURL = document.getElementById(
        "cover_url"
    ).value;


    let preview = document.getElementById(
        "image_preview"
    );


    if(imageURL){

        preview.src = imageURL;
        preview.style.display = "block";

    }

    else{

        preview.style.display = "none";

    }

}

function validateScore(){

    let score = document.getElementById(
        "score"
    );


    if(score){

        let value = parseFloat(score.value);


        if(value < 1 || value > 10){

            alert(
                "Score harus berada di antara 1 sampai 10"
            );


            score.value = "";

        }

    }

}

function searchAnime(){

    let input = document.getElementById(
        "searchInput"
    );


    let filter = input.value.toLowerCase();


    let cards = document.querySelectorAll(
        ".anime-card"
    );


    cards.forEach(function(card){

        let title = card
            .querySelector(".anime-title")
            .innerText
            .toLowerCase();


        if(title.includes(filter)){

            card.style.display="block";

        }

        else{

            card.style.display="none";

        }

    });

}

window.addEventListener(
    "scroll",
    function(){

        let button = document.getElementById(
            "backTop"
        );


        if(button){

            if(
                document.documentElement.scrollTop > 200
            ){

                button.style.display="block";

            }

            else{

                button.style.display="none";

            }

        }

    }
);

function scrollTopPage(){

    window.scrollTo({

        top:0,

        behavior:"smooth"

    });

}

function togglePassword(){

    let password = document.getElementById(
        "password"
    );


    if(password.type === "password"){

        password.type="text";

    }

    else{

        password.type="password";

    }

}