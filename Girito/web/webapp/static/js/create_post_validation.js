function displayFileName(input) {
    const label = input.nextElementSibling;
    if (input.files.length > 0) {
      label.innerHTML = input.files[0].name;
    } else {
      label.innerHTML = "Elija un Archivo";
    }
  }

  function validateForm() {
    document.getElementById("titleError").textContent = "";
    document.getElementById("summaryError").textContent = "";
    document.getElementById("fileError").textContent = "";
  
    const title = document.getElementById("title").value.trim();
    const summary = document.getElementById("summary").value.trim();
    const attachment = document.getElementById("attachment");
  
    let isValid = true;
  
    if (title === "") {
      document.getElementById("titleError").textContent = "Por favor, ingrese un título.";
      isValid = false;
    } else if (title.length > 255) {
      document.getElementById("titleError").textContent = "¡Título demasiado largo! Máximo de 255 caracteres.";
      isValid = false;
    }
  
    if (summary === "") {
      document.getElementById("summaryError").textContent = "Por favor, ingrese una descripción.";
      isValid = false;
    } else if (summary.length > 255) {
      document.getElementById("summaryError").textContent = "¡Descripción demasiada larga! Máximo de 255 caracteres.";
      isValid = false;
    }
  
    if (!attachment.files[0]) {
      document.getElementById("fileError").textContent = "Por favor, seleccione un archivo.";
      isValid = false;
    } else {
      const allowedExtensions = [".mp4", ".png"];
      const fileName = attachment.files[0].name;
      const fileExtension = fileName.slice(((fileName.lastIndexOf(".") - 1) >>> 0) + 2).toLowerCase();
  
      if (!allowedExtensions.includes("." + fileExtension)) {
        document.getElementById("fileError").textContent = "Solo se permiten archivos .mp4 y .png.";
        isValid = false;
      }
    }
  
    return isValid;
  }
  
  
  document.getElementById("insert_post_form").onsubmit = function (event) {
    if (!validateForm()) {
      event.preventDefault();
    }
  };