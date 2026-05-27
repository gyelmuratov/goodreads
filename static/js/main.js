(() => {
  const forms = document.querySelectorAll("form[data-submit-loading]");
  forms.forEach((form) => {
    form.addEventListener("submit", () => {
      const submitButton = form.querySelector("button[type='submit']");
      if (!submitButton) {
        return;
      }
      submitButton.disabled = true;
      const originalText = submitButton.textContent;
      submitButton.dataset.originalText = originalText || "";
      submitButton.textContent = "Please wait...";
    });
  });
})();

