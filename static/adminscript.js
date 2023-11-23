document.addEventListener("DOMContentLoaded", function () {
  // Function to open a dialog by its ID
  function openDialog(dialogId) {
    const dialog = document.getElementById(dialogId);
    dialog.style.display = "block";
  }

  // Function to close a dialog by its ID
  function closeDialog(dialogId) {
    const dialog = document.getElementById(dialogId);
    dialog.style.display = "none";
  }

  function upload() {
    const fileInput = document.getElementById("txtFileInput");
    const file = fileInput.files[0];

    if (file) {
      // Use FormData to send the file to a server (you can use AJAX for this)
      // For simplicity, we're not implementing the server-side handling in this example
      console.log("Uploading file:", file.name);
    } else {
      console.log("No file selected.");
    }
  }

  function download() {
    // You can trigger the file download using JavaScript
    // For simplicity, we'll use a placeholder link with a sample CSV file

    const sampleTxtUrl =
      "data:text/plain;base64,MTEyIAo5OCAKNjkgCjgyIAo5MSAKOTMgCjkxIAo5NSAKMTExIAo5NiAKOTcgCjEyNCAKOTUgCjEwNyAKODMgCjg0IAo1MCAKMjggCjg3IAoxNiAKNTcgCjExMSAKMTEzIAoyMCAKMTQ1IAoxMTkgCjY2IAo5NyAKOTAgCjExNSAKOCAKNDggCjEwNiAKNyAKMTEgCjE5IAoyMSAKNTAgCjE0MiAKMjggCjE4IAoxMCAKNTkgCjEwOSAKMTE0IAo0NyAKMTM1IAo5MiAKMjEgCjc5IAoxMTQgCjI5IAoyNiAKOTcgCjEzNyAKMTUgCjEwMyAKMzcgCjExNCAKMTAwIAoyMSAKNTQgCjcyIAoyOCAKMTI4IAoxNCAKNzcgCjggCjEyMSAKOTQgCjExOCAKNTAgCjEzMSAKMTI2IAoxMTMgCjEwIAozNCAKMTA3IAo2MyAKOTAgCjggCjkgCjEzNyAKNTggCjExOCAKODkgCjExNiAKMTE1IAoxMzYgCjI4IAozOCAKMjAgCjg1IAo1NSAKMTI4IAoxMzcgCjgyIAo1OSAKMTE3IAoyMCAK";
    const link = document.createElement("a");
    link.href = sampleTxtUrl;
    link.download = "RUL.txt";

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    // After the download, you can move the file to another directory using a server-side language like PHP
    // Make an AJAX request to the PHP file to handle the file moving operation
    moveFile();
  }

  function moveFile() {
    // Make an AJAX request to the PHP file
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          console.log(xhr.responseText);
        } else {
          console.error("Error moving file:", xhr.status, xhr.statusText);
        }
      }
    };

    // Replace 'move_file.php' with the actual path to your PHP file
    xhr.open("GET", "uploadproc.php", true);
    xhr.send();
  }

  /*  function uploadDataset() {
    const fileInput = document.getElementById("dataset-file");
    const uploadMessage = document.getElementById("upload-message");

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        uploadMessage.textContent = data.message;
      })
      .catch((error) => {
        console.error("Error:", error);
        uploadMessage.textContent = "Error uploading dataset.";
      });
  }

  function downloadDataset() {
    window.location.href = "/download";
  }

  // Add event listener for logout
  document.getElementById("logout").addEventListener("click", () => logout());

  function logout() {
    window.location.href = "login.html";
  }*/
});
