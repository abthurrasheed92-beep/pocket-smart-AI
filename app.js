/* =========================================
   PocketSmart AI - Main JavaScript
========================================= */


document.addEventListener(
    "DOMContentLoaded",
    function () {

        setupLoginForm();

        setupNavigation();

    }
);


/* =========================================
   LOGIN
========================================= */

function setupLoginForm() {

    const form =
        document.getElementById(
            "login-form"
        );

    if (!form) {
        return;
    }

    form.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            const email =
                document.getElementById(
                    "email"
                ).value.trim();

            const password =
                document.getElementById(
                    "password"
                ).value;

            const button =
                document.getElementById(
                    "login-button"
                );

            const message =
                document.getElementById(
                    "login-message"
                );


            if (!email || !password) {

                showMessage(
                    message,
                    "Please enter your email and password.",
                    "error"
                );

                return;
            }


            button.disabled = true;

            button.textContent =
                "Logging in...";


            try {

                const response =
                    await fetch(
                        "/login",
                        {

                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            credentials: "include",

                            body: JSON.stringify({

                                email:
                                    email,

                                password:
                                    password

                            })

                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        data.detail ||
                        "Login failed."
                    );

                }


                /*
                 * Save token locally as well.
                 * The backend also creates an
                 * HttpOnly cookie.
                 */

                if (data.access_token) {

                    localStorage.setItem(
                        "access_token",
                        data.access_token
                    );

                }


                showMessage(
                    message,
                    "Login successful. Redirecting...",
                    "success"
                );


                setTimeout(
                    function () {

                        window.location.href =
                            "/dashboard";

                    },
                    700
                );


            } catch (error) {

                showMessage(
                    message,
                    error.message ||
                    "Unable to login.",
                    "error"
                );

            } finally {

                button.disabled = false;

                button.textContent =
                    "Login";

            }

        }
    );
}


/* =========================================
   MESSAGE
========================================= */

function showMessage(
    element,
    text,
    type
) {

    if (!element) {
        return;
    }

    element.textContent = text;

    element.className =
        "message " + type;

}


/* =========================================
   NAVIGATION
========================================= */

function setupNavigation() {

    const currentPath =
        window.location.pathname;


    const links =
        document.querySelectorAll(
            ".nav-links a"
        );


    links.forEach(
        function (link) {

            const href =
                link.getAttribute(
                    "href"
                );

            if (
                href &&
                href !== "/" &&
                currentPath.startsWith(href)
            ) {

                link.classList.add(
                    "active"
                );

            }

        }
    );

}


/* =========================================
   API HELPER
========================================= */

async function apiRequest(
    url,
    options = {}
) {

    const token =
        localStorage.getItem(
            "access_token"
        );


    const headers =
        options.headers || {};


    if (token) {

        headers["Authorization"] =
            "Bearer " + token;

    }


    options.headers = headers;

    options.credentials =
        "include";


    const response =
        await fetch(
            url,
            options
        );


    let data = null;


    try {

        data =
            await response.json();

    } catch {

        data = null;

    }


    if (!response.ok) {

        const message =
            data?.detail ||
            "Request failed.";

        throw new Error(
            message
        );

    }


    return data;
}


/* =========================================
   LOGOUT
========================================= */

async function logoutUser() {

    try {

        await apiRequest(
            "/logout",
            {
                method: "POST"
            }
        );

    } catch (error) {

        console.error(
            "Logout error:",
            error
        );

    }


    localStorage.removeItem(
        "access_token"
    );


    window.location.href =
        "/login";
}


/* =========================================
   FORMAT CURRENCY
========================================= */

function formatCurrency(
    value
) {

    const number =
        Number(value) || 0;


    return new Intl.NumberFormat(
        "en-IN",
        {
            style: "currency",
            currency: "INR",
            maximumFractionDigits: 0
        }
    ).format(number);
}


/* =========================================
   DISPLAY API ERROR
========================================= */

function displayApiError(
    error,
    element
) {

    if (!element) {
        return;
    }


    showMessage(
        element,
        error?.message ||
        "Something went wrong.",
        "error"
    );

}


/* =========================================
   MOBILE MENU
========================================= */

function toggleMobileMenu() {

    const nav =
        document.querySelector(
            ".nav-links"
        );


    if (!nav) {
        return;
    }


    nav.classList.toggle(
        "mobile-open"
    );

}