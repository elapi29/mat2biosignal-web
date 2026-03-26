const API_BASE = "http://127.0.0.1:8000";

const form = document.getElementById("uploadForm");
const resultBox = document.getElementById("result");
const messageEl = document.getElementById("message");
const fileList = document.getElementById("fileList");
const downloadLink = document.getElementById("downloadLink");
const errorBox = document.getElementById("errorBox");
const errorText = document.getElementById("errorText");
const submitBtn = document.getElementById("submitBtn");
const loadingText = document.getElementById("loadingText");

function setLoading(isLoading) {
  submitBtn.disabled = isLoading;
  submitBtn.textContent = isLoading ? "Processing..." : "Convert";
  loadingText.classList.toggle("hidden", !isLoading);
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  resultBox.classList.add("hidden");
  errorBox.classList.add("hidden");
  fileList.innerHTML = "";
  downloadLink.classList.add("hidden");

  const fileInput = document.getElementById("file");
  const prefixInput = document.getElementById("output_prefix");

  const file = fileInput.files[0];
  const outputPrefix = prefixInput.value.trim();

  if (!file || !outputPrefix) {
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  formData.append("output_prefix", outputPrefix);

  setLoading(true);

  try {
    const response = await fetch(`${API_BASE}/convert`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(JSON.stringify(data, null, 2));
    }

    messageEl.textContent = data.message;

    data.files.forEach((name) => {
      const li = document.createElement("li");
      li.textContent = name;
      fileList.appendChild(li);
    });

    downloadLink.href = `${API_BASE}${data.download_url}`;
    downloadLink.classList.remove("hidden");
    resultBox.classList.remove("hidden");
  } catch (err) {
    errorText.textContent = err.message;
    errorBox.classList.remove("hidden");
  } finally {
    setLoading(false);
  }
});