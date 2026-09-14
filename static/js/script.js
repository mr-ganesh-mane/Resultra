/* ========================================
   Resultra - Main JavaScript
   ======================================== */


/* ========================================
   Page Loaded
   ======================================== */

document.addEventListener("DOMContentLoaded", function () {

    /* ------------------------------------
       Delete Profile Confirmation
       ------------------------------------ */

    const deleteLinks = document.querySelectorAll(
        ".delete-profile"
    );

    deleteLinks.forEach(function (link) {

        link.addEventListener("click", function (event) {

            const confirmed = confirm(
                "Are you sure you want to delete this profile?"
            );

            if (!confirmed) {
                event.preventDefault();
            }

        });

    });


    /* ------------------------------------
       File Input
       ------------------------------------ */

    const fileInput = document.querySelector(
        'input[type="file"]'
    );

    const fileName = document.querySelector(
        ".file-name"
    );

    if (fileInput && fileName) {

        fileInput.addEventListener("change", function () {

            if (fileInput.files.length > 0) {

                fileName.textContent =
                    fileInput.files[0].name;

            } else {

                fileName.textContent =
                    "No file selected";

            }

        });

    }


    /* ------------------------------------
       Form Submit Protection
       ------------------------------------ */

    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {

        form.addEventListener("submit", function () {

            const submitButton = form.querySelector(
                'button[type="submit"]'
            );

            if (submitButton) {

                submitButton.disabled = true;

                submitButton.dataset.originalText =
                    submitButton.textContent;

                submitButton.textContent =
                    "Processing...";

            }

        });

    });


    /* ------------------------------------
       Auto Hide Messages
       ------------------------------------ */

    const messages = document.querySelectorAll(
        ".success, .error"
    );

    messages.forEach(function (message) {

        setTimeout(function () {

            message.classList.add("message-hidden");

        }, 5000);

    });


    /* ------------------------------------
       PDF Preview Links
       ------------------------------------ */

    const previewLinks = document.querySelectorAll(
        'a[target="_blank"]'
    );

    previewLinks.forEach(function (link) {

        link.addEventListener("click", function () {

            /*
             * PDF preview opens in a new browser tab.
             * No additional action is required here.
             */

        });

    });


    /* ------------------------------------
       Number Input Validation
       ------------------------------------ */

    const numberInputs = document.querySelectorAll(
        'input[type="number"]'
    );

    numberInputs.forEach(function (input) {

        input.addEventListener("input", function () {

            if (input.value !== "" && input.value < 0) {
                input.value = 0;
            }

        });

    });


    /* ------------------------------------
       Orientation Preview
       ------------------------------------ */

    const orientationSelect = document.querySelector(
        "#orientation"
    );

    const pageSizeSelect = document.querySelector(
        "#page_size"
    );

    if (orientationSelect && pageSizeSelect) {

        function updatePagePreview() {

            /*
             * This currently only keeps the selected
             * values available to the form.
             *
             * Actual PDF page size and orientation
             * are handled by the Flask backend.
             */

            const orientation =
                orientationSelect.value;

            const pageSize =
                pageSizeSelect.value;

            console.log(
                "PDF Settings:",
                pageSize,
                orientation
            );

        }


        orientationSelect.addEventListener(
            "change",
            updatePagePreview
        );


        pageSizeSelect.addEventListener(
            "change",
            updatePagePreview
        );

    }

});