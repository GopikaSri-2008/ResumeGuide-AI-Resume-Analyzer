function showFileName(input) {
    const fileName = document.getElementById("file-name");

    if (input.files.length > 0) {
        fileName.textContent = input.files[0].name;
    } else {
        fileName.textContent = "PDF or DOCX format";
    }
}