let toast_notification = document.getElementById("messages");
const WAITING_TIME = 2500;
const THEME = ['emerald', 'dim'];

let signup_email="undone";
let signup_sms="undone";

let polling;

let options = { childList: true, subtree: true };


/*** Theme control ***/
if(!("theme" in localStorage)) {
    localStorage.setItem('theme', 'emerald');
}

let site = document.querySelector('html');
let theme_switch = document.getElementById('theme-toggle');

// Applying default theme from localStorage 
if(localStorage.getItem('theme') === 'emerald' ) {
    site.dataset.theme = localStorage.getItem('theme');
    theme_switch.checked = false;
} else {
    site.dataset.theme = localStorage.getItem('theme');
    theme_switch.checked = true;
}

theme_switch.addEventListener('change', (e) => {
    // Dark Theme
    if(e.target.checked) {
        localStorage.setItem('theme', 'dim');
        site.dataset.theme = localStorage.getItem('theme');
    } 
    // Light Theme
    else {
        localStorage.setItem('theme', 'emerald');
        site.dataset.theme = localStorage.getItem('theme');
    }
});

/*** End Theme control ***/


function NotificationStatus(url) {
    fetch(url)
    .then(res => res.json())
    .then(data => {
        console.log(data);
        if(data.status !== 'NA'){
            toast_notification.insertAdjacentHTML(
                'afterbegin',
                `<div class="alert alert-${data.type} items-center flex-shrink-0 notification w-fit ms-auto status-notification">
                    <span>${data.message}</span>
                    <i class='bx bx-x dismiss text-2xl cursor-pointer hover:scale-125'></i>
                </div>`        
            );
            if (data.status === 'success' && data.action === "forgot-pwd"){
                toast_notification.insertAdjacentHTML(
                    'afterbegin',
                    `<div class="alert alert-info items-center flex-shrink-0 notification w-fit ms-auto status-notification">
                        <span>you can close this window</span>
                        <i class='bx bx-x dismiss text-2xl cursor-pointer hover:scale-125'></i>
                    </div>`
                );
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
    toast_notification.insertAdjacentHTML(
        'afterbegin',
        `<div class="alert alert-${content.type} items-center flex-shrink-0 notification w-fit ms-auto status-notification">
            <span>${content.message}</span>
            <i class='bx bx-x dismiss text-2xl cursor-pointer hover:scale-125'></i>
        </div>`        
    );
    if (content.action === 'signup-sms' && content.status === 'success' ){
        toast_notification.insertAdjacentHTML(
            'afterbegin',
            `<div class="alert alert-info items-center flex-shrink-0 notification w-fit ms-auto status-notification">
                <span>you can close this window</span>
                <i class='bx bx-x dismiss text-2xl cursor-pointer hover:scale-125'></i>
            </div>`
        );
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


function detectNotifications(mutations) {
    for (let mutation of mutations) {
        if(mutation.type === 'childList') {
            console.log("going to remove notifications");
            let notifications = document.querySelectorAll('.status-notification');
            notifications.forEach(notification => {
                setTimeout(() => {
                    notification.remove();
                }, WAITING_TIME);
            });

        }
    }
}


function imageUpload(event, imgID){
    const file = event.target.files[0];

    if(file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.getElementById(imgID);
            if(img) {
                console.log("Image found");
                img.src = e.target.result;
                console.log("Img changed");
            } else {
                console.log("Img not found");
            }
        }
        reader.readAsDataURL(file);
    }
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


// Removing toast notifications
toast_notification.addEventListener('click', (e) => {
    if(e.target.className.includes('dismiss')){
        let notification = e.target.parentElement;
        toast_notification.removeChild(notification);
    }
});

observer = new MutationObserver(detectNotifications);

observer.observe(toast_notification, options);

// Profile picture
if(document.getElementById('id_avatar')){
    const img_input = document.getElementById('id_avatar');
    img_input.addEventListener('change', (e) => {
        imageUpload(e, "avatar-pic-overview");
    });
}


/***  Password strength checker ***/

// Patterns to check whether password contains lowercase, uppercase, numbers, special characters respectively
const PATTERNS = [ /[a-z]+/, /[A-Z]+/, /[0-9]+/, /[\!@#$%^&*+_\-=\[\]{};:'",.<>?/\\|`~]+/ ];

// Pattern check flags
let LOWERCASE_CHECK = false;
let UPPERCASE_CHECK = false;
let DIGIT_CHECK = false;
let SPECIAL_CHARACTERS_CHECK = false;

// Minimum Password length
const MINIMUM_PASSWORD_LENGTH = 8;

// Indicator, Message
let message = '';
let indicator = '';
let text_color = '';

function passwordStrength(password) {

    if (typeof password !== 'string' || password === null) {
        return null;
    }
    const password_length = password.length;

    if (password_length < MINIMUM_PASSWORD_LENGTH) {
        message = 'Password should be atleast 8 characters long';
        indicator = 'Weak';
        text_color = '#dc2626';

    } else {
        LOWERCASE_CHECK = PATTERNS[0].test(password);
        UPPERCASE_CHECK = PATTERNS[1].test(password);
        DIGIT_CHECK = PATTERNS[2].test(password);
        SPECIAL_CHARACTERS_CHECK = PATTERNS[3].test(password);

        // determing password strength indicator
        if(LOWERCASE_CHECK && UPPERCASE_CHECK && DIGIT_CHECK && SPECIAL_CHARACTERS_CHECK) {
            indicator = "Very Strong";
            message = "Your password is highly secure";
            text_color = '#16a34a';
        } 
        else if (LOWERCASE_CHECK && UPPERCASE_CHECK && DIGIT_CHECK) {
            indicator = "Strong";
            message = "For better security, use special characters (!@#$%^&* etc,.)";
            text_color = '#10b981';
        }
        else if (DIGIT_CHECK && LOWERCASE_CHECK) {
            indicator = "Moderate";
            message = "For better security, use uppercase (A-Z), special characters (!@#$%^&* etc,.)";
            text_color = '#f59e0b';
        }
        else if(LOWERCASE_CHECK) {
            indicator = "Weak";
            message = "For better security, use uppercase (A-Z), digits (0-9), special characters (!@#$%^&* etc,.)";
            text_color = '#dc2626';
        }
    }

    // Returning indicator message
    return {'indicator': indicator, 'message': message, 'text_color': text_color};
}

// Password check for account creation page
if (document.getElementById('id_password1')){
    let password_field = document.getElementById('id_password1');
    let password_text_display = document.querySelector('.password-strength');

    password_field.addEventListener('input', (e) => {
        result = passwordStrength(e.target.value);
        if(result !== null) {
            // changing the color based on indicator text
            password_text_display.style.color = result.text_color;
            
            let text = `<i class='bx bxs-lock-alt text-xl'></i> <b>${result.indicator}</b> - ${result.message}`;
            password_text_display.innerHTML = text;
        }
    });
}

// Password check for Logged user
if (document.getElementById('id_new_password1')){
    let password_field = document.getElementById('id_new_password1');
    let password_text_display = document.querySelector('.password-strength');

    password_field.addEventListener('input', (e) => {
        result = passwordStrength(e.target.value);
        if(result !== null) {
            // changing the color based on indicator text
            password_text_display.style.color = result.text_color;

            let text = `<i class='bx bxs-lock-alt text-xl'></i> <b>${result.indicator}</b> - ${result.message}`;
            password_text_display.innerHTML = text;
        }
    });
}

// Show & hide password
if(document.querySelector(".show-password")) {
    let passwords = document.querySelectorAll(".show-password");

    passwords.forEach(password => {
        password.addEventListener('click', (e) => {

            let show_password = e.target;
            if(show_password.classList.contains('fa-eye-slash')) {
                show_password.parentElement.children[0].type = 'text';
                show_password.classList.add('fa-eye');
                show_password.classList.remove('fa-eye-slash');
            }
            else if(show_password.classList.contains('fa-eye')) {
                show_password.parentElement.children[0].type = 'password';
                show_password.classList.add('fa-eye-slash');
                show_password.classList.remove('fa-eye');
            }
        })
    }); 
}

/*** End Password strength checker ***/

// clearing notifications
if(document.querySelector('.toast-notification-message')) {
    let notifications = document.querySelectorAll('.toast-notification-message');
    notifications.forEach(notification => {
        setTimeout(()=>{
            notification.remove();
        }, WAITING_TIME);    
    });
}
