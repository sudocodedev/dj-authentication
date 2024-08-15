let message_status = document.querySelector(".status");

let signup_email="undone";
let signup_sms="undone";

let polling;

function NotificationStatus(url) {
    fetch(url)
    .then(res => res.json())
    .then(data => {
        console.log(data);
        if(data.status !== 'NA'){
            message_status.innerHTML += `
                <p class="alert alert-${data.type}">${data.message}</p>
            `
            if (data.status === 'success' && data.action === "forgot-pwd"){
                message_status.innerHTML += `
                    <p class="alert alert-info">you can close this window</p>
                `
            }
            if(data.status !== 'pending'){
                clearInterval(polling);
            }
        } else {
            console.log("no request was made");
        }
    })
}

function DisplayStatus(content) {
    message_status.innerHTML += `
        <p class="alert alert-${content.type}">${content.message}</p>
    `
    if (content.action === 'signup-sms' && content.status === 'success' ){
        message_status.innerHTML += `
            <p class="alert alert-info">you can close this window</p>
        `
    }
    if(content.status !== 'pending'){
        
        // Changing respective status
        if(content.action === 'signup-sms'){
            signup_sms = 'done';
        }
        if(content.action === 'signup-email'){
            signup_email = 'done';
        }
        
    }
}

function SignUpNotificationStatus(url) {
    fetch(url)
    .then(res => res.json())
    .then(data => {
        // check data length ? if 2 proceed else handle differently
        if(data['key'] !== 1) {
            console.log("signup polling");
            console.log(data);
            if(signup_email === "undone"){
                DisplayStatus(data['email']);
            }

            if(signup_sms === "undone"){
                DisplayStatus(data['sms']);
            }

            if(signup_email === "done" && signup_sms === "done"){
                clearInterval(polling);
            }
        } else {
            console.log("no request was made");
        }
    })
}

if(document.getElementById('userid') && document.getElementById('userid').value) {
    let user_id = document.getElementById('userid').value;
    const URL = `/account/password-reset-status/${user_id}/`;

    polling = setInterval(() => NotificationStatus(URL), 5000); //Polling at an interval of 5s
}

if(document.getElementById('signup-userid') && document.getElementById('signup-userid').value) {
    let user_id = document.getElementById('signup-userid').value;
    const URL = `/account/signup-status/${user_id}/`;

    polling = setInterval(() => SignUpNotificationStatus(URL), 5000); //Polling at an interval of 5s
}

if(document.getElementById("signin-userid") && document.getElementById("signin-userid").value){
    let user_id = document.getElementById("signin-userid").value;
    const URL = `/account/signin-status/${user_id}/`;

    polling = setInterval(() => NotificationStatus(URL), 5000);
}


if(document.getElementById('resend-userid') && document.getElementById('resend-userid').value) {
    let user_id = document.getElementById('resend-userid').value;
    const URL = `/account/signup-status/${user_id}/`;

    polling = setInterval(() => SignUpNotificationStatus(URL), 5000); //Polling at an interval of 5s
}


