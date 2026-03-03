async function generateSummary() {
  const url = document.getElementById("urlInput").value.trim();
  if (!url) return;

  // Reset UI and show loader
  document.getElementById("error").style.display = "none";
  document.getElementById("result").style.display = "none";
  document.getElementById("loader").style.display = "block";
  document.getElementById("submitBtn").disabled = true;

  try {
    const response = await fetch("/summarize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });

    const data = await response.json();

    if (!response.ok) {
      showError(data.detail || "Something went wrong.");
      return;
    }

    document.getElementById("videoTitle").textContent = data.title;
    document.getElementById("summaryContent").innerHTML = marked.parse(data.summary);
    document.getElementById("result").style.display = "block";

  } catch (err) {
    showError("Could not connect to the server. Is it running?");
  } finally {
    document.getElementById("loader").style.display = "none";
    document.getElementById("submitBtn").disabled = false;
  }
}

function showError(message) {
  const el = document.getElementById("error");
  el.textContent = message;
  el.style.display = "block";
}

// Allow pressing Enter to submit
document.getElementById("urlInput").addEventListener("keydown", (e) => {
  if (e.key === "Enter") generateSummary();
});
