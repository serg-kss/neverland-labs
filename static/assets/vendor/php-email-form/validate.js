/**
 * Contact Form Handler (Django-friendly)
 * Based on php-email-form styles
 */
(function () {
  "use strict";

  const forms = document.querySelectorAll(".php-email-form");

  forms.forEach((form) => {
    form.addEventListener("submit", function (event) {
      event.preventDefault();

      if (form.dataset.submitted === "true") return;

      if (!validateForm(form)) return;

      form.dataset.submitted = "true";

      const action = form.getAttribute("action");
      if (!action) {
        showError(form, "Form action is not defined.");
        return;
      }

      showLoading(form);

      const formData = new FormData(form);

      fetch(action, {
        method: "POST",
        body: formData,
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((response) => response.text())
        .then((data) => {
          hideLoading(form);

          if (data.trim() === "OK") {
            showSuccess(form);
            form.reset();
          } else {
            throw new Error(data || "Submission failed");
          }
        })
        .catch((error) => {
          form.dataset.submitted = "false";
          showError(form, error.message);
        });
    });
  });

  // -----------------------
  // Validation
  // -----------------------

  function validateForm(form) {
    const name = form.querySelector('[name="name"]')?.value.trim();
    const email = form.querySelector('[name="email"]')?.value.trim();
    const subject = form.querySelector('[name="subject"]')?.value.trim();
    const message = form.querySelector('[name="message"]')?.value.trim();

    if (!name || name.length < 2) {
      return showError(form, "Please enter your name.");
    }

    if (!validateEmail(email)) {
      return showError(form, "Please enter a valid email address.");
    }

    if (!subject || subject.length < 2) {
      return showError(form, "Please enter a subject.");
    }

    if (!message || message.length < 10) {
      return showError(form, "Message should be at least 10 characters.");
    }

    clearError(form);
    return true;
  }

  function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  // -----------------------
  // UI helpers
  // -----------------------

  function showLoading(form) {
    form.querySelector(".loading")?.classList.add("d-block");
    form.querySelector(".error-message")?.classList.remove("d-block");
    form.querySelector(".sent-message")?.classList.remove("d-block");
  }

  function hideLoading(form) {
    form.querySelector(".loading")?.classList.remove("d-block");
  }

  function showError(form, message) {
    hideLoading(form);
    const errorBox = form.querySelector(".error-message");
    errorBox.innerHTML = message;
    errorBox.classList.add("d-block");
    return false;
  }

  function clearError(form) {
    const errorBox = form.querySelector(".error-message");
    errorBox.innerHTML = "";
    errorBox.classList.remove("d-block");
  }

  function showSuccess(form) {
    form.querySelector(".sent-message")?.classList.add("d-block");
    form.dataset.submitted = "false"; // разрешаем повторную отправку после cooldown на сервере
  }
})();
